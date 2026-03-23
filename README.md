# Avant de lancer le docker ROS2 
`xhost +`
TODO: Find a way to do it in launchRos2
# Lancer le container
`./launchRos2`

Les dépendances (apt, pip) sont gérées dans le Dockerfile a l'aide de l'outil 
Rosdep
Chaque paquet Ros a sa liste de dependances dans son package.xml

# Une fois le container lancé
## Compiler le code ROS2
`colcon build --cmake-args -DBUILD_TESTING=ON`
## Sourcer l'environnement ROS2 produit
`source install/setup.sh`
## Lancer la simulation
`ros2 launch ros_gz_bringup X3_wall.launch.py`
## Envoyer un message de controle du drone via Ros2
`ros2 topic pub /X3/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0, y: 0, z: 0.1}, angular: {z: 0}}" -1`
## Lancer le service du contrôle du drone avec le clavier
`ros2 run teleop_twist_keyboard teleop_twist_keyboard`
## Lancer le streaming du flux video Simu/Vrai drone via UDP
`ros2 run image2udp image2udp`
## Lancer le streaming du flux video Simu/Vrai drone vers RTSP
`ros2 launch image2rtsp image2rtsp.launch.py`

# Une fois le container fermé
`xhost -`
Pour des raisons de securité

[Page du template du projet ROS](https://gazebosim.org/docs/harmonic/ros_gz_project_template_guide/)
Contient des informations detaillées sur les différents éléments de l'arborescence
