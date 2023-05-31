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

```To put it simply, our aim is to determine the current state of the system by considering both its underlying dynamics and the presence of imperfect measurements.```

### 1.3 Types of Kalman Filter

 #### Linear Kalman Filter
 
 
 #### Extenden Kalman Filter
 
 
 
 #### Unscented Kalman Filter








### 1.3 The States
Kalman Filter (KF) are ideal for systems which are ```continuously changing```. Why? Because KF keep only the ```previous state``` hence, they are fast and well-suited for ```real-time problems```. 

So what is this ```"state"``` term? The state is the **underlying configuration** of our system. It can be the ```position```, ```velocity```, ```volume```, ```temperature``` and so on of our system. We will take example of our drone which has two states: **position** and **velocity**. And it will be represented in a ```state vector```. 

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227746812-5be18f7e-769a-4a39-b55a-2fa9c413bc73.png"/>
</p>

Now that we know what are states, let's define the steps of a KF. In a nutshell, KF can be expressed in a two-step process: **prediction** and **update** which provides an ```optimal state estimate```.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/1c7657df-7f67-46e3-9f1e-5d9352449fcb" width="750" height="250"/>
</p>

Suppose we want to track the position of our drone at time ```t```. Our GPS and other sensors have **noise** hence, will not provide an accurate result. But what if we can provide a ```mathematical model``` of our system. With Newton's Equation of Motion we can predict at time ```t+1``` what will be the position of our drone using its velocity. However, this will be a flawed model as we are not taking into account **external factors** such as wind resistance, snow, rain and so on. Hence, this is a ```flawed model```. In summary we have a sensor with **uncertainty** and a mathematical model with its own **uncertainty**. What if we could **combine both**? And that is exactly what the Kalman Filter does.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227795840-0f3e94db-1ad8-4a7b-8364-c68bc89abf0e.png" width="460" height="150"/>
</p>


- The Kalman Filter will combine ```measurements``` from a **noisy sensor** and the ```prediction``` of a **flawed model** to get a more ```accurate estimate``` of the system state than either one **independently**.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/a5a161fe-b74b-43ea-acc3-7cbe5752f3da" width="750" height="390"/>
</p>

- The Kalman Filter computes the ideal **weightage** for the ```measured``` and ```predicted``` states, so that the resulting ```corrected state``` is positioned precisely at the **optimal** location between them.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227746239-7e4262ad-888f-48b6-9125-4ee5175449a6.png" width="800" height="340"/>
</p>

Note that we do not know what is the **actual** positon and velocity due to the uncertainties. But we do know that there is a whole range of possible combinaties that may be true.
 
 One important **assumption** of KF is that it expect our variables to be ```random``` and ```Gaussian``` distributed. Hence, if we denote our variables using a state vector ```x```. Each variable has a **mean** and a **variance** such that:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227746364-6a3ae6c7-2dee-450f-8fd8-7a46737f29ba.png"/>
</p>

Note that the variables may be **correlated**. For example, here, position and velocity are correlated as a higher velocity expects to give a higher position. Hence, this correlation is captured in a **covariance matrix**:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227746761-aaab051f-fdfc-4d8b-9f97-545dbe6529f0.png"/>
</p>

A positive covariance indicates that the variables tend to increase or decrease together, while a negative covariance indicates that as one variable increases, the other tends to decrease.

- The Kalman filter works by propagating the mean and covariance of the Gaussian distributions for the estimated state through time using a **linear process model**. This is known as the prediction step or process update, where the estimates move forward in time.

- When measurements are available, which are a linear combination of the state, the Kalman filter updates the estimated state's mean and covariance based on the the measurements' mean and covariance of the Gaussian distribution. This is the update step or corrections step for the Kalman filter.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/be184cda-d18e-4a59-9a2a-dc5f38022697" width="800" height="540"/>
</p>

- These two processes form the prediction and correction step, which is recursively run in the filter with time. The estimates are propagated forward in time to the current time.
If the measurements information are available at the current time, it is used to improve the current state estimates. This is then repeated as time moves forward, 






---------------------------------------

### 1.4 Process Model: Prediction

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227795937-6a3f48d5-ff84-4220-a872-cba57fad5ff4.png" width="460" height="140"/>
</p>

We will denote our current state as ```k-1``` and the next state we will predict as ```k```. 
Our best estimate at the current time step ```k-1``` will be:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227747266-59082f7d-d8a2-4f49-9c68-86cfe47cd4b7.png"/>
</p>

And the next best estimate at time step ```k``` will be:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227747207-9b564ab0-63ed-4f52-88dc-30b717f3cdbe.png"/>
</p>

In we expand our state vector to represent a 2D model:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/b0b1b999-9bb3-4cbb-8ad0-c446de7b57a8"/>
</p>


Again, we do not know which state is the actual one, even the initial state has uncertainty, hence, our prediction model will output a new distribution after working on all the possible values.

