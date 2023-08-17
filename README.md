# UAV Drone: Object Tracking using Kalman Filter

## Problem Statement

In our scenario, we have a drone that is engaged in delivering packages within a bustling urban environment. Unlike other existing systems in the market where packages are dropped from above using ```parachutes```, our innovative approach employs a ```cord mechanism```. This cord is securely attached to the package and is gradually lowered once the drone reaches its destination. While this novel system offers an enhanced user experience and prioritizes the well-being of all involved parties, it does come with a potential **drawback**. There is a possibility that an individual or an animal, either intentionally or unintentionally, may pull or trip on the attached cord. Such an action poses **risks** to both the user and the drone, potentially leading to **injuries** in certain circumstances.

The drone is equipped with an RGB camera and a Stereo camera. Utilizing the data collected by these cameras, we can develop a sophisticated tracking system. This system will enable the drone to safely lower the package to the ground, ensuring that it does so only when it predicts a **minimal risk** of the cord being pulled. By analyzing the camera data, the tracking system will be capable of identifying and tracking individuals or animals that are in close proximity to the intended landing position of the drone's package. This proactive approach will allow the drone to avoid potential risks and ensure the ```safe delivery``` of packages without endangering users or causing harm to surrounding individuals or animals.

While computer vision-based tracking algorithms have been widely used, it's important to consider the challenges posed by urban delivery environments. In city settings, the presence of obstructions such as trees, electric poles, and buildings can hinder the effectiveness of computer vision alone. Additionally, the dynamic nature of urban environments introduces a multitude of moving objects that need to be accounted for. To ensure safe and reliable operations, it is crucial for our tracking system to be capable of accurately detecting and tracking not only stationary objects but also individuals or animals approaching the drone's landing position, as they pose a significant risk of collision with the drone or the package it carries.


<!-- https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/185ab3fe-8e05-4ea2-8f97-edfbec99ddea
 -->
 
In the video below, an obstructed object is shown where YOLOv8 fails to detect it. However, utilizing the Kalman Filter, we are still able to predict the future states of the object by leveraging the Process model and the current states.



<video src="https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/c17304b6-4e4c-481d-a881-63331c907699" controls="controls" style="max-width: 730px;">
</video>



## Abstract
This project involved designing and implementing a linear Kalman filter from scratch to track both stationary objects and moving entities, such as individuals or animals, near the drone's landing position. Real-world testing demonstrated the filter's effectiveness in providing accurate position and velocity estimates, reducing the risk of collision. However, limitations were observed in handling non-linear dynamics and uncertainties. It was concluded that non-linear Kalman filters, like the **Extended Kalman Filter** or **Unscented Kalman Filter**, would be more suitable for complex scenarios. Further research on non-linear Kalman filters is recommended to improve tracking accuracy and robustness in dynamic environments.

Brian Douglas's blog, Bzarg's online tutorial, and Dr. Steven Dumble's course provided essential guidance and insights on Kalman filters and tracking algorithms. Their resources greatly influenced my understanding and implementation of the Kalman filter, enhancing the success of this project. I sincerely appreciate their valuable contributions and acknowledge their significant impact on my work. Some of the graphs and visualization have been adapted from their work.


----------

## Plan of Action

