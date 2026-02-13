# Avant de lancer le docker ROS2 
`xhost +`
# Lancer le container
`./launchRos2`
# Une fois le container lancé
## Avant toute opération
`cd ros2_ws/`
`export GZ_VERSION=harmonic`
TODO: set GZ_VERSION dans un hook colcon
## Compiler le code ROS2
`colcon build --cmake-args -DBUILD_TESTING=ON`
## Sourcer l'environnement ROS2 produit
`source install/setup.sh`
## Lancer la simulation
`ros2 launch ros_gz_example_bringup X3.launch.py`
# Une fois le container fermé
`xhost -`
Pour des raisons de securité

[Page du template du projet ROS](https://gazebosim.org/docs/harmonic/ros_gz_project_template_guide/)
Contient des informations detaillées sur les différents éléments de l'arborescence
