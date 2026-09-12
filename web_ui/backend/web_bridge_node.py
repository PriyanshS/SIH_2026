from __future__ import annotations

import os
import sys
import json
import math
import time
import uuid
import base64
import hashlib
import struct
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

try:
    import rclpy
    from rclpy.node import Node
    from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
    from geometry_msgs.msg import PointStamped, PoseStamped, Twist
    from std_msgs.msg import String, Int32
    from amr_msgs.msg import RobotStatus, ChokeRequest, DetectedObstacle
    ROS2_AVAILABLE = True
except ImportError:
    # ROS 2 not available — run in standalone HTTP/WebSocket demo mode
    ROS2_AVAILABLE = False
    rclpy = None

    class Node:  # stub
        def __init__(self, name):
            self._name = name
        def get_logger(self):
            import logging
            return logging.getLogger(self._name)
        def create_publisher(self, *a, **kw): return None
        def create_subscription(self, *a, **kw): return None
        def create_timer(self, *a, **kw): return None
        def get_clock(self): return self
        def now(self): return self
        def to_msg(self): return None
        def destroy_node(self): pass

    class RobotStatus:
        IDLE = 0
        BUSY = 1
    class ChokeRequest:
        REQUEST = 1
        GRANT = 2
        RELEASE = 3
        HEARTBEAT = 4
    class DetectedObstacle: pass
    class PointStamped: pass
    class PoseStamped: pass
    class Twist: pass
    class String: pass
    class Int32: pass


# ──────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────
WEB_PORT      = int(os.environ.get("WEB_PORT", 8090))
ADMIN_USER    = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin2026")
SESSION_TTL   = 3600  # seconds

candidate_dirs = [
    "/home/piyansh46/Code/SIH_2026/web_ui/frontend",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../web_ui/frontend")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend")),
]
FRONTEND_DIR = "/home/piyansh46/Code/SIH_2026/web_ui/frontend"
for cdir in candidate_dirs:
    if os.path.isdir(cdir) and os.path.exists(os.path.join(cdir, "index.html")):
        FRONTEND_DIR = cdir
        break

# ──────────────────────────────────────────────────────────
# Session Store (in-memory)
# ──────────────────────────────────────────────────────────
_sessions: dict[str, float] = {}   # token → expiry timestamp
_sessions_lock = threading.Lock()


def create_session() -> str:
    token = uuid.uuid4().hex
    with _sessions_lock:
        _sessions[token] = time.time() + SESSION_TTL
    return token


def is_valid_session(token: str) -> bool:
    if not token:
        return False
    with _sessions_lock:
        expiry = _sessions.get(token)
        if expiry is None:
            return False
        if time.time() > expiry:
            del _sessions[token]
            return False
        return True


def delete_session(token: str):
    with _sessions_lock:
        _sessions.pop(token, None)


def get_cookie_value(cookie_header: str, name: str) -> str:
    """Parse a specific cookie value from the Cookie header."""
    if not cookie_header:
        return ""
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith(f"{name}="):
            return part[len(f"{name}="):]
    return ""