1. [Basics of Kalman Filter](#basics-of-kalman-filter)

2. [Kalman Filter Implementation](#kalman-filter-implementation)

3. [Autonomous Car Tracking](#autonomous-vehicle-tracking)

4. [UAV Object Tracking](#uav-object-tracking)

----------

<a name="basics-of-kalman-filter"></a>
## 1. Basics of Kalman Filter

### 1.1 The Origin
The Kalman Filter was invented by the great ```Rudolf E. Kálmán``` who received the **National Medal of Science** on Oct. 7, 2009, from President Barack Obama at the White House. Kalman filters were first used during the **Apollo space program** that put men on the moon, in the **NASA Space Shuttle**, **U.S. Navy submarines**, and in **unmanned aerospace vehicles** and **weapons**.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227087845-8ff20652-62aa-4df9-a3bb-2439f3c0f171.jpg" width="450" height="300"/>
</p>
<div align="center">
    <p>Image Source: <a href="https://www.gainesville.com/story/news/2009/10/08/obama-honors-former-uf-professor-with-science-medal/31724964007/">Obama honors former UF professor with science medal</a></p>
</div>


### 1.2 The Purpose
Let's see examples of why we may need Kalman Filters. 

**Example 1**: We need to measure the internal temperature of a core reactor of a nuclear power plant. You may guess that we cannot put any type of sensors directly into the core as they will melt instantaneously. The best we can do is measure external temperature outside the core and then use a Kalman Filter to find the best estimate of the internal temperature from an indirect measurement. That is, we use a Kalman Filter when ```we cannot measure directly the variables of interest```.

**Example 2**: Suppose we want to track the location of our drone at a specific time ```t```. We may use the a **GPS** to do so but the precision may differ based on the number of satellites available and other factors. We may use the onboard **IMU** sensor to deduce the distance traveled but our sensor can be ```noisy```. So what we can do is ```fuse``` both sensors' measurements to find the optimal estimate of the exact location of our drone. That is, we use Kalman Filter when we want to find ```the best estimate of states by combining measurements from various sensors in the presence of noise```.

```To put it simply, our aim is to determine the current state of the system by considering both its underlying dynamics and the presence of imperfect measurements.```

### 1.3 Types of Kalman Filter
The choice of the filter depends on the specific characteristics of the system being modeled and the accuracy requirements of the application. In some cases, it may be necessary to perform experiments or simulations to determine which filter performs best for a given situation.

 ### Linear Kalman Filter

- Assumes the system dynamics and measurement models are linear.
- Updates the state estimate and covariance directly using linear equations.
- Suitable for systems that can be accurately represented by linear models.
- Widely used in applications such as tracking, navigation, and control systems.
 
 
 ###  Extenden Kalman Filter

- Extends the linear Kalman filter to handle nonlinear system dynamics and/or measurement models.
- Approximates the nonlinear models using a first-order Taylor series expansion.
- Requires calculating Jacobian matrices for nonlinear models.
- Used when the system dynamics or measurements exhibit nonlinear behavior.
- Commonly used in applications such as robotics, autonomous vehicles, and aerospace systems.
 
 
 ###  Unscented Kalman Filter

- Overcomes the need for linearization in the EKF by using a deterministic sampling-based approach.
- Represents the probability distribution of the state using a set of sigma points.
- Propagates these sigma points through the nonlinear functions to estimate the mean and covariance of the state.
- More accurate than the EKF for highly nonlinear systems.
- Suitable for applications where the system dynamics are highly nonlinear and/or the EKF fails to provide accurate results due to significant nonlinearities in the system.

### 1.4 The States
Kalman Filter (KF) are ideal for systems that are ```continuously changing```. Why? Because KF keeps only the ```previous state``` hence, they are fast and well-suited for ```real-time problems```. 

So what is this ```"state"``` term? The state is the **underlying configuration** of our system. It can be the ```position```, ```velocity```, ```volume```, ```temperature``` and so on of our system. We will take the example of our drone which has two states: **position** and **velocity**. And it will be represented in a ```state vector```. 

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227746812-5be18f7e-769a-4a39-b55a-2fa9c413bc73.png"/>
</p>

Now that we know what are states, let's define the steps of a KF. In a nutshell, KF can be expressed in a two-step process: **prediction** and **update** which provides an ```optimal state estimate```.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/f0ed980d-9063-44d9-a8b8-6c67fe037380" width="750" height="250"/>
</p>

Suppose we want to track the position of our drone at time ```t```. Our GPS and other sensors have **noise** hence, will not provide an accurate result. But what if we can provide a ```mathematical model``` of our system? With Newton's Equation of Motion, we can predict at time ```t+1``` what will be the position of our drone using its velocity. However, this will be a flawed model as we are not taking into account **external factors** such as wind resistance, snow, rain, and so on. Hence, this is a ```flawed model```. In summary, we have a sensor with **uncertainty** and a mathematical model with its own **uncertainty**. What if we could **combine both**? And that is exactly what the Kalman Filter does.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227795840-0f3e94db-1ad8-4a7b-8364-c68bc89abf0e.png" width="460" height="150"/>
</p>


- The Kalman Filter will combine ```measurements``` from a **noisy sensor** and the ```prediction``` of a **flawed model** to get a more ```accurate estimate``` of the system state than either one **independently**.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/dc991fe4-ae3f-482f-8019-933ca8a51bc7" width="750" height="390"/>
</p>

- The Kalman Filter computes the ideal **weightage** for the ```measured``` and ```predicted``` states, so that the resulting ```corrected state``` is positioned precisely at the **optimal** location between them.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227746239-7e4262ad-888f-48b6-9125-4ee5175449a6.png" width="800" height="340"/>
</p>

Note that we do not know what is the **actual** position and velocity due to the uncertainties. But we do know that there is a whole range of possible combinations that may be true.
 
 One important **assumption** of KF is that it expects our variables to be ```random``` and ```Gaussian``` distributed. Hence, if we denote our variables using a state vector ```x```. Each variable has a **mean** and a **variance** such that:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227746364-6a3ae6c7-2dee-450f-8fd8-7a46737f29ba.png"/>
</p>

Note that the variables may be **correlated**. For example, here, position and velocity are correlated as a higher velocity expects to give a higher position. Hence, this correlation is captured in a **covariance matrix**:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227746761-aaab051f-fdfc-4d8b-9f97-545dbe6529f0.png"/>
</p>

A positive covariance indicates that the variables tend to increase or decrease together, while a negative covariance indicates that as one variable increases, the other tends to decrease.

- The Kalman filter works by propagating the mean and covariance of the Gaussian distributions for the estimated state through time using a **linear process model**. This is known as the prediction step or process update, where the estimates move forward in time.

- When measurements are available, which are a linear combination of the state, the Kalman filter updates the estimated state's mean and covariance based on the measurements' mean and covariance of the Gaussian distribution. This is the update step or corrections step for the Kalman filter.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/bdc9e6a8-25f9-44d2-a650-8e891263024e" width="800" height="540"/>
</p>

- These two processes form the prediction and correction step, which is recursively run in the filter with time. The estimates are propagated forward in time to the current time.
If the measurement information is available at the current time, it is used to improve the current state estimates. This is then repeated as time moves forward, 

---------------------------------------

### 1.5 Process Model: Prediction

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
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/f4696875-f649-4080-bd66-b8c9e5f6b6f1"/>
</p>

In we expand our state vector to represent a 2D model:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/97021005-c68a-4144-85d6-e53c77601294"/>
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
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/aeecaa91-c11d-4dfa-be4d-d39a483d1217"/>
</p>



Re-writting again with ![CodeCogsEqn (13)](https://user-images.githubusercontent.com/59663734/227747531-e7627dec-8a96-4afb-b979-f4534a56b60c.png) being the **State Transition Matrix**.:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227752027-0ef3a998-3b4e-4c60-985d-ca3956437482.png"/>
</p>

The State Transition Matrix propagates the state at sample ```k-1```to the state sample ```k```. 

Now we need to propagate the error covariance forward. Note that uncertainty comes from ```2``` sources when predicting:

    1. Initial uncertainty in the system before prediction
    2. Additional uncertainty as we propagate the state forward in time

We will define the ```initial uncertainty``` first with ![CodeCogsEqn (16)](https://user-images.githubusercontent.com/59663734/227752062-7d98795d-a74d-4e2e-bf6b-900d0cd43d4d.png)
 known as the **Prediction Error Covariance Matrix**:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227751910-a6be1fd4-a1b4-41b0-be37-5b754f6d48f6.png"/>
</p>

Note that we use the State Transition Matrix F to propagate the initial error covariance.

### 1.6 Process Model: External Influence
In the first part of our prediction model, we assumed a **constant velocity**. But that is not always the case in the real world. External forces may cause a system to accelerate. There may be changes that are not related to the state itself. Thus, we assume a **linear acceleration**.

We use Newton's Equation of Motion to update our model:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227752300-584aa592-68e1-42b4-9c9e-9aece1a9a3b5.png"/>
</p>

Re-writing it in matrix form:

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227752403-ac80ac8c-1047-4606-821a-869eb718289f.png"/>
</p>

In 2D:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/9d722940-c766-414d-96cf-c6fe5ad0f7db"/>
</p>

![CodeCogsEqn (19)](https://user-images.githubusercontent.com/59663734/227752417-2ce97302-ebe7-4394-a3b8-1ceea6bde07f.png) is the **control matrix** and ![CodeCogsEqn (20)](https://user-images.githubusercontent.com/59663734/227752424-7e4f1d27-6aeb-4f89-aabb-6c81dd5997e5.png) is called the **control vector**. By factoring in the system's dynamics and the effects of external controls on its future state, we can derive an estimated state projection

However, when we do external tracking we may not know about this input vector. Instead of having a known deterministic input, we assume that the input is just going to be due to noise. Hence, we replace![CodeCogsEqn (3)](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/643831d6-edae-424b-9f2c-9b32010b7084) with ![CodeCogsEqn (4)](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/5221e057-7167-447f-bf88-6acf11c39334) which is the Process Model Noise Sensiivity Matrix and the Process Model Noise vector respectively.

We then have:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/52e3e590-a253-496a-857e-42e60550d45c"/>
</p>


### 1.7 Process Model: External Uncertainty
It is impossible to model every external force (friction, air resistance,...) acting on our system. In order to counter that, we add some new uncertainty after every prediction step. We will model the **second** source of uncertainty into our system: ```uncertainty as we propagate the state forward in time```.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227753050-b7eb3810-2031-4e86-9489-e7cfd6e118b9.png" width="400" height="300"/>
</p>


- Each blue point in the diagram above can be our current state though it is most likely the actual state will be at the **center** of the Gaussian blob.
- When predicting the next time step, a new **Gaussian** blob is created whereby each new green point can be the actual predicted state.
- Each predicted point (green) has its own Gaussian blob, i.e., when we deal with **unobserved factors** that can impact the system's performance, we treat them as random disturbances or ```noise``` with a particular **covariance matrix**.

The new **Prediction Error Covariance Matrix** ![CodeCogsEqn (16)](https://user-images.githubusercontent.com/59663734/227752062-7d98795d-a74d-4e2e-bf6b-900d0cd43d4d.png) is: 

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227753925-5e2deb93-b4d2-477e-89da-6e194fe633e8.png"/>
</p>

where:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/7b8f1d6e-f9ad-41b7-9292-1da2cbee9518"/>
</p>

where 

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/96a88bec-772c-4443-8412-2d16f0b16d99"/>
</p>

 and 
 
<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/ef8e8f99-911c-408b-89c0-dd909cefaf4e"/>
</p>


Note that we build up the new uncertainty from the old one by adding some uncertainty from the ```environment```. This new uncertainty is **proportional** to the ```time horizon```. That is, the further we predict, the **bigger** this new uncertainty will be. So, the **Prediction Covariance Matrix** ```grows``` over time.

This additional uncertainty is modelled by the **Process Noise Covariance Matrix**, ![CodeCogsEqn (24)](https://user-images.githubusercontent.com/59663734/227754179-426ee4b2-400e-40c8-ad7f-53803289f3b0.png). This matrix captures all uncertainty which we **cannot** model coming from ```unknown inputs``` or from the **discrepancy** in our ```predicting model```.

To sum up:

1. The new best estimate is a prediction model from the previous best estimate  ```+``` a correction for known external influences.
2. The new uncertainty is predicted from the old uncertainty ```+``` additional uncertainty from the environment.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227754762-ebf90ab8-24a4-4b3c-ae62-68a56cdfb1f3.png"/>
</p>

---------------------------------------


### 1.8 Measurement: Noise & Estimate
Recall that the Kalman Filter will combine measurements from a **noisy sensor** and the **prediction of a flawed model** to get a more accurate estimate of the system state than either one independently. What we have done since then is build a mathematical model in order to predict the next state of our system. What we will do now, is take readings from our sensor in order to get a ```measurement estimate```.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227795993-e89ba02b-17eb-4c05-95d2-46638e337fbe.png" width="460" height="140"/>
</p>

When we buy a sensor, the manufacturer tells us about the ```precision``` of the module. Precision is how close all the sensor readings are grouped to each other. When we need to measure distance using a laser for example, we cannot expect to get the same reading every time we take a measurement with our sensor. There will be some small variations and this is due to ```random noise``` in the sensor. 

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

From the diagram above, notice how as we propagate further into the future our **Process Noise Covariance Matrix**, ![CodeCogsEqn (24)](https://user-images.githubusercontent.com/59663734/227754179-426ee4b2-400e-40c8-ad7f-53803289f3b0.png), grows bigger and bigger. In total, we have ```3``` error covariance matrices: ![CodeCogsEqn (33)](https://user-images.githubusercontent.com/59663734/227801696-c2b50054-c440-4c04-9300-b0da0e787fef.png), ![CodeCogsEqn (32)](https://user-images.githubusercontent.com/59663734/227801712-9bee671b-ecf0-40aa-b297-c719afb2febc.png), 
![CodeCogsEqn (31)](https://user-images.githubusercontent.com/59663734/227801722-7d6cb918-9657-40c9-8a44-ea358e062373.png).


To sum up, we now have ```2``` Gaussian blobs:

1. One surrounding the mean of our ```transformed prediction``` (**green**)
2. One surrounding the actual ```sensor reading``` we got (**pink**)


<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227800213-591ff178-ef81-4605-8acd-c70dae5c57d8.png" width="700" height="270"/>
</p>

- _Our next step will be to ```reconcile our guess``` about the readings we would see based on the **predicted state** with a different guess based on our **sensor readings** that we actually observe_.
-  _To find our ```new most likely state```, we simply need to **multiply** the two Gaussian distributions and the output will be another **Gaussian distribution** where the mean of this distribution is the configuration for which both estimates are **most likely**, and is, therefore, the **best guess** of the true configuration given all the information we have._

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227800582-45f60f77-d2ff-4825-88f7-ef8c8d50a86b.png" width="700" height="160"/>
</p>

--------------
                                                                                                                                            
### 1.9 Gaussian Multiplication
As explained above, if we multiply two Gaussian distributions, our output will still be a Gaussian distribution. We will have something like this:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/e28ba619-4a84-4c0d-a47f-c0c5b4f6761f"/>
</p>

After some simplification, our new mean can be expressed as:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/d862d849-7fc7-41a8-93fd-d944b1437228"/>
</p>

and the new variance as:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/7f72f9ae-27dd-4d3a-83a2-b8153a721f1a"/>
</p>

We can factor out ```k``` where k: 

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/b507b7e9-3cf2-4fcf-98d9-30cd43793f9b"/>
</p>
                                                                                                                                              
Hence, re-writing the new mean and new covariance:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/bbdb91f2-ad97-4981-afcf-ca49aca4d14e"/>
</p>

Re-writing them in matrix form:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/291c837d-54c7-42f0-b109-d47a1417d5e6"/>
</p>

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/0ce857b1-a27d-43b4-adf9-904a861c87b9"/>
</p>

Note that ```K``` is the **Kalman Gain** which is the ```ratio``` of the covariance of the predicted state estimate to the sum of the covariance of the predicted state estimate and the covariance of the measurement. 

The Kalman gain ratio plays a crucial role in determining the **weight** given to the current measurement and the predicted state estimate during the update step of the Kalman filter. It represents the relative importance of the measurement in adjusting the state estimate. 

- A **higher** Kalman gain ratio means that the ```measurement``` has a **larger influence** on the updated state estimate.
- A **lower** ratio indicates a greater reliance on the ```predicted state estimate```.

---------------------------------

### 2.0 Putting all together
We have 2 Gaussian distributions: one for the process model and another for the measurements:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/fde466c2-ea4c-43e0-b51b-052bf34435b9"/>
</p>

The new mean for our new Gaussian distribution is then:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/ba23389f-1371-4281-bda3-1dc957c49735"/>
</p>
              
And the new covariance is: 

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/5d1c030e-cc51-4137-a99a-4c15397d5754"/>
</p>

The Kalman Gain is then defined as:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/bf44caa6-7f9c-426e-bc26-ee3fc396ab9b"/>
</p>

Let's define some more terms.

#### Innovation Residual
The innovation residual represents the discrepancy between the predicted measurement and the actual measurement.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/196760eb-9eb8-4af1-9c6a-f011f8c9cde3"/>
</p>

#### Innovation Covariance
The innovation covariance represents the measure of uncertainty in the prediction error between the estimated measurement and the actual measurement.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/ca3b5f4e-5ed1-4ea5-a03f-f2ca795e797a"/>
</p>

#### Kalman Gain
The Kalman gain determines the optimal weight given to the predicted state and the measurement to obtain an improved state estimate.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/4f00c69b-2eca-4ce2-b531-2135e7a82349"/>
</p>


#### Corrected State Estimate
The corrected state estimate  is the updated estimation of the true state, obtained by combining the predicted state estimate with the measurement using the Kalman gain.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/cff16101-694a-4f29-aba5-0869eca5d39e"/>
</p>

#### Corrected Estimate Covariance
The corrected estimate covariance represents the updated measure of uncertainty in the estimated state after incorporating the measurement information. It reflects the accuracy of the corrected state estimate.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/f30e9af1-6bc1-4d68-8185-32eb745d11cf"/>
</p>

Note that ![242158558-1854582f-f5d7-4a19-85c6-4e05637d46f3](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/08a5e1c9-ea36-4576-be39-81c50fb7f9ef)
 is less than 1 hence, ![242158606-aa29b71c-c649-440e-9b77-65efacacbff9](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/76038d21-fcdb-4d2c-9679-e02110e21aff) is always smaller than ![242158773-b817bde2-c875-499d-9f3a-b8cccfccc74a](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/539547ac-7e73-42de-997f-700aae5a32af). This way we reduce uncertainty in the estimates and improve accuracy.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/17e02f15-763e-4197-b39b-cd1a76f29c9e" width="700" height="400"/>
</p>


<a name="kalman-filter-implementation"></a>
## 2. Kalman Filter Implementation

We will now code our Kalman Filter from scratch. We start with a Kalman filter class and define the following parameters in the __ init __ function:

```python
class KalmanFilter(object):
    def __init__(self, dt, INIT_POS_STD, INIT_VEL_STD, ACCEL_STD, GPS_POS_STD):
        
        """
        :param dt: sampling time (time for 1 cycle)
        :param INIT_POS_STD: initial position standard deviation in x-direction
        :param INIT_VEL_STD: initial position standard deviation in y-direction
        :param ACCEL_STD: process noise magnitude
        :param GPS_POS_STD: standard deviation of the measurement
        """
```

We do not know our initial state hence, we declare it as zero values:

```python
        # Intial State
        self.x = np.zeros((4, 1))
```

We want to initialize our covariance matrix based on the standard deviation of the position and velocity as such:

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/a1811292-99d0-40d2-925a-8ba95655328d"/>
</p>

```python
        # State Estimate Covariance Matrix
        cov = np.zeros((4, 4))
        cov[0, 0] = INIT_POS_STD ** 2
        cov[1, 1] = INIT_POS_STD ** 2
        cov[2, 2] = INIT_VEL_STD ** 2
        cov[3, 3] = INIT_VEL_STD ** 2
        self.P = cov
```

The state transition matrix:

```python
        # State Transition Matrix
        self.F = np.array([[1, 0, self.dt, 0],
                           [0, 1, 0, self.dt],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
```

Next we define the process model noise using the covariance of the process model noise and the process model noise sensitivity matrix:

```python
        # Covariance of Process model noise
        q = np.zeros((2, 2))
        q[0, 0] = ACCEL_STD ** 2
        q[1, 1] = ACCEL_STD ** 2
        self.q = q

        # Process Model Sensitivity Matrix
        L = np.zeros((4, 2))
        L[0, 0] = 0.5 * self.dt ** 2
        L[1, 1] = 0.5 * self.dt ** 2
        L[2, 0] = self.dt
        L[3, 1] = self.dt
        self.L = L

        # Process model noise
        self.Q = np.dot(self.L, np.dot(self.q, (self.L).T))
```

Lastly, we want to define our Measurement matrix and the Measurement covariance matrix:

```python
        # Define Measurement Mapping Matrix
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]])

        # Measurement Covariance Matrix
        R = np.zeros((2, 2))
        R[0, 0] = GPS_POS_STD ** 2
        R[1, 1] = GPS_POS_STD ** 2
        self.R = R
```

The **predict()** function projects the current state estimate ![242317104-39d341e8-aeb8-4aaa-856b-ae24e42f5756](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/593f59f0-bfca-4feb-8c45-0f262ae06854)
 and error covariance ![242317203-03e7b0c4-f539-4b19-bb50-e3931ff4cf9d](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/feff0149-69e8-457d-975e-0ec5c30c87ba)
 forward to the next time step. It calculates the predicted state estimate ![242317580-f0c29a9a-98f6-4991-8705-560e3301259f](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/0b02e343-4ad3-4593-95e0-58528bee9743)
 and the predicted error covariance ![242317601-0a5e354c-1b00-4ebc-9233-3c991dc9522b](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/4f93e926-c10b-4319-875f-82b4a4f166f1) using the state transition matrix ```F``` and the process noise covariance matrix ```Q```. This step is crucial for updating the state estimate based on the system dynamics and accounting for the uncertainty introduced by the process noise.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/108af78d-e723-4a6e-9bd6-ef1f4f8fbee1"/>
</p>

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/915b00e4-a799-4b0d-88a4-98391ae7534f"/>
</p>

```python
    # PREDICTION STEP
    def predict(self):
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(self.F, np.dot(self.P, (self.F).T)) + self.Q
        return self.x
```

In the **update function**, we calculate the Kalman gain ![242318987-3c6bd5db-d304-453f-8b2b-b3b0b4298b37](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/5668dd7c-c5fc-461a-a2d2-de8034272f38) and use it to update the predicted state estimate ![242317580-f0c29a9a-98f6-4991-8705-560e3301259f (1)](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/72056272-756c-459c-9506-1b90de7c956d)  and predicted error covariance ![242317601-0a5e354c-1b00-4ebc-9233-3c991dc9522b (1)](https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/a2f31391-5e29-4bf4-bd4c-533e3a62a8f3). This step involves incorporating the measurement information and adjusting the state estimate based on the measurement residuals and the measurement noise covariance matrix ```R```. By applying the Kalman gain, we obtain an improved estimate of the true state, taking into account both the predicted state and the available measurement information.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/673b81ef-01ed-476d-a6bb-a5676c554e4a"/>
</p>

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/01b99da5-031b-4b0c-ad1d-c398e230ba05"/>
</p>


```python
    # UPDATE STEP
    def update(self, z):
        # Innovation
        z_hat = np.dot(self.H, self.x)
        self.y = z - z_hat

        # Innovation Covariance
        self.S = np.dot(self.H, np.dot(self.P, (self.H).T)) + self.R

        # Kalman Gain
        self.K = np.dot(self.P, np.dot((self.H).T, np.linalg.inv(self.S)))

        I = np.eye(4)

        self.x = self.x + np.dot(self.K, self.y)
        self.P = np.dot((I - np.dot(self.K, self.H)), self.P)
        return self.x
```
----------------------------
                                                                                                                                              
<a name="autonomous-vehicle-tracking"></a>
## 3. Autonomous Vehicle Tracking

Now we need to test if our implementation really works. Consider an autonomous vehicle starting at position ```(0,0)```traveling at a constant speed of ```5 m/s``` with a heading of ```45``` degrees. We have a GPS tracking the x and y positions of the vehicle.

```python
# Car parameters
initial_position = np.array([0, 0])
speed = 5.0  # m/s
heading = 45.0  # degrees

# Convert heading to radians
heading_rad = math.radians(heading)
```

We calculate the true positions based on constant speed and heading and use a Gaussian distribution to generate the measurements.

```python
# Calculate true positions based on constant speed and heading
true_positions = [initial_position]
for _ in range(num_measurements-1):
    delta_x = speed * math.cos(heading_rad)
    delta_y = speed * math.sin(heading_rad)
    new_position = true_positions[-1] + np.array([delta_x, delta_y])
    true_positions.append(new_position)
true_positions = np.array(true_positions).T

# Add noise to simulate measurement errors
measurement_noise_std = 5
measurements = true_positions + np.random.normal(0, measurement_noise_std, size=true_positions.shape)
```
We define the Kalman Filter parameters as such:

```python
# Kalman filter parameters
dt = 1.0  # Sampling time
INIT_POS_STD = 10  # Initial position standard deviation
INIT_VEL_STD = 10  # Initial velocity standard deviation
ACCEL_STD = 5  # Acceleration standard deviation
GPS_POS_STD = 3  # Measurement position standard deviation
```
We then apply the Kalman filter to calculate the estimated states:

```python
# Kalman filter initialization
kf = KalmanFilter(dt, INIT_POS_STD, INIT_VEL_STD, ACCEL_STD, GPS_POS_STD)

# Lists to store filtered states
filtered_states = []

# Perform prediction and update steps for each measurement
for measurement in measurements.T:
    # Prediction step
    predicted_state = kf.predict()

    # Update step
    updated_state = kf.update(measurement)

    # Store the filtered state
    filtered_states.append(updated_state)

# Convert filtered states to NumPy array
filtered_states = np.array(filtered_states).T
```

We then plot our filtered or estimated states along with the true position and the measurements. We observe that initially, our estimated states follow the GPS measurements. But with time, it converges close to the true value even when the GPS measurements are off by a lot as indicated by the yellow arrows.

<p align="center">
  <img src= "https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/4df703f4-9b6d-45d7-a5ed-bd3d60e51940"/>
</p>

Now, we will test our filter using the simulation created by Dr. Steven Dumble in his online course. It is using the same Kalman Filter we designed above but here we used C++. 


**1. ACCEL_STD = 0**

- The position and velocity uncertainty starts to the true value.
- The estimates are going to use the information contained inside the process model and converge to the truth.
- However, this won't work if we have a more dynamic system where the car changes direction abruptly.
- By having zero process model noise, the filter is going to become inconsistent because the estimated position is not close to the true position.


<video src="https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/c0c84391-03b8-46ae-be5f-627c7ccf997b" controls="controls" style="max-width: 730px;">
</video>


**2. ACCEL_STD = 0.1**

- As prediction happens, the uncertainty inside the system is inflating.
- When the car changes direction, the estimated state catches up with the true state a lot quicker than it did when we had zero process model uncertainty.
- Notice that now, we have lots of jumping around with the estimates because the amount of uncertainty in the system is growing quite rapidly.
- That is, the estimates are going to rely on the GPS measurements more than the process model.


<video src="https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/306f85db-1b73-4748-949a-c3e976cd6c4d" controls="controls" style="max-width: 730px;">
</video>


**3. ACCEL_STD = 1.0**

- We have a higher ACCEL_STD, and we have a larger uncertainty growth with time.
- The estimate catches up quicker with the true state in the corners.
- The state estimates follow the GPS measurements a lot more. It is going to trust them a lot more because it got less uncertainty inside the prediction model.

    

<video src="https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/eea33ab5-2d37-487b-9fc8-93249863a7b4" controls="controls" style="max-width: 730px;">
</video>

                                                                                                                                          

In summary:

1. **GPS_std** directly affects the size of ```R```, however **Acc_std** affects the ```Rate Of Increase in P``` (not directly the size of P). If **Acc_std** is ```large```, then ```P``` will grow quickly, so that when a new GPS measurement is made, the value of ```P will be greater than R```. Therefore, the system will trust the GPS more, since ```R is smaller than P```.

2. If we want a nice smooth response that trusts the prediction model more, we want a lower noise value for the acceleration. (Lower Q)

3. However, if the car changes direction a lot and we want the process model to try to keep up, we are going to need a larger acceleration standard deviation to let the filter update quickly for the new response. (Higher Q)

4. We assumed the initial state to be zero however, we would also have waited for the first measurement. Either way, the Linear Kalman Filter will always be updated to minimize the estimation error. 

------------------------

<a name="uav-object-tracking"></a>
## 4. UAV Object Tracking
Kalman filters are used to track the positions and velocities of objects of interest, such as other vehicles, pedestrians, or stationary obstacles. By fusing data from different sensors, such as cameras, the filter estimates the object's state with high accuracy, even in the presence of sensor noise or measurement uncertainties. This tracking information is crucial for collision avoidance as it allows the drone to perceive the current and future positions of objects in its environment.

In this scenario, we do not want to track the drone but instead people or animals approaching the drone's landing position. This is important because these moving objects can potentially collide with the drone or the package it is carrying as shown below.

<p align="center">
  <img src= "https://user-images.githubusercontent.com/59663734/227095956-3c4415f1-d365-4899-ba95-85255d433a47.gif"/>
</p>


Using ```YOLOv8```, we will get the bounding box of the region of interest and consecutively its **center**. We will use the centers as GPS Measurements that we had in the simulation before. We will still use the same Process Model we designed and update our estimates based on the center of the bounding boxes. 

```python
  # Process the frame to get bounding box centers
    centers = get_bounding_box_center_frame(frame, model, names, object_class='person')
```

With a low value for ```ACCEL_STD```, the estimates were not as close to the real value. I had to increase it to ```40``` such that the estimates now rely on the center of the bounding boxes more than the process model.

We check first if there is a bounding box, if there is we perform the predict function of our Kalman Filter then we perform the update function using the center of the bounding box. We plot the value for the predict, update and the center to check how the model is performing.


```python
    # Check if center is detected
    if len(centers) > 0:
        center = centers[0]  # Extract the first center tuple

        # Draw circle at the center
        if isinstance(center, tuple):
            print("Center = ", center)
            cv2.circle(frame, center, radius=8, color=(0, 255, 0), thickness=4) # Green

            # Predict
            x_pred, y_pred = kf.predict()
            if isFirstFrame:  # First frame
                x_pred = round(x_pred[0])
                y_pred = round(y_pred[0])
                print("Predicted: ", (x_pred, y_pred))
                isFirstFrame = False
            else:
                x_pred = round(x_pred[0])
                y_pred = round(y_pred[1])
                print("Predicted: ", (x_pred, y_pred))

            cv2.circle(frame, (x_pred, y_pred), radius=8, color=(255, 0, 0), thickness=4) #  Blue

            # Update
            (x1, y1) = kf.update(center)
            x_updt = round(x1[0])
            y_updt =  round(x1[1])
            print("Update: ", (x_updt, y_updt))
            cv2.circle(frame, (x_updt, y_updt), radius=8, color= (0, 0, 255), thickness=4) # Red
```

Below are two examples where the object changes direction abruptly. This is a good example to see how our Linear Kalman Filter is performing on a dynamic non-linear system. We observe that there is still a discrepancy between the true value and the estimated one. This is because of the process model we are using which is a linear model. 

<video src="https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/08dff052-36fb-4fcb-917e-61aec04c55ab" controls="controls" style="max-width: 730px;">
</video>


By increasing the ACCEL_STD to a high value, we rely much more on the detector than our process model. This is working fine for now however, if the detector wrongly detects the position of the object then our estimates will be off from the true value as well.


<video src="https://github.com/yudhisteer/UAV-Drone-Object-Tracking-using-Kalman-Filter/assets/59663734/ffe3bc9a-17b4-4c1a-9f15-c01652635657" controls="controls" style="max-width: 730px;">
</video>


### Conclusion

In conclusion, the implementation of a ```linear Kalman filter``` in our project has proven to be instrumental in achieving accurate and reliable tracking of both stationary objects and moving entities, such as individuals or animals, near the drone's landing position. By continuously estimating their position, the Kalman filter enables us to anticipate and respond to potential collision risks effectively. This capability is crucial in urban environments where obstructions and dynamic elements pose challenges to the drone's path. With the Kalman filter, we can enhance the safety and reliability of the drone operations, mitigating the risks associated with collisions and ensuring the successful delivery of packages. By combining computer vision with the Kalman filter, we have developed a robust tracking system that contributes to the overall efficiency and effectiveness of our delivery services.

In addition, while the linear Kalman filter has provided satisfactory results, it is worth noting that more advanced tracking algorithms such as **DeepSORT** or **ByteTrack** may offer enhanced performance and robustness in scenarios with complex dynamics and uncertainties. These algorithms leverage deep learning techniques and non-linear models to handle more challenging tracking scenarios effectively. In future iterations of our project, integrating these advanced tracking algorithms could further improve our ability to track and anticipate the movements of objects and individuals, ensuring even greater safety and efficiency in drone deliveries.


## References
[1] Engineering Media. (n.d.). The Kalman Filter. Webpage. [https://engineeringmedia.com/controlblog/the-kalman-filter](https://engineeringmedia.com/controlblog/the-kalman-filter)

[2] Bzarg, C. (n.d.). How a Kalman Filter Works in Pictures. Webpage. [https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/](https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/)

[3] MATLAB. (n.d.). Kalman Filters and Control. YouTube playlist. [https://www.youtube.com/watch?v=mwn8xhgNpFY&list=PLn8PRpmsu08pzi6EMiYnR-076Mh-q3tWr&ab_channel=MATLAB](https://www.youtube.com/watch?v=mwn8xhgNpFY&list=PLn8PRpmsu08pzi6EMiYnR-076Mh-q3tWr&ab_channel=MATLAB)

[4] MathWorks. (n.d.). Understanding Kalman Filters. Video series. [https://www.mathworks.com/videos/series/understanding-kalman-filters.html](https://www.mathworks.com/videos/series/understanding-kalman-filters.html)

[5] Arshren. (n.d.). An Easy Explanation of Kalman Filter. Webpage. [https://arshren.medium.com/an-easy-explanation-of-kalman-filter-ec2ccb759c46](https://arshren.medium.com/an-easy-explanation-of-kalman-filter-ec2ccb759c46)

[6] Udemy. (n.d.). Advanced Kalman Filtering and Sensor Fusion. Course. [https://www.udemy.com/course/advanced-kalman-filtering-and-sensor-fusion/](https://www.udemy.com/course/advanced-kalman-filtering-and-sensor-fusion/)

[7] Michel van Biezen. (n.d.). Kalman Filter Lectures. YouTube playlist. [https://www.youtube.com/watch?v=CaCcOwJPytQ&list=PLX2gX-ftPVXU3oUFNATxGXY90AULiqnWT&ab_channel=MichelvanBiezen](https://www.youtube.com/watch?v=CaCcOwJPytQ&list=PLX2gX-ftPVXU3oUFNATxGXY90AULiqnWT&ab_channel=MichelvanBiezen)

[8] Kalman Filter. (n.d.). Website. [https://www.kalmanfilter.net/default.aspx](https://www.kalmanfilter.net/default.aspx)

[9] Zucconi, A. (2022, July 24). Kalman Filter [Part 3]. Webpage. [https://www.alanzucconi.com/2022/07/24/kalman-filter-3/](https://www.alanzucconi.com/2022/07/24/kalman-filter-3/)

[10] Machine Learning Space. (n.d.). 2D Object Tracking using Kalman Filter. Webpage. [https://machinelearningspace.com/2d-object-tracking-using-kalman-filter/](https://machinelearningspace.com/2d-object-tracking-using-kalman-filter/)

[11] Towards Data Science. (n.d.). Kalman Filter Interview. Webpage. [https://towardsdatascience.com/kalman-filter-interview-bdc39f3e6cf3](https://towardsdatascience.com/kalman-filter-interview-bdc39f3e6cf3)


