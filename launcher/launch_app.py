#!/usr/bin/env python3
"""
BEL FleetLink Launcher
━━━━━━━━━━━━━━━━━━━━━
A retro-terminal style desktop launcher for the SIH_2026 Multi-AMR system.
Provides one-click start/stop for:
  ① Gazebo Simulator (amr_gazebo sim_world.launch.py)
  ② RViz2           (amr_bringup rviz_demo.launch.py)
  ③ Web UI Bridge   (web_ui/backend/web_bridge_node.py)

Requirements: python3-tk (usually pre-installed)
Usage:  python3 launch_app.py
        OR double-click the .desktop shortcut after install_launcher.sh
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import os
import sys
import time
import signal
import webbrowser
from pathlib import Path

# ──────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent.resolve()
WORKSPACE    = SCRIPT_DIR.parent / "ros2_ws"
BACKEND_DIR  = SCRIPT_DIR.parent / "web_ui" / "backend"
WEB_UI_URL   = "http://localhost:8090"

def find_ros_setup() -> tuple[str, Path | None]:
    for distro in [os.environ.get("ROS_DISTRO", "jazzy"), "jazzy", "iron", "humble", "rolling"]:
        p = Path(f"/opt/ros/{distro}/setup.bash")
        if p.exists():
            return distro, p
    return "unknown", None

ROS_DISTRO, ROS_SETUP_PATH = find_ros_setup()
WS_SETUP = WORKSPACE / "install" / "setup.bash"
RVIZ_CONFIG = WORKSPACE / "src" / "amr_gazebo" / "rviz" / "multi_robot.rviz"

def ros_source_prefix() -> str:
    """Build a bash source prefix for ROS 2 environment."""
    cmds = []
    if ROS_SETUP_PATH and ROS_SETUP_PATH.exists():
        cmds.append(f"source {ROS_SETUP_PATH}")
    if WS_SETUP.exists():
        cmds.append(f"source {WS_SETUP}")
    return " && ".join(cmds) + " && " if cmds else ""

# ──────────────────────────────────────────────────────────
# Colors (retro 80s terminal)
# ──────────────────────────────────────────────────────────
C = {
    "bg":          "#000000",
    "bg_panel":    "#050510",
    "bg_button":   "#000814",
    "cyan":        "#00ffff",
    "magenta":     "#ff00ff",
    "green":       "#00ff41",
    "amber":       "#ffb300",
    "red":         "#ff0033",
    "muted":       "#006644",
    "white":       "#e0ffe0",
    "border":      "#00338866",
}

FONT_RETRO = ("Courier", 10, "bold")
FONT_TITLE = ("Courier", 14, "bold")
FONT_LOG   = ("Courier", 9)
FONT_KPI   = ("Courier", 18, "bold")

# ──────────────────────────────────────────────────────────
# Process Manager
# ──────────────────────────────────────────────────────────
class ManagedProcess:
    def __init__(self, name: str, cmd: str, log_fn):
        self.name    = name
        self.cmd     = cmd
        self.log_fn  = log_fn
        self.proc    = None
        self.running = False
        self._thread = None

    def start(self):
        if self.running:
            return False
        prefix = ros_source_prefix()
        full_cmd = f"bash -c '{prefix}{self.cmd}'"
        self.log_fn(f"[{self.name}] Starting...", "amber")
        self.log_fn(f"[CMD] {self.cmd}", "muted")
        try:
            self.proc = subprocess.Popen(
                full_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                preexec_fn=os.setsid,
                bufsize=1,
            )
            self.running = True
            self._thread = threading.Thread(target=self._reader, daemon=True)
            self._thread.start()
            return True
        except Exception as e:
            self.log_fn(f"[{self.name}] FAILED: {e}", "red")
            return False

    def stop(self):
        if not self.running or self.proc is None:
            return
        self.log_fn(f"[{self.name}] Stopping...", "amber")
        try:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        except Exception:
            try:
                self.proc.terminate()
            except Exception:
                pass
        self.running = False
        self.proc    = None
        self.log_fn(f"[{self.name}] Stopped.", "muted")

    def _reader(self):
        try:
            for line in self.proc.stdout:
                self.log_fn(f"[{self.name}] {line.rstrip()}", "muted")
        except Exception:
            pass
        finally:
            if self.proc:
                self.proc.wait()
            if self.running:
                self.running = False
                self.log_fn(f"[{self.name}] Process exited.", "red")


# ──────────────────────────────────────────────────────────
# Launcher GUI
# ──────────────────────────────────────────────────────────
class FleetLauncherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("BEL FleetLink — System Launcher")
        root.configure(bg=C["bg"])
        root.resizable(True, True)
        root.minsize(780, 600)

        # Configure grid weight
        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)

        self._build_header()
        self._build_process_panel()
        self._build_log_panel()
        self._build_footer()

        # Processes
        self.procs = {
            "gazebo": ManagedProcess(
                "GAZEBO",
                "ros2 launch amr_gazebo sim_world.launch.py",
                self._log
            ),
            "rviz": ManagedProcess(
                "RVIZ2",
                f"rviz2 -d {RVIZ_CONFIG}",
                self._log
            ),
            "webui": ManagedProcess(
                "WEB-UI",
                f"{sys.executable} {BACKEND_DIR / 'web_bridge_node.py'}",
                self._log
            ),
        }

        # Status labels dict
        self.status_vars = {
            "gazebo": self._status_vars["gazebo"],
            "rviz":   self._status_vars["rviz"],
            "webui":  self._status_vars["webui"],
        }

        # Poll status periodically
        self._poll_status()
        self._log("FleetLink Launcher ready.", "cyan")
        self._log(f"ROS 2 Distro: {ROS_DISTRO}", "green")
        self._log(f"Workspace:    {WORKSPACE}", "green")
        self._log(f"Web UI:       {WEB_UI_URL}", "green")
        self._log("━" * 60, "muted")

    # ── Build UI sections ────────────────────────────────

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=C["bg"], pady=6)
        hdr.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 0))

        title = tk.Label(hdr, text="▶  BEL FLEETLINK  ◀",
                         font=FONT_TITLE, fg=C["cyan"], bg=C["bg"])
        title.pack(side="left")

        sub = tk.Label(hdr,
                       text="Multi-AMR Warehouse System Launcher  |  ROS 2 Harmonic",
                       font=FONT_LOG, fg=C["muted"], bg=C["bg"])
        sub.pack(side="left", padx=(12, 0))

        # Global controls
        ctrl = tk.Frame(hdr, bg=C["bg"])
        ctrl.pack(side="right")

        self._btn(ctrl, "▶ LAUNCH ALL", self._launch_all, C["green"]).pack(side="left", padx=4)
        self._btn(ctrl, "■ STOP ALL",   self._stop_all,   C["red"]).pack(side="left", padx=4)
        self._btn(ctrl, "🌐 OPEN UI",   self._open_browser, C["cyan"]).pack(side="left", padx=4)

        # Separator
        sep = tk.Frame(self.root, height=1, bg=C["cyan"])
        sep.grid(row=0, column=0, sticky="ew", padx=0, pady=(48, 0))

    def _build_process_panel(self):
        panel = tk.Frame(self.root, bg=C["bg_panel"], pady=8, padx=8)
        panel.grid(row=1, column=0, sticky="ew", padx=12, pady=8)
        panel.columnconfigure((0, 1, 2), weight=1)

        self._status_vars = {}
        configs = [
            ("gazebo", "① GAZEBO SIM",  C["amber"],   "sim_world.launch.py",
             "Spawn warehouse world & AMR models"),
            ("rviz",   "② RVIZ2",       C["magenta"],  "rviz2 -d multi_robot.rviz",
             "3D visualization & navigation paths"),
            ("webui",  "③ WEB BRIDGE",  C["cyan"],    "web_bridge_node.py",
             f"Dashboard at {WEB_UI_URL}"),
        ]

        for col, (key, title, color, cmd, desc) in enumerate(configs):
            card = tk.Frame(panel, bg=C["bg"], bd=1, relief="flat",
                            highlightthickness=1, highlightbackground=color)
            card.grid(row=0, column=col, padx=6, pady=4, sticky="nsew")

            # Title
            tk.Label(card, text=title, font=("Courier", 11, "bold"),
                     fg=color, bg=C["bg"], pady=6).pack(fill="x")

            # Description
            tk.Label(card, text=desc, font=("Courier", 8),
                     fg=C["muted"], bg=C["bg"], wraplength=200).pack(fill="x", padx=6)

            # Command chip
            tk.Label(card, text=f"CMD: {cmd}", font=("Courier", 7),
                     fg=C["muted"], bg=C["bg"], pady=2).pack(fill="x", padx=6)

            # Status indicator
            sv = tk.StringVar(value="● STOPPED")
            self._status_vars[key] = sv
            stat = tk.Label(card, textvariable=sv, font=("Courier", 9, "bold"),
                            fg=C["red"], bg=C["bg"], pady=4)
            stat.pack(fill="x")
            # Store ref so we can update color
            setattr(self, f"_stat_lbl_{key}", stat)

            # Buttons
            btn_row = tk.Frame(card, bg=C["bg"])
            btn_row.pack(fill="x", padx=6, pady=(4, 8))

            self._btn(btn_row, "START",
                      lambda k=key: self._start(k), C["green"], width=6).pack(side="left", padx=2)
            self._btn(btn_row, "STOP",
                      lambda k=key: self._stop(k), C["red"], width=6).pack(side="left", padx=2)
            self._btn(btn_row, "RESTART",
                      lambda k=key: self._restart(k), C["amber"], width=8).pack(side="left", padx=2)

    def _build_log_panel(self):
        log_frame = tk.Frame(self.root, bg=C["bg"])
        log_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 4))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=1)

        hdr = tk.Frame(log_frame, bg=C["bg"])
        hdr.grid(row=0, column=0, sticky="ew")
        tk.Label(hdr, text="◈ CONSOLE LOG", font=FONT_RETRO,
                 fg=C["green"], bg=C["bg"]).pack(side="left")
        self._btn(hdr, "CLR", self._clear_log, C["muted"], width=4).pack(side="right")

        self.log_box = scrolledtext.ScrolledText(
            log_frame, bg="#000005", fg=C["green"], insertbackground=C["green"],
            font=FONT_LOG, state="disabled", wrap="word",
            highlightthickness=1, highlightbackground=C["cyan"],
            bd=0, relief="flat"
        )
        self.log_box.grid(row=1, column=0, sticky="nsew")

        # Tag colors
        self.log_box.tag_config("cyan",    foreground=C["cyan"])
        self.log_box.tag_config("magenta", foreground=C["magenta"])
        self.log_box.tag_config("green",   foreground=C["green"])
        self.log_box.tag_config("amber",   foreground=C["amber"])
        self.log_box.tag_config("red",     foreground=C["red"])
        self.log_box.tag_config("muted",   foreground=C["muted"])
        self.log_box.tag_config("white",   foreground=C["white"])

    def _build_footer(self):
        ft = tk.Frame(self.root, bg=C["bg"], pady=4)
        ft.grid(row=3, column=0, sticky="ew", padx=12)

        tk.Label(ft, text="SIH26123 · BEL FleetLink · ROS 2 Harmonic",
                 font=("Courier", 7), fg=C["muted"], bg=C["bg"]).pack(side="left")

        self._clock_var = tk.StringVar()
        tk.Label(ft, textvariable=self._clock_var,
                 font=("Courier", 7), fg=C["muted"], bg=C["bg"]).pack(side="right")
        self._tick_clock()

    # ── Helpers ──────────────────────────────────────────

    def _btn(self, parent, text, command, color, width=None):
        kw = dict(text=text, command=command, font=FONT_RETRO,
                  fg=color, bg=C["bg_button"], activeforeground=C["white"],
                  activebackground=C["bg"], bd=1, relief="solid",
                  cursor="hand2", pady=3, padx=6,
                  highlightthickness=1, highlightbackground=color)
        if width:
            kw["width"] = width
        return tk.Button(parent, **kw)

    def _log(self, msg: str, color: str = "green"):
        def _do():
            self.log_box.configure(state="normal")
            ts = time.strftime("%H:%M:%S")
            self.log_box.insert("end", f"[{ts}] {msg}\n", color)
            self.log_box.configure(state="disabled")
            self.log_box.see("end")
        self.root.after(0, _do)

    def _clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def _tick_clock(self):
        self._clock_var.set(time.strftime("  %Y-%m-%d  %H:%M:%S"))
        self.root.after(1000, self._tick_clock)

    def _set_status(self, key: str, running: bool):
        sv   = self._status_vars[key]
        lbl  = getattr(self, f"_stat_lbl_{key}", None)
        if running:
            sv.set("● RUNNING")
            if lbl: lbl.configure(fg=C["green"])
        else:
            sv.set("● STOPPED")
            if lbl: lbl.configure(fg=C["red"])

    def _poll_status(self):
        for key, proc in self.procs.items() if hasattr(self, "procs") else []:
            self._set_status(key, proc.running)
        self.root.after(1000, self._poll_status)

    # ── Process actions ──────────────────────────────────

    def _start(self, key: str):
        proc = self.procs[key]
        if proc.running:
            self._log(f"[{key.upper()}] Already running.", "amber")
            return
        ok = proc.start()
        if ok:
            self._log(f"[{key.upper()}] Launched ✓", "green")
        self._set_status(key, proc.running)

    def _stop(self, key: str):
        proc = self.procs[key]
        proc.stop()
        self._set_status(key, False)

    def _restart(self, key: str):
        self._stop(key)
        time.sleep(0.5)
        self._start(key)

    def _launch_all(self):
        self._log("━━━ LAUNCHING ALL SYSTEMS ━━━", "cyan")
        for key in ["gazebo", "rviz", "webui"]:
            threading.Thread(target=self._start, args=(key,), daemon=True).start()
            time.sleep(1.5)  # stagger start

    def _stop_all(self):
        self._log("━━━ STOPPING ALL SYSTEMS ━━━", "red")
        for key in ["webui", "rviz", "gazebo"]:
            self.procs[key].stop()
            self._set_status(key, False)

    def _open_browser(self):
        self._log(f"Opening Web UI: {WEB_UI_URL}", "cyan")
        webbrowser.open(WEB_UI_URL)

    def on_close(self):
        if messagebox.askyesno("Quit", "Stop all processes and exit?"):
            self._stop_all()
            self.root.destroy()


# ──────────────────────────────────────────────────────────
# Entry
# ──────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    app  = FleetLauncherApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)

    # Center window
    root.update_idletasks()
    w, h = 900, 680
    x = (root.winfo_screenwidth()  - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
