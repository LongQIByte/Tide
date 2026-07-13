# Video-Oasis: Rethinking Evaluation of Video Understanding

[arXiv](https://arxiv.org/abs/2603.29616) · [HuggingFace](https://huggingface.co/papers/2603.29616) · ▲58

## 摘要（原文）

> The inherent complexity of video understanding makes it difficult to determine whether Video-LLM benchmark performance stems from visual perception, linguistic reasoning, or knowledge priors. While many benchmarks have emerged to assess high-level reasoning, shared criteria for evaluating video understanding remain largely overlooked. Instead of introducing yet another benchmark, we take a step back to re-examine the criteria for evaluating video understanding. In this work, we introduce Video-Oasis, a sustainable diagnostic suite for systematically auditing existing video understanding benchmarks. This audit reveals that 55\% of existing benchmark samples are solvable without visual input or temporal context. After filtering these shortcuts, the remaining video-native challenges expose a substantial capability gap: state-of-the-art models perform only marginally above random guessing. Building on these findings, we use the distilled challenges as a testbed to investigate which algorithmic design choices contribute to robust video understanding. We hope our work provides a practical foundation for constructing rigorous video benchmarks and evaluating future Video-LLMs. Code is available at https://github.com/sejong-rcv/Video-Oasis.

## 摘要（中译）

视频理解的内在复杂性使得难以确定Video - LLM基准性能是源于视觉感知、语言推理还是知识先验（knowledge priors）。虽然已经出现了许多用于评估高层次推理的基准，但评估视频理解的共享标准在很大程度上被忽视了。我们没有引入另一个基准，而是退后一步重新审视评估视频理解的标准。在这项工作中，我们引入了Video - Oasis，这是一个用于系统审计现有视频理解基准的可持续诊断套件。这次审计揭示了现有基准样本中有55%在没有视觉输入或时间上下文的情况下是可以解决的。在过滤掉这些捷径之后，剩余的视频原生挑战暴露出一个巨大的能力差距：最先进的模型表现仅略高于随机猜测。基于这些发现，我们使用提炼出的挑战作为测试平台，以研究哪些算法设计选择有助于实现鲁棒的视频理解。我们希望我们的工作为构建严格的视频基准和评估未来的视频大语言模型（Video - LLMs）提供一个实用的基础。代码可在https://github.com/sejong - rcv/Video - Oasis获取。

## 背景剖析

### 背景剖析  

**1. 技术背景**  
随着多模态大模型的发展，视频理解技术已从单一任务（如动作识别）转向更复杂的感知与推理结合场景。这类技术的核心需求是让AI模型能够像人类一样“看懂”视频——不仅要识别画面中的物体或动作，还要理解事件的时间顺序、因果关系，甚至回答涉及逻辑推理的问题（例如“为什么这个人会摔倒？”）。典型应用包括智能监控、视频问答、自动驾驶中的环境感知等。然而，当前基准测试（benchmark）往往无法准确评估模型是否真正掌握了视频理解的核心能力，导致性能提升可能来自视觉感知、语言推理或背景知识，而非真正的视频理解。  

**2. 之前的问题**  
早期基准测试（如动作识别）聚焦于特定领域，但视频大模型（Video-LLMs）需要处理更复杂的动态和长时推理任务。现有测试的一个关键缺陷是：许多任务可以通过“捷径”完成，例如仅依赖文本描述或静态图像，而无需分析视频的时空依赖关系。这导致基准测试无法区分模型是否真正理解了视频内容。例如，一个模型可能在“描述视频内容”任务中表现优异，但实际上只是通过文本信息猜测答案，而非观察画面。这种评估偏差使得研究人员难以判断模型的真实能力，也阻碍了视频理解技术的发展。  

**3. 本文的解法**  
本文提出了一种名为Video-Oasis的诊断框架，旨在系统性地审计现有视频理解基准测试。其核心思路是：通过屏蔽视觉或时间信息，测试任务是否真的需要视频特有的时空推理能力。例如，如果一个任务在仅提供文本描述时就能被解决，那么它可能是一个“捷径”，而非真正的视频理解任务。通过这种方法，Video-Oasis发现现有基准测试中约55%的任务可以通过非视频输入完成，而剩余的“纯视频挑战”则暴露出模型的能力差距——即使是顶尖模型，其表现也仅略高于随机猜测。  

**4. 切入角度**  
与以往工作不同，Video-Oasis并未引入新的基准测试，而是重新审视了视频理解的本质标准。它通过三个关键设计解决了前人的不足：（1）通过视觉-时间解耦测试，过滤掉依赖捷径的任务；（2）通过跨模型共识机制减少偏见和不确定性；（3）通过人工验证解决视频问答中的歧义。这种方法使得评估更加严格和可靠，为未来视频基准测试的设计提供了实用指南。

## 方法图解

![Figure 2 : Overview of the V-Oasis diagnostic suite, which assesses (a) whether ](fig2_1.webp)

> Figure 2 : Overview of the V-Oasis diagnostic suite, which assesses (a) whether visual information is required, (b) whether temporal context is necessary, and (c) whether the task contains ambiguity in video data, followed by human verification.

这张图（图2）展示了Video-Oasis诊断工具套件的概述，它主要用于评估视频理解任务中的三个关键方面：视觉依赖性、时间依赖性和歧义检查。

首先看(a)部分，标题为“Visual Dependency”（视觉依赖性）。这个部分的目的是判断一个视频理解任务是否真的需要视觉信息。
1.  数据输入：从左到右，首先是“Query Prompt (Task)”（查询提示或任务描述），接着是“Blind Video”（盲视频）。这里的“盲视频”可能指的是没有提供视觉内容的视频，或者是一个用于测试模型是否依赖视觉输入的视频。
2.  处理流程：
    *   “Blind Visual”模块接收“Blind Video”，并将其分解或处理成不同的形式，如图中所示的“Blind”（原始盲视频）、“Audio”（音频）和“Summary”（摘要）。这表明该模块可能在尝试从非视觉信息（如音频或文本摘要）中提取线索。
    *   接下来，有三个模型（Model 1, Model 2, Model 3），每个模型都接收这些处理后的信息（例如，Model 1可能主要看“Blind”部分，Model 2看“Audio”，Model 3看“Summary”，或者它们以某种方式结合这些信息）。每个模型都有一个输出（用圆圈内的符号表示）。
    *   最后，这些模型的输出被汇总到一个“Agreement”（一致性）模块，该模块判断这些模型是否在没有视觉输入的情况下达成一致的结果。如果达成一致，则会得出一个“Visual Shortcut”（视觉捷径）的结论，意味着任务可能不需要真正的视觉理解，模型可以通过其他方式（如音频或文本）解决。

然后是(b)部分，标题为“Temporal Dependency”（时间依赖性）。这个部分评估任务是否需要时间上下文。
1.  数据输入：同样从“Query Prompt (Task)”开始，然后是“Frame Sampling”（帧采样），这意味着从视频中抽取一些关键帧。
2.  处理流程：
    *   “Blind Temporal”模块接收这些采样的帧，并对它们进行处理。图中显示了三种处理方式：“Center”（中心帧）、“Shuffling”（打乱帧的顺序）和“Bag of Frame”（将帧视为一个集合，不考虑顺序）。这表明该模块在测试模型对时间顺序的敏感性。
    *   接下来，同样的三个模型（Model 1, Model 2, Model 3）接收这些处理后的帧信息。每个模型都有一个输出。
    *   模型的输出再次被汇总到“Agreement”模块。如果模型在没有正确时间顺序的情况下达成一致，则会得出一个“Temporal Shortcut”（时间捷径）的结论，意味着任务可能不需要真正的时间理解，模型可以通过其他方式（如单帧内容）解决。

最后是(c)部分，标题为“Ambiguity Check”（歧义检查）。这个部分检查视频数据中的任务是否包含歧义。
1.  数据输入：从“Query Prompt (Task)”开始，然后是“Frame Sampling”。
2.  处理流程：
    *   “Find Error Case”模块接收采样的帧，并从三个方面进行检查：“Consistency”（一致性）、“Redundancy”（冗余性）和“Sensitivity”（敏感性）。图中显示了“All Correct”（全部正确）的情况，以及一些可能存在的错误情况（用红色叉号标记）。
    *   然后，有三个人类评估者（Human 1, Human 2, Human 3）对这些帧进行检查，他们可能会有不同的判断（用不同颜色的图标表示）。
    *   最后，这些人类评估者的判断被汇总到“Agreement”模块，以确定任务是否存在歧义。如果存在歧义，则会进行进一步的“Ambiguity Check”（歧义检查）。

总的来说，这张图展示了Video-Oasis如何通过三个步骤来诊断视频理解任务：首先检查是否需要视觉信息，然后检查是否需要时间上下文，最后检查任务是否包含歧义。每个步骤都涉及模型和/或人类的评估，并通过“Agreement”模块来判断是否存在某种“捷径”或歧义。这个过程有助于揭示现有视频理解基准测试中可能存在的问题，并为构建更严格的视频基准测试提供基础。

---

![Table 7 : Benchmarking state-of-the-art models under video-native challenges. Th](fig5_1.webp)

> Table 7 : Benchmarking state-of-the-art models under video-native challenges. The metric is accuracy. Table 8: Ablation study of temporal grounding in video-LLMs. The metric is accuracy. Table 9: Upper bound performance (%) with oracle temporal grounding. Table 10: Ablation study of reasoning depth modulation. The metric is accuracy. Table 11: Comparison of SFT and RLVR training paradigms for video understanding. All models share the same base LLM, Qwen2.5-VL [ 2 ] . The metric is accuracy. (a) Blind Test (b) Audio (c) Narrative (d) Center-Frame (e) Frame Shuffling (f) Bag-of-Frames Table S1 : Quantitative results of Video-Oasis under different diagnostic model configurations to evaluate robustness. The metric is accuracy. Table S2: Per-benchmark statistics before and after Video-Oasis filtering. Table S3: Benchmark-wise results (%) for the Blind Test, where the model answers without visual input or auxiliary context, relying only on linguistic priors. Table S4: Benchmark-wise results (%) for the Audio Test, where the model answers using only the speech transcript from the video’s audio. Table S5: Benchmark-wise results (%) for the Narrative Test, where the model answers using concatenated video captions as textual context. Table S6: Benchmark-wise results (%) for the Center-Frame Test, where the model answers using only the center frame of the video. Table S7: Benchmark-wise results (%) for the Frame Shuffling Test, where the temporal order of video frames is randomly permuted. Table S8: Benchmark-wise results (%) for the Bag-of-Frames Test, where frames are processed independently without modeling temporal relations. Table S9: Prompt template used in the visual dependency tests with different context. Algorithm 1 Temporal Dependency Diagnostic Procedure Table S10: Statistics of the identified video-native challenges: (a) category distribution and (b) video duration statistics. Table S11: Multiple-Choice Answer distribution across categories. Table S12 : Per-benchmark distribution of samples across video-native challenges. Figure S1: Qualitative examples of Fine-Grained Perception Challenges. Figure S2: Qualitative examples of Spatial World Understanding Challenges. Figure S3: Qualitative examples of Temporal Dynamics & Tracking Challenges. Figure S4: Qualitative examples of Causality & Logical Reasoning Challenges. Figure S5: Qualitative examples of Global Narrative Challenges. Figure S6: Qualitative examples of shortcut problems identified by Video-Oasis. Table S13: Reproduction results on LongVideoBench and VideoMME. For each comparison, higher scores are highlighted in bold , while lower scores are underlined .

这张图来自论文《Video-Oasis: Rethinking Evaluation of Video Understanding》，展示了两个**定性示例**，用于说明“视频原生挑战”（Video-Native Challenges）的概念。这些示例旨在揭示，要解决视频中的问题，模型需要具备哪些特定的视觉感知和时空推理能力，而这些能力是简单的基于文本的推理或知识先验无法解决的。

我们来分别解析这两个示例：

**第一个示例（上半部分）：**
*   **问题与答案：** 问题是“客厅里有多少个沙发？”（How many sofas are in the living room?），答案是“3”。这表明任务是**沙发计数**（Sofa Counting），属于对特定物体的属性识别。
*   **视频帧序列：** 上方展示了一系列视频帧，捕捉了一个动态场景。这些帧共同构成了问题的视觉上下文。
*   **标注与流程：**
    *   关键的视觉元素（沙发）被绿色方框突出显示。这些方框出现在不同的帧中，表明沙发在视频的不同时间点出现。
    *   红色方框圈出了一个更广泛的区域，可能代表“客厅”这个空间背景。
    *   下方的文字“Why Video Native Challenges?”（为什么是视频原生挑战？）引出了一个流程：从“客厅识别”（Living Room Recognition）到“沙发计数”（Sofa Counting）。
    *   “客厅识别”旁边标注了“(Spatial Temporal Grounding)”（时空定位），意味着模型首先需要在时空上确定哪个区域是“客厅”。
    *   “沙发计数”旁边标注了“(Attribute and Object)”（属性和物体），意味着在确定了客厅之后，模型需要在该区域内识别并计数“沙发”这个物体。
*   **信息流动与方法揭示：** 这个示例展示了方法的运作方式：要解决“数沙发”的问题，模型不能仅仅依赖于单帧图像或文本描述。它需要：
    1.  **时空理解：** 跟踪视频中的空间区域（客厅）。
    2.  **目标识别与计数：** 在该空间区域内识别并统计特定物体（沙发）的数量。
    这个过程需要模型具备处理视频的固有能力，而不是简单地记忆或推理。

**第二个示例（下半部分）：**
*   **问题与答案：** 问题是“背景中除了白色之外，还能观察到哪些颜色？”（What are the colors other than white that are observable in the background?），答案是“黑色、绿色、灰色、蓝色”（black, green, grey, blue）。这表明任务是**背景颜色识别**（Different Color Recognition），属于对背景属性的感知。
*   **视频帧序列：** 同样展示了一系列视频帧，构成了问题的视觉上下文。
*   **标注与流程：**
    *   关键的视觉元素（背景中的颜色区域）被绿色方框突出显示。这些方框出现在不同的帧中，表明背景颜色可能在视频的不同时间点有所变化或需要跨帧观察。
    *   下方的文字“Why Video Native Challenges?”（为什么是视频原生挑战？）引出了另一个流程：从“背景跟踪”（Background Tracking）到“不同颜色识别”（Different Color Recognition）。
    *   “背景跟踪”旁边标注了“(Spatial Temporal Grounding)”（时空定位），意味着模型首先需要在时空上跟踪和理解“背景”这个区域。
    *   “不同颜色识别”旁边标注了“(Attribute and Object)”（属性和物体），意味着在跟踪了背景之后，模型需要识别并区分背景中的不同颜色属性。
*   **信息流动与方法揭示：** 这个示例同样展示了方法的运作方式：要解决“识别背景颜色”的问题，模型需要：
    1.  **时空理解：** 跟踪视频中的背景区域。
    2.  **属性识别：** 在该背景区域内识别并区分不同的颜色。
    这再次强调了视频理解任务对时空感知和特定视觉属性识别的依赖。

**总结：**
这张图通过两个具体的例子，清晰地说明了“视频原生挑战”的核心思想。它表明，解决这些问题需要模型具备：
*   **时空定位能力：** 能够在时间和空间上识别和跟踪相关的区域或对象（如“客厅”或“背景”）。
*   **特定视觉属性识别能力：** 能够识别和计数特定的物体（如“沙发”）或区分特定的属性（如“颜色”）。
这些挑战是视频理解任务特有的，不能仅通过文本理解或静态图像分析来解决。图中的流程箭头（如“客厅识别” -> “沙发计数”）清晰地展示了从高层次的空间理解到具体的目标识别和属性分析的信息处理顺序。通过这些示例，读者可以直观地理解论文中所指的“视频原生挑战”是什么，以及模型需要如何运作才能应对这些挑战。

---

![Figure 4 : Video-native challenges such as temporal continuity, causal interacti](fig4_1.webp)

> Figure 4 : Video-native challenges such as temporal continuity, causal interaction, and multi-event narratives distilled from existing benchmarks.

这张图来自论文《Video-Oasis: Rethinking Evaluation of Video Understanding》，它清晰地展示了现有视频理解基准测试（Previous Benchmarks）中存在的问题，以及由此提炼出的视频原生挑战（Video-Native Challenges）。

首先，我们看左侧的“Previous Benchmarks”部分。这里列出了几种不同类型的视频理解任务，并用绿色的对勾（✔️）和红色的叉号（❌）来标记这些任务是否容易被“捷径”（Identified Shortcut）解决。绿色对勾表示该任务主要依赖于视觉感知或时间上下文等视频固有信息，而红色叉号则表示该任务可以通过语言推理或静态上下文等非视频原生信息来解决，即存在捷径。

具体来看：
- “Spatial World Understanding”（空间世界理解）任务，例如“镜子相对于叉子玩具在哪里？”，答案是“在它前面”。这个任务被标记为绿色对勾，说明它需要真正的视频理解能力。
- “Linguistic Reasoning”（语言推理）任务，例如一个关于股票价格的数学问题，答案是“每股4.5美元”。这个任务被标记为红色叉号，说明它可以通过语言理解直接解决，而不需要观看视频。
- “Auditory Reasoning”（听觉推理）任务，例如“视频如何组织切·格瓦拉的故事？”，答案是“通过进行审判来评估他的优点和缺点”。这个任务也被标记为红色叉号，说明它可能依赖于文本描述而非视频内容。
- “Temporal Tracking”（时间跟踪）任务，例如“在‘Volcano Eco Retreat’出现之前，视频中显示了多少个不同的酒店位置？”，答案是“3”。这个任务被标记为绿色对勾，说明它需要时间上下文。
- “Static Context”（静态上下文）任务，例如“当前的天气怎么样？”，答案是“晴朗”。这个任务被标记为红色叉号，说明它可能只需要一张静态图片就能解决。
- “Logical Reasoning”（逻辑推理）任务，例如“猴子对鸽子的态度是什么？”，答案是“想赶走鸽子”。这个任务被标记为绿色对勾，说明它需要真正的视频理解能力。

接下来，我们看中间的“Video-Oasis”部分。这个部分代表了论文提出的方法，即通过系统地审计现有视频理解基准测试，来揭示哪些任务是真正考验视频理解能力的，哪些任务存在捷径。这个过程就像一个过滤器，将现有基准测试中的任务分为两类：可以通过捷径解决的任务和真正的视频原生挑战。

然后，我们看右侧的“Video-Native Challenges”部分。这部分展示了从现有基准测试中提炼出的视频原生挑战，包括：
- “Fine-Grained Perception”（细粒度感知）：例如“视频中第四只猫尖叫的原因是什么？”，答案是“在镜子里看到了自己”。这个任务需要细粒度的视觉感知。
- “Spatial World Understanding”（空间世界理解）：例如“楼梯相对于壁炉在哪里？”，答案是“在它前面”。这个任务需要理解空间关系。
- “Temporal Dynamics & Tracking”（时间动态与跟踪）：例如“视频中显示的动作序列是什么？”，答案是“拿起罐子，打开罐盖，放下罐盖，倒出罐子里的东西，放下罐子”。这个任务需要理解时间顺序。
- “Causality & Logical Reasoning”（因果关系与逻辑推理）：例如“雪豹是如何出现在其他动物后面的？”，答案是“利用桥上的绳子作为秋千跳过峡谷”。这个任务需要理解因果关系。
- “Global Narrative”（全局叙事）：例如“请用两个形容词描述这个女孩”，答案是“勇敢和自由”。这个任务需要理解整个视频的叙事。

这张图的结论是：现有基准测试中有55%的任务可以通过捷径解决，而不需要真正的视频理解能力。在过滤掉这些捷径之后，剩下的视频原生挑战暴露出一个巨大的能力差距：最先进的模型在这些任务上的表现仅略高于随机猜测。这表明现有的视频理解基准测试并不能有效地评估模型的视频理解能力，需要新的方法来构建更严格的基准测试。

---

![Figure 1 : (a) Examples of video-QA instances that can be solved without spatio-](fig1_1.webp)

> Figure 1 : (a) Examples of video-QA instances that can be solved without spatio-temporal video understanding. (b) Benchmarks with higher ratios of video-independent samples tend to exhibit inflated video-QA scores.(c) Current SOTA models consistently exhibit a substantial drop when facing video-native challenges, revealing the inherent difficulty of robust spatio-temporal understanding.

这张图（图1）来自论文《Video-Oasis: Rethinking Evaluation of Video Understanding》，旨在揭示当前视频理解基准测试中存在的问题，并为后续研究提供诊断依据。我们可以将这张图分为三个主要部分来详细讲解：

**第一部分：(a) Misalignment with Video-Native Criteria（与视频原生标准的错位）**

这部分通过四个具体的“视频问答（video-QA）”实例，展示了哪些问题可以在**不需要**时空视频理解的情况下被解决。每个实例都包含一个问题、几个选项以及一个高亮显示的正确答案，并标注了该问题所依赖的能力类型。

1.  **第一个实例（左一）：**
    *   **问题：** “Which of these objects is the closest to the keyboard?”（哪个物体离键盘最近？）
    *   **选项：** A. bowl（碗），B. ceiling light（天花板灯），C. cutting board（砧板），D. computer mouse（电脑鼠标）。
    *   **正确答案：** D. computer mouse（高亮显示）。
    *   **能力类型：** Common Sense Prior（常识先验）。这意味着解决这个问题主要依赖于常识，而不是对视频内容的视觉感知或时间理解。即使没有看到视频，根据常识也能推断出鼠标通常离键盘很近。

2.  **第二个实例（左二）：**
    *   **问题：** “Which year marked the debut of the typewriter?”（哪一年是打字机首次亮相的年份？）
    *   **选项：** A. 1961，B. 1971，C. 1981，D. 1986。
    *   **正确答案：** B. 1971（高亮显示）。
    *   **能力类型：** Document Understanding（文档理解）。图中有一个小插图，显示了一段文字提到“Selelectric II which was first released in 1971”。解决这个问题需要从文档（或类似文本信息）中提取信息，而不是分析视频的视觉或时间动态。

3.  **第三个实例（右二）：**
    *   **问题：** “What color is the stationary cube?”（静止的立方体是什么颜色？）
    *   **选项：** A. brown（棕色），B. green（绿色），C. red（红色），D. cyan（青色）。
    *   **正确答案：** D. cyan（高亮显示）。
    *   **能力类型：** Single Frame Understanding（单帧理解）。图中显示了一个包含几个物体的静态图像，其中一个立方体被红色方框标出。解决这个问题只需要观察单个图像（或视频中的某一帧），而不需要理解视频的时间序列变化。

4.  **第四个实例（右一）：**
    *   **问题：** “What is the weather like?”（天气怎么样？）
    *   **选项：** A. Cloudy（多云），B. Foggy（有雾），C. Rainy（下雨），D. Sunny（晴朗）。
    *   **正确答案：** A. Cloudy 或 B. Foggy（两者都被高亮显示，可能表示图像模糊，难以精确判断，但答案属于这一类）。
    *   **能力类型：** Static Context over Time（静态上下文）。图中显示了四幅相似的场景，可能是不同时间点的快照，但天气状况在这些快照中看起来是静态的。解决这个问题可能依赖于对静态图像或短时间内不变的视觉信息的理解，而不是对长时间序列的动态分析。

**结论（a部分）：** 这部分揭示了现有视频理解基准中存在大量“捷径”问题，这些问题可以通过常识、文档理解、单帧分析或静态上下文来解决，而无需真正的时空视频理解能力。这导致了基准测试结果可能无法准确反映模型在核心视频理解任务上的表现。

**第二部分：(b) Performance vs Shortcut Ratio（性能与捷径比例）**

这是一个柱状图，用于展示不同视频理解基准测试的性能与其包含的“视频独立样本”（即可以通过非视频理解方式解决的问题）比例之间的关系。

*   **X轴：** 不同的视频理解基准测试，如MVBench, EgoSchema, VideoMME, LongVideoBench, MLVU, TVBench, VCR-Bench, MMR-V Bench, ImplicitQA, LVBench, Video-Holmes, RTV-Bench, VSI-Bench, MINERVA。
*   **Y轴：** 百分比（%）。
*   **蓝色柱子：** Accuracy (%)（准确率），表示模型在该基准测试上的准确率。
*   **红色折线：** Shortcut Ratio (%)（捷径比例），表示该基准测试中可以通过视频独立方式解决的问题所占的比例。

**数据流动与结论（b部分）：**
*   观察图表可以发现，那些Shortcut Ratio（红色折线）较高的基准测试（例如MVBench, EgoSchema, VideoMME），其Accuracy（蓝色柱子）也相对较高。
*   相反，那些Shortcut Ratio较低的基准测试，其Accuracy也相对较低。
*   **结论：** 基准测试中“视频独立样本”的比例越高，模型在该基准上的得分（准确率）往往越高。这进一步证实了(a)部分的发现：模型可能在利用这些捷径来获得高分，而不是真正掌握了视频理解能力。

**第三部分：(c) Performance Collapse of current SOTA Models（当前SOTA模型的性能崩溃）**

这部分展示了当前最先进的（SOTA）视频理解模型在面对“视频原生挑战”时的性能表现。这里的“视频原生挑战”指的是那些无法通过捷径解决，真正需要时空视频理解能力的问题。

*   **X轴：** 不同的SOTA模型，如Qwen2.5-VL (7B), InternVL-3 (8B), Qwen3-VL-Think (8B), Eagle2.5 (8B), InternVL-3.5 (8B), VideoAuto-R1 (8B), Video-R1 (7B), LongViLA-R1 (7B)。
*   **Y轴：** Accuracy (%)（准确率）。
*   **灰色柱子：** Original Benchmarks（原始基准），表示模型在原始基准测试上的准确率。
*   **深蓝色柱子：** Remained Benchmarks（剩余基准），表示在过滤掉所有“视频独立样本”后，模型在真正的视频原生挑战上的准确率。
*   **红色虚线：** Random Guess (25%)（随机猜测，25%），作为性能基准线，表示如果模型完全随机猜测，其准确率应为25%（对于四选一问题）。
*   **红色百分比标签：** 表示模型在剩余基准上的准确率相比原始基准的下降幅度（例如，↓22.0% 表示准确率下降了22.0%）。

**数据流动与结论（c部分）：**
*   对于所有展示的模型，Remained Benchmarks（深蓝色柱子）的准确率都显著低于Original Benchmarks（灰色柱子）的准确率。
*   例如，Qwen2.5-VL (7B) 在原始基准上的准确率为51.17%，但在剩余基准上仅为29.2%，下降了22.0%。
*   更重要的是，许多模型在剩余基准上的准确率非常低，甚至接近或低于随机猜测的水平（25%）。例如，Video-R1 (7B) 在剩余基准上的准确率仅为26.3%，VideoAuto-R1 (8B) 为33.6%，LongViLA-R1 (7B) 为28.6%。
*   **结论：** 当前SOTA模型在面对真正的视频原生挑战时，其性能会大幅下降（“性能崩溃”）。这揭示了稳健的时空理解能力的固有难度，表明现有模型在核心视频理解任务上仍然存在巨大差距。

**整体方法的运作方式（基于图的结论）：**

1.  **识别问题：** 论文首先通过(a)部分展示了现有视频理解基准中存在大量可以通过非视频理解方式解决的问题（捷径）。
2.  **量化问题：** 通过(b)部分，论文量化了不同基准中捷径问题的比例，并将其与模型性能相关联，证明了高捷径比例会导致虚高的性能评分。
3.  **过滤捷径：** 论文的方法（Video-Oasis）旨在系统地审计现有基准，过滤掉这些捷径问题，留下真正需要时空视频理解的“视频原生挑战”。
4.  **评估真实能力：** 通过(c)部分，论文展示了当模型面对这些过滤后的“视频原生挑战”时，其性能会显著下降，甚至接近随机猜测水平。这表明现有模型在核心视频理解能力上还很薄弱。
5.  **提供诊断工具：** Video-Oasis作为一个诊断工具套件，帮助研究人员识别基准中的弱点，并理解模型在哪些方面真正需要改进，从而为构建更严格的视频基准和评估未来的Video-LLMs提供基础。

总而言之，这张图清晰地展示了当前视频理解研究和评估中存在的核心问题：现有基准包含大量捷径，导致模型性能被高估；而当面对真正的视频原生挑战时，即使是SOTA模型也表现不佳。这强调了重新思考和设计视频理解评估标准的必要性。

---

![Figure 3 : (a) Inaccurate annotations identified by the redundancy and consisten](fig3_1.webp)

> Figure 3 : (a) Inaccurate annotations identified by the redundancy and consistency tests. (b) Questions incorrectly filtered by the shuffling test but manually restored.

这张图（图3）来自论文《Video-Oasis: Rethinking Evaluation of Video Understanding》，它清晰地展示了两种视频理解评估中的关键问题：不准确的标注过滤和不准确的时间过滤。这张图通过具体的例子来说明这些问题是如何被识别和处理的。

图的布局分为左右两大部分，分别是(a) 不准确的标注过滤 和 (b) 不准确的时间过滤。每部分又包含两个子图，用以展示不同类型的问题。

**左侧部分：(a) 不准确的标注过滤**

这部分旨在说明一些视频理解任务中的标注存在问题，导致模型可能依赖错误的或不充分的信息来得出答案。

1.  **上半部分子图：**
    *   **问题 (Question):** "In the given video, when does the action 'person fixes their hair' take place?" (在给定的视频中，“人整理头发”的动作发生在什么时候？)
    *   **视频帧示例:** 下方展示了几个连续的视频帧。其中，绿色框标出了与“整理头发”动作相关的帧。
    *   **错误标注 (Wrong Annotation):** 红色文字指出，原始标注是“Throughout the entire video”（在整个视频中）。这显然是一个不准确的标注，因为它过于宽泛，没有精确指出动作发生的具体时间。
    *   **正确答案 (Correct Answer):** 绿色文字给出了正确答案：“In the middle of the video”（在视频中间）。这表明，通过分析，可以发现原始标注的错误，并确定正确的答案。
    *   **方法解读:** 这个例子展示了如何通过**冗余性测试**（redundancy test）或**一致性测试**（consistency test）来识别不准确的标注。例如，如果多个模型或人类标注者对同一动作的时间点给出不一致的答案，或者答案在逻辑上不合理（如“整个视频”），那么这个标注就可能被认为是不准确的。

2.  **下半部分子图：**
    *   **问题 (Question):** "Where is the man with brown hair in relation to the man in the black suit?" (棕色头发的男人相对于穿黑色西装的男人在哪里？)
    *   **视频帧示例:** 下方展示了一系列视频帧，其中用红色和绿色框标出了不同的人物。
    *   **模糊主体 (Ambiguous Subject):** 红色文字指出，问题是“Multiple 'the man with brown hair'”（多个“棕色头发的男人”）。这意味着视频中可能存在多个符合描述的主体，导致答案无法明确锚定。
    *   **无法锚定答案 (Fail to anchor the answer):** 黄色文字强调了这个问题，即由于主体不明确，模型无法给出一个确切的答案。
    *   **方法解读:** 这个例子同样是通过**冗余性测试**或**一致性测试**来识别的。当一个问题涉及到模糊的主体时，不同的标注或模型可能会指向不同的对象，导致答案不一致或无法确定。这种方法帮助过滤掉那些由于标注问题而无法有效评估模型能力的样本。

**右侧部分：(b) 不准确的时间过滤**

这部分关注的是在评估视频理解时，时间信息的处理可能存在问题，导致一些需要时间上下文的问题被错误地过滤掉了。

1.  **上半部分子图：**
    *   **问题 (Question):** "What did the baseball umpire do after the second ball?" (棒球裁判在第二球之后做了什么？)
    *   **视频帧示例:** 下方展示了几个连续的视频帧，蓝色框标出了与问题相关的关键帧，特别是“第二球之后”的场景。
    *   **答案 (Answer):** "He got down on one knee"（他单膝跪下）。
    *   **时间上下文 (Temporal Context):** 蓝色文字强调了“Temporal Context”（时间上下文）的重要性。这个问题需要理解动作发生的先后顺序。
    *   **方法解读:** 这个例子代表了那些被**打乱测试**（shuffling test）错误地过滤掉的问题。打乱测试可能是指将视频帧的顺序打乱，然后评估模型的性能。如果一个模型在没有正确时间顺序的情况下仍然能给出正确答案（或者如果问题本身在时间被打乱后变得没有意义但被错误地保留），那么这个问题可能就被错误地过滤了。这里的“manually restored”（手动恢复）意味着研究人员手动识别出这些问题，并认为它们对于评估时间理解是重要的，应该保留在评估集中。

2.  **下半部分子图：**
    *   **问题 (Question):** "What does the basketball coach do after the interviewer asks his first question?" (篮球教练在采访者提出第一个问题后做了什么？)
    *   **视频帧示例:** 下方展示了几个连续的视频帧，蓝色框标出了与问题相关的关键帧，特别是“第一个问题之后”的场景。
    *   **答案 (Answer):** "He scratches his head"（他挠了挠头）。
    *   **时间上下文 (Temporal Context):** 蓝色文字再次强调了“Temporal Context”（时间上下文）的重要性。
    *   **方法解读:** 与上一个子图类似，这个问题也是被**打乱测试**错误地过滤掉，但后来被手动恢复的。这表明这些问题对于评估模型对时间顺序的理解至关重要，不应该因为测试方法的缺陷而被排除在外。

**总结：**

这张图通过具体的例子，生动地展示了Video-Oasis诊断套件如何系统地审计现有的视频理解基准。它揭示了两种主要的评估问题：
*   **不准确的标注：** 导致模型可能依赖错误的或不充分的信息（如图(a)所示）。
*   **不准确的时间过滤：** 导致一些需要时间上下文的关键问题被错误地排除（如图(b)所示）。

通过识别和过滤掉这些有问题的样本，剩余的“原生视频挑战”能够更准确地评估模型的真实视频理解能力。这张图的方法核心是利用**冗余性测试**、**一致性测试**和**打乱测试**等手段来诊断基准数据的质量，并手动恢复那些对评估至关重要的问题。这使得研究人员能够更好地理解现有模型的能力差距，并为构建更严格的视频基准提供依据。
