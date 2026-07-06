# Benchmarking Robot Manipulation with the Rubik's Cube

[arXiv](https://arxiv.org/abs/2202.07074)

## Abstract (verbatim)

> Benchmarks for robot manipulation are crucial to measuring progress in the field, yet there are few benchmarks that demonstrate critical manipulation skills, possess standardized metrics, and can be attempted by a wide array of robot platforms. To address a lack of such benchmarks, we propose Rubik's cube manipulation as a benchmark to measure simultaneous performance of precise manipulation and sequential manipulation. The sub-structure of the Rubik's cube demands precise positioning of the robot's end effectors, while its highly reconfigurable nature enables tasks that require the robot to manage pose uncertainty throughout long sequences of actions. We present a protocol for quantitatively measuring both the accuracy and speed of Rubik's cube manipulation. This protocol can be attempted by any general-purpose manipulator, and only requires a standard 3x3 Rubik's cube and a flat surface upon which the Rubik's cube initially rests (e.g. a table). We demonstrate this protocol for two distinct baseline approaches on a PR2 robot. The first baseline provides a fundamental approach for pose-based Rubik's cube manipulation. The second baseline demonstrates the benchmark's ability to quantify improved performance by the system, particularly that resulting from the integration of pre-touch sensing. To demonstrate the benchmark's applicability to other robot platforms and algorithmic approaches, we present the functional blocks required to enable the HERB robot to manipulate the Rubik's cube via push-grasping.

## Background

### Background Analysis  

#### 1. Technical Context and Real-World Needs  
Robot manipulation (e.g., grasping, rotating, assembling objects) is a core technology in AI and automation, with applications in industrial manufacturing, home service, and medical assistance. For instance, factories need robots to assemble parts precisely, while home robots must manipulate daily items (e.g., twisting bottle caps, organizing desks). A key challenge here is that robots must not only "perceive" the environment but also "interact" with it to complete tasks. Existing benchmarks (e.g., object recognition or simple grasping) fail to comprehensively measure such complex abilities.  

#### 2. Limitations of Previous Approaches  
While researchers agree on the importance of quantitative evaluation, current robot manipulation benchmarks have two major flaws:  
- **Single-focus** Most benchmarks (e.g., "moving boxes" or "placing cups") test only one skill (e.g., precise positioning or short-sequence operations) and cannot evaluate the combination of "high precision" and "long-sequence operations." For example, solving a Rubik’s cube requires repeated precise adjustments of multiple components while managing accumulated errors.  
- **Lack of generality** Existing benchmarks either rely on specialized hardware (e.g., complex robotic arms) or are too simplistic to adapt to different robot platforms.  

#### 3. Proposed Solution  
The paper introduces "Rubik’s cube manipulation" as a new benchmark to address these issues:  
- **Dual requirements** The cube’s structure demands both "high precision" (each small cube is only 1.9 cm wide) and "long-sequence operations" (solving requires >20 steps).  
- **Standardized protocol** A protocol is designed to measure accuracy and speed, requiring only a standard 3×3 cube and a flat surface, making it applicable to various general-purpose robots (e.g., PR2 or HERB).  
- **Openness** Open-source software and two baseline methods (e.g., pose-based manipulation and tactile feedback optimization) are provided for easy comparison of algorithm improvements.  

#### 4. Key Differences from Prior Work  
Compared to existing benchmarks, this work stands out by:  
- **Task complexity** Rubik’s cube manipulation tests both precision and sequential operations, rather than a single skill.  
- **Generality** It requires only basic equipment and general robots, lowering entry barriers.  
- **Extensibility** Error accumulation and feedback mechanisms directly link to advances in planning, perception, and control.  

This benchmark not only provides a quantitative tool for researchers but also makes the complexity of robotics accessible to the public through a familiar challenge.

## Method, Figure by Figure

![Figure 3 : HERB’s simulated Barrett hands manipulate the Rubik’s cube in blue. L](fig3_1.webp)

> Figure 3 : HERB’s simulated Barrett hands manipulate the Rubik’s cube in blue. Left: The right gripper uses a push-grasp to make contact with the Rubik’s cube. Upon making contact, the right gripper reaches the desired pre-grasp. Right: The right gripper closes its outer fingers to transition from pre-grasp to grasp.

This figure (Figure 3) from the paper "Benchmarking Robot Manipulation with the Rubik's Cube" illustrates two key steps of the "push-grasp" method used by HERB robot's simulated Barrett hands to manipulate a blue Rubik's cube. The core purpose of this figure is to visualize a specific grasping strategy.

First, let's examine the left image:
- **Main Components**: The image shows both arms of the HERB robot, each equipped with a simulated Barrett hand. The right arm (referred to as the "right gripper") is the focus of the operation.
- **Rubik's Cube**: A blue Rubik's cube is positioned on the left side of the scene, serving as the target object.
- **Action Description (Left Image)**: The right gripper is executing a "push-grasp" action. Specifically, its "outer fingers" have made contact with one face of the Rubik's cube, establishing a "pre-grasp" position. In this stage, the fingers may not be fully closed yet but are in a preparatory posture, using contact with the cube to adjust its position or orientation for a subsequent grasp. The image shows the cube being slightly pushed to the right, while the right gripper's fingers have made contact with the cube's surface, forming an initial contact point.

Next, we look at the right image:
- **Main Components**: Similar to the left image, it shows both arms of the HERB robot and the blue Rubik's cube.
- **Action Description (Right Image)**: The right gripper has transitioned from the "pre-grasp" state to the "grasp" state. It is evident that the "outer fingers" of the right gripper are fully closed, firmly gripping the Rubik's cube. This action indicates that the robot has successfully completed the push-grasp process, and the cube is now securely held in hand. The position of the cube has changed slightly relative to the left image, likely due to the grasping action.

This figure reveals how the HERB robot uses its simulated Barrett hands to execute the "push-grasp" operation in specific steps:
1. **Pre-grasp Phase**: The right gripper uses its outer fingers to contact the Rubik's cube, adjusting its position or orientation by pushing the cube to reach an ideal pre-grasp position. The purpose of this phase is to prepare for the subsequent grasping action.
2. **Grasp Phase**: Once the pre-grasp position is determined, the outer fingers of the right gripper close, firmly grasping the Rubik's cube. The purpose of this phase is to ensure the cube is stably held in hand for the next operation.

By comparing the two images, we can clearly see the execution process of the "push-grasp" method. This method may be used to handle objects that are difficult to grasp directly, adjusting their position by pushing to make grasping easier. The figure demonstrates this process as a specific example of the HERB robot manipulating a Rubik's cube in a simulated environment, showcasing its capabilities in precise and sequential manipulation.

In summary, this figure visually presents how the HERB robot's simulated Barrett hands use the "push-grasp" method to manipulate a blue Rubik's cube through two consecutive actions. The left image shows the pre-grasp phase, and the right image shows the grasp phase, clearly illustrating the specific steps and process of this operation.

---

![Figure 2 : The robot must precisely position its grippers to rotate the left col](fig2_1.webp)

> Figure 2 : The robot must precisely position its grippers to rotate the left column of the Rubik’s cube while constraining the middle and right columns in place. Top Row: The robot correctly positions its grippers: it is constraining the two right columns of the cube. The yellow box highlights the position of the constraining gripper. Middle Row: The robot only touches one column of the Rubik’s cube and therefore fails to constrain its middle column. Bottom Row: The right gripper is touching all three columns of the cube; this prevents the left gripper from rotating the left column of the cube.

This image (Figure 2) is from the paper "Benchmarking Robot Manipulation with the Rubik's Cube" and clearly demonstrates how a robot manipulates a Rubik's Cube by precisely adjusting the position of its end effector (i.e., the gripper) to achieve a specific goal—rotating the left column while keeping the middle and right columns fixed. The entire image is divided into three horizontal rows, each representing a different constraint state, and the operation process is shown through a sequence of arrows from left to right.

1.  **First Row (Top, Blue Background Title: "Rubik's Cube Correctly Constrained")**:
    *   **Left Image**: Shows the initial state where the robot gripper correctly grasps the cube. A yellow box highlights the gripper used for "constraining" (usually the right gripper). The position of this gripper ensures that the middle and right columns are firmly fixed, preventing them from moving during subsequent operations. The other gripper (on the left) is ready to manipulate the left column.
    *   **Middle Image**: Displays the robot beginning to rotate the left column. You can see that the blocks in the left column have rotated relative to the middle and right columns (for example, a green face block becomes visible on the right).
    *   **Right Image**: Shows the state after the rotation is complete. The left column has been successfully rotated, while the middle and right columns remain stable without unnecessary movement. The arrows indicate the order of operations: from correctly constrained state -> performing rotation -> completed rotation.

2.  **Second Row (Middle, Orange Background Title: "Rubik's Cube Under Constrained")**:
    *   **Left Image**: Shows the situation where the robot gripper is under-constrained. The gripper within the yellow box is incorrectly positioned, touching only part of a column (possibly the middle or right column) and not effectively fixing the middle column.
    *   **Middle Image**: When the robot tries to rotate the left column, since the middle column is not sufficiently constrained, it also moves during the rotation (you can see a larger movement range of the green face block, or the blocks in the middle column also rotate).
    *   **Right Image**: Displays the state after the rotation is complete. Although the left column has rotated, the middle column has also been affected, causing the overall structure of the cube to not remain stable as expected. This indicates that insufficient constraint leads to imprecise operation. The arrows also indicate the order of operations: from under-constrained state -> attempting rotation -> middle column also moves after rotation.

3.  **Third Row (Bottom, Green Background Title: "Rubik's Cube Over Constrained")**:
    *   **Left Image**: Shows the situation where the robot gripper is over-constrained. The position of the gripper within the yellow box causes it to touch all three columns (left, middle, and right) of the cube.
    *   **Middle Image**: When the robot tries to rotate the left column, due to the over-constraint from the right gripper, the smooth rotation of the left column is prevented. You can see that the rotation of the left column is hindered or does not succeed at all.
    *   **Right Image**: Displays the state after the attempted rotation. The left column has barely rotated because over-constraint causes mechanical interference. The arrows indicate the order of operations: from over-constrained state -> attempting rotation -> rotation fails or is restricted.

**How the Method Works**:
This image reveals one of the core challenges in robot manipulation of a Rubik's Cube: precise control of constraints. To rotate a specific part of the cube (e.g., the left column), the robot must:
*   **Correctly Constrain**: Firmly fix the parts that should not move (the middle and right columns) with one gripper. This way, when the other gripper (or a different part of the same gripper) applies force to rotate the target part, the entire cube does not produce errors due to the movement of other parts.
*   **Avoid Under-Constraint**: If the constraint is not enough, the unfixed parts will move during rotation, leading to imprecise operation and potentially disarranging already arranged blocks.
*   **Avoid Over-Constraint**: If there is too much constraint, the part being rotated will get stuck by the other fixed parts and cannot rotate smoothly.

The arrows in the image indicate the order of operations: first is the initial position of the gripper (correctly, under-, or over-constrained), then is the action of attempting rotation, and finally is the resulting state after rotation. By comparing these three rows, we can clearly see that correct constraint is crucial for achieving precise and controllable manipulation of the Rubik's Cube.

**Conclusion**:
This image effectively demonstrates, in a visual way, the impact of the precision of constraints on the success of robot manipulation tasks involving a Rubik's Cube. It shows that to achieve complex manipulation tasks, robots not only need precise positioning capabilities but also need to understand how to interact correctly with the environment (in this case, the Rubik's Cube) to avoid unnecessary movement or obstruction.

