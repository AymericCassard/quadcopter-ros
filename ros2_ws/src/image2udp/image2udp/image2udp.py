import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image

from image2udp.udp_video_service import UdpVideoService


class Image2udp(Node):
    def __init__(self):
        super().__init__("minimal_subscriber")

        # Default is from Simu to my phone
        self.declare_parameter("topic", "/camera/camera_image")
        self.declare_parameter("target_ip", "10.54.117.130")

        self.topic = self.get_parameter("topic").get_parameter_value().string_value
        self.target_ip = (
            self.get_parameter("target_ip").get_parameter_value().string_value
        )

        self.subscription = self.create_subscription(
            Image,
            self.topic,
            self.listener_callback,
            10,
        )
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()
        self.video_service = UdpVideoService(host=self.target_ip)

    def listener_callback(self, img_msg):
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, desired_encoding="passthrough")
        self.video_service.send(cv_image)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = Image2udp()

    minimal_subscriber.get_logger().info(
        f"Streaming {minimal_subscriber.topic} to {minimal_subscriber.target_ip}:8554"
    )
    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
