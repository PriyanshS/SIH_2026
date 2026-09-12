/**
 * Decentralized Multi-AMR Fleet Console — Core Application Logic
 * Features:
 * - High-performance 60 FPS Canvas rendering loop with metric coordinate mapping.
 * - Bidirectional WebSocket telemetry streaming with automatic reconnection & REST fallback.
 * - Interactive Click-to-Dispatch with spatial coordinate conversion & visual ripple.
 * - Dynamic P2P event log, chokepoint lock visualizer, and KPI metrics.
 */

// Warehouse geometry (meters)
const WORLD_WIDTH = 20.0;
const WORLD_HEIGHT = 15.0;

// State Cache
const state = {
  connected: false,
  robots: {
    robot1: { id: "robot1", x: 3.0, y: 2.0, yaw: 0.0, targetX: 3.0, targetY: 2.0, targetYaw: 0.0, status: "IDLE", reason: "", color: "#ef4444", trail: [] },
    robot2: { id: "robot2", x: 10.0, y: 1.5, yaw: 0.0, targetX: 10.0, targetY: 1.5, targetYaw: 0.0, status: "IDLE", reason: "", color: "#10b981", trail: [] },
    robot3: { id: "robot3", x: 17.0, y: 2.0, yaw: 0.0, targetX: 17.0, targetY: 2.0, targetYaw: 0.0, status: "IDLE", reason: "", color: "#3b82f6", trail: [] },
  },
  chokepoint: {
    occupied_by: null,
    status: "FREE",
    contenders: [],
    polygon: [
      { x: 8.5, y: 5.5 },
      { x: 12.0, y: 5.5 },
      { x: 12.0, y: 9.5 },
      { x: 8.5, y: 9.5 }
    ]
  },
  obstacles: [],
  queue_size: 0,
  metrics: {
    completed_goals: 0,
    throughput: 0.0
  },
  events: [],
  mouse: {
    worldX: 10.0,
    worldY: 7.5,
    onCanvas: false
  },
  emergencyHalt: false
};

// Canvas & Rendering Context
const canvas = document.getElementById("warehouse-canvas");
const ctx = canvas.getContext("2d");
const container = document.getElementById("canvas-container");
let transform = { scale: 30, originX: 40, originY: 40 };

// Initialize Canvas Size
function resizeCanvas() {
  const rect = container.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

  // Compute scale maintaining 20x15 aspect ratio with padding
  const pad = 40;
  const availW = rect.width - pad * 2;
  const availH = rect.height - pad * 2;
  const scaleX = availW / WORLD_WIDTH;
  const scaleY = availH / WORLD_HEIGHT;
  const scale = Math.min(scaleX, scaleY);

  transform.scale = scale;
  transform.originX = (rect.width - WORLD_WIDTH * scale) / 2;
  transform.originY = (rect.height - WORLD_HEIGHT * scale) / 2;
}

window.addEventListener("resize", resizeCanvas);

// Coordinate Transformations (World Metric Meters <-> Screen Pixels)
function worldToScreen(wx, wy) {
  return {
    x: transform.originX + wx * transform.scale,
    y: transform.originY + (WORLD_HEIGHT - wy) * transform.scale
  };
}

function screenToWorld(sx, sy) {
  return {
    x: Math.max(0, Math.min(WORLD_WIDTH, (sx - transform.originX) / transform.scale)),
    y: Math.max(0, Math.min(WORLD_HEIGHT, WORLD_HEIGHT - (sy - transform.originY) / transform.scale))
  };
}

