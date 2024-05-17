# 3D Robotic Vision Using Movement

**By Marc van Zyl**  
**Seth Bishop**  

## Table of Contents
- [Introduction](#introduction)
- [Experimental Design](#experimental-design)
  - [Problem](#problem)
  - [Hypothesis](#hypothesis)
  - [Control Group](#control-group)
  - [Experimental Group](#experimental-group)
  - [Independent Variable](#independent-variable)
  - [Dependent Variable](#dependent-variable)
  - [Procedure](#procedure)
    - [Experimental Setup](#experimental-setup)
    - [Calibration Procedure](#calibration-procedure)
    - [Data Gathering Procedure](#data-gathering-procedure)
    - [Analysis Procedure](#analysis-procedure)
      - [Stereo Camera](#stereo-camera)
      - [Optical Flow Camera](#optical-flow-camera)
    - [Data Analysis](#data-analysis)
- [Results](#results)
  - [Stereo Camera Results](#stereo-camera-results)
  - [Sparse Optical Flow Camera Results](#sparse-optical-flow-camera-results)
  - [Dense Optical Flow Camera Results](#dense-optical-flow-camera-results)
- [Discussion](#discussion)
- [Conclusion](#conclusion)
- [Future Work](#future-work)

## Introduction
In 2018, 25,000 children were reported missing or lost. Almost 92% were runaways, and many are found dead from the elements. If a child is not found within the first 24 hours, their chance of survival is halved, and by 48 hours the odds are extremely against them. Currently, the only effective solution to search for children in wilderness areas is to organize hundreds of people to form a search chain, which is costly and often inefficient.

Drones are a potential solution due to their speed and ability to cover large areas autonomously. However, most drones rely on stereo vision for distance detection, which requires significant processing power and reduces battery life. By using optical flow, which only requires a single camera, we can potentially improve the efficiency and battery life of drones, making them a more viable solution for search and rescue operations.

## Experimental Design

### Problem
68 children are reported missing every day in the US, with 80% being lost and endangered. The only currently effective solution is using chains of hundreds of people to comb through forested areas, which is costly and prone to errors.

### Hypothesis
If optical flow applied to depth perception is more accurate and less computationally intense than stereo cameras, it will be a useful alternative or replacement.

### Control Group
The control group is a stereo camera setup using:
- Raspberry Pi 3 B+
- Arducam Multi Camera Board
- 2 x PiCamera V2.1 8M color cameras
- 3D printed stereo camera mounts

### Experimental Group
The experimental group consists of a single camera mounted on two rods, moved by an accurate stepper motor using:
- Raspberry Pi 3 B+
- 1 x PiCamera V2.1 8M color camera
- 3D printed parts
- Linear slides and bearings
- Nema 17 stepper motor
- Polulu DRV8825 high current stepper motor driver carrier

### Independent Variable
- Control Group: Distance between cameras
- Experimental Group: Distance between each picture

### Dependent Variable
Accuracy of both setups in determining the distance to objects.

### Procedure

#### Experimental Setup
1. **Stereo Camera Setup**
    - Components: Raspberry Pi 3 B+, Arducam Multi Camera Board, 2 x PiCamera V2.1 8M color cameras, 3D printed stereo camera mounts.
    - ![Stereo Camera Setup](URL_to_Stereo_Camera_Setup_Image)

2. **Optical Flow Linear Slide Setup**
    - Components: Raspberry Pi 3 B+, 1 x PiCamera V2.1 8M color camera, 3D printed parts, linear slides and bearings, Nema 17 stepper motor, Polulu DRV8825 high current stepper motor driver carrier.
    - ![Optical Flow Setup](URL_to_Optical_Flow_Setup_Image)

3. **Calibration Board**
    - 30” x 20” CharUco calibration board on foam board mounted on a tripod.
    - ![Calibration Board](URL_to_Calibration_Board_Image)

4. **Target Scene**
    - 10 x 8”x8” ArUco targets carefully laid out and measured in the target scene.
    - ![Target Scene](URL_to_Target_Scene_Image)

#### Calibration Procedure

1. **Stereo Camera Calibration**
    - Take 40 stereo images of the CharUco calibration board.
    - Perform individual camera calibration to remove distortions and obtain camera matrix (mtx) and distortion matrix (dist).
    - ![Distortion Correction](URL_to_Distortion_Correction_Image)

2. **Optical Flow Camera Calibration**
    - Take 40 images of the CharUco calibration board.
    - Perform individual camera calibration to remove distortions and obtain camera matrix (mtx) and distortion matrix (dist).

3. **Scene Calibration**
    - Mount ArUco markers in the scene and measure their cartesian coordinates.
    - Calculate distances from the camera to each marker using Python.

#### Data Gathering Procedure

1. **Stereo Camera**
    - Take 50 stereo pictures of the scene with slight adjustments between each picture.
    - Automate the process with a program on the Raspberry Pi.

2. **Optical Flow Camera**
    - Write a program to automate recording, moving the camera, and saving the files.
    - Run the program for velocities of 15, 30, 45, 60, and 75 mm/s.

#### Analysis Procedure

##### Stereo Camera
1. Apply rectification maps to Left-Right image pairs.
2. Find and optimize the four corners of the ArUco markers.
3. Calculate the pixel disparity and determine the distance using:
   $$\[
   Z = \frac{T \cdot f \cdot \text{Resolution}}{\text{Pixel Disparity} \cdot \text{Sensor Width}}
   \]$$

##### Optical Flow Camera
1. Split video frames into individual images.
2. Apply camera calibration matrices to undistort each frame.
3. Find and optimize the four corners of the ArUco markers.
4. Calculate the distance using:
   $$\[
   Z = \frac{\text{Velocity} \cdot \text{Camera Constant} \cdot \text{fps}}{\text{Pixel Disparity}}
   \]$$
   Where Camera Constant = $\(\frac{f \cdot \text{Resolution}}{\text{Sensor Width}}\)$.

### Data Analysis
Calculate the difference between the calculated distance and the actual distance to each target. Calculate the mean, standard deviation, minimum, and maximum errors for each target.

## Results

### Stereo Camera Results

![Error Comparison](URL_to_Error_Comparison_Image)

## Discussion
- The stereo camera was more accurate at closer distances, while the optical flow camera performed better at higher velocities and longer distances.
- The variance in the stereo camera measurements was higher than that of the optical flow camera at higher velocities.

## Conclusion
For linear camera motion, the optical flow algorithm achieved comparable accuracy to traditional stereo vision systems with lower variance. The optical flow was particularly effective at higher velocities and longer distances, suggesting potential for future robotic vision applications.

## Future Work
- Enhance the algorithm to account for both linear and rotational camera motion.
- Improve the dense optical flow algorithm to identify separate objects and convert the scene into a 3D map.

