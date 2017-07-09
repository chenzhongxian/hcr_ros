# HCR command:

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










# Remote Mapping
# [`robot`]
roslaunch hcr_nav freenect_throttle.launch rate:=5

# [`remote`]
roslaunch hcr_nav rtabmap.launch rgb_topic:=/camera/data_throttled_image depth_topic:=/camera/data_throttled_image_depth camera_info_topic:=/camera/data_throttled_camera_info compressed:=true rtabmap_args:="--delete_db_on_start"


# Setup RTAB-Map on Your Robot!
# [`robot`]
??? roslaunch freenect_launch freenect.launch depth_registration:=true
or
??? roslaunch hcr_nav freenect_throttle.launch rate:=5

# mapping mode
roslaunch hcr_nav demo_hcr_rtabmap.launch
roslaunch hcr_nav demo_hcr_rtabmap.launch args:="--delete_db_on_start"
# localization mode
roslaunch hcr_nav demo_hcr_rtabmap.launch localization:="true"

# [`remote`]
roslaunch hcr_nav demo_hcr_rtabmap_view.launch rviz:="true"
# or
roslaunch hcr_nav demo_hcr_rtabmap_view.launch rtabmapviz:="true"






# W: Possible missing firmware /lib/firmware/i915/kbl_dmc_ver1_01.bin for module i915



[ WARN] [1499430908.812086872]: /rtabmap/rtabmapviz: Did not receive data since 5 seconds! Make sure the input topics are published ("$ rostopic hz my_topic") and the timestamps in their header are set. If topics are coming from different computers, make sure the clocks of the computers are synchronized ("ntpdate"). If topics are not published at the same rate, you could increase "queue_size" parameter (current=30).
/rtabmap/rtabmapviz subscribed to (approx sync):
   /odom,
   /camera/rgb/image_rect_color,
   /camera/depth_registered/image_raw,
   /camera/rgb/camera_info,
   /scan
[ WARN] [1499430916.153545931]: Could not get transform from base_link to base_laser after 0.200000 seconds (for stamp=1499430915.083688)! Error="Lookup would require extrapolation into the future.  Requested time 1499430915.083687441 but the latest data is at time 1499430914.965119792, when looking up transform from frame [base_laser] to frame [base_link]. canTransform returned after 0.204896 timeout was 0.2.".
[ERROR] [1499430916.154042335]: Could not convert laser scan msg! Aborting rtabmapviz update...
[ WARN] [1499430967.310933525]: Could not get transform from base_link to kinect_rgb_optical_frame after 0.200000 seconds (for stamp=1499430965.791297)! Error="Lookup would require extrapolation into the future.  Requested time 1499430965.791297306 but the latest data is at time 1499430965.482147477, when looking up transform from frame [kinect_rgb_optical_frame] to frame [base_link]. canTransform returned after 0.201982 timeout was 0.2.".
[ERROR] [1499430967.311004621]: TF of received depth image 0 at time 1499430965.791297s is not set!
[ERROR] [1499430967.311062473]: Could not convert rgb/depth msgs! Aborting rtabmapviz update...
[ WARN] [1499430968.850804850]: Could not get transform from base_link to kinect_rgb_optical_frame after 0.200000 seconds (for stamp=1499430966.972971)! Error="Lookup would require extrapolation into the future.  Requested time 1499430966.972970722 but the latest data is at time 1499430965.482147477, when looking up transform from frame [kinect_rgb_optical_frame] to frame [base_link]. canTransform returned after 0.201817 timeout was 0.2.".
[ERROR] [1499430968.850866294]: TF of received depth image 0 at time 1499430966.972971s is not set!
[ERROR] [1499430968.850892071]: Could not convert rgb/depth msgs! Aborting rtabmapviz update...
[ WARN] [1499430986.242549543]: Could not get transform from base_link to kinect_rgb_optical_frame after 0.200000 seconds (for stamp=1499430983.718071)! Error="Lookup would require extrapolation into the future.  Requested time 1499430983.718070869 but the latest data is at time 1499430983.269946197, when looking up transform from frame [kinect_rgb_optical_frame] to frame [base_link]. canTransform returned after 0.201853 timeout was 0.2.".
[ERROR] [1499430986.242601051]: TF of received depth image 0 at time 1499430983.718071s is not set!
[ERROR] [1499430986.242656861]: Could not convert rgb/depth msgs! Aborting rtabmapviz update...
[ WARN] [1499430986.890472372]: Could not get transform from base_link to kinect_rgb_optical_frame after 0.200000 seconds (for stamp=1499430984.709357)! Error="Lookup would require extrapolation into the future.  Requested time 1499430984.709356431 but the latest data is at time 1499430983.269946197, when looking up transform from frame [kinect_rgb_optical_frame] to frame [base_link]. canTransform returned after 0.201711 timeout was 0.2.".
[ERROR] [1499430986.890523027]: TF of received depth image 0 at time 1499430984.709357s is not set!
[ERROR] [1499430986.890560058]: Could not convert rgb/depth msgs! Aborting rtabmapviz update...