Let's try to predict the position and velocity at the next time step.
Assuming a **constant velocity** (zero acceleration) scenario, therefore:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227747109-04108abd-1013-43b7-9ff1-b5403b91abcd.png"/>
</p>

We predict the position as such:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227747129-368580dd-6157-4778-a16b-d3f29e17aadd.png"/>
</p>

The two last equations can be written in matric form as such:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227747447-bb159a4d-2056-4d67-a5f0-8b82748ba1b4.png"/>
</p>

In 2D:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/9918f6e3-e3e8-4043-8fe9-2343a280b86f"/>
</p>



Re-writting again with ![CodeCogsEqn (13)](https://user-images.githubusercontent.com/59663734/227747531-e7627dec-8a96-4afb-b979-f4534a56b60c.png) being the **State Transition Matrix**.:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227752027-0ef3a998-3b4e-4c60-985d-ca3956437482.png"/>
</p>

The State Transition Matrix propagates the state at sample ```k-1```to the state sample ```k```. 

Now we need to propagate the error covariance forward. Note that uncertainty comes from ```2``` sources when predicting:

    1. Initial uncertainty in system before prediction
    2. Additional uncertainty as we propagate the state forward in time

We will define the ```initial uncertainty``` first with ![CodeCogsEqn (16)](https://user-images.githubusercontent.com/59663734/227752062-7d98795d-a74d-4e2e-bf6b-900d0cd43d4d.png)
 known as the **Prediction Error Covariance Matrix**:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227751910-a6be1fd4-a1b4-41b0-be37-5b754f6d48f6.png"/>
</p>

Note that we use the State Transition Matrix F to propagate the initial error covariance.

### 1.6 Process Model: External Influence
In the first part of our prediction model, we assumed a **constant velocity**. But that is not always the case in real-world. External forces may cause a system to accelerate. There may be changes that are not related to the state itself. Thus, we assume a **linear acceleration**.

We use Newton's Equation of Motion to update our model:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227752300-584aa592-68e1-42b4-9c9e-9aece1a9a3b5.png"/>
</p>

Re-writting it in matrix form:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227752403-ac80ac8c-1047-4606-821a-869eb718289f.png"/>
</p>

In 2D:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/4146e349-28d6-45f5-b7a6-9b9e5811bf5c"/>
</p>

![CodeCogsEqn (19)](https://user-images.githubusercontent.com/59663734/227752417-2ce97302-ebe7-4394-a3b8-1ceea6bde07f.png) is the **control matrix** and ![CodeCogsEqn (20)](https://user-images.githubusercontent.com/59663734/227752424-7e4f1d27-6aeb-4f89-aabb-6c81dd5997e5.png) is called the **control vector**. By factoring in the system's dynamics and the effects of external controls on its future state, we can derive an estimated state projection









### 1.7 Process Model: External Uncertainty
It is impossible to model every external forces (friction, air resistance,...) acting on our system. In order to counter for that, we add some new uncertainty after every prediction step. We will model the **second** source of uncertainty into our system: ```uncertainty as we propagate the state forward in time```.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227753050-b7eb3810-2031-4e86-9489-e7cfd6e118b9.png" width="400" height="300"/>
</p>


- Each blue point in the diagram above can be our current state though it is most likely the actual state will be at the **center** of the Gaussian blob.
- When predicting the next time step, a new **Gaussian** blob is created whereby each new green points can be the actual predicted state.
- Each predicted point (green) has its own Gaussian blob, i.e, when we deal with **unobserved factors** that can impact the system's performance, we treat them as random disturbances or ```noise``` with a particular **covariance matrix**.

The new **Prediction Error Covariance Matrix** ![CodeCogsEqn (16)](https://user-images.githubusercontent.com/59663734/227752062-7d98795d-a74d-4e2e-bf6b-900d0cd43d4d.png) is: 

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227753925-5e2deb93-b4d2-477e-89da-6e194fe633e8.png"/>
</p>


Note that we build up the new uncertainty from the old one by adding some uncertainty from the ```environment```. This new uncertainty is **proportional** to the ```time horizon```. That is, the further we predict, the **bigger** this new uncertainty will be. So, the **Prediction Covariance Matrix** ```grows``` over time.

This additional uncertainty is modelled by the **Process Noise Covariance Matrix**, ![CodeCogsEqn (24)](https://user-images.githubusercontent.com/59663734/227754179-426ee4b2-400e-40c8-ad7f-53803289f3b0.png). This matrix captures all uncertainty which we **cannot** model coming from ```unknown inputs``` or from the **discrepancy** in our ```predicting model```.

To sum up:

1. The new best estiate is a prediction model from the previous best estimate  ```+``` a correction for known external influences.
2. The new uncertainty is predicted from the old uncertainty ```+``` additional uncertainty from the environment.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227754762-ebf90ab8-24a4-4b3c-ae62-68a56cdfb1f3.png"/>
</p>

---------------------------------------


### 1.8 Measurement: Noise & Estimate
Recall that the Kalman Filter will combine measurements from a **noisy sensor** and the **prediction of a flawed model** to get a more accurate estimate of the system state than either one independently. What we have done since now is building a mathematical model in order to predict the next state of our system. What we will do now, is take readings from our sensor in order to get a ```measurement estimate```.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227795993-e89ba02b-17eb-4c05-95d2-46638e337fbe.png" width="460" height="140"/>
</p>

When we buy a sensor, the manufacturer tells us about the ```precision``` of the module. Precision is how close all the sensor readings are grouped to each other. When we need to measure distance using a laser for example, we cannot expect to get the same reading everytime we take a measurement with our sensor. There will be some small variations and this is due to ```random noise``` in the sensor. 

One important factor is that the scale of readings from our sensor may not be of the same scale as the states we are measuring.  Hence, we’ll model the sensors with a matrix, ![CodeCogsEqn (26)](https://user-images.githubusercontent.com/59663734/227796992-96f8438a-2f93-42c1-824c-3c14ecd6bf8c.png). We can use this matrix to formulate a distribution of what our ```predicted measurement``` would be using the **next best estimate** + its **uncertainty** of our **prediction model**:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227797793-e6e3b0a8-d86d-43c4-89cc-7716e0cb3c1b.png"/>
</p>

Note that ```P``` is rotated into the sensor frame using ```H```. As we analyze a reading, we can make an educated guess about the state of our system. However, due to the presence of uncertainty, some states have a greater probability of producing the observed reading than others.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227798246-3e2e5cd5-d754-468f-9359-a81a1f581066.png" width="400" height="300"/>
</p>

- We denote the **Measurement Covariance Matrix** as ![CodeCogsEqn (28)](https://user-images.githubusercontent.com/59663734/227798527-16f6d3af-ccc8-4cb9-9c9f-1afa2ce7f1b6.png), which reflects the inherent variability and uncertainty in our sensor measurements.
- This new distribution from our sensor readings has a **mean** represented with a vector: ![CodeCogsEqn (29)](https://user-images.githubusercontent.com/59663734/227798797-df07ef11-f407-4cc2-8a77-f08b98ed8980.png)

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227801851-53e36354-d682-4dae-a37d-e026bf815f6a.png" width="750" height="230"/>
</p>

From the diagram above, notice that how as we propagate further into the future our **Process Noise Covariance Matrix**, ![CodeCogsEqn (24)](https://user-images.githubusercontent.com/59663734/227754179-426ee4b2-400e-40c8-ad7f-53803289f3b0.png), grows bigger and bigger. In total, we have ```3``` error covariance matrices: ![CodeCogsEqn (33)](https://user-images.githubusercontent.com/59663734/227801696-c2b50054-c440-4c04-9300-b0da0e787fef.png), ![CodeCogsEqn (32)](https://user-images.githubusercontent.com/59663734/227801712-9bee671b-ecf0-40aa-b297-c719afb2febc.png), 
![CodeCogsEqn (31)](https://user-images.githubusercontent.com/59663734/227801722-7d6cb918-9657-40c9-8a44-ea358e062373.png).


To sum up, we now have ```2``` Gaussian blobs:

1. One surrounding the mean of our ```transformed prediction``` (**green**)
2. One surrounding the actual ```sensor reading``` we got (**pink**)


<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227800213-591ff178-ef81-4605-8acd-c70dae5c57d8.png" width="700" height="270"/>
</p>

- _Our next step will be to ```reconcile our guess``` about the readings we would see based on the **predicted state** with a different guess based on our **sensor readings** that we actually observe_.
-  _To find our ```new most likely state```, we simply need to **multiply** the two Gaussian distribution and the ouput will be another **Gaussian distribution** where the mean of this distribution is the configuration for which both estimates are **most likely**, and is therefore the **best guess** of the true configuration given all the information we have._

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227800582-45f60f77-d2ff-4825-88f7-ef8c8d50a86b.png" width="700" height="160"/>
</p>













### 1.9 Final Equation


<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227095956-3c4415f1-d365-4899-ba95-85255d433a47.gif"/>
</p>








--------------

## 2. Object Tracking






## References

1. https://engineeringmedia.com/controlblog/the-kalman-filter
2. https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/
3. https://www.youtube.com/watch?v=mwn8xhgNpFY&list=PLn8PRpmsu08pzi6EMiYnR-076Mh-q3tWr&ab_channel=MATLAB
4. https://www.mathworks.com/videos/series/understanding-kalman-filters.html
5. https://arshren.medium.com/an-easy-explanation-of-kalman-filter-ec2ccb759c46
6. https://www.youtube.com/watch?v=CaCcOwJPytQ&list=PLX2gX-ftPVXU3oUFNATxGXY90AULiqnWT&ab_channel=MichelvanBiezen
7. https://www.kalmanfilter.net/default.aspx
8. https://www.alanzucconi.com/2022/07/24/kalman-filter-3/
9. https://machinelearningspace.com/2d-object-tracking-using-kalman-filter/
















