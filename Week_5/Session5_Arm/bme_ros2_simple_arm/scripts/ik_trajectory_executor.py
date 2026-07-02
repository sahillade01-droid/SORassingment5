#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class IKTrajectoryExecutor(Node):
    def __init__(self):
        super().__init__('ik_trajectory_executor')
        self.publisher_ = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        
        self.timer = self.create_timer(3.0, self.execute_trajectory)
        self.executed = False

    def execute_trajectory(self):
        if self.executed:
            return
            
        self.get_logger().info("Publishing Calculated IK Joint Angles...")

        msg = JointTrajectory()
        msg.joint_names = [
            'shoulder_pan_joint', 
            'shoulder_lift_joint', 
            'elbow_joint', 
            'wrist_joint'
        ]

        q1 = 0.785
        q2 = -0.728
        q3 = -2.421
        q4 = 3.149

        point = JointTrajectoryPoint()
        point.positions = [q1, q2, q3, q4]
        point.time_from_start = Duration(sec=4, nanosec=0)
        
        msg.points.append(point)
        self.publisher_.publish(msg)
        
        self.get_logger().info(f"Target reached: [Pan:{q1:.2f}, Lift:{q2:.2f}, Elbow:{q3:.2f}, Wrist:{q4:.2f}]")
        self.executed = True

def main(args=None):
    rclpy.init(args=args)
    node = IKTrajectoryExecutor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()