from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tello',
            executable='tello',
            namespace='/',
            name='tello',
            parameters=[
                {'tello_ip': '192.168.1.22'}
                ],
            remappings=[
                ],
            respawn=True
            )
        ])
