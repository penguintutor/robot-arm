All commands are prefixed with RobotArm (eg. RobotArmConnect)

Can be accessed using sensor variables or broadcast
Using broadcast only one motor can be controlled at a time (light can be controlled at the same time though)
Also can only move one step at a time, although can send multiple commands one-after another


## Warning
The robot arm does not have any way of knowing when it has reached the stop position in each direction. Requests to move the arm beyond that will result in the gears clicking and could in extreme circumstances cause damage to the robot arm.


Messages


RobotArmLightOn
RobotArmLightOff

Status (from python to scratch)
RobotArmConnected


Errors (broadcast from python to scratch)
RobotArmNotConnected


# Grip movement - approx 10 steps
RobotArmGripOpen
RobotArmGripClose

RobotArmWristUp
RobotArmWristDown
RobotArmElbowUp
RobotArmElbowDown
RobotArmShoulderUp
RobotArmShoulderDown
RobotArmBaseCW
RobotArmBaseCCW





RobotArmInvalidCommand # If broadcast begins with "RobotArm", but then does not have a valid command

RobotArmConnect
# Exit - wil terminate the server application
RobotArmQuit
