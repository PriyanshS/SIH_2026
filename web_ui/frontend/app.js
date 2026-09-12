/**
 * BEL FleetLink — RETRO 80s AMR Fleet Console
 * Features:
 * - Admin login gate with session token
 * - Hardened WebSocket connection to DDS service (ws://localhost:8090/ws)
 * - Rich industrial warehouse canvas (40m × 30m)
 * - Neon 80s rendering: magenta/cyan/green robots, rack systems, nav paths
 * - Smooth 60 FPS animation with trail rendering
 */

// ══════════════════════════════════════════════════════════
// ADMIN AUTHENTICATION (client-side gate)
// ══════════════════════════════════════════════════════════
const AUTH = {
  // Session is validated server-side; this just controls UI visibility
  // after server sets a cookie. For offline/demo mode we do a local check.
  SESSION_KEY: "fleetlink_session",

  isAuthenticated() {
    return sessionStorage.getItem(this.SESSION_KEY) === "1";
  },

  login(user, pass) {
    // Primary: try server-side auth
    return fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: user, password: pass }),
    })
      .then((res) => {
        if (res.ok) {
          sessionStorage.setItem(this.SESSION_KEY, "1");
          return true;
        }
        return false;
      })
      .catch(() => {
        // Offline/demo fallback — local credential check
        const validUser = "admin";
        const validPass = "admin2026";
        if (user === validUser && pass === validPass) {
          sessionStorage.setItem(this.SESSION_KEY, "1");
          return true;
        }
        return false;
      });
  },

  logout() {
    sessionStorage.removeItem(this.SESSION_KEY);
    fetch("/api/auth/logout", { method: "POST" }).catch(() => {});
    location.reload();
  },
};

// DOM ready: check auth, wire login form
document.addEventListener("DOMContentLoaded", () => {
  const overlay  = document.getElementById("login-overlay");
  const mainApp  = document.getElementById("main-app");
  const loginForm = document.getElementById("login-form");
  const loginErr  = document.getElementById("login-error");
  const logoutBtn = document.getElementById("btn-logout");

  function showApp() {
    overlay.style.display = "none";
    mainApp.style.display = "flex";
    mainApp.style.flexDirection = "column";
    mainApp.style.minHeight = "100vh";
    resizeCanvas();
    connectWebSocket();
    requestAnimationFrame(animate);
  }

  // Check server-side session first via a lightweight ping
  fetch("/api/state")
    .then((res) => {
      if (res.ok) {
        // Server is reachable — check if session cookie is valid
        return res.json().then(() => {
          // If server responded 200, session is valid (server will 401/redirect if not)
          sessionStorage.setItem(AUTH.SESSION_KEY, "1");
          showApp();
        });
      }
      throw new Error("not authenticated");
    })
    .catch(() => {
      // Show login or check local session
      if (AUTH.isAuthenticated()) {
        showApp();
      }
      // otherwise login overlay stays visible
    });

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const user = document.getElementById("login-user").value.trim();
    const pass = document.getElementById("login-pass").value;
    const btn  = document.getElementById("login-submit");

    document.getElementById("login-btn-text").textContent = "AUTHENTICATING...";
    btn.disabled = true;
    loginErr.style.display = "none";

    const ok = await AUTH.login(user, pass);

    if (ok) {
      showApp();
    } else {
      loginErr.style.display = "block";
      document.getElementById("login-btn-text").textContent = "▶ AUTHENTICATE";
      btn.disabled = false;
      document.getElementById("login-pass").value = "";
    }
  });

  logoutBtn.addEventListener("click", () => AUTH.logout());
});

// ══════════════════════════════════════════════════════════
// WORLD GEOMETRY (meters)
// ══════════════════════════════════════════════════════════
const WORLD_WIDTH  = 40.0;
const WORLD_HEIGHT = 30.0;

// ══════════════════════════════════════════════════════════
// FLEET STATE CACHE
// ══════════════════════════════════════════════════════════
const state = {
  connected: false,
  robots: {
    robot1: { id: "robot1", x: 5.0, y: 4.0, yaw: 0.0, targetX: 5.0, targetY: 4.0, targetYaw: 0.0, status: "IDLE", reason: "", color: "#ff00ff", trail: [] },
    robot2: { id: "robot2", x: 20.0, y: 4.0, yaw: 0.0, targetX: 20.0, targetY: 4.0, targetYaw: 0.0, status: "IDLE", reason: "", color: "#00ffff", trail: [] },
    robot3: { id: "robot3", x: 35.0, y: 4.0, yaw: 0.0, targetX: 35.0, targetY: 4.0, targetYaw: 0.0, status: "IDLE", reason: "", color: "#00ff41", trail: [] },
  },
  chokepoint: {
    occupied_by: null,
    status: "FREE",
    contenders: [],
    polygon: [
      { x: 16.0, y: 12.0 },
      { x: 24.0, y: 12.0 },
      { x: 24.0, y: 18.0 },
      { x: 16.0, y: 18.0 }
    ]
  },
  obstacles: [],
  queue_size: 0,
  metrics: { completed_goals: 0, throughput: 0.0 },
  events: [],
  mouse: { worldX: 20.0, worldY: 15.0, onCanvas: false },
  emergencyHalt: false
};

// ══════════════════════════════════════════════════════════
// CANVAS SETUP
// ══════════════════════════════════════════════════════════
const canvas    = document.getElementById("warehouse-canvas");
const ctx       = canvas.getContext("2d");
const container = document.getElementById("canvas-container");
let transform   = { scale: 15, originX: 40, originY: 40 };

function resizeCanvas() {
  const rect = container.getBoundingClientRect();
  canvas.width  = rect.width  * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

  const pad    = 30;
  const availW = rect.width  - pad * 2;
  const availH = rect.height - pad * 2;
  const scaleX = availW / WORLD_WIDTH;
  const scaleY = availH / WORLD_HEIGHT;
  const scale  = Math.min(scaleX, scaleY);

  transform.scale   = scale;
  transform.originX = (rect.width  - WORLD_WIDTH  * scale) / 2;
  transform.originY = (rect.height - WORLD_HEIGHT * scale) / 2;
}