---

![Figure 1 : Rubik’s cube manipulation can be used to benchmark robot manipulation](fig1_1.webp)

> Figure 1 : Rubik’s cube manipulation can be used to benchmark robot manipulation across a wide array of algorithmic approaches and robot platforms, such as the PR2 and HERB.

This image, Figure 1 from the paper "Benchmarking Robot Manipulation with the Rubik's Cube," visually presents the core concept of the research: using Rubik's cube manipulation as a benchmark to evaluate the performance of different robotic platforms and algorithms in manipulation tasks.

The image is composed of two main sections, positioned side-by-side on the left and right, contrasting the execution of Rubik's cube manipulation on two different robotic platforms.

**Left Section:**
*   **Component/Scene**: This part shows a real robot, specifically a PR2 robot. The PR2 is a well-known mobile manipulator robot equipped with two manipulator arms and a sensor head on top.
*   **Action**: One of the PR2's arms (appearing to be the right arm) is holding a standard 3x3 Rubik's cube with its end effector (gripper). The colors of the cube are clearly visible, indicating it is in a specific initial or intermediate state. The robot's posture is stable, suggesting it is in the process of or preparing for cube manipulation.
*   **Environment**: The background is a simple white backdrop, and the floor is dark, likely a laboratory setting. This setup is typical for precise control and recording of robot operations.
*   **Information Conveyed**: This section represents the implementation of the Rubik's cube manipulation task in a real-world physical environment. It demonstrates the practical application scenario of how a robot interacts with the cube in the real world. This corresponds to the paper's "protocol for quantitatively measuring both the accuracy and speed of Rubik's cube manipulation" in a real-world setting.

