# UAV Drone: Object Tracking using Kalman Filter

## Problem Statement
We have a scenario where we have a drone delivery packages in a a ```city```. Compared to other system which exist on the market whereby the package is dropped from above using a ```parachute```, this new system uses a ```cord``` attached to the package which is lowered when reached a destination. While this system is more **ergonomic** and **humane**, the drawback is that someone or an animal can intentionally or unintentionally ```pull the cord``` which is linked to the package. This is risky to both the user and the drone and it may also cause **injury** in certain circumstances. 

The drone is already equipped with a range of sensors such as  a```Lidar```, a ```camera```, and/or ```Stereo Camera```. We will need to use these data in order to build a ```tracking system``` that will allow the drone to lower the package to the ground only when it predicts there is **no risk** of the cord being pulled. This tracking system shound be able to track people or animals which are too close to the drone's package landing position. 

Building a tracking algorithm using Computer Vision is old technology these days however, one thing to keep in mind is that since the deliveries will be in cities, we may have **obstruction** by trees, electric poles, houses etc. That is, our computer vision system should be able to track the motion of a person coming towards the drone landing position even though he latter is partially obstructed by trees for example. And that is something most tracking system, such as ```YoLo```, fail to do as shown below:

In summary, our tracking system should be able to predict the motion of users or animals even if it is **blocked** by some external objects and based on these predictions we will design an algorithm which will enable the drone to ```safely``` lower the package without any crash or risk to humans. 


## Abstract


## Plan of Action

1. Basics of Kalman Filter

2. Object Tracking

3. Object Tracking with Kalman Filter

----------


## 1. Basics of Kalman Filter

### 1.1 The Origin
The Kalman Filter was invented by the great ```Rudolf E. Kálmán``` who received the **National Medal of Science** on Oct. 7, 2009, from President Barack Obama at the White House. Kalman filters were first used during the **Apollo space program** that put men on the moon, in the **NASA Space Shuttle**, in **U.S. Navy submarines**, and in **unmanned aerospace vehicles** and **weapons**.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227087845-8ff20652-62aa-4df9-a3bb-2439f3c0f171.jpg" width="450" height="300"/>
</p>

### 1.2 The Purpose
Let's see at examples of why we may need Kalman Filters. 

**Example 1**: We need to measure the internal temperature of a core reactor of a nuclear power plant. You may guess that we cannot put any type of sensors directly into the core as they will melt instantaneously. The best we can do is measure external tempeature outside the core and then use a Kalman Filter to find the best estimate of the internal temperature from an indirect measurement. That is, we use a Kalman Filter when ```we cannot measure directly the variables of interest```.

**Example 2**: Suppose we want to track the location of our drone at a specific time ```t```. We may use the a **GPS** to do so but the precision may differ based on the number of satellites available and other factors. We may use the onboard **IMU** sensor to deduce the distance travelled but our sensor can be ```noisy```. So what we can so is to ```fuse``` both sensors measurements to find the optimal estimate of the exact location of our drone. That is, we use Kalman Filter when we want to find ```the best estimate of states by combining measurements from various sensors in the presence of noise```.

### 1.3 The States
Kalman Filter (KF) are ideal for systems which are ```continuously changing```. Why? Because KF keep only the ```previous state``` hence, they are fast and well-suited for ```real-time problems```. 

So what is this ```"state"``` term? The state is the **underlying configuration** of our system. It can be the ```position```, ```velocity```, ```volume```, ```temperature``` and so on of our system. We will take example of our drone which has two states: **position** and **velocity**. And it will be represented in a ```state vector```. 

Now that we know what are states, let's define the steps of a KF. In a nutshell, KF can be expressed in a two-step process: **prediction** and **correction** which provides an ```optimal state estimate```.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227108866-4f18f449-f8af-4810-b50e-c3602dadd754.png" width="450" height="250"/>
</p>

Suppose we want to track the position of our drone at time ```t```. Our GPS and other sensors have **noise** hence, will not provide an accurate result. But what if we can provide a ```mathematical model``` of our system. With Newton's Equation of Motion we can predict at time ```t+1``` what will be the position of our drone using its velocity. However, this will be a flawed model as we are not taking into account **external factors** such as wind resistance, snow, rain and so on. Hence, this is a ```flawed model```. In summary we have a sensor with **uncertainty** and a mathematical model with its own **uncertainty**. What if we could **combine both**? And that is exactly what the Kalman Filter does:

- The Kalman Filter will combine ```measurements``` from a **noisy sensor** and the ```prediction``` of a **flawed model** to get a more ```accurate estimate``` of the system state than either one **independently**.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227113149-0d790863-03fb-4999-bba0-47fa75e27359.png" width="750" height="350"/>
</p>



### 1.4 Prediction Model


### 1.6 External Influence


### 1.7 External Uncertainty


### 1.8 Measurement Estimate


### 1.9 Final Equation


<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227095956-3c4415f1-d365-4899-ba95-85255d433a47.gif"/>
</p>







--------------

## 2. Object Tracking






## References

1. https://engineeringmedia.com/controlblog/the-kalman-filter
2. https://www.youtube.com/watch?v=mwn8xhgNpFY&list=PLn8PRpmsu08pzi6EMiYnR-076Mh-q3tWr&ab_channel=MATLAB
3. https://www.mathworks.com/videos/series/understanding-kalman-filters.html
4. https://arshren.medium.com/an-easy-explanation-of-kalman-filter-ec2ccb759c46
5. https://www.youtube.com/watch?v=CaCcOwJPytQ&list=PLX2gX-ftPVXU3oUFNATxGXY90AULiqnWT&ab_channel=MichelvanBiezen
6. https://www.kalmanfilter.net/default.aspx
7. https://www.alanzucconi.com/2022/07/24/kalman-filter-3/
8. 
