window.addEventListener("resize", resizeCanvas);

function worldToScreen(wx, wy) {
  return {
    x: transform.originX + wx * transform.scale,
    y: transform.originY + (WORLD_HEIGHT - wy) * transform.scale
  };
}

function screenToWorld(sx, sy) {
  return {
    x: Math.max(0, Math.min(WORLD_WIDTH,  (sx - transform.originX) / transform.scale)),
    y: Math.max(0, Math.min(WORLD_HEIGHT, WORLD_HEIGHT - (sy - transform.originY) / transform.scale))
  };
}

// ══════════════════════════════════════════════════════════
// CANVAS DRAWING — RICH INDUSTRIAL WAREHOUSE
// ══════════════════════════════════════════════════════════

// Navigation path network nodes (spider/star pattern)
const NAV_NODES = [
  // Dock row
  { x: 5, y: 3 }, { x: 10, y: 3 }, { x: 15, y: 3 }, { x: 20, y: 3 }, { x: 25, y: 3 }, { x: 30, y: 3 }, { x: 35, y: 3 },
  // Aisle row 1
  { x: 5, y: 8 }, { x: 10, y: 8 }, { x: 15, y: 8 }, { x: 20, y: 8 }, { x: 25, y: 8 }, { x: 30, y: 8 }, { x: 35, y: 8 },
  // Staging row
  { x: 5, y: 15 }, { x: 10, y: 15 }, { x: 15, y: 15 }, { x: 20, y: 15 }, { x: 25, y: 15 }, { x: 30, y: 15 }, { x: 35, y: 15 },
  // Aisle row 2
  { x: 5, y: 22 }, { x: 10, y: 22 }, { x: 15, y: 22 }, { x: 20, y: 22 }, { x: 25, y: 22 }, { x: 30, y: 22 }, { x: 35, y: 22 },
  // Top bay row
  { x: 5, y: 27 }, { x: 10, y: 27 }, { x: 15, y: 27 }, { x: 20, y: 27 }, { x: 25, y: 27 }, { x: 30, y: 27 }, { x: 35, y: 27 },
];

const NAV_EDGES = [
  // Horizontal rows
  [0,1],[1,2],[2,3],[3,4],[4,5],[5,6],
  [7,8],[8,9],[9,10],[10,11],[11,12],[12,13],[13,14],
  [15,16],[16,17],[17,18],[18,19],[19,20],[20,21],
  [22,23],[23,24],[24,25],[25,26],[26,27],[27,28],
  [29,30],[30,31],[31,32],[32,33],[33,34],[34,35],
  // Vertical columns
  [0,7],[7,15],[15,22],[22,29],
  [1,8],[8,16],[16,23],[23,30],
  [2,9],[9,17],[17,24],[24,31],
  [3,10],[10,18],[18,25],[25,32],
  [4,11],[11,19],[19,26],[26,33],
  [5,12],[12,20],[20,27],[27,34],
  [6,13],[13,21],[21,28],[28,35],
  // Diagonal cross-links — dense spider-web
  [0,8],[1,7],[1,9],[2,8],[2,10],[3,9],[3,11],[4,10],[4,12],[5,11],[5,13],[6,12],
  [7,16],[8,15],[9,16],[10,17],[11,18],[12,19],[13,20],
  [15,23],[16,22],[17,23],[18,24],[19,25],[20,26],[21,27],
  [22,30],[23,29],[24,30],[25,31],[26,32],[27,33],[28,34],
  // Long-range diagonals for web density
  [8,18],[10,16],[12,18],[18,26],[20,24],[16,24],
  [9,19],[11,17],[13,19],[19,27],[21,25],[17,25],
  [0,11],[1,10],[5,12],[6,11],[22,32],[23,33],[24,34],[25,35],
];

// ── Animation clock ───────────────────────────────────────
let _animClock = 0;

