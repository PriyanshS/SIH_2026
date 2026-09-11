"""Path Sharer — publishes own Nav2 plan, subscribes to peers' plans."""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, LivelinessPolicy
from nav_msgs.msg import Path, Odometry
from amr_msgs.msg import RobotPlan
from builtin_interfaces.msg import Time


class PathSharer(Node):
    def __init__(self):
        super().__init__('path_sharer')

        self.declare_parameter('robot_id', 'robot1')
        self.declare_parameter('peer_ids', ['robot1', 'robot2', 'robot3'])

        self.robot_id = self.get_parameter('robot_id').value
        self.peer_ids = self.get_parameter('peer_ids').value

        self.plan_seq = 0
        self.current_velocity = 0.3  # default estimate m/s
        self.peer_plans = {}  # {robot_id: RobotPlan}

        # QoS for shared plans: reliable, transient-local so late joiners get last plan
        shared_plan_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            depth=3,
        )

        # Subscribe to own Nav2 plan
        self.plan_sub = self.create_subscription(
            Path,
            f'/{self.robot_id}/plan',
            self._plan_cb,
            10,
        )

        # Subscribe to own odom for velocity estimate
        self.odom_sub = self.create_subscription(
            Odometry,
            f'/{self.robot_id}/odom',
            self._odom_cb,
            10,
        )

        # Publisher for shared plans
        self.shared_plan_pub = self.create_publisher(
            RobotPlan,
            '/shared_plans',
            shared_plan_qos,
        )

        # Subscribe to shared plans from all robots
        self.shared_plan_sub = self.create_subscription(
            RobotPlan,
            '/shared_plans',
            self._shared_plan_cb,
            shared_plan_qos,
        )

        self.get_logger().info(f'[{self.robot_id}] Path sharer started')

    def _plan_cb(self, msg: Path):
        """Received a new plan from own Nav2 planner."""
        self.plan_seq += 1

        robot_plan = RobotPlan()
        robot_plan.robot_id = self.robot_id
        robot_plan.plan_seq = self.plan_seq
        robot_plan.path = msg
        robot_plan.estimated_velocity = self.current_velocity
        robot_plan.stamp = self.get_clock().now().to_msg()

        self.shared_plan_pub.publish(robot_plan)
        self.get_logger().debug(
            f'[{self.robot_id}] Published plan seq={self.plan_seq} '
            f'with {len(msg.poses)} poses'
        )

    def _odom_cb(self, msg: Odometry):
        """Update velocity estimate from odometry."""
        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y
        speed = (vx**2 + vy**2) ** 0.5
        # Smooth the estimate
        self.current_velocity = 0.7 * self.current_velocity + 0.3 * max(speed, 0.05)

    def _shared_plan_cb(self, msg: RobotPlan):
        """Received a shared plan from another robot (or self — filter)."""
        if msg.robot_id == self.robot_id:
            return  # ignore own echoed messages

        # Store/update peer's plan
        existing = self.peer_plans.get(msg.robot_id)
        if existing is None or msg.plan_seq > existing.plan_seq:
            self.peer_plans[msg.robot_id] = msg
            self.get_logger().debug(
                f'[{self.robot_id}] Received plan from {msg.robot_id} '
                f'seq={msg.plan_seq} with {len(msg.path.poses)} poses'
            )


def main(args=None):
    rclpy.init(args=args)
    node = PathSharer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