// ==========================================================================
// Canvas Drawing Routines
// ==========================================================================
function drawWarehouse() {
  const width = canvas.width / window.devicePixelRatio;
  const height = canvas.height / window.devicePixelRatio;
  ctx.clearRect(0, 0, width, height);

  // 1. Grid lines (1m subtle, 5m highlighted)
  ctx.lineWidth = 1;
  for (let x = 0; x <= WORLD_WIDTH; x += 1.0) {
    const isMajor = x % 5 === 0;
    const p1 = worldToScreen(x, 0);
    const p2 = worldToScreen(x, WORLD_HEIGHT);
    ctx.strokeStyle = isMajor ? "rgba(255, 255, 255, 0.12)" : "rgba(255, 255, 255, 0.035)";
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();

    if (isMajor) {
      ctx.fillStyle = "rgba(148, 163, 184, 0.4)";
      ctx.font = "10px JetBrains Mono";
      ctx.fillText(`${x}m`, p1.x + 2, p1.y + 14);
    }
  }

  for (let y = 0; y <= WORLD_HEIGHT; y += 1.0) {
    const isMajor = y % 5 === 0;
    const p1 = worldToScreen(0, y);
    const p2 = worldToScreen(WORLD_WIDTH, y);
    ctx.strokeStyle = isMajor ? "rgba(255, 255, 255, 0.12)" : "rgba(255, 255, 255, 0.035)";
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();

    if (isMajor) {
      ctx.fillStyle = "rgba(148, 163, 184, 0.4)";
      ctx.font = "10px JetBrains Mono";
      ctx.fillText(`${y}m`, p1.x - 24, p1.y - 2);
    }
  }

  // 2. Chokepoint Critical Section Polygon
  const poly = state.chokepoint.polygon;
  ctx.beginPath();
  const cp0 = worldToScreen(poly[0].x, poly[0].y);
  ctx.moveTo(cp0.x, cp0.y);
  for (let i = 1; i < poly.length; i++) {
    const cp = worldToScreen(poly[i].x, poly[i].y);
    ctx.lineTo(cp.x, cp.y);
  }
  ctx.closePath();

  // Color according to choke status
  let chokeFill = "rgba(16, 185, 129, 0.08)";
  let chokeBorder = "rgba(16, 185, 129, 0.4)";
  if (state.chokepoint.status === "OCCUPIED") {
    chokeFill = "rgba(239, 68, 68, 0.18)";
    chokeBorder = "rgba(239, 68, 68, 0.6)";
  } else if (state.chokepoint.status === "REQUESTED") {
    chokeFill = "rgba(245, 158, 11, 0.14)";
    chokeBorder = "rgba(245, 158, 11, 0.5)";
  }
  ctx.fillStyle = chokeFill;
  ctx.fill();
  ctx.lineWidth = 1.5;
  ctx.setLineDash([4, 4]);
  ctx.strokeStyle = chokeBorder;
  ctx.stroke();
  ctx.setLineDash([]);

  // Label inside chokepoint
  const chokeCenter = worldToScreen(10.25, 7.5);
  ctx.font = "11px Outfit, sans-serif";
  ctx.fillStyle = state.chokepoint.status === "OCCUPIED" ? "#ef4444" : "#f59e0b";
  ctx.textAlign = "center";
  const chokeText = state.chokepoint.occupied_by ? `CHOKE: ${state.chokepoint.occupied_by}` : "CHOKEPOINT (2.4m)";
  ctx.fillText(chokeText, chokeCenter.x, chokeCenter.y);

  // 3. Storage Shelves / Racks
  drawShelf(3.8, 4.0, 3.0, 7.0, "STORAGE RACK A");
  drawShelf(13.2, 4.0, 3.0, 7.0, "STORAGE RACK B");

  // Center structural wall segments
  drawWall(9.8, 0.0, 0.4, 5.5);
  drawWall(9.8, 9.5, 0.4, 5.5);

  // 4. Perimeter Warehouse Walls
  const origin = worldToScreen(0, WORLD_HEIGHT);
  const wWidth = WORLD_WIDTH * transform.scale;
  const wHeight = WORLD_HEIGHT * transform.scale;
  ctx.strokeStyle = "#38bdf8";
  ctx.lineWidth = 3;
  ctx.strokeRect(origin.x, origin.y, wWidth, wHeight);

  // 5. Dynamic Obstacles
  for (const obs of state.obstacles) {
    const spos = worldToScreen(obs.x, obs.y);
    const srad = Math.max(obs.radius * transform.scale, 8);

    ctx.beginPath();
    ctx.arc(spos.x, spos.y, srad, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(249, 115, 22, 0.4)";
    ctx.fill();
    ctx.strokeStyle = "#f97316";
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = "#fff";
    ctx.font = "9px Inter, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(`Hazard (${obs.reporter})`, spos.x, spos.y - srad - 4);
  }

  // 6. Draw Robots with Smooth Interpolation
  for (const [ns, bot] of Object.entries(state.robots)) {
    // Interpolate towards target
    bot.x += (bot.targetX - bot.x) * 0.25;
    bot.y += (bot.targetY - bot.y) * 0.25;
    bot.yaw += (bot.targetYaw - bot.yaw) * 0.25;

    // Add trail
    if (!bot.trail) bot.trail = [];
    bot.trail.push({ x: bot.x, y: bot.y });
    if (bot.trail.length > 25) bot.trail.shift();

    // Draw trail
    if (bot.trail.length > 1) {
      ctx.beginPath();
      const tp0 = worldToScreen(bot.trail[0].x, bot.trail[0].y);
      ctx.moveTo(tp0.x, tp0.y);
      for (let i = 1; i < bot.trail.length; i++) {
        const tp = worldToScreen(bot.trail[i].x, bot.trail[i].y);
        ctx.lineTo(tp.x, tp.y);
      }
      ctx.strokeStyle = bot.color + "44";
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    drawRobotGlyph(bot);
  }

  // 7. Mouse Crosshair & Coordinate Indicator
  if (state.mouse.onCanvas) {
    const mPos = worldToScreen(state.mouse.worldX, state.mouse.worldY);
    ctx.strokeStyle = "rgba(6, 182, 212, 0.4)";
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);

    ctx.beginPath();
    ctx.moveTo(mPos.x, origin.y);
    ctx.lineTo(mPos.x, origin.y + wHeight);
    ctx.moveTo(origin.x, mPos.y);
    ctx.lineTo(origin.x + wWidth, mPos.y);
    ctx.stroke();
    ctx.setLineDash([]);

    // Small target circle
    ctx.beginPath();
    ctx.arc(mPos.x, mPos.y, 6, 0, Math.PI * 2);
    ctx.strokeStyle = "#06b6d4";
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }
}

function drawShelf(x, y, w, h, label) {
  const p = worldToScreen(x, y + h);
  const sw = w * transform.scale;
  const sh = h * transform.scale;

  // Background
  ctx.fillStyle = "rgba(30, 41, 59, 0.65)";
  ctx.fillRect(p.x, p.y, sw, sh);

  // Border
  ctx.strokeStyle = "rgba(71, 85, 105, 0.8)";
  ctx.lineWidth = 1.5;
  ctx.strokeRect(p.x, p.y, sw, sh);

  // Internal shelf racks lines
  const slots = 6;
  ctx.strokeStyle = "rgba(100, 116, 139, 0.35)";
  ctx.lineWidth = 1;
  for (let i = 1; i < slots; i++) {
    const ly = p.y + (sh / slots) * i;
    ctx.beginPath();
    ctx.moveTo(p.x, ly);
    ctx.lineTo(p.x + sw, ly);
    ctx.stroke();
  }

  // Label
  ctx.font = "10px JetBrains Mono";
  ctx.fillStyle = "rgba(203, 213, 225, 0.5)";
  ctx.textAlign = "center";
  ctx.fillText(label, p.x + sw / 2, p.y + sh / 2);
}

function drawWall(x, y, w, h) {
  const p = worldToScreen(x, y + h);
  const sw = w * transform.scale;
  const sh = h * transform.scale;
  ctx.fillStyle = "#1e293b";
  ctx.fillRect(p.x, p.y, sw, sh);
  ctx.strokeStyle = "#475569";
  ctx.lineWidth = 1.5;
  ctx.strokeRect(p.x, p.y, sw, sh);
}

function drawRobotGlyph(bot) {
  const p = worldToScreen(bot.x, bot.y);
  const radius = 0.25 * transform.scale; // physical radius = 0.25m

  ctx.save();
  ctx.translate(p.x, p.y);

  // Pulse Halo
  ctx.beginPath();
  ctx.arc(0, 0, radius + 4, 0, Math.PI * 2);
  ctx.fillStyle = bot.color + "22";
  ctx.fill();

  // Rotate by orientation yaw (flips angle because Y is flipped in canvas)
  ctx.rotate(-bot.yaw);

  // Robot Body
  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.fillStyle = bot.color;
  ctx.fill();
  ctx.strokeStyle = "#fff";
  ctx.lineWidth = 2;
  ctx.stroke();

  // Heading pointer nose
  ctx.beginPath();
  ctx.moveTo(radius * 0.6, 0);
  ctx.lineTo(radius * 1.35, 0);
  ctx.strokeStyle = "#fff";
  ctx.lineWidth = 3;
  ctx.stroke();

  // Lidar sensor center dot
  ctx.beginPath();
  ctx.arc(0, 0, 3, 0, Math.PI * 2);
  ctx.fillStyle = "#0f172a";
  ctx.fill();

  ctx.restore();

  // Text label above robot
  ctx.font = "11px Outfit, sans-serif";
  ctx.fillStyle = "#fff";
  ctx.textAlign = "center";
  ctx.fillText(bot.id.toUpperCase(), p.x, p.y - radius - 6);

  // Status tag
  const isBusy = bot.status === "BUSY";
  ctx.font = "9px Inter, sans-serif";
  ctx.fillStyle = isBusy ? "#38bdf8" : "#34d399";
  ctx.fillText(bot.status, p.x, p.y + radius + 14);
}

// Animation Loop (60 FPS)
function animate() {
  drawWarehouse();
  requestAnimationFrame(animate);
}

// ==========================================================================
// User Interaction & Dispatch
// ==========================================================================
container.addEventListener("mousemove", (e) => {
  const rect = canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left;
  const sy = e.clientY - rect.top;
  const wCoords = screenToWorld(sx, sy);
  state.mouse.worldX = parseFloat(wCoords.x.toFixed(2));
  state.mouse.worldY = parseFloat(wCoords.y.toFixed(2));
  state.mouse.onCanvas = true;

  document.getElementById("cursor-coords").textContent = `X: ${state.mouse.worldX.toFixed(1)}m, Y: ${state.mouse.worldY.toFixed(1)}m`;
});

container.addEventListener("mouseleave", () => {
  state.mouse.onCanvas = false;
});

// Canvas Click-to-Dispatch
container.addEventListener("click", (e) => {
  const rect = canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left;
  const sy = e.clientY - rect.top;
  const wCoords = screenToWorld(sx, sy);

  // Visual ripple
  const ripple = document.getElementById("click-ripple");
  ripple.style.left = `${sx}px`;
  ripple.style.top = `${sy}px`;
  ripple.classList.remove("active");
  void ripple.offsetWidth; // trigger reflow
  ripple.classList.add("active");

  const selectedRobot = document.getElementById("select-robot").value;
  sendDispatch(wCoords.x, wCoords.y, selectedRobot);
});

// Preset Buttons
document.querySelectorAll(".preset-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const x = parseFloat(btn.dataset.x);
    const y = parseFloat(btn.dataset.y);
    const selectedRobot = document.getElementById("select-robot").value;
    sendDispatch(x, y, selectedRobot);
  });
});