function drawWarehouse() {
  _animClock += 0.018;
  const width  = canvas.width  / window.devicePixelRatio;
  const height = canvas.height / window.devicePixelRatio;
  ctx.clearRect(0, 0, width, height);

  const origin = worldToScreen(0, WORLD_HEIGHT);
  const wW = WORLD_WIDTH  * transform.scale;
  const wH = WORLD_HEIGHT * transform.scale;

  // ── 1. FLOOR — concrete gradient ────────────────────────
  const floorGrad = ctx.createLinearGradient(origin.x, origin.y, origin.x + wW, origin.y + wH);
  floorGrad.addColorStop(0,   "#050d18");
  floorGrad.addColorStop(0.45,"#070f1b");
  floorGrad.addColorStop(1,   "#040a12");
  ctx.fillStyle = floorGrad;
  ctx.fillRect(origin.x, origin.y, wW, wH);

  // Floor zone tints
  const nsH = 6 * transform.scale;
  ctx.fillStyle = "rgba(5,20,45,0.55)";
  ctx.fillRect(origin.x, origin.y, wW, nsH);          // north rack area darker

  const cfTL = worldToScreen(0, 20);
  ctx.fillStyle = "rgba(9,17,30,0.28)";
  ctx.fillRect(cfTL.x, cfTL.y, wW, 10 * transform.scale);  // centre lighter

  // ── 2. METRIC GRID ──────────────────────────────────────
  ctx.lineWidth = 0.5;
  for (let gx = 0; gx <= WORLD_WIDTH; gx++) {
    const major = gx % 5 === 0;
    const p1 = worldToScreen(gx, 0), p2 = worldToScreen(gx, WORLD_HEIGHT);
    ctx.strokeStyle = major ? "rgba(0,220,255,0.055)" : "rgba(0,220,255,0.016)";
    ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
  }
  for (let gy = 0; gy <= WORLD_HEIGHT; gy++) {
    const major = gy % 5 === 0;
    const p1 = worldToScreen(0, gy), p2 = worldToScreen(WORLD_WIDTH, gy);
    ctx.strokeStyle = major ? "rgba(0,220,255,0.055)" : "rgba(0,220,255,0.016)";
    ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
  }

  // ── 3. RED WORK ZONES ───────────────────────────────────
  _drawRedZone( 8.0,  9.0, 6.0, 5.0);
  _drawRedZone(26.0,  9.0, 6.0, 5.0);
  _drawRedZone(14.5,  5.5, 5.0, 3.0);
  _drawRedZone(17.0, 18.5, 6.0, 4.5);

  // ── 4. YELLOW LOADING BAYS ──────────────────────────────
  _drawLoadingBay( 0.3, 1.2, 3.5, 3.0, "BAY-1");
  _drawLoadingBay( 9.2, 1.2, 3.5, 3.0, "BAY-2");
  _drawLoadingBay(27.5, 1.2, 3.5, 3.0, "BAY-3");
  _drawLoadingBay(36.0, 1.2, 3.5, 3.0, "BAY-4");

  // ── 5. CONVEYOR SPINE ───────────────────────────────────
  _drawConveyor(16.0, 7.5, 8.0, 12.0);

  // ── 6. PALLET RACK BLOCKS ───────────────────────────────
  _drawRackBlock( 0.4, 23.5,  9.5, 5.8, "#1a5fb4", 5, "RACK-W");
  _drawRackBlock(30.0, 23.5,  9.5, 5.8, "#1a5fb4", 5, "RACK-NE");
  _drawRackBlock(30.0, 15.5,  9.5, 7.5, "#c0392b", 4, "RACK-SE");
  _drawRackBlock(11.5, 23.0,  7.5, 5.5, "#1a5fb4", 3, "RACK-NC");
  _drawRackBlock(20.5, 23.0,  8.5, 5.5, "#2980b9", 3, "RACK-NC2");
  _drawRackBlock( 0.4, 14.5,  4.5, 8.5, "#1a5fb4", 4, "RACK-SW");

  // ── 7. GREY MESH WALL ───────────────────────────────────
  _drawMeshWall(36.5, 10.0, 3.0, 13.0);

  // ── 8. NAV PATH NETWORK (animated spider web) ───────────
  const pulse = 0.12 + 0.06 * Math.sin(_animClock * 2);
  for (const [ai, bi] of NAV_EDGES) {
    const a = NAV_NODES[ai], b = NAV_NODES[bi];
    if (!a || !b) continue;
    const pa = worldToScreen(a.x, a.y);
    const pb = worldToScreen(b.x, b.y);
    const dist = Math.hypot(b.x - a.x, b.y - a.y);
    const alpha = dist <= 5.1 ? 0.22 + pulse * 0.38 : 0.10 + pulse * 0.18;
    ctx.strokeStyle = `rgba(0,255,65,${alpha.toFixed(3)})`;
    ctx.lineWidth = dist <= 5.1
      ? Math.max(0.8, transform.scale * 0.055)
      : Math.max(0.4, transform.scale * 0.028);
    ctx.setLineDash(dist <= 7.2 ? [] : [3, 5]);
    ctx.beginPath(); ctx.moveTo(pa.x, pa.y); ctx.lineTo(pb.x, pb.y); ctx.stroke();
  }
  ctx.setLineDash([]);

  // Nav nodes
  const nodePulse = 0.40 + 0.20 * Math.sin(_animClock * 3);
  for (const node of NAV_NODES) {
    const p = worldToScreen(node.x, node.y);
    const r = Math.max(2.5, transform.scale * 0.13);
    ctx.beginPath();
    ctx.arc(p.x, p.y, r * 2.4, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(0,255,65,${(0.035 + nodePulse * 0.035).toFixed(3)})`;
    ctx.fill();
    ctx.beginPath();
    ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(0,255,65,${nodePulse.toFixed(2)})`;
    ctx.fill();
    ctx.strokeStyle = "rgba(0,255,65,0.85)";
    ctx.lineWidth = 0.5;
    ctx.stroke();
  }

  // ── 9. CHOKEPOINT ZONE ──────────────────────────────────
  const poly = state.chokepoint.polygon;
  ctx.beginPath();
  const cp0 = worldToScreen(poly[0].x, poly[0].y);
  ctx.moveTo(cp0.x, cp0.y);
  for (let i = 1; i < poly.length; i++) {
    const cp = worldToScreen(poly[i].x, poly[i].y);
    ctx.lineTo(cp.x, cp.y);
  }
  ctx.closePath();
  let chokeFill = "rgba(0,255,65,0.04)", chokeBorder = "rgba(0,255,65,0.35)";
  if (state.chokepoint.status === "OCCUPIED")  { chokeFill = "rgba(255,0,51,0.12)";    chokeBorder = "rgba(255,0,51,0.7)"; }
  if (state.chokepoint.status === "REQUESTED") { chokeFill = "rgba(255,179,0,0.08)"; chokeBorder = "rgba(255,179,0,0.6)"; }
  ctx.fillStyle = chokeFill; ctx.fill();
  ctx.lineWidth = 1.5; ctx.setLineDash([5,4]); ctx.strokeStyle = chokeBorder; ctx.stroke();
  ctx.setLineDash([]);
  const chokeCenter = worldToScreen(20.0, 15.0);
  ctx.font = `${Math.max(9, transform.scale * 0.42)}px 'Share Tech Mono'`;
  ctx.fillStyle = state.chokepoint.status === "OCCUPIED" ? "#ff0033" : "#ffb300";
  ctx.textAlign = "center";
  ctx.fillText(
    state.chokepoint.occupied_by ? `CHOKE: ${state.chokepoint.occupied_by}` : "CHOKEPOINT (2.4m)",
    chokeCenter.x, chokeCenter.y
  );

  // ── 10. FORKLIFTS ───────────────────────────────────────
  _drawForklift( 9.0,  6.5, 0.4);
  _drawForklift(27.5, 17.0, Math.PI);
  _drawForklift(14.5, 20.5, 1.8);

  // ── 11. WORKERS ─────────────────────────────────────────
  _drawWorker(13.0, 12.5, "#ffdd66");
  _drawWorker(22.5, 16.0, "#ff8800");
  _drawWorker(18.0, 21.5, "#ffdd66");
  _drawWorker( 7.0, 19.0, "#ffdd66");
  _drawWorker(31.0,  6.0, "#ff8800");

  // ── 12. PERIMETER WALLS ─────────────────────────────────
  ctx.strokeStyle = "rgba(0,220,255,0.85)";
  ctx.lineWidth = 2.5;
  ctx.shadowBlur = 14; ctx.shadowColor = "#00d4ff";
  ctx.strokeRect(origin.x, origin.y, wW, wH);
  ctx.shadowBlur = 0;

  // Dock door gaps (south)
  for (const dx of [2.8, 10.5, 19.2, 27.8]) {
    const d1 = worldToScreen(dx, 0), d2 = worldToScreen(dx + 2.8, 0);
    ctx.fillStyle = "#040a12";
    ctx.fillRect(d1.x, d1.y - 3, d2.x - d1.x, 6);
    ctx.strokeStyle = "rgba(255,179,0,0.5)"; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(d1.x, origin.y + wH); ctx.lineTo(d1.x, d1.y); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(d2.x, origin.y + wH); ctx.lineTo(d2.x, d1.y); ctx.stroke();
    ctx.font = `${Math.max(6, transform.scale * 0.3)}px 'Share Tech Mono'`;
    ctx.fillStyle = "rgba(255,179,0,0.65)"; ctx.textAlign = "center";
    ctx.fillText("DOCK", (d1.x + d2.x) / 2, origin.y + wH + 10);
  }

  // ── 13. OBSTACLES ───────────────────────────────────────
  for (const obs of state.obstacles) {
    const spos = worldToScreen(obs.x, obs.y);
    const srad = Math.max(obs.radius * transform.scale, 8);
    ctx.beginPath(); ctx.arc(spos.x, spos.y, srad, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(255,0,51,0.25)"; ctx.fill();
    ctx.strokeStyle = "#ff0033"; ctx.lineWidth = 2;
    ctx.shadowBlur = 10; ctx.shadowColor = "#ff0033"; ctx.stroke(); ctx.shadowBlur = 0;
    ctx.fillStyle = "#fff"; ctx.font = `9px 'Share Tech Mono'`; ctx.textAlign = "center";
    ctx.fillText(`\u26a0 ${obs.reporter}`, spos.x, spos.y - srad - 4);
  }

  // ── 14. ROBOTS ──────────────────────────────────────────
  for (const [ns, bot] of Object.entries(state.robots)) {
    bot.x   += (bot.targetX   - bot.x)   * 0.2;
    bot.y   += (bot.targetY   - bot.y)   * 0.2;
    bot.yaw += (bot.targetYaw - bot.yaw) * 0.2;
    if (!bot.trail) bot.trail = [];
    bot.trail.push({ x: bot.x, y: bot.y });
    if (bot.trail.length > 30) bot.trail.shift();
    if (bot.trail.length > 1) {
      for (let i = 1; i < bot.trail.length; i++) {
        const alpha = (i / bot.trail.length) * 0.5;
        const pa = worldToScreen(bot.trail[i-1].x, bot.trail[i-1].y);
        const pb = worldToScreen(bot.trail[i].x,   bot.trail[i].y);
        ctx.beginPath(); ctx.moveTo(pa.x, pa.y); ctx.lineTo(pb.x, pb.y);
        ctx.strokeStyle = bot.color + Math.floor(alpha * 255).toString(16).padStart(2, "0");
        ctx.lineWidth = Math.max(1, transform.scale * 0.08); ctx.stroke();
      }
    }
    drawRobotGlyph(bot);
  }

  // ── 15. MOUSE CROSSHAIR ─────────────────────────────────
  if (state.mouse.onCanvas) {
    const mPos = worldToScreen(state.mouse.worldX, state.mouse.worldY);
    ctx.strokeStyle = "rgba(0,255,255,0.28)"; ctx.lineWidth = 1; ctx.setLineDash([3,4]);
    ctx.beginPath();
    ctx.moveTo(mPos.x, origin.y); ctx.lineTo(mPos.x, origin.y + wH);
    ctx.moveTo(origin.x, mPos.y); ctx.lineTo(origin.x + wW, mPos.y);
    ctx.stroke(); ctx.setLineDash([]);
    ctx.beginPath(); ctx.arc(mPos.x, mPos.y, 5, 0, Math.PI * 2);
    ctx.strokeStyle = "#00ffff"; ctx.lineWidth = 1;
    ctx.shadowBlur = 8; ctx.shadowColor = "#00ffff"; ctx.stroke(); ctx.shadowBlur = 0;
  }
}

// ── Helper: hex string → "R,G,B" ─────────────────────────
function _hexRgb(hex) {
  const m = hex.replace("#","").match(/.{2}/g);
  return m ? `${parseInt(m[0],16)},${parseInt(m[1],16)},${parseInt(m[2],16)}` : "100,150,200";
}

// ── Multi-level pallet rack ───────────────────────────────
function _drawRackBlock(x, y, w, h, steelHex, levels, label) {
  const p = worldToScreen(x, y + h);
  const sw = w * transform.scale, sh = h * transform.scale;
  const lh = sh / levels;
  const cols = Math.max(4, Math.floor(w / 1.2));

  // Drop shadow
  ctx.fillStyle = "rgba(0,0,0,0.55)";
  ctx.fillRect(p.x + 3, p.y + 3, sw, sh);
  // Background
  ctx.fillStyle = "rgba(3,8,18,0.92)";
  ctx.fillRect(p.x, p.y, sw, sh);

  // Shelves & boxes
  for (let lv = 0; lv < levels; lv++) {
    const ly = p.y + sh - (lv + 1) * lh;
    // Shelf beam
    ctx.fillStyle = `rgba(${_hexRgb(steelHex)},0.50)`;
    ctx.fillRect(p.x, ly + lh - 3, sw, 4);

    const boxW = sw / cols - 3, boxH = lh * 0.70;
    for (let c = 0; c < cols; c++) {
      const bx = p.x + (sw / cols) * c + 1.5;
      const by = ly + (lh - boxH) * 0.5;
      // 4-way colour cycle: orange, blue, brown, blue-tote
      const v = (lv + c) % 4;
      const [bFill, bStroke] = [
        ["rgba(210,140,50,0.72)","rgba(240,175,70,0.55)"],
        ["rgba(28,88,185,0.68)", "rgba(55,128,220,0.55)"],
        ["rgba(175,95,28,0.58)", "rgba(210,130,50,0.46)"],
        ["rgba(45,108,200,0.60)","rgba(78,140,230,0.48)"],
      ][v];
      ctx.fillStyle = bFill; ctx.fillRect(bx, by, boxW, boxH);
      ctx.strokeStyle = bStroke; ctx.lineWidth = 0.5; ctx.strokeRect(bx, by, boxW, boxH);
      // Highlight top edge
      ctx.fillStyle = "rgba(255,255,255,0.07)"; ctx.fillRect(bx, by, boxW, 2);
    }
  }
  // Uprights
  for (let c = 0; c <= cols; c++) {
    const lx = p.x + (sw / cols) * c;
    ctx.fillStyle = (c === 0 || c === cols)
      ? `rgba(${_hexRgb(steelHex)},0.82)` : `rgba(${_hexRgb(steelHex)},0.50)`;
    ctx.fillRect(lx - 2, p.y, 4, sh);
  }
  // Neon border
  ctx.strokeStyle = `rgba(${_hexRgb(steelHex)},0.72)`;
  ctx.lineWidth = 1.5; ctx.shadowBlur = 5; ctx.shadowColor = steelHex;
  ctx.strokeRect(p.x, p.y, sw, sh); ctx.shadowBlur = 0;
  // Label
  if (label) {
    const fs = Math.max(6, transform.scale * 0.37);
    ctx.font = `${fs}px 'Share Tech Mono'`;
    ctx.fillStyle = "rgba(0,200,255,0.62)";
    ctx.textAlign = "center";
    ctx.fillText(label, p.x + sw / 2, p.y - 3);
  }
}

// ── Red hazard zone with cross-hatch ─────────────────────
function _drawRedZone(x, y, w, h) {
  const p = worldToScreen(x, y + h);
  const sw = w * transform.scale, sh = h * transform.scale;
  ctx.fillStyle = "rgba(210,25,25,0.065)"; ctx.fillRect(p.x, p.y, sw, sh);
  ctx.strokeStyle = "rgba(210,25,25,0.20)"; ctx.lineWidth = 0.8; ctx.setLineDash([4,6]);
  for (let i = -sh; i < sw + sh; i += 13) {
    ctx.beginPath(); ctx.moveTo(p.x + i, p.y); ctx.lineTo(p.x + i + sh, p.y + sh); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(p.x + sw - i, p.y); ctx.lineTo(p.x + sw - i - sh, p.y + sh); ctx.stroke();
  }
  ctx.setLineDash([]);
  ctx.strokeStyle = "rgba(210,25,25,0.46)"; ctx.lineWidth = 1.2; ctx.strokeRect(p.x, p.y, sw, sh);
}

// ── Yellow loading bay ────────────────────────────────────
function _drawLoadingBay(x, y, w, h, label) {
  const p = worldToScreen(x, y + h);
  const sw = w * transform.scale, sh = h * transform.scale;
  const strW = Math.max(3, transform.scale * 0.24);
  for (let i = 0; i < sw; i += strW * 2) {
    ctx.fillStyle = "rgba(255,200,0,0.11)"; ctx.fillRect(p.x + i, p.y, strW, sh);
  }
  ctx.strokeStyle = "rgba(255,200,0,0.52)"; ctx.lineWidth = 1.5;
  ctx.setLineDash([5,3]); ctx.strokeRect(p.x, p.y, sw, sh); ctx.setLineDash([]);
  const fs = Math.max(6, transform.scale * 0.33);
  ctx.font = `${fs}px 'Share Tech Mono'`; ctx.fillStyle = "rgba(255,200,0,0.72)";
  ctx.textAlign = "center"; ctx.fillText(label, p.x + sw / 2, p.y + sh / 2 + 2);
}

// ── Conveyor / staging area ───────────────────────────────
function _drawConveyor(x, y, w, h) {
  const p = worldToScreen(x, y + h);
  const sw = w * transform.scale, sh = h * transform.scale;
  const strW = Math.max(4, transform.scale * 0.27);
  for (let i = 0; i < sw; i += strW * 2) {
    ctx.fillStyle = "rgba(255,160,0,0.032)"; ctx.fillRect(p.x + i, p.y, strW, sh);
  }
  ctx.strokeStyle = "rgba(255,160,0,0.26)"; ctx.lineWidth = 1; ctx.setLineDash([8,5]);
  for (let r = 0; r < 4; r++) {
    const ly = p.y + (sh / 4) * r + sh / 8;
    ctx.beginPath(); ctx.moveTo(p.x, ly); ctx.lineTo(p.x + sw, ly); ctx.stroke();
  }
  ctx.setLineDash([]);
  const fc = worldToScreen(x + w / 2, y + h / 2);
  const fs = Math.max(7, transform.scale * 0.4);
  ctx.font = `bold ${fs}px 'Share Tech Mono'`; ctx.fillStyle = "rgba(255,160,0,0.38)";
  ctx.textAlign = "center"; ctx.fillText("STAGING / CONVEYOR", fc.x, fc.y);
}

// ── Mesh shelving wall ────────────────────────────────────
function _drawMeshWall(x, y, w, h) {
  const p = worldToScreen(x, y + h);
  const sw = w * transform.scale, sh = h * transform.scale;
  ctx.fillStyle = "rgba(120,130,140,0.11)"; ctx.fillRect(p.x, p.y, sw, sh);
  const cell = Math.max(4, transform.scale * 0.34);
  ctx.strokeStyle = "rgba(140,158,178,0.28)"; ctx.lineWidth = 0.5;
  for (let gx = p.x; gx < p.x + sw; gx += cell) {
    ctx.beginPath(); ctx.moveTo(gx, p.y); ctx.lineTo(gx, p.y + sh); ctx.stroke();
  }
  for (let gy = p.y; gy < p.y + sh; gy += cell) {
    ctx.beginPath(); ctx.moveTo(p.x, gy); ctx.lineTo(p.x + sw, gy); ctx.stroke();
  }
  ctx.strokeStyle = "rgba(140,158,178,0.42)"; ctx.lineWidth = 1.2;
  ctx.strokeRect(p.x, p.y, sw, sh);
}

// ── Forklift ─────────────────────────────────────────────
function _drawForklift(wx, wy, angle) {
  const p = worldToScreen(wx, wy);
  const sz = Math.max(5, transform.scale * 0.55);
  ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(angle);
  ctx.fillStyle = "rgba(215,155,18,0.78)"; ctx.fillRect(-sz*.9,-sz*.55, sz*1.8, sz*1.1);
  ctx.fillStyle = "rgba(175,115,8,0.82)";  ctx.fillRect(-sz*.9,-sz*1.1, sz*.9,  sz*0.6);
  ctx.fillStyle = "rgba(100,100,110,0.82)";
  ctx.fillRect(sz*.9,-sz*.55, sz*.55, sz*.18);
  ctx.fillRect(sz*.9, sz*.18, sz*.55, sz*.18);
  ctx.fillStyle = "#111";
  [[-sz*.6,sz*.55],[sz*.4,sz*.55]].forEach(([ex,ey])=>{
    ctx.beginPath(); ctx.arc(ex,ey,sz*.22,0,Math.PI*2); ctx.fill();
  });
  ctx.restore();
}

// ── Worker silhouette ─────────────────────────────────────
function _drawWorker(wx, wy, vest) {
  const p = worldToScreen(wx, wy);
  const sz = Math.max(3, transform.scale * 0.37);
  ctx.save(); ctx.translate(p.x, p.y);
  ctx.beginPath(); ctx.arc(0,-sz*1.7,sz*.45,0,Math.PI*2);
  ctx.fillStyle="rgba(210,170,130,0.80)"; ctx.fill();
  ctx.beginPath();
  ctx.moveTo(-sz*.5,-sz*1.2); ctx.lineTo(sz*.5,-sz*1.2);
  ctx.lineTo(sz*.6,sz*.2);    ctx.lineTo(-sz*.6,sz*.2); ctx.closePath();
  ctx.fillStyle=vest+"cc"; ctx.fill();
  ctx.fillStyle="rgba(40,40,80,0.70)";
  ctx.fillRect(-sz*.44,sz*.2,sz*.37,sz*.8);
  ctx.fillRect( sz*.07,sz*.2,sz*.37,sz*.8);
  ctx.restore();
}

// Keep old wrapper names for backward-compat (not called but safe to keep)
function drawPalletRackBlock(x,y,w,h,label,rows) { _drawRackBlock(x,y,w,h,"#1a5fb4",rows,label); }
function drawStagingArea(x,y,w,h)                { _drawConveyor(x,y,w,h); }
function drawWorkZone(x,y,w,h,fill,stroke,label)  { _drawRedZone(x,y,w,h); }
function drawLoadingBay(x,y,w,h,label)            { _drawLoadingBay(x,y,w,h,label); }

function drawRobotGlyph(bot) {
  const p = worldToScreen(bot.x, bot.y);
  const radius = Math.max(7, 0.42 * transform.scale);
  ctx.save(); ctx.translate(p.x, p.y);
  const halo = ctx.createRadialGradient(0,0,radius,0,0,radius*2.6);
  halo.addColorStop(0, bot.color+"44"); halo.addColorStop(1,"transparent");
  ctx.beginPath(); ctx.arc(0,0,radius*2.6,0,Math.PI*2);
  ctx.fillStyle=halo; ctx.fill();
  ctx.rotate(-bot.yaw);
  ctx.beginPath(); ctx.arc(0,0,radius,0,Math.PI*2);
  ctx.fillStyle="#000814"; ctx.fill();
  ctx.strokeStyle=bot.color; ctx.lineWidth=2.5;
  ctx.shadowBlur=14; ctx.shadowColor=bot.color; ctx.stroke(); ctx.shadowBlur=0;
  ctx.beginPath(); ctx.moveTo(radius*.4,0); ctx.lineTo(radius*1.45,0);
  ctx.strokeStyle=bot.color; ctx.lineWidth=2.5;
  ctx.shadowBlur=8; ctx.shadowColor=bot.color; ctx.stroke(); ctx.shadowBlur=0;
  ctx.beginPath(); ctx.arc(0,0,3,0,Math.PI*2);
  ctx.fillStyle=bot.color; ctx.shadowBlur=8; ctx.shadowColor=bot.color; ctx.fill(); ctx.shadowBlur=0;
  ctx.restore();
  const fs=Math.max(9,transform.scale*.45);
  ctx.font=`${fs}px 'Share Tech Mono'`;
  ctx.fillStyle=bot.color; ctx.shadowBlur=6; ctx.shadowColor=bot.color;
  ctx.textAlign="center"; ctx.fillText(bot.id.toUpperCase(),p.x,p.y-radius-5);
  ctx.font=`${Math.max(7,transform.scale*.35)}px 'Share Tech Mono'`;
  ctx.fillStyle=bot.status==="BUSY"?"#00ffff":"#00ff41";
  ctx.shadowColor=bot.status==="BUSY"?"#00ffff":"#00ff41";
  ctx.fillText(bot.status,p.x,p.y+radius+13); ctx.shadowBlur=0;
}

// Animation loop
function animate() {
  drawWarehouse();
  requestAnimationFrame(animate);
}


// ══════════════════════════════════════════════════════════
// USER INTERACTIONS
// ══════════════════════════════════════════════════════════
container.addEventListener("mousemove", (e) => {
  const rect = canvas.getBoundingClientRect();
  const wc = screenToWorld(e.clientX - rect.left, e.clientY - rect.top);
  state.mouse.worldX = parseFloat(wc.x.toFixed(2));
  state.mouse.worldY = parseFloat(wc.y.toFixed(2));
  state.mouse.onCanvas = true;
  document.getElementById("cursor-coords").textContent =
    `X: ${state.mouse.worldX.toFixed(1)}m, Y: ${state.mouse.worldY.toFixed(1)}m`;
});

container.addEventListener("mouseleave", () => { state.mouse.onCanvas = false; });

container.addEventListener("click", (e) => {
  const rect = canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left;
  const sy = e.clientY - rect.top;
  const wc = screenToWorld(sx, sy);

  const ripple = document.getElementById("click-ripple");
  ripple.style.left = `${sx}px`;
  ripple.style.top  = `${sy}px`;
  ripple.classList.remove("active");
  void ripple.offsetWidth;
  ripple.classList.add("active");

  const selectedRobot = document.getElementById("select-robot").value;
  sendDispatch(wc.x, wc.y, selectedRobot);
});

document.querySelectorAll(".preset-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const x = parseFloat(btn.dataset.x);
    const y = parseFloat(btn.dataset.y);
    sendDispatch(x, y, document.getElementById("select-robot").value);
  });
});