# ──────────────────────────────────────────────────────────
# WebSocket Client Handler (RFC 6455)
# ──────────────────────────────────────────────────────────
class WebSocketClientHandler:
    """Lightweight RFC 6455 WebSocket connection (no external deps)."""

    def __init__(self, sock, bridge_node):
        self.sock = sock
        self.bridge_node = bridge_node
        self.active = True

    def run(self):
        try:
            while self.active and (not ROS2_AVAILABLE or (rclpy is not None and rclpy.ok())):
                data = self.sock.recv(2)
                if not data or len(data) < 2:
                    break
                b1, b2 = data[0], data[1]
                opcode   = b1 & 0x0F
                has_mask = b2 & 0x80
                payload_len = b2 & 0x7F

                if opcode == 0x8:   # Close
                    break
                elif opcode == 0x9:  # Ping
                    self.send_pong()
                    continue

                if payload_len == 126:
                    ext = self.sock.recv(2)
                    payload_len = struct.unpack("!H", ext)[0]
                elif payload_len == 127:
                    ext = self.sock.recv(8)
                    payload_len = struct.unpack("!Q", ext)[0]

                masks      = self.sock.recv(4) if has_mask else b""
                raw        = bytearray(self.sock.recv(payload_len))
                if has_mask:
                    for i in range(len(raw)):
                        raw[i] ^= masks[i % 4]

                self.handle_incoming_json(raw.decode("utf-8", errors="ignore"))
        except Exception:
            pass
        finally:
            self.active = False
            try:
                self.sock.close()
            except Exception:
                pass
            self.bridge_node.remove_client(self)

    def send_text(self, text: str):
        if not self.active:
            return
        try:
            payload = text.encode("utf-8")
            header  = bytearray([0x81])
            length  = len(payload)
            if length <= 125:
                header.append(length)
            elif length <= 65535:
                header.append(126)
                header.extend(struct.pack("!H", length))
            else:
                header.append(127)
                header.extend(struct.pack("!Q", length))
            self.sock.sendall(header + payload)
        except Exception:
            self.active = False

    def send_pong(self):
        try:
            self.sock.sendall(b"\x8a\x00")
        except Exception:
            pass

    def handle_incoming_json(self, raw_str: str):
        try:
            data     = json.loads(raw_str)
            msg_type = data.get("type", "")
            if msg_type == "dispatch":
                x        = float(data.get("x", 0.0))
                y        = float(data.get("y", 0.0))
                robot_id = data.get("robot_id", "auto")
                self.bridge_node.dispatch_goal(x, y, robot_id)
            elif msg_type == "estop":
                action = data.get("action", "halt")
                self.bridge_node.trigger_estop(action == "halt")
        except Exception as e:
            self.bridge_node.get_logger().warn(f"Invalid WS message: {e}")