// Custom Form Dispatch
document.getElementById("form-custom-dispatch").addEventListener("submit", (e) => {
  e.preventDefault();
  const x = parseFloat(document.getElementById("input-x").value);
  const y = parseFloat(document.getElementById("input-y").value);
  const selectedRobot = document.getElementById("select-robot").value;
  sendDispatch(x, y, selectedRobot);
});

// Reset View Button
document.getElementById("btn-reset-view").addEventListener("click", () => {
  resizeCanvas();
});

// Emergency Stop Button
const estopBtn = document.getElementById("btn-estop");
estopBtn.addEventListener("click", () => {
  state.emergencyHalt = !state.emergencyHalt;
  if (state.emergencyHalt) {
    estopBtn.classList.remove("btn-danger");
    estopBtn.classList.add("btn-primary");
    estopBtn.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polygon points="5 3 19 12 5 21 5 3"></polygon>
      </svg>
      <span>RESUME FLEET</span>`;
    sendEstop("halt");
  } else {
    estopBtn.classList.remove("btn-primary");
    estopBtn.classList.add("btn-danger");
    estopBtn.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <rect x="9" y="9" width="6" height="6"></rect>
      </svg>
      <span>EMERGENCY HALT</span>`;
    sendEstop("resume");
  }
});

// Tabs Switching
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach((c) => c.classList.remove("active"));

    btn.classList.add("active");
    const target = document.getElementById(btn.dataset.tab);
    if (target) target.classList.add("active");
  });
});