document.getElementById("form-custom-dispatch").addEventListener("submit", (e) => {
  e.preventDefault();
  const x = parseFloat(document.getElementById("input-x").value);
  const y = parseFloat(document.getElementById("input-y").value);
  sendDispatch(x, y, document.getElementById("select-robot").value);
});

document.getElementById("btn-reset-view").addEventListener("click", resizeCanvas);

const estopBtn = document.getElementById("btn-estop");
estopBtn.addEventListener("click", () => {
  state.emergencyHalt = !state.emergencyHalt;
  if (state.emergencyHalt) {
    estopBtn.classList.remove("btn-danger");
    estopBtn.classList.add("btn-primary");
    estopBtn.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg><span>RESUME</span>`;
    sendEstop("halt");
  } else {
    estopBtn.classList.remove("btn-primary");
    estopBtn.classList.add("btn-danger");
    estopBtn.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><rect x="9" y="9" width="6" height="6"></rect></svg><span>E-HALT</span>`;
    sendEstop("resume");
  }
});

document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach((c) => c.classList.remove("active"));
    btn.classList.add("active");
    const target = document.getElementById(btn.dataset.tab);
    if (target) target.classList.add("active");
  });
});

document.getElementById("btn-clear-events").addEventListener("click", () => {
  document.getElementById("events-feed").innerHTML = `
    <div class="event-item system">
      <span class="event-time">${new Date().toLocaleTimeString()}</span>
      <span class="event-tag">SYSTEM</span>
      <span class="event-msg">Event log cleared</span>
    </div>`;
});

