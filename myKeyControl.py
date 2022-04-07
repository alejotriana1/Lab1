
from pynput.keyboard import Key, Listener, KeyCode
import rospy
from geometry_msgs.msg import Twist 
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios, sys, os
import numpy as np
from std_srvs.srv import Empty


def pubVel(vel_x, ang_z, t):
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('velPub', anonymous=False)
    vel = Twist()
    vel.linear.x = vel_x
    vel.angular.z = ang_z
    endTime = rospy.Time.now() + rospy.Duration(t)
    while rospy.Time.now() < endTime:
        pub.publish(vel)



def on_press(key):
    if key == KeyCode.from_char('w'):
        pubVel(1,0,2.2)

    if key == KeyCode.from_char('s'):
        pubVel(-1,0,2.2)

    if key == KeyCode.from_char('d'):
        pubVel(0,-1/2,2.2)

    if key == KeyCode.from_char('a'):
        pubVel(0,1/2,2.1)

    if key == Key.space:
        try:
            rospy.wait_for_service('/turtle1/teleport_relative')
            rotateTurtle = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
            moveRsp = rotateTurtle(0, np.pi)

            rospy.loginfo('Turtle rotated')
        except rospy.ServiceException as e:
            rospy.logwarn("Service teleport_relative call failed")

    if key == KeyCode.from_char('r'):
        try:
            rospy.wait_for_service('/turtle1/teleport_absolute')
            resetTurtle = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
            resetRsp = resetTurtle(6,6, np.pi)

            rospy.wait_for_service('/clear')
            clearTraje = rospy.ServiceProxy('/clear', Empty)
            resetRsp = clearTraje()

            rospy.loginfo('Turtle reset')
        except rospy.ServiceException as e:
            rospy.logwarn("Service teleport_absolute call failed")

def on_release(key):
    if key == Key.esc:
        return False




if __name__ == '__main__':
    pubVel(0,0,0.1)
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except rospy.ROSInterruptException:
        pass