# Benchmarking Robot Manipulation with the Rubik's Cube

[arXiv](https://arxiv.org/abs/2202.07074)

## 摘要（原文）

> Benchmarks for robot manipulation are crucial to measuring progress in the field, yet there are few benchmarks that demonstrate critical manipulation skills, possess standardized metrics, and can be attempted by a wide array of robot platforms. To address a lack of such benchmarks, we propose Rubik's cube manipulation as a benchmark to measure simultaneous performance of precise manipulation and sequential manipulation. The sub-structure of the Rubik's cube demands precise positioning of the robot's end effectors, while its highly reconfigurable nature enables tasks that require the robot to manage pose uncertainty throughout long sequences of actions. We present a protocol for quantitatively measuring both the accuracy and speed of Rubik's cube manipulation. This protocol can be attempted by any general-purpose manipulator, and only requires a standard 3x3 Rubik's cube and a flat surface upon which the Rubik's cube initially rests (e.g. a table). We demonstrate this protocol for two distinct baseline approaches on a PR2 robot. The first baseline provides a fundamental approach for pose-based Rubik's cube manipulation. The second baseline demonstrates the benchmark's ability to quantify improved performance by the system, particularly that resulting from the integration of pre-touch sensing. To demonstrate the benchmark's applicability to other robot platforms and algorithmic approaches, we present the functional blocks required to enable the HERB robot to manipulate the Rubik's cube via push-grasping.

## 摘要（中译）

机器人操作基准测试对于衡量该领域的进展至关重要，但很少有基准测试能够展示关键的操纵技能、拥有标准化的指标，并且可以被广泛的机器人平台尝试。为了解决这类基准测试的缺乏问题，我们提出将魔方操作作为一个基准，用以衡量精确操作和顺序操作的同步性能。魔方的子结构要求机器人的末端执行器进行精确定位，而其高度可重构的特性使得需要机器人在长序列动作中管理姿态不确定性的任务成为可能。我们提出了一个协议，用于定量测量魔方操作的准确性和速度。任何通用操纵器都可以尝试这个协议，只需要一个标准的3x3魔方和一个魔方最初放置的平面（例如，桌子）。我们在PR2机器人上展示了这个协议的两个不同基线方法。第一个基线提供了一种基于姿态的魔方操作的基本方法。第二个基线展示了基准测试量化系统改进性能的能力，特别是那些通过集成接触前感知而产生的改进。为了展示基准测试对其他机器人平台和算法方法的适用性，我们展示了使HERB机器人能够通过推抓方式操纵魔方所需的功能模块。

## 背景剖析

### 背景剖析  

#### 1. 技术背景与真实需求  
机器人操作（如抓取、旋转、组装物体）是人工智能和自动化领域的核心技术，广泛应用于工业制造、家庭服务、医疗辅助等场景。例如，工厂需要机器人精确装配零件，家庭机器人需灵活操作日常物品（如拧瓶盖、整理桌面）。这类技术的核心挑战在于：机器人不仅要“感知”环境，还要“交互”并完成任务，而现有基准测试（如物体识别或简单抓取任务）无法全面衡量这种复杂能力。  

#### 2. 之前的问题与不足  
尽管研究者认同量化评估的重要性，但现有的机器人操作基准存在两大缺陷：  
- **单一性**：多数基准（如“搬箱子”或“放杯子”）仅测试单一技能（如精确定位或短序列操作），无法同时评估“高精度”和“长序列操作”的结合能力。例如，魔方还原需要机器人反复精确定位并调整多个部件，过程中还需处理累积误差。  
- **通用性差**：现有基准要么依赖特定硬件（如复杂机械臂），要么任务设计过于简单，无法适应不同类型的机器人平台。  

#### 3. 本文的解决方案  
论文提出以“魔方操作”作为新基准，通过以下方式解决问题：  
- **双重要求**：魔方的结构要求机器人同时具备“精确定位”（每个小方块仅1.9厘米宽）和“长序列操作”（还原需20步以上）的能力。  
- **标准化协议**：设计了一套测量准确性和速度的协议，仅需标准3×3魔方和平面表面，适用于各种通用机器人（如PR2或HERB）。  
- **开放性**：提供开源软件和两种基线方法（如基于姿态的操控和触觉感知优化），方便研究者对比算法改进。  

#### 4. 与前人工作的关键差异  
与现有基准相比，本文的切入点在于：  
- **任务复杂性**：魔方操作同时考验精度和序列操作，而非单一技能。  
- **通用性**：只需基本设备和通用机器人，降低了参与门槛。  
- **可扩展性**：通过误差累积和反馈机制，直接关联到规划、感知和控制等子领域的进步。  

这一基准不仅为研究者提供了量化工具，还通过魔方这一大众熟悉的挑战，让公众直观理解机器人技术的复杂性。

## 方法图解

![Figure 3 : HERB’s simulated Barrett hands manipulate the Rubik’s cube in blue. L](fig3_1.webp)

> Figure 3 : HERB’s simulated Barrett hands manipulate the Rubik’s cube in blue. Left: The right gripper uses a push-grasp to make contact with the Rubik’s cube. Upon making contact, the right gripper reaches the desired pre-grasp. Right: The right gripper closes its outer fingers to transition from pre-grasp to grasp.

这张图（图3）来自论文《Benchmarking Robot Manipulation with the Rubik's Cube》，展示了HERB机器人的模拟Barrett手在操作蓝色魔方时的两个关键步骤。这张图的核心目的是可视化一种特定的抓取策略，即“推-抓取”（push-grasp）方法。

首先，我们来看左侧的图像：
- **主体**：图中显示了HERB机器人的两只手臂，每只手臂末端都装有模拟的Barrett手。右侧的手臂（我们称之为“右 gripper”）是当前操作的对象。
- **魔方**：一个蓝色的魔方位于场景的左侧，是操作的目标。
- **动作描述（左图）**：右 gripper 正在执行一个“推-抓取”动作。具体来说，它的“外手指”（outer fingers）已经接触到魔方的一个面，这个接触点是为了建立一个“预抓取”（pre-grasp）位置。在这个阶段，手指可能还没有完全闭合，而是处于一个准备姿态，通过推动魔方来调整其位置或姿态，以便更好地进行后续的抓取。图中可以看到，魔方被轻微地向右推，而右 gripper 的手指已经接触到魔方的表面，形成了一个初步的接触点。

接下来，我们看右侧的图像：
- **主体**：与左图相同，仍然是HERB机器人的两只手臂和蓝色魔方。
- **动作描述（右图）**：右 gripper 已经从“预抓取”状态过渡到“抓取”（grasp）状态。可以看到，右 gripper 的“外手指”已经完全闭合，紧紧地抓住了魔方。这个动作表明，机器人已经成功地完成了推-抓取过程，现在魔方被牢固地握在手中。魔方的位置相对于左图有所变化，这可能是由于抓取动作导致的。

这张图揭示了HERB机器人如何使用其模拟的Barrett手执行“推-抓取”操作的具体步骤：
1. **预抓取阶段**：右 gripper 使用其外手指接触魔方，通过推动魔方来调整其位置或姿态，达到一个理想的预抓取位置。这个阶段的目的是为后续的抓取动作做好准备。
2. **抓取阶段**：一旦预抓取位置确定，右 gripper 的外手指会闭合，将魔方牢牢地抓住。这个阶段的目的是确保魔方被稳定地握在手中，以便进行下一步的操作。

通过这两个图像的对比，我们可以清楚地看到“推-抓取”方法的执行过程。这种方法可能用于处理那些难以直接抓取的物体，通过推动物体来调整其位置，从而更容易地进行抓取。图中展示的这个过程是HERB机器人在模拟环境中操作魔方的一个具体示例，展示了其在精确操作和序列操作方面的能力。

总结来说，这张图通过两个连续的动作展示了HERB机器人的模拟Barrett手如何使用“推-抓取”方法来操作蓝色魔方。左图显示了预抓取阶段，右图显示了抓取阶段，清晰地展示了这一操作的具体步骤和过程。

---

![Figure 2 : The robot must precisely position its grippers to rotate the left col](fig2_1.webp)

> Figure 2 : The robot must precisely position its grippers to rotate the left column of the Rubik’s cube while constraining the middle and right columns in place. Top Row: The robot correctly positions its grippers: it is constraining the two right columns of the cube. The yellow box highlights the position of the constraining gripper. Middle Row: The robot only touches one column of the Rubik’s cube and therefore fails to constrain its middle column. Bottom Row: The right gripper is touching all three columns of the cube; this prevents the left gripper from rotating the left column of the cube.

这张图（图2）来自论文《Benchmarking Robot Manipulation with the Rubik's Cube》，它清晰地展示了机器人在操作魔方时，如何通过精确调整其末端执行器（即夹爪）的位置来实现特定的目标——旋转魔方的左列，同时固定中间和右列。整个图像分为三个水平排列的行，每行代表一种不同的约束状态，并通过从左到右的箭头序列展示操作过程。

1.  **第一行（顶部，蓝色背景标题：“Rubik's Cube Correctly Constrained” - 魔方被正确约束）**：
    *   **左侧图像**：展示了机器人夹爪正确抓取魔方的初始状态。黄色方框突出显示了用于“约束”的夹爪（通常是右侧的夹爪）。这个夹爪的位置确保了魔方的中间列和右列被牢固地固定住，防止它们在后续操作中移动。另一个夹爪（左侧）则准备操作左列。
    *   **中间图像**：显示了机器人开始执行旋转左列的动作。可以看到左列的魔方块相对于中间和右列发生了旋转（例如，绿色面块从右侧露出）。
    *   **右侧图像**：展示了旋转动作完成后的状态。左列已经成功旋转，而中间和右列仍然保持稳定，没有发生不必要的移动。箭头指示了操作的顺序：从正确约束状态 -> 执行旋转 -> 完成旋转。

2.  **第二行（中间，橙色背景标题：“Rubik's Cube Under Constrained” - 魔方约束不足）**：
    *   **左侧图像**：展示了机器人夹爪约束不足的情况。黄色方框内的夹爪位置不正确，只接触到了魔方的一列（可能是中间列或右列的一部分），而没有有效地固定住中间列。
    *   **中间图像**：当机器人尝试旋转左列时，由于中间列没有被充分约束，它在旋转过程中也发生了移动（可以看到绿色面块的移动范围更大，或者中间列的块也跟着转动）。
    *   **右侧图像**：显示了旋转动作完成后的状态。左列虽然旋转了，但中间列也受到了影响，导致魔方的整体结构没有按照预期保持稳定。这表明约束不足会导致操作不精确。箭头同样指示了操作的顺序：从约束不足状态 -> 尝试旋转 -> 旋转后中间列也移动了。

3.  **第三行（底部，绿色背景标题：“Rubik's Cube Over Constrained” - 魔方过度约束）**：
    *   **左侧图像**：展示了机器人夹爪过度约束的情况。黄色方框内的夹爪位置导致它接触到了魔方的所有三列（左、中、右）。
    *   **中间图像**：当机器人尝试旋转左列时，由于右夹爪过度约束，阻止了左列的顺利旋转。可以看到左列的旋转受到阻碍，或者根本没有成功旋转。
    *   **右侧图像**：显示了尝试旋转后的状态。左列几乎没有旋转，因为过度约束导致机械干涉。箭头指示了操作的顺序：从过度约束状态 -> 尝试旋转 -> 旋转失败或受限。

**方法运作原理**：
这张图揭示了机器人操作魔方的核心挑战之一：精确控制约束。为了旋转魔方的一个特定部分（例如左列），机器人必须：
*   **正确约束**：用一个夹爪牢固地固定住不需要移动的部分（中间和右列）。这样，当另一个夹爪（或同一夹爪的不同部分）施力旋转目标部分时，整个魔方不会因为其他部分的移动而产生误差。
*   **避免约束不足**：如果约束不够，未固定的部分会在旋转过程中移动，导致操作不精确，可能打乱已经排列好的其他块。
*   **避免过度约束**：如果约束过多，试图旋转的部分会被其他被固定的部分卡住，无法顺利进行旋转。

图中的箭头表示了操作的顺序：首先是夹爪的初始位置（正确、不足或过度约束），然后是尝试旋转的动作，最后是旋转后的结果状态。通过对比这三行，我们可以清楚地看到正确约束对于实现精确、可控的魔方操作至关重要。

**结论**：
这张图通过视觉化的方式，有效地展示了在机器人操作魔方任务中，约束的精确性对操作成功与否的影响。它说明了为了实现复杂的操纵任务，机器人不仅需要精确的定位能力，还需要理解如何正确地与环境（这里是魔方）交互，以避免不必要的移动或阻碍。

---

![Figure 1 : Rubik’s cube manipulation can be used to benchmark robot manipulation](fig1_1.webp)

> Figure 1 : Rubik’s cube manipulation can be used to benchmark robot manipulation across a wide array of algorithmic approaches and robot platforms, such as the PR2 and HERB.

这张图是论文《Benchmarking Robot Manipulation with the Rubik's Cube》中的Figure 1，它直观地展示了该研究的核心思想：使用魔方操作作为基准来评估不同机器人平台和算法在机器人操作任务中的表现。

这张图由两个主要部分组成，分别位于图像的左侧和右侧，通过并列展示的方式，对比了两种不同的机器人平台执行魔方操作的场景。

**左侧部分：**
*   **组件/场景**：这部分展示了一个真实的机器人——PR2机器人。PR2是一个著名的移动操作机器人，具有两个机械臂和一个位于顶部的传感器头部。
*   **动作**：PR2机器人的一个机械臂（看起来是右臂）正用其末端执行器（夹爪）夹持着一个标准的3x3魔方。魔方的颜色清晰可见，表明它处于一个特定的初始或中间状态。机器人的姿态稳定，似乎正在进行或准备进行魔方操作。
*   **环境**：背景是一个简单的白色幕布，地面是深色的，可能是实验室环境。这种设置通常用于精确控制和记录机器人的操作。
*   **信息传达**：这部分代表了在实际物理环境中对魔方操作任务的实现。它展示了研究的实际应用场景，即机器人如何在真实世界中与魔方互动。这对应了论文中提到的“protocol for quantitatively measuring both the accuracy and speed of Rubik's cube manipulation”的实际执行。

**右侧部分：**
*   **组件/场景**：这部分展示了一个模拟环境中的机器人——HERB机器人。HERB是另一个具有双臂的移动操作机器人，但这里的表示是三维模型，通常用于仿真研究。
*   **动作**：HERB机器人的一个机械臂（看起来也是右臂）正伸向一个物体，这个物体被高亮显示为蓝色。虽然这个物体看起来不像一个完整的魔方，但它可能代表了魔方操作任务中的一个特定元素或状态，或者是仿真环境中魔方的一个简化表示。这表明HERB机器人正在执行或准备执行与魔方相关的操作。
*   **环境**：背景是一个典型的三维仿真环境，有网格地板和简单的几何体（如红色的箱子）作为障碍物或背景元素。这种环境允许研究人员在不涉及实际硬件的情况下测试和开发算法。
*   **信息传达**：这部分代表了在仿真环境中对魔方操作任务的实现。它展示了研究的另一种方式，即如何利用仿真来开发、测试和改进机器人操作算法。这与左侧的真实机器人实验形成对比，说明该基准测试可以应用于不同的实验平台。

**整体理解与方法流程：**
这张图揭示了该研究方法的核心：提出一个通用的基准测试（魔方操作），该测试可以在不同的机器人平台（如PR2和HERB）上执行。
*   **目标**：评估机器人在精确操作（如定位魔方的特定部分）和顺序操作（如执行一系列动作来解决魔方）方面的能力。
*   **方法**：
    1.  **定义基准任务**：使用魔方作为任务对象，因为它既需要精确的位置控制，又涉及到处理姿势不确定性（由于魔方可以多种配置出现）。
    2.  **平台适用性**：该基准测试设计得足够通用，以便任何通用操作器都可以尝试。只需要一个标准的3x3魔方和一个平坦的表面（如桌子）。
    3.  **实验设置**：
        *   在真实的PR2机器人上进行实验，如图左侧所示，以测量实际的准确性和速度。
        *   在仿真的HERB机器人上进行实验，如图右侧所示，以开发和测试算法，并可能评估不同方法（如预触觉感知）的性能提升。
*   **数据/信息流动**：虽然图中没有明确的数据流箭头，但可以推断出方法的流程是：
    *   **输入**：一个标准的3x3魔方，放置在一个平坦的表面上。
    *   **处理**：机器人（无论是真实的还是仿真的）使用其算法和传感器来感知魔方的状态，规划并执行一系列操作来解决魔方。
    *   **输出**：解决魔方的结果（例如，魔方是否被正确还原）以及完成任务所花费的时间。这些数据用于评估机器人的性能。
*   **结论暗示**：通过展示两种不同类型的机器人（一个真实，一个仿真）都能执行这个基准测试，图片暗示了该基准测试的广泛适用性和重要性。它表明该基准可以用来比较不同的算法、传感器技术或机器人平台在解决复杂操作任务方面的能力。

总而言之，这张图通过展示PR2和HERB两种机器人在不同环境（真实世界和仿真）下操作魔方的场景，有效地传达了论文的核心贡献：提出了一个用于评估机器人操作能力的通用基准——魔方操作。这个基准既考验了机器人的精确操作技能，也考验了其处理序列操作和姿势不确定性的能力。
