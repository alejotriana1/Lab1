
# Lab 1/ ROS Introduction

In this first repository you will find everything related to the first robotics laboratory focused on the handling of ROS through different terminals.


## Authors

- Diego Alejandro Chacon Rangel [@Wassau](https://github.com/Wassau)
- Sergio Alejandro Triana Labrador [@alejotriana1 ](https://github.com/alejotriana1)


## Matlab
As this first part of the lab we will use the Matlab software and connect it to ROS, for that as a first step we will use:

- With Linux operating launched 2 terminals. In the first terminal typed the next command to started the master node:
 ```bash
  roscore 
```

- In the second terminal typed 
 ```bash
  rosrun turtlesim turtlesim node.
```

- A script was created with the following code:

``` Matlab
%%
rosinit; %Conexión con nodo maestro
%%
velPub = rospublisher(’/turtle1/cmd_vel’,’geometry_msgs/Twist’); %Creación publicador
velMsg = rosmessage(velPub); %Creación de mensaje
%%
velMsg.Linear.X = 1; %Valor del mensaje
send(velPub,velMsg); %Envio
pause(1)
```
The codes were run and we obtained the following result:
[![Captura-de-pantalla-de-2022-04-07-14-56-55.png](https://i.postimg.cc/fbPCdTv6/Captura-de-pantalla-de-2022-04-07-14-56-55.png)](https://postimg.cc/7CgS84dV)

- We create a Matlab script to subscribe to the pose topic, using the following code:

``` Matlab
%%
poseSub=rossubscriber('/turtle1/pose','turtlesim/Pose');
poseSub.LatestMessage
```
where we use the *rossubscriber* command, to subscribe to the desired topic and the LatestMessage function that shows us the properties that the topic has.

A Matlab script was created to send all the values associated with the topic pose of *turtle1*. We used the command *rossvcclient*, this "service client" uses a persistent connection to send requests to, and receive responses from, a ROS service server, and the command *rosmessage* that creates a ROS message object which are implemented in the following code section:

``` Matlab
rosSrv = rossvcclient("/turtle1/teleport_absolute");
rosMsgPose = rosmessage(rosSrv);

rosMsgPose.X= 2;
rosMsgPose.Y= 8;
call(rosSrv, rosMsgPose)

```
we can see the result of executing the code in the following image:
[![Captura-de-pantalla-de-2022-04-07-15-26-24.png](https://i.postimg.cc/d0F6mxM9/Captura-de-pantalla-de-2022-04-07-15-26-24.png)](https://postimg.cc/w1WD9Fjt)
Finally, we use the *rosshutdown* command to terminate the connection node between ROS and matlab, which we implement in the code as follows:


``` Matlab
%% Stop MATLAB node
rosshutdown;

```

## Python

Then Python is used to run scripts, the first script is called myTeleopKey.py; in this way it is important to achieve the next objectives:

- Move forward with key W and move backwards with the key S
- Turn around the turtle simulation with the key A clockwise and key D counterclockwise.
- Send the turtle back in the initial position and orientation with the key R.
- Finally the turtle has to make a 180 flip with the key ESPACIO.

In order to program those objectives is needed to import the following libraries, 
then Some code is used from the script turtlevel.py. This code was used just to run 
the correct commands to set position and orientation with the given keys.
```python
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
```