// ══════════════════════════════════════════════════════════
// WEBSOCKET + REST — HARDENED DDS CONNECTION
// ══════════════════════════════════════════════════════════
let ws = null;
let wsReconnectTimer = null;
const WS_PRIMARY_PORT  = 8090;
const WS_FALLBACK_PORT = 8080;

function getWsUrl(port) {
  // If page is served from file:// or a different host, use explicit localhost
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  if (!window.location.host || window.location.protocol === "file:") {
    return `${proto}//localhost:${port}/ws`;
  }
  // If served from the bridge server itself, use same host but explicit ws path
  const host = window.location.hostname;
  return `${proto}//${host}:${port}/ws`;
}

function getApiBase(port) {
  if (!window.location.host || window.location.protocol === "file:") {
    return `http://localhost:${port}`;
  }
  return `http://${window.location.hostname}:${port}`;
}

let currentPort = WS_PRIMARY_PORT;

function connectWebSocket() {
  if (wsReconnectTimer) clearTimeout(wsReconnectTimer);
  const url = getWsUrl(currentPort);
  updateConnectionStatus("connecting", `CONNECTING:${currentPort}...`);

  try {
    ws = new WebSocket(url);

    ws.onopen = () => {
      state.connected = true;
      updateConnectionStatus("online", `DDS MESH ONLINE :${currentPort}`);
      addLocalEvent("SYSTEM", `WebSocket connected on port ${currentPort}`);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleTelemetry(data);
      } catch (err) {
        console.warn("Telemetry parse error:", err);
      }
    };

    ws.onerror = () => { /* handled in onclose */ };

    ws.onclose = () => {
      state.connected = false;
      updateConnectionStatus("offline", "RECONNECTING...");
      // Try fallback port once before retrying primary
      if (currentPort === WS_PRIMARY_PORT) {
        currentPort = WS_FALLBACK_PORT;
      } else {
        currentPort = WS_PRIMARY_PORT;
      }
      wsReconnectTimer = setTimeout(connectWebSocket, 2500);
    };
  } catch (e) {
    console.warn("WebSocket init failed, falling back to HTTP polling:", e);
    updateConnectionStatus("connecting", "HTTP POLL MODE");
    setInterval(pollTelemetryFallback, 500);
  }
}

