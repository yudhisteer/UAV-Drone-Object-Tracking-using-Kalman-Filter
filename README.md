# UAV Drone: Object Tracking using Kalman Filter

## Problem Statement
We have a scenario where we have a drone delivery packages in a a city. Compared to other system which exist on the market whereby the package is dropped from above using a parachute, this new system uses a cord attached to the package which is lowered when reached a destination. While this system is more ergonomic and humane, the drawback is that someone or an animal can intentionally or unintentionally pull the cord which is linked to the package. This is risky to both the user and the drone and it may also cause injury in certain circumstances. 

The drone is already equipped with a range of sensors such as Lidar and Stereo Camera. We will need to use these data in order to build a tracking system that will allow the drone to lower the package to the ground only when it predicts there is no risk of the cord being pulled. This tracking system shound be able to track people or animals which are too close to the drone's package landing position. 

Building a tracking algorithm using Computer Vision is old technology these days however, one thing to keep in mind is that since the deliveries will be in cities, we may have obstruction by trees, electric poles, houses etc. That is, our computer vision system should be able to track the motion of a person coming towards the drone landing position even though he latter is partially obstructed by trees for example. And that is something most tracking system, such as YoLo, fail to do as shown below:

In summary, our tracking system will be able to predict the motion of users or animals even if it is blocked by some external objects and based on these predictions we will design an algorithm which will enable the drone to safely lower the package without any crash or risk to humans. 


## Abstract


## Plan of Action

1. Basics of Kalman Filter

2. Object Tracking

3. Object Tracking with Kalman Filter

----------


## 1. Basics of Kalman Filter
