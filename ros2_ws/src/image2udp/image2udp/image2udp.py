import rclpy
from rclpy.node import Node

from image2udp.udp_video_service import UdpVideoService

from cv_bridge import CvBridge
from sensor_msgs.msg import Image


class Image2udp(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        # TODO: Set topic as parameter
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera_image',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()
        self.video_service = UdpVideoService(host="127.0.0.1")

    def listener_callback(self, img_msg):
        # self.get_logger().info('I heard a message' % img_msg.data)
        # self.get_logger().info(f'Message type: {type(img_msg.data)}')
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, desired_encoding='passthrough')
        self.video_service.send(cv_image)
        # self.get_logger().info('IMAGE SENT')



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = Image2udp()

    # TODO: Parameterize
    minimal_subscriber.get_logger().info('image server started at: 127.0.0.1:8554')
    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
