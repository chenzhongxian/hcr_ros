#!/usr/bin/env python

# http://www.guyuehome.com/273
 
# import roslib; roslib.load_manifest('rbx1_nav')  
import rospy  
import actionlib  
from actionlib_msgs.msg import *  
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist  
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal  
from random import sample  
from math import pow, sqrt  
 
class NavTest():  
    def __init__(self):  
        rospy.init_node('nav_test', anonymous=True)  
 
        rospy.on_shutdown(self.shutdown)  
 
        # How long in seconds should the robot pause at each location?  
        # 在每个目标位置暂停的时间  
        self.rest_time = rospy.get_param("~rest_time", 10)  
 
        # Are we running in the fake simulator?  
        # 是否仿真？  
        self.fake_test = rospy.get_param("~fake_test", False)  
 
        # Goal state return values  
        # 到达目标的状态  
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED',   
                       'SUCCEEDED', 'ABORTED', 'REJECTED',  
                       'PREEMPTING', 'RECALLING', 'RECALLED',  
                       'LOST']  
 
        # Set up the goal locations. Poses are defined in the map frame.    
        # An easy way to find the pose coordinates is to point-and-click  
        # Nav Goals in RViz when running in the simulator.  
        # Pose coordinates are then displayed in the terminal  
        # that was used to launch RViz.  
        # 设置目标点的位置  
        # 如果想要获得某一点的坐标，在rviz中点击 2D Nav Goal 按键，然后单机地图中一点  
        # 在终端中就会看到坐标信息  
        locations = dict()  
 
        locations['hall_foyer'] = Pose(Point(0.643, 4.720, 0.000), Quaternion(0.000, 0.000, 0.223, 0.975))  
        locations['hall_kitchen'] = Pose(Point(-1.994, 4.382, 0.000), Quaternion(0.000, 0.000, -0.670, 0.743))  
        locations['hall_bedroom'] = Pose(Point(-3.719, 4.401, 0.000), Quaternion(0.000, 0.000, 0.733, 0.680))  
        locations['living_room_1'] = Pose(Point(0.720, 2.229, 0.000), Quaternion(0.000, 0.000, 0.786, 0.618))  
        locations['living_room_2'] = Pose(Point(1.471, 1.007, 0.000), Quaternion(0.000, 0.000, 0.480, 0.877))  
        locations['dining_room_1'] = Pose(Point(-0.861, -0.019, 0.000), Quaternion(0.000, 0.000, 0.892, -0.451))  
 
        # Publisher to manually control the robot (e.g. to stop it)  
        # 发布控制机器人的消息  
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)  
 
        # Subscribe to the move_base action server  
        # 订阅move_base服务器的消息  
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)  
 
        rospy.loginfo("Waiting for move_base action server...")  
 
        # Wait 60 seconds for the action server to become available  
        # 60s等待时间限制  
        self.move_base.wait_for_server(rospy.Duration(60))  
 
        rospy.loginfo("Connected to move base server")  
 
        # A variable to hold the initial pose of the robot to be set by   
        # the user in RViz  
        # 保存机器人的在rviz中的初始位置  
        initial_pose = PoseWithCovarianceStamped()  
 
        # Variables to keep track of success rate, running time,  
        # and distance traveled  
        # 保存成功率、运行时间、和距离的变量  
        n_locations = len(locations)  
        n_goals = 0  
        n_successes = 0  
        i = n_locations  
        distance_traveled = 0  
        start_time = rospy.Time.now()  
        running_time = 0  
        location = ""  
        last_location = ""  
 
        # Get the initial pose from the user  
        # 获取初始位置(仿真中可以不需要)  
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")  
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)  
        self.last_location = Pose()  
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)  
 
        # Make sure we have the initial pose  
        # 确保有初始位置  
        while initial_pose.header.stamp == "":  
            rospy.sleep(1)  
 
        rospy.loginfo("Starting navigation test")  
 
        # Begin the main loop and run through a sequence of locations  
        # 开始主循环，随机导航  
        while not rospy.is_shutdown():  
            # If we've gone through the current sequence,  
            # start with a new random sequence  
            # 如果已经走完了所有点，再重新开始排序  
            if i == n_locations:  
                i = 0  
                sequence = sample(locations, n_locations)  
                # Skip over first location if it is the same as  
                # the last location  
                # 如果最后一个点和第一个点相同，则跳过  
                if sequence[0] == last_location:  
                    i = 1  
 
            # Get the next location in the current sequence  
            # 在当前的排序中获取下一个目标点  
            location = sequence[i]  
 
            # Keep track of the distance traveled.  
            # Use updated initial pose if available.  
            # 跟踪形式距离  
            # 使用更新的初始位置  
            if initial_pose.header.stamp == "":  
                distance = sqrt(pow(locations[location].position.x -   
                                    locations[last_location].position.x, 2) +  
                                pow(locations[location].position.y -   
                                    locations[last_location].position.y, 2))  
            else:  
                rospy.loginfo("Updating current pose.")  
                distance = sqrt(pow(locations[location].position.x -   
                                    initial_pose.pose.pose.position.x, 2) +  
                                pow(locations[location].position.y -   
                                    initial_pose.pose.pose.position.y, 2))  
                initial_pose.header.stamp = ""  
 
            # Store the last location for distance calculations  
            # 存储上一次的位置，计算距离  
            last_location = location  
 
            # Increment the counters  
            # 计数器加1  
            i += 1  
            n_goals += 1  
 
            # Set up the next goal location  
            # 设定下一个目标点  
            self.goal = MoveBaseGoal()  
            self.goal.target_pose.pose = locations[location]  
            self.goal.target_pose.header.frame_id = 'map'  
            self.goal.target_pose.header.stamp = rospy.Time.now()  
 
            # Let the user know where the robot is going next  
            # 让用户知道下一个位置  
            rospy.loginfo("Going to: " + str(location))  
 
            # Start the robot toward the next location  
            # 向下一个位置进发  
            self.move_base.send_goal(self.goal)  
 
            # Allow 5 minutes to get there  
            # 五分钟时间限制  
            finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))   
 
            # Check for success or failure  
            # 查看是否成功到达  
            if not finished_within_time:  
                self.move_base.cancel_goal()  
                rospy.loginfo("Timed out achieving goal")  
            else:  
                state = self.move_base.get_state()  
                if state == GoalStatus.SUCCEEDED:  
                    rospy.loginfo("Goal succeeded!")  
                    n_successes += 1  
                    distance_traveled += distance  
                    rospy.loginfo("State:" + str(state))  
                else:  
                  rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))  
 
            # How long have we been running?  
            # 运行所用时间  
            running_time = rospy.Time.now() - start_time  
            running_time = running_time.secs / 60.0  
 
            # Print a summary success/failure, distance traveled and time elapsed  
            # 输出本次导航的所有信息  
            rospy.loginfo("Success so far: " + str(n_successes) + "/" +   
                          str(n_goals) + " = " +   
                          str(100 * n_successes/n_goals) + "%")  
            rospy.loginfo("Running time: " + str(trunc(running_time, 1)) +   
                          " min Distance: " + str(trunc(distance_traveled, 1)) + " m")  
            rospy.sleep(self.rest_time)  
 
    def update_initial_pose(self, initial_pose):  
        self.initial_pose = initial_pose  
 
    def shutdown(self):  
        rospy.loginfo("Stopping the robot...")  
        self.move_base.cancel_goal()  
        rospy.sleep(2)  
        self.cmd_vel_pub.publish(Twist())  
        rospy.sleep(1)  
 
def trunc(f, n):  
    # Truncates/pads a float f to n decimal places without rounding  
    slen = len('%.*f' % (n, f))  
    return float(str(f)[:slen])  
 
if __name__ == '__main__':  
    try:  
        NavTest()  
        rospy.spin()  
    except rospy.ROSInterruptException:  
        rospy.loginfo("AMCL navigation test finished.")
