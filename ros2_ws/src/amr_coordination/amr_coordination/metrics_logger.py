"""Metrics Logger — collects timing data from all robots, writes results.

Upgraded (addendum Section 4) to track:
  - Goals completed per minute (rolling 60-second window)
  - Dispatcher queue stats (goals queued, avg wait time)
  - Throughput comparison: coordinated vs baseline mode
"""

import json
import os
import csv
import time
from collections import deque
from datetime import datetime

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import String, Int32


class MetricsLogger(Node):
    def __init__(self):
        super().__init__('metrics_logger')

        self.declare_parameter('output_dir', '')
        self.declare_parameter('expected_robots', 3)

        self.output_dir = self.get_parameter('output_dir').value
        self.expected_robots = self.get_parameter('expected_robots').value

        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

        self.events = []
        self.done_robots = {}  # {robot_id: {mode, total_time}}

        # Throughput tracking — rolling 60-second completion window
        self._completion_times: deque = deque()  # wall-clock timestamps of each goal completion
        self._session_start: float = time.monotonic()
        self._total_goals_completed: int = 0

        # Dispatcher queue tracking
        self._max_queue_depth: int = 0
        self._goals_queued: int = 0

        metrics_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=50,
        )

        self.sub = self.create_subscription(
            String, '/metrics', self._metrics_cb, metrics_qos
        )

        # Track dispatcher queue depth
        self.create_subscription(
            Int32, '/dispatcher/queue_size', self._queue_size_cb, 10
        )
        self.create_subscription(
            String, '/dispatcher/log', self._dispatcher_log_cb, 10
        )

        # Periodic throughput report every 30 s
        self.create_timer(30.0, self._report_throughput)

        self.get_logger().info('Metrics logger started — waiting for events')

    def _metrics_cb(self, msg: String):
        try:
            data = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warn(f'Invalid JSON: {msg.data}')
            return

        self.events.append(data)

        robot_id = data.get('robot_id', '?')
        event = data.get('event', '')

        if event == 'ALL_DONE':
            total_time = data.get('total_time', 0)
            mode = data.get('mode', '?')
            self.done_robots[robot_id] = {
                'mode': mode,
                'total_time': total_time,
            }
            self.get_logger().info(
                f'[{robot_id}] ALL_DONE in {total_time:.1f}s ({mode})'
            )

            if len(self.done_robots) >= self.expected_robots:
                self._print_results()
                self._write_csv()
        elif event == 'CONFLICT_YIELD':
            self.get_logger().info(
                f'[{robot_id}] Yielded to {data.get("peer", "?")} at '
                f'{data.get("position", [])}'
            )
        elif event == 'OBSTACLE_RECEIVED':
            self.get_logger().info(
                f'[{robot_id}] Received obstacle from {data.get("from", "?")}'
            )
        elif 'waypoint_idx' in data:
            # Individual goal completion — record for throughput
            now = time.monotonic()
            self._completion_times.append(now)
            self._total_goals_completed += 1
            # Prune old entries outside 60-second window
            cutoff = now - 60.0
            while self._completion_times and self._completion_times[0] < cutoff:
                self._completion_times.popleft()

            self.get_logger().info(
                f'[{robot_id}] Waypoint {data["waypoint_idx"]} done in '
                f'{data.get("duration", 0):.1f}s '
                f'[throughput: {self._current_throughput():.2f} goals/min]'
            )

    def _queue_size_cb(self, msg: Int32):
        """Track maximum queue depth seen during the session."""
        if msg.data > self._max_queue_depth:
            self._max_queue_depth = msg.data

    def _dispatcher_log_cb(self, msg: String):
        """Count goals that had to be queued."""
        if 'queuing goal' in msg.data:
            self._goals_queued += 1

    def _current_throughput(self) -> float:
        """Goals per minute in the rolling 60-second window."""
        now = time.monotonic()
        cutoff = now - 60.0
        while self._completion_times and self._completion_times[0] < cutoff:
            self._completion_times.popleft()
        window_secs = min(60.0, now - self._session_start)
        if window_secs < 1.0:
            return 0.0
        return len(self._completion_times) / window_secs * 60.0

    def _report_throughput(self):
        """Periodic throughput summary."""
        tput = self._current_throughput()
        elapsed = time.monotonic() - self._session_start
        self.get_logger().info(
            f'[metrics] Throughput: {tput:.2f} goals/min '
            f'(total={self._total_goals_completed}, elapsed={elapsed:.0f}s)'
        )

    def _print_results(self):
        mode = list(self.done_robots.values())[0]['mode']
        elapsed = time.monotonic() - self._session_start
        overall_throughput = (
            self._total_goals_completed / elapsed * 60.0
            if elapsed > 0 else 0.0
        )

        self.get_logger().info('')
        self.get_logger().info(f'{"="*50}')
        self.get_logger().info(f'  RESULTS ({mode})')
        self.get_logger().info(f'{"="*50}')

        max_time = 0
        for rid in sorted(self.done_robots.keys()):
            t = self.done_robots[rid]['total_time']
            max_time = max(max_time, t)
            self.get_logger().info(f'  {rid}: {t:.1f}s')

        self.get_logger().info(f'  Total (slowest robot): {max_time:.1f}s')
        self.get_logger().info(
            f'  Throughput: {overall_throughput:.2f} goals/min '
            f'(total {self._total_goals_completed} goals in {elapsed:.0f}s)'
        )
        if self._goals_queued > 0:
            self.get_logger().info(
                f'  Dispatcher: {self._goals_queued} goals queued '
                f'(max queue depth={self._max_queue_depth})'
            )
        self.get_logger().info(f'{"="*50}')
        self.get_logger().info('')

    def _write_csv(self):
        if not self.output_dir:
            return

        mode = list(self.done_robots.values())[0]['mode']
        csv_file = os.path.join(self.output_dir, f'metrics_{mode}.csv')
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['robot_id', 'event', 'data'])
            for event in self.events:
                writer.writerow([
                    event.get('robot_id', ''),
                    event.get('event', event.get('waypoint_idx', '')),
                    json.dumps(event),
                ])

        self.get_logger().info(f'Metrics written to {csv_file}')

        # Also write summary
        summary_file = os.path.join(self.output_dir, f'summary_{mode}.txt')
        with open(summary_file, 'w') as f:
            f.write(f'=== RESULTS ({mode}) ===\n')
            max_time = 0
            for rid in sorted(self.done_robots.keys()):
                t = self.done_robots[rid]['total_time']
                max_time = max(max_time, t)
                f.write(f'{rid}: {t:.1f}s\n')
            f.write(f'Total (slowest): {max_time:.1f}s\n')

        self.get_logger().info(f'Summary written to {summary_file}')


def main(args=None):
    rclpy.init(args=args)
    node = MetricsLogger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
