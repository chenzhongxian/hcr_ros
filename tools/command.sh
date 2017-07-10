# HCRbot command:

###########################################################
# bringup
###########################################################
roslaunch hcr_bringup hcr_robot.launch

roslaunch hcr_bringup hcr_model_view.launch

###########################################################
# teleop
###########################################################
roslaunch hcr_teleop keyboard_teleop.launch
roslaunch hcr_teleop xbox360_teleop.launch

###########################################################
# slam / mapping
###########################################################

###################### laser mapping ######################

roslaunch hcr_nav hcr_laser_slam.launch

roslaunch hcr_nav slam_view.launch

rosrun map_server map_saver -f ~/skl302_map_rplidar

#################### 3dsensor mapping #####################

roslaunch hcr_nav hcr_3dsensor_slam.launch

roslaunch hcr_nav slam_view.launch

rosrun map_server map_saver -f ~/skl338_map_kinect
rosrun map_server map_saver -f ~/skl338_map_r200

###########################################################
# navgation
###########################################################
# laser nav
roslaunch hcr_nav hcr_laser_nav.launch

roslaunch hcr_nav nav_view.launch

# 3dsenser nav
roslaunch hcr_nav hcr_3dsensor_nav.launch map_file:=/home/jarvis/skl338_map_kinect.yaml

# Or
roslaunch hcr_nav hcr_3dsensor_nav.launch map_file:=/home/jarvis/skl338_map_r200.yaml

roslaunch hcr_nav nav_view.launch

###########################################################
# r200 view
###########################################################
roslaunch realsense_camera r200_nodelet_default.launch
rqt_image_view

###########################################################
# RTAB map
###########################################################
# [`robot`]
roslaunch hcr_nav hcr_rtabmap_robot.launch
# [`remote`]
roslaunch hcr_nav hcr_rtabmap_view.launch