# ──────────────────────────────────────────────────────────
# Web Bridge ROS 2 Node
# ──────────────────────────────────────────────────────────
class WebBridgeNode(Node):
    """ROS 2 Node: embedded HTTP + WebSocket bridge for fleet dashboard."""

    def __init__(self):
        super().__init__("web_bridge_node")
        self.get_logger().info(
            "Initializing Web Bridge Node (Retro FleetLink)" +
            (" [DEMO MODE — ROS2 not available]" if not ROS2_AVAILABLE else "") + "..."
        )

        # Fleet state — robot initial positions match new 60×40m warehouse staging zones
        self.robots = {
            "robot1": {"id": "robot1", "x": 10.0, "y": 2.0, "yaw": 0.0, "status": "IDLE", "reason": "", "color": "#ff00ff"},
            "robot2": {"id": "robot2", "x": 30.0, "y": 2.0, "yaw": 0.0, "status": "IDLE", "reason": "", "color": "#00ffff"},
            "robot3": {"id": "robot3", "x": 50.0, "y": 2.0, "yaw": 0.0, "status": "IDLE", "reason": "", "color": "#00ff41"},
        }
        self.chokepoint = {
            "occupied_by": None,
            "status": "FREE",
            "last_heartbeat": None,
            "contenders": [],
        }
        self.obstacles   = []
        self.queue_size  = 0
        self.events      = []
        self.metrics     = {
            "completed_goals": 0,
            "throughput": 0.0,
            "start_time": time.time(),
        }

        self.ws_clients      = []
        self.ws_clients_lock = threading.Lock()

        if ROS2_AVAILABLE:
            # Publishers
            self.pub_click = self.create_publisher(PointStamped, "/clicked_point", 10)
            self.pub_goal  = self.create_publisher(PoseStamped, "/goal_pose", 10)
            self.pub_cmd_vels = {
                ns: self.create_publisher(Twist, f"/{ns}/cmd_vel", 10)
                for ns in self.robots
            }

            # QoS profiles
            qos_be = QoSProfile(
                reliability=ReliabilityPolicy.BEST_EFFORT,
                durability=DurabilityPolicy.VOLATILE, depth=10)
            qos_rel = QoSProfile(
                reliability=ReliabilityPolicy.RELIABLE,
                durability=DurabilityPolicy.VOLATILE, depth=10)

            for ns in self.robots:
                self.create_subscription(PoseStamped,   f"/{ns}/ground_truth_pose",
                    lambda msg, ns=ns: self._on_pose(ns, msg),   qos_be)
                self.create_subscription(RobotStatus,   f"/{ns}/robot_status",
                    lambda msg, ns=ns: self._on_status(ns, msg), qos_rel)
                self.create_subscription(String,        f"/{ns}/choke_reason",
                    lambda msg, ns=ns: self._on_choke_reason(ns, msg), qos_rel)

            self.create_subscription(ChokeRequest,   "/choke_negotiation",  self._on_choke_request, qos_rel)
            self.create_subscription(DetectedObstacle, "/detected_obstacles", self._on_obstacle,     qos_rel)
            self.create_subscription(Int32,          "/dispatcher/queue_size", self._on_queue_size, qos_rel)
            self.create_subscription(String,         "/metrics",             self._on_metrics,      qos_rel)

            self.create_timer(0.1, self._broadcast_telemetry)
            self.create_timer(1.0, self._prune_obstacles)
        else:
            # Demo mode: simulate robot movement via a background thread
            self.pub_cmd_vels = {}
            self.pub_click = None
            self.pub_goal  = None
            self._demo_tick = 0
            self._custom_goals = {r: None for r in self.robots}
            threading.Thread(target=self._demo_loop, daemon=True).start()

        self.start_web_server()
        mode_str = "DEMO" if not ROS2_AVAILABLE else "ROS2"
        self.add_event("SYSTEM", f"FleetLink Web Bridge online [{mode_str}] — port {WEB_PORT}")

    def _demo_loop(self):
        """Simulates autonomous robot movements and missions in demo mode."""
        patrol_routes = {
            "robot1": [(10.0, 2.0), (10.0, 15.0), (20.0, 20.0), (10.0, 32.0), (10.0, 2.0)],
            "robot2": [(30.0, 2.0), (30.0, 18.0), (30.0, 26.0), (25.0, 35.0), (30.0, 2.0)],
            "robot3": [(50.0, 2.0), (50.0, 15.0), (42.0, 22.0), (45.0, 32.0), (50.0, 2.0)],
        }
        targets = {r: 0 for r in patrol_routes}

        while True:
            time.sleep(0.1)
            for r_id, r_data in self.robots.items():
                target = self._custom_goals.get(r_id)
                if not target:
                    route = patrol_routes[r_id]
                    idx = targets[r_id]
                    target = route[idx]

                tx, ty = target
                cx, cy = r_data["x"], r_data["y"]
                dx = tx - cx
                dy = ty - cy
                dist = math.hypot(dx, dy)

                if dist < 0.4:
                    if self._custom_goals.get(r_id):
                        self._custom_goals[r_id] = None
                        r_data["status"] = "IDLE"
                        self.metrics["completed_goals"] += 1
                        self.add_event(r_id, f"Delivered payload to ({tx:.1f}, {ty:.1f})")
                    else:
                        targets[r_id] = (targets[r_id] + 1) % len(patrol_routes[r_id])
                else:
                    speed = 0.35
                    r_data["status"] = "BUSY"
                    angle = math.atan2(dy, dx)
                    r_data["yaw"] = round(angle, 2)
                    step = min(speed, dist)
                    r_data["x"] = round(cx + math.cos(angle) * step, 2)
                    r_data["y"] = round(cy + math.sin(angle) * step, 2)

            self._broadcast_telemetry()

    # ── ROS Callbacks ────────────────────────────────────
    def _on_pose(self, ns, msg: PoseStamped):
        x = msg.pose.position.x
        y = msg.pose.position.y
        q = msg.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw  = math.atan2(siny, cosy)
        if ns in self.robots:
            self.robots[ns]["x"]   = round(x,   2)
            self.robots[ns]["y"]   = round(y,   2)
            self.robots[ns]["yaw"] = round(yaw, 2)

    def _on_status(self, ns, msg: RobotStatus):
        if ns in self.robots:
            s = "BUSY" if msg.status == 1 else "IDLE"
            if self.robots[ns]["status"] == "BUSY" and s == "IDLE":
                self.metrics["completed_goals"] += 1
                self.add_event(ns, "Mission complete — robot IDLE")
            self.robots[ns]["status"] = s

    def _on_choke_reason(self, ns, msg: String):
        if ns in self.robots and msg.data:
            self.robots[ns]["reason"] = msg.data
            self.add_event(ns, msg.data)

    def _on_choke_request(self, msg: ChokeRequest):
        rid   = msg.robot_id
        t_now = time.time()
        if msg.msg_type == ChokeRequest.REQUEST:
            if rid not in self.chokepoint["contenders"]:
                self.chokepoint["contenders"].append(rid)
            if self.chokepoint["status"] == "FREE":
                self.chokepoint["status"] = "REQUESTED"
            self.add_event(rid, f"Requested chokepoint (pri {msg.priority})")
        elif msg.msg_type == ChokeRequest.GRANT:
            self.chokepoint.update({"occupied_by": rid, "status": "OCCUPIED", "last_heartbeat": t_now})
            if rid in self.chokepoint["contenders"]:
                self.chokepoint["contenders"].remove(rid)
            self.add_event(rid, "GRANTED chokepoint token")
        elif msg.msg_type == ChokeRequest.RELEASE:
            if self.chokepoint["occupied_by"] == rid:
                self.chokepoint["occupied_by"] = None
                self.chokepoint["status"] = "FREE" if not self.chokepoint["contenders"] else "REQUESTED"
                self.add_event(rid, "Chokepoint token RELEASED")
        elif msg.msg_type == ChokeRequest.HEARTBEAT:
            if self.chokepoint["occupied_by"] == rid:
                self.chokepoint["last_heartbeat"] = t_now

    def _on_obstacle(self, msg: DetectedObstacle):
        ox, oy = round(msg.position.x, 2), round(msg.position.y, 2)
        r      = round(msg.radius, 2)
        ttl    = msg.ttl if msg.ttl > 0 else 10.0
        for obs in self.obstacles:
            if math.hypot(obs["x"] - ox, obs["y"] - oy) < 0.5:
                obs["expiry"] = time.time() + ttl
                return
        self.obstacles.append({"x": ox, "y": oy, "radius": r,
                                "reporter": msg.reporter_id, "expiry": time.time() + ttl})
        self.add_event(msg.reporter_id, f"Obstacle at ({ox},{oy})")

    def _prune_obstacles(self):
        now = time.time()
        self.obstacles = [o for o in self.obstacles if o["expiry"] > now]
        if self.chokepoint["status"] == "OCCUPIED" and self.chokepoint["last_heartbeat"]:
            if now - self.chokepoint["last_heartbeat"] > 3.0:
                stale = self.chokepoint["occupied_by"]
                self.chokepoint.update({"occupied_by": None,
                    "status": "FREE" if not self.chokepoint["contenders"] else "REQUESTED"})
                self.add_event("SYSTEM", f"Watchdog evicted stale occupant {stale}")

    def _on_queue_size(self, msg: Int32):
        self.queue_size = msg.data

    def _on_metrics(self, msg: String):
        try:
            d = json.loads(msg.data)
            if "throughput_60s" in d:
                self.metrics["throughput"] = round(d["throughput_60s"], 2)
        except Exception:
            pass

    def add_event(self, source: str, message: str):
        self.events.insert(0, {"time": time.strftime("%H:%M:%S"), "source": source, "msg": message})
        if len(self.events) > 50:
            self.events.pop()

    def get_fleet_snapshot(self) -> dict:
        elapsed = max(time.time() - self.metrics["start_time"], 1.0)
        calc_tp = round((self.metrics["completed_goals"] / elapsed) * 60.0, 2)
        return {
            "type": "telemetry",
            "timestamp": time.time(),
            "robots": self.robots,
            "chokepoint": self.chokepoint,
            "obstacles": self.obstacles,
            "queue_size": self.queue_size,
            "metrics": {
                "completed_goals": self.metrics["completed_goals"],
                "throughput": self.metrics["throughput"] or calc_tp,
            },
            "events": self.events[:20],
        }

    def dispatch_goal(self, x: float, y: float, robot_id: str = "auto"):
        self.get_logger().info(f"Dispatch: ({x},{y}) → {robot_id}")
        if ROS2_AVAILABLE and self.pub_click and self.pub_goal:
            if robot_id == "auto":
                msg = PointStamped()
                msg.header.stamp    = self.get_clock().now().to_msg()
                msg.header.frame_id = "map"
                msg.point.x = float(x); msg.point.y = float(y); msg.point.z = 0.0
                self.pub_click.publish(msg)
                self.add_event("OPERATOR", f"Auto-dispatch → ({x:.1f},{y:.1f})")
            else:
                msg = PoseStamped()
                msg.header.stamp    = self.get_clock().now().to_msg()
                msg.header.frame_id = "map"
                msg.pose.position.x = float(x); msg.pose.position.y = float(y)
                msg.pose.orientation.w = 1.0
                self.pub_goal.publish(msg)
                self.add_event("OPERATOR", f"Direct → {robot_id} ({x:.1f},{y:.1f})")
        else:
            target_r = robot_id if robot_id in self.robots else "robot1"
            if robot_id == "auto":
                best_d = 9999
                for rid, rdata in self.robots.items():
                    d = math.hypot(rdata["x"] - x, rdata["y"] - y)
                    if d < best_d:
                        best_d = d
                        target_r = rid
            if hasattr(self, "_custom_goals"):
                self._custom_goals[target_r] = (float(x), float(y))
            self.robots[target_r]["status"] = "BUSY"
            self.add_event("OPERATOR", f"Dispatched {target_r} → ({x:.1f}, {y:.1f})")

    def trigger_estop(self, halt: bool = True):
        self.get_logger().warn(f"E-STOP: halt={halt}")
        if ROS2_AVAILABLE and self.pub_cmd_vels:
            for pub in self.pub_cmd_vels.values():
                pub.publish(Twist())
        self.add_event("OPERATOR", "EMERGENCY HALT" if halt else "Fleet resumed")

    def _broadcast_telemetry(self):
        if not self.ws_clients:
            return
        snap = json.dumps(self.get_fleet_snapshot())
        with self.ws_clients_lock:
            for client in list(self.ws_clients):
                client.send_text(snap)

    def add_client(self, client: WebSocketClientHandler):
        with self.ws_clients_lock:
            self.ws_clients.append(client)
        client.send_text(json.dumps(self.get_fleet_snapshot()))

    def remove_client(self, client: WebSocketClientHandler):
        with self.ws_clients_lock:
            if client in self.ws_clients:
                self.ws_clients.remove(client)

    # ── HTTP Server ──────────────────────────────────────
    def start_web_server(self):
        node = self

        class FleetHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

            def log_message(self, fmt, *args):
                pass  # suppress noise

            # ── CORS + common helpers ──
            def _cors_headers(self):
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, Cookie")
                self.send_header("Access-Control-Allow-Credentials", "true")

            def _json_ok(self, data: dict, extra_headers: list | None = None):
                body = json.dumps(data).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self._cors_headers()
                if extra_headers:
                    for k, v in extra_headers:
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(body)

            def _json_err(self, code: int, msg: str):
                body = json.dumps({"error": msg}).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self._cors_headers()
                self.end_headers()
                self.wfile.write(body)

            def _get_session_token(self) -> str:
                cookie_hdr = self.headers.get("Cookie", "")
                return get_cookie_value(cookie_hdr, "flsession")

            def _authenticated(self) -> bool:
                return is_valid_session(self._get_session_token())

            def do_OPTIONS(self):
                self.send_response(204)
                self._cors_headers()
                self.end_headers()

            def do_GET(self):
                parsed = urlparse(self.path)
                path   = parsed.path.rstrip("/") or "/"

                # ── WebSocket upgrade (any path ending in /ws) ──
                if self.headers.get("Upgrade", "").lower() == "websocket":
                    key = self.headers.get("Sec-WebSocket-Key", "")
                    if not key:
                        self._json_err(400, "Missing WS key")
                        return
                    magic  = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
                    accept = base64.b64encode(
                        hashlib.sha1(key.encode() + magic).digest()
                    ).decode()
                    self.send_response(101)
                    self.send_header("Upgrade",              "websocket")
                    self.send_header("Connection",           "Upgrade")
                    self.send_header("Sec-WebSocket-Accept", accept)
                    # Allow unauthenticated WS for demos; uncomment to enforce:
                    # self._cors_headers()
                    self.end_headers()
                    client = WebSocketClientHandler(self.connection, node)
                    node.add_client(client)
                    client.run()
                    return

                # ── REST: fleet state ──
                if path == "/api/state":
                    self._json_ok(node.get_fleet_snapshot())
                    return

                # ── Auth check for all other routes ──
                # Login page is always public
                if path in ("/login", "/login.html"):
                    # Serve index.html (login overlay is built-in)
                    self.path = "/index.html"
                    super().do_GET()
                    return

                # For normal static files: proceed (auth is enforced in browser via JS)
                super().do_GET()

            def do_POST(self):
                parsed  = urlparse(self.path)
                path    = parsed.path.rstrip("/")
                length  = int(self.headers.get("Content-Length", 0))
                body    = self.rfile.read(length).decode("utf-8") if length else "{}"
                try:
                    payload = json.loads(body)
                except Exception:
                    payload = {}

                # ── Auth: Login ──
                if path == "/api/auth/login":
                    username = payload.get("username", "")
                    password = payload.get("password", "")
                    if username == ADMIN_USER and password == ADMIN_PASSWORD:
                        token = create_session()
                        node.get_logger().info(f"Admin login: {username}")
                        node.add_event("SYSTEM", f"Admin authenticated: {username}")
                        cookie = (
                            f"flsession={token}; HttpOnly; Path=/; "
                            f"Max-Age={SESSION_TTL}; SameSite=Lax"
                        )
                        self._json_ok(
                            {"status": "ok", "message": "Authenticated"},
                            extra_headers=[("Set-Cookie", cookie)]
                        )
                    else:
                        node.get_logger().warn(f"Failed login attempt: {username}")
                        self._json_err(401, "Invalid credentials")
                    return

                # ── Auth: Logout ──
                if path == "/api/auth/logout":
                    token = self._get_session_token()
                    delete_session(token)
                    cookie = "flsession=; HttpOnly; Path=/; Max-Age=0"
                    self._json_ok(
                        {"status": "ok"},
                        extra_headers=[("Set-Cookie", cookie)]
                    )
                    return

                # ── Fleet: Dispatch ──
                if path == "/api/dispatch":
                    x        = float(payload.get("x", 0.0))
                    y        = float(payload.get("y", 0.0))
                    robot_id = payload.get("robot_id", "auto")
                    node.dispatch_goal(x, y, robot_id)
                    self._json_ok({"status": "dispatched"})
                    return

                # ── Fleet: E-Stop ──
                if path == "/api/estop":
                    action = payload.get("action", "halt")
                    node.trigger_estop(action == "halt")
                    self._json_ok({"status": "ok"})
                    return

                self._json_err(404, "Not found")

        def serve():
            port = WEB_PORT
            for attempt_port in [WEB_PORT, 8080, 8088, 9090]:
                try:
                    httpd = HTTPServer(("0.0.0.0", attempt_port), FleetHandler)
                    node.get_logger().info(
                        f"═══ FleetLink Web Dashboard → http://localhost:{attempt_port} ═══"
                    )
                    node.add_event("SYSTEM", f"HTTP server started on port {attempt_port}")
                    httpd.serve_forever()
                    break
                except OSError as e:
                    node.get_logger().warn(f"Port {attempt_port} busy ({e}), trying next...")
                    continue

        t = threading.Thread(target=serve, daemon=True)
        t.start()


# ──────────────────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────────────────
def main(args=None):
    if ROS2_AVAILABLE:
        rclpy.init(args=args)
        node = WebBridgeNode()
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        finally:
            node.destroy_node()
            rclpy.shutdown()
    else:
        # Standalone demo mode — just keep the HTTP/WebSocket server alive
        import logging
        logging.basicConfig(level=logging.INFO)
        logging.info("[FleetLink] Starting in DEMO mode (ROS2 not available)")
        node = WebBridgeNode()
        logging.info(f"[FleetLink] Dashboard ready at http://localhost:{WEB_PORT}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