**Right Section:**
*   **Component/Scene**: This part shows a robot, specifically a HERB robot, within a simulated environment. HERB is another mobile manipulator robot with two arms, but here it is represented as a 3D model, typically used for simulation research.
*   **Action**: One of HERB's arms (also appearing to be the right arm) is reaching towards an object, which is highlighted in blue. While this object does not look like a complete Rubik's cube, it likely represents a specific element or state related to the Rubik's cube manipulation task, or a simplified representation of the cube within the simulation environment. This indicates that HERB is executing or preparing to execute an action related to the cube.
*   **Environment**: The background is a typical 3D simulation environment with a grid floor and simple geometric shapes (like a red box) as obstacles or background elements. Such an environment allows researchers to test and develop algorithms without involving actual hardware.
*   **Information Conveyed**: This section represents the implementation of the Rubik's cube manipulation task in a simulated environment. It shows another way to develop, test, and improve robot manipulation algorithms. This contrasts with the real-world robot experiment on the left, illustrating that the benchmark can be applied to different experimental platforms.

**Overall Understanding and Methodology Flow:**
This image reveals the core methodology of the research: proposing a general benchmark (Rubik's cube manipulation) that can be executed on different robotic platforms (such as PR2 and HERB).
*   **Objective**: To evaluate a robot's capabilities in precise manipulation (e.g., positioning specific parts of the cube) and sequential manipulation (e.g., executing a series of actions to solve the cube).
*   **Method**:
    1.  **Define the Benchmark Task**: Use the Rubik's cube as the task object because it requires both precise positional control and handling of pose uncertainty (as the cube can be in multiple configurations).
    2.  **Platform Applicability**: The benchmark is designed to be generic enough so that any general-purpose manipulator can attempt it. It only requires a standard 3x3 Rubik's cube and a flat surface (like a table).
    3.  **Experimental Setup**:
        *   Experiments are conducted on a real PR2 robot, as shown on the left, to measure actual accuracy and speed.
        *   Experiments are conducted on a simulated HERB robot, as shown on the right, to develop and test algorithms and potentially evaluate performance improvements from different methods (such as pre-touch sensing).
*   **Data/Information Flow**: Although the image does not explicitly show data flow arrows, the methodology flow can be inferred:
    *   **Input**: A standard 3x3 Rubik's cube placed on a flat surface.
    *   **Processing**: The robot (either real or simulated) uses its algorithms and sensors to perceive the cube's state, plans, and executes a sequence of actions to manipulate the cube (e.g., solve it).
    *   **Output**: The result of solving the cube (e.g., whether the cube is correctly solved) and the time taken to complete the task. This data is used to evaluate the robot's performance.
*   **Implication of Conclusion**: By showing two different types of robots (one real, one simulated) capable of performing this benchmark, the image suggests the broad applicability and importance of this benchmark. It indicates that the benchmark can be used to compare different algorithms, sensor technologies, or robotic platforms in solving complex manipulation tasks.

In summary, this image effectively communicates the paper's core contribution by showing PR2 and HERB robots manipulating a Rubik's cube in different environments (real world and simulation). It proposes a general benchmark—Rubik's cube manipulation—for evaluating robot manipulation capabilities, testing both precise manipulation skills and the ability to handle sequential operations and pose uncertainty.
