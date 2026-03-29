from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="image2udp",
                executable="image2udp",
                name="real_parameters_launch",
                output="screen",
                emulate_tty=True,
                parameters=[
                    {"topic": "/image_raw"},
                    {"target_ip": "10.54.117.130"},
                ],
            )
        ]
    )
