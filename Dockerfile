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
RUN apt-get update && \
    apt-get install -y sudo && \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Switch from root to user
USER $USERNAME

# Update all packages
#RUN sudo apt update && sudo apt upgrade -y
RUN sudo apt update && sudo apt upgrade -y

# Rosdep update and Gazebo installation + necessary ros packages
RUN rosdep update --rosdistro=${ROS_DISTRO} && sudo apt-get install -y ros-${ROS_DISTRO}-ros-gz '~nros-jazzy-rqt*' 

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc && mkdir ~/ros2_ws
