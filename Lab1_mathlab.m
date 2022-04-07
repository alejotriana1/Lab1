
%%
rosinit; %Conxion con el nodo maestro
%%
velPub=rospublisher('/turtle1/cmd_vel', 'geometry_msgs/Twist'); %Creación del publicador
velMsg = rosmessage(velPub); %Creación del mensaje
%%
velMsg.Linear.X = 1; %Valor del mensaje
send(velPub,velMsg); %Envio
pause(1)

%%
poseSub=rossubscriber('/turtle1/pose','turtlesim/Pose');
poseSub.LatestMessage
%%
rosSrv = rossvcclient("/turtle1/teleport_absolute");
rosMsgPose = rosmessage(rosSrv);

rosMsgPose.X= 2;
rosMsgPose.Y= 8;
call(rosSrv, rosMsgPose)


%% Stop MATLAB node
rosshutdown;

%% 
rosSrvClear = rossvcclient("/clear");
call(rosSrvClear)
