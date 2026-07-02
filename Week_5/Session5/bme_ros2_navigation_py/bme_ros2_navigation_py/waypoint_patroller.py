import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped

class WaypointPatroller(Node):
    def __init__(self):
        super().__init__('waypoint_patroller')
        
        self.action_client = ActionClient(self, FollowWaypoints, 'follow_waypoints')
        self.get_logger().info("Waiting for 'follow_waypoints' action server...")
        self.action_client.wait_for_server()
        self.get_logger().info("Action server found! Sending waypoints...")

    def send_waypoints(self):
        goal_msg = FollowWaypoints.Goal()
        
        waypoints_data = [
            [2.0, 0.0, 1.0],
            [2.0, 2.0, 0.707],
            [0.0, 2.0, 0.0]
        ]

        for idx, wp in enumerate(waypoints_data):
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.pose.position.x = wp[0]
            pose.pose.position.y = wp[1]
            pose.pose.orientation.w = wp[2]
            goal_msg.poses.append(pose)
            self.get_logger().info(f"Loaded Waypoint {idx+1}: x={wp[0]}, y={wp[1]}")

        self.send_goal_future = self.action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        current_wp = feedback_msg.feedback.current_waypoint
        self.get_logger().info(f"Navigating to Waypoint {current_wp + 1}...")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return
        self.get_logger().info('Goal accepted! Patrol started.')
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Patrol Complete! All waypoints reached successfully.')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = WaypointPatroller()
    node.send_waypoints()
    rclpy.spin(node)

if __name__ == '__main__':
    main()