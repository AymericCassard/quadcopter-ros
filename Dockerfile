FROM ros:jazzy-perception-noble

# Add ubuntu user with same UID and GID as your host system
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN if ! id -u $USER_UID >/dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME && \
        useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi

# Add sudo support for the non-root user
# NOTE: added pip for DJI Tello python dependencies
RUN apt-get update && \
    apt-get install -y sudo python3-pip && \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Switch from root to user
USER $USERNAME

# Update all packages
#RUN sudo apt update && sudo apt upgrade -y && -y
RUN sudo apt update && sudo apt upgrade -y

# Gazebo harmonic prerequisites https://gazebosim.org/docs/harmonic/install_ubuntu/ 
RUN sudo apt-get install -y  curl lsb-release gnupg && sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Rosdep update and Gazebo installation + necessary ros packages
RUN sudo apt update && rosdep update --rosdistro=${ROS_DISTRO} && sudo apt-get install -y gz-harmonic ros-${ROS_DISTRO}-ros-gz '~nros-jazzy-rqt*' 

# Add our project dependencies keys
RUN echo "yaml file:///home/${USERNAME}/ros2_ws/src/tello/rosdep.yaml" | sudo tee -a /etc/ros/rosdep/sources.list.d/40-tello.list > /dev/null

# Install needed rosdeps to launch project
COPY ros2_ws/src /home/${USERNAME}/ros2_ws/src
RUN rosdep update && \
    PIP_BREAK_SYSTEM_PACKAGES=1 rosdep install --from-paths /home/${USERNAME}/ros2_ws/src --ignore-src -r -y && \
    sudo rm -rf /home/${USERNAME}/ros2_ws && \
    PIP_BREAK_SYSTEM_PACKAGES=1 sudo -H --preserve-env=PIP_BREAK_SYSTEM_PACKAGES pip3 install -U --no-deps djitellopy2 && \
    sudo ln -s /usr/lib/python3/dist-packages/numpy/core/include/numpy/ /usr/include/numpy

# Source the ROS setup file
RUN cat << 'EOF' > ~/.bashrc && mkdir ~/ros2_ws  
source /opt/ros/${ROS_DISTRO}/setup.bash 
export GZ_VERSION=harmonic
EOF