function updateConnectionStatus(type, text) {
  const pill  = document.getElementById("connection-pill");
  const ptext = document.getElementById("connection-text");
  if (pill)  pill.className  = `status-pill ${type}`;
  if (ptext) ptext.textContent = text;
}

function sendDispatch(x, y, robotId = "auto") {
  const payload = { type: "dispatch", x: parseFloat(x.toFixed(2)), y: parseFloat(y.toFixed(2)), robot_id: robotId };
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(payload));
  } else {
    fetch(`${getApiBase(currentPort)}/api/dispatch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).catch((err) => console.error("Dispatch error:", err));
  }
  addLocalEvent("OPERATOR", `Dispatch → (${x.toFixed(1)}, ${y.toFixed(1)}) → ${robotId}`);
}

function sendEstop(action) {
  const payload = { type: "estop", action };
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(payload));
  } else {
    fetch(`${getApiBase(currentPort)}/api/estop`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).catch((err) => console.error("Estop error:", err));
  }
}

function handleTelemetry(data) {
  if (data.robots) {
    for (const [id, r] of Object.entries(data.robots)) {
      if (state.robots[id]) {
        state.robots[id].targetX  = r.x;
        state.robots[id].targetY  = r.y;
        state.robots[id].targetYaw = r.yaw;
        state.robots[id].status   = r.status;
        state.robots[id].reason   = r.reason || "";
      }
    }
  }
  if (data.chokepoint) {
    state.chokepoint.status      = data.chokepoint.status;
    state.chokepoint.occupied_by = data.chokepoint.occupied_by;
    state.chokepoint.contenders  = data.chokepoint.contenders || [];
  }
  if (data.obstacles)         state.obstacles  = data.obstacles;
  if (data.queue_size !== undefined) state.queue_size = data.queue_size;
  if (data.metrics) {
    state.metrics.completed_goals = data.metrics.completed_goals;
    state.metrics.throughput      = data.metrics.throughput;
  }
  if (data.events && Array.isArray(data.events)) updateEventsUI(data.events);
  updateDOM();
}

function updateDOM() {
  let idleCount = 0;
  for (const [id, bot] of Object.entries(state.robots)) {
    const pill = document.getElementById(`pill-${id}`);
    if (pill) {
      pill.textContent = `${id.replace("robot", "R")}: ${bot.status}`;
      pill.style.background = bot.status === "BUSY" ? "rgba(0,255,255,0.1)" : "";
    }
    if (bot.status !== "BUSY") idleCount++;
  }

  const fleetEl = document.getElementById("kpi-fleet-count");
  if (fleetEl) fleetEl.textContent = `${3 - idleCount} / 3 Active`;

  const thruEl = document.getElementById("kpi-throughput");
  if (thruEl) thruEl.textContent = state.metrics.throughput.toFixed(2);

  const compEl = document.getElementById("kpi-completed");
  if (compEl) compEl.textContent = state.metrics.completed_goals;

  const qEl = document.getElementById("kpi-queue-count");
  if (qEl) qEl.textContent = state.queue_size;

  // Choke badge
  const cb = document.getElementById("kpi-choke-badge");
  const cs = document.getElementById("kpi-choke-subtext");
  if (cb && cs) {
    if (state.chokepoint.status === "OCCUPIED") {
      cb.className = "choke-badge occupied";
      cb.textContent = `LOCKED (${state.chokepoint.occupied_by})`;
      cs.textContent = "HEARTBEAT ACTIVE · TOKEN LEASED";
    } else if (state.chokepoint.status === "REQUESTED") {
      cb.className = "choke-badge requested";
      cb.textContent = "CONTENDING";
      cs.textContent = "ARBITRATING PRIORITY JITTER...";
    } else {
      cb.className = "choke-badge free";
      cb.textContent = "FREE";
      cs.textContent = "TOKEN AVAILABLE";
    }
  }

  // Diagnostics tab
  for (const [id, bot] of Object.entries(state.robots)) {
    const rid = id === "robot1" ? "r1" : id === "robot2" ? "r2" : "r3";
    const statusEl = document.getElementById(`diag-status-${rid}`);
    const coordsEl = document.getElementById(`diag-coords-${rid}`);
    const reasonEl = document.getElementById(`diag-reason-${rid}`);
    if (statusEl) { statusEl.className = `rh-status ${bot.status.toLowerCase()}`; statusEl.textContent = bot.status; }
    if (coordsEl) coordsEl.textContent = `X: ${bot.x.toFixed(2)}m  Y: ${bot.y.toFixed(2)}m  YAW: ${(bot.yaw * 180 / Math.PI).toFixed(0)}°`;
    if (reasonEl) reasonEl.textContent = bot.reason || "Normal Navigation";
  }
}

function updateEventsUI(events) {
  const feed = document.getElementById("events-feed");
  if (!events || events.length === 0 || !feed) return;
  feed.innerHTML = events.map((ev) => {
    const cls = ev.source ? ev.source.toLowerCase().replace(/\s/g, "") : "system";
    return `<div class="event-item ${cls}">
      <span class="event-time">${ev.time}</span>
      <span class="event-tag">${ev.source}</span>
      <span class="event-msg">${ev.msg}</span>
    </div>`;
  }).join("");
}

function addLocalEvent(source, msg) {
  const feed = document.getElementById("events-feed");
  if (!feed) return;
  const t = new Date().toLocaleTimeString();
  const div = document.createElement("div");
  div.className = `event-item ${source.toLowerCase()}`;
  div.innerHTML = `<span class="event-time">${t}</span><span class="event-tag">${source}</span><span class="event-msg">${msg}</span>`;
  feed.prepend(div);
  while (feed.children.length > 50) feed.removeChild(feed.lastChild);
}

function pollTelemetryFallback() {
  if (state.connected) return;
  const bases = [getApiBase(WS_PRIMARY_PORT), getApiBase(WS_FALLBACK_PORT)];
  const base = bases[Math.floor(Date.now() / 2000) % 2];
  fetch(`${base}/api/state`)
    .then((r) => r.json())
    .then((data) => {
      updateConnectionStatus("online", "DDS HTTP POLL");
      handleTelemetry(data);
    })
    .catch(() => {
      updateConnectionStatus("offline", "OFFLINE");
    });
}