// Clear Events Button
document.getElementById("btn-clear-events").addEventListener("click", () => {
  document.getElementById("events-feed").innerHTML = `
    <div class="event-item system">
      <span class="event-time">${new Date().toLocaleTimeString()}</span>
      <span class="event-tag">SYSTEM</span>
      <span class="event-msg">Event log cleared</span>
    </div>`;
});

// ==========================================================================
// WebSocket & REST Telemetry Communication
// ==========================================================================
let ws = null;

function connectWebSocket() {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws`;

  updateConnectionStatus("connecting", "Connecting to DDS...");

  try {
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      state.connected = true;
      updateConnectionStatus("online", "DDS Mesh Online");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleTelemetry(data);
      } catch (err) {
        console.warn("Failed to parse telemetry:", err);
      }
    };

    ws.onerror = () => {
      ws.close();
    };

    ws.onclose = () => {
      state.connected = false;
      updateConnectionStatus("offline", "Reconnecting...");
      // Reconnect after 2 seconds
      setTimeout(connectWebSocket, 2000);
    };
  } catch (e) {
    console.warn("WebSocket init error, falling back to HTTP polling:", e);
    setInterval(pollTelemetryFallback, 400);
  }
}

function updateConnectionStatus(type, text) {
  const pill = document.getElementById("connection-pill");
  const ptext = document.getElementById("connection-text");
  pill.className = `status-pill ${type}`;
  ptext.textContent = text;
}

// Telemetry Dispatch
function sendDispatch(x, y, robotId = "auto") {
  const payload = {
    type: "dispatch",
    x: parseFloat(x.toFixed(2)),
    y: parseFloat(y.toFixed(2)),
    robot_id: robotId
  };

  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(payload));
  } else {
    // REST POST fallback
    fetch("/api/dispatch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).catch((err) => console.error("Dispatch error:", err));
  }
}

function sendEstop(action) {
  const payload = { type: "estop", action: action };
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(payload));
  } else {
    fetch("/api/estop", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).catch((err) => console.error("Estop error:", err));
  }
}

// Ingest Telemetry Snapshot
function handleTelemetry(data) {
  // 1. Robots
  if (data.robots) {
    for (const [id, r] of Object.entries(data.robots)) {
      if (state.robots[id]) {
        state.robots[id].targetX = r.x;
        state.robots[id].targetY = r.y;
        state.robots[id].targetYaw = r.yaw;
        state.robots[id].status = r.status;
        state.robots[id].reason = r.reason || "";
      }
    }
  }

  // 2. Chokepoint
  if (data.chokepoint) {
    state.chokepoint.status = data.chokepoint.status;
    state.chokepoint.occupied_by = data.chokepoint.occupied_by;
    state.chokepoint.contenders = data.chokepoint.contenders || [];
  }

  // 3. Obstacles
  if (data.obstacles) {
    state.obstacles = data.obstacles;
  }

  // 4. Queue & Metrics
  if (data.queue_size !== undefined) state.queue_size = data.queue_size;
  if (data.metrics) {
    state.metrics.completed_goals = data.metrics.completed_goals;
    state.metrics.throughput = data.metrics.throughput;
  }

  // 5. Events Feed
  if (data.events && Array.isArray(data.events)) {
    updateEventsUI(data.events);
  }

  // Update UI Elements
  updateDOM();
}

function updateDOM() {
  // KPI Header
  let idleCount = 0;
  for (const [id, bot] of Object.entries(state.robots)) {
    const pill = document.getElementById(`pill-${id}`);
    if (pill) {
      pill.textContent = `${id.toUpperCase().replace("ROBOT", "R")}: ${bot.status}`;
      if (bot.status === "BUSY") {
        pill.style.background = "rgba(6, 182, 212, 0.2)";
        pill.style.borderColor = "rgba(6, 182, 212, 0.4)";
      } else {
        pill.style.background = "rgba(255, 255, 255, 0.06)";
        pill.style.borderColor = "";
        idleCount++;
      }
    }
  }
  document.getElementById("kpi-fleet-count").textContent = `${3 - idleCount} / 3 Active`;
  document.getElementById("kpi-throughput").textContent = state.metrics.throughput.toFixed(2);
  document.getElementById("kpi-completed").textContent = state.metrics.completed_goals;
  document.getElementById("kpi-queue-count").textContent = state.queue_size;

  // Choke Badge
  const chokeBadge = document.getElementById("kpi-choke-badge");
  const chokeSub = document.getElementById("kpi-choke-subtext");
  if (state.chokepoint.status === "OCCUPIED") {
    chokeBadge.className = "choke-badge occupied";
    chokeBadge.textContent = `LOCKED (${state.chokepoint.occupied_by})`;
    chokeSub.textContent = `Heartbeat active • Token leased`;
  } else if (state.chokepoint.status === "REQUESTED") {
    chokeBadge.className = "choke-badge requested";
    chokeBadge.textContent = `CONTENDING`;
    chokeSub.textContent = `Arbitrating priority jitter...`;
  } else {
    chokeBadge.className = "choke-badge free";
    chokeBadge.textContent = "FREE";
    chokeSub.textContent = "Distributed Token Available";
  }

  // Diagnostics Tab
  for (const [id, bot] of Object.entries(state.robots)) {
    const rid = id === "robot1" ? "r1" : id === "robot2" ? "r2" : "r3";
    const statusEl = document.getElementById(`diag-status-${rid}`);
    const coordsEl = document.getElementById(`diag-coords-${rid}`);
    const reasonEl = document.getElementById(`diag-reason-${rid}`);

    if (statusEl) {
      statusEl.className = `rh-status ${bot.status.toLowerCase()}`;
      statusEl.textContent = bot.status;
    }
    if (coordsEl) {
      coordsEl.textContent = `X: ${bot.x.toFixed(2)}m, Y: ${bot.y.toFixed(2)}m, Yaw: ${(bot.yaw * 180 / Math.PI).toFixed(0)}°`;
    }
    if (reasonEl) {
      reasonEl.textContent = bot.reason || "Normal Navigation";
    }
  }
}

function updateEventsUI(events) {
  const container = document.getElementById("events-feed");
  if (!events || events.length === 0) return;

  container.innerHTML = events.map((ev) => {
    let sourceClass = ev.source ? ev.source.toLowerCase() : "system";
    return `
      <div class="event-item ${sourceClass}">
        <span class="event-time">${ev.time}</span>
        <span class="event-tag">${ev.source}</span>
        <span class="event-msg">${ev.msg}</span>
      </div>`;
  }).join("");
}

// REST Fallback Polling (if WebSocket fails)
function pollTelemetryFallback() {
  if (state.connected) return;
  fetch("/api/state")
    .then((res) => res.json())
    .then((data) => {
      updateConnectionStatus("online", "DDS HTTP Polling");
      handleTelemetry(data);
    })
    .catch(() => {
      updateConnectionStatus("offline", "Offline");
    });
}

// ==========================================================================
// Kickoff
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
  resizeCanvas();
  connectWebSocket();
  requestAnimationFrame(animate);
});
