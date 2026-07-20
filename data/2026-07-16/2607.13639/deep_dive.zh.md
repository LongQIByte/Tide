# OvisOCR2 Technical Report

[arXiv](https://arxiv.org/abs/2607.13639) · [HuggingFace](https://huggingface.co/papers/2607.13639) · ▲52

## 摘要（原文）

> We introduce OvisOCR2, a 0.8B document parsing model. OvisOCR2 is designed as an end-to-end parser: given a document page image, it generates a Markdown representation in natural reading order, covering text, formulas, tables, and visual regions. We build a data engine that combines filtered real-document annotations with synthetic pages whose rendered images and Markdown targets are derived from the same HTML source. The training recipe includes supervised fine-tuning, reinforcement learning on a 4B branch with a multi-component reward design, on-policy distillation into the 0.8B model, and model fusion. On OmniDocBench v1.6, OvisOCR2 achieves a state-of-the-art overall score of 96.58, placing an end-to-end model at the top of this leaderboard previously dominated by pipeline methods and highlighting the potential of end-to-end document parsing. On PureDocBench, OvisOCR2 also achieves the highest Avg3 score of 75.06. Beyond these two public benchmarks, we evaluate OvisOCR2 on an in-house benchmark designed to cover a broader set of long-tail and challenging scenarios. OvisOCR2 obtains the best overall performance among the compared methods, providing further evidence of its generalization and robustness. OvisOCR2 is available at https://huggingface.co/ATH-MaaS/OvisOCR2.

## 摘要（中译）

我们介绍了OvisOCR2，这是一个0.8B文档解析模型。OvisOCR2被设计为一个端到端的解析器：给定一个文档页面图像，它按自然阅读顺序生成Markdown表示，涵盖文本、公式、表格和视觉区域。我们构建了一个数据引擎，该引擎将过滤后的真实文档注释与合成页面相结合，这些合成页面的渲染图像和Markdown目标都是从同一HTML源派生的。训练方法包括监督微调、在具有多组件奖励设计的4B分支上进行强化学习、将策略蒸馏到0.8B模型中以及模型融合。在OmniDocBench v1.6上，OvisOCR2实现了96.58的整体最高分，使端到端模型在这个此前由管道方法主导的排行榜上名列前茅，并突显了端到端文档解析的潜力。在PureDocBench上，OvisOCR2也实现了最高的Avg3分数75.06。除了这两个公共基准测试之外，我们还在一个内部基准测试上评估了OvisOCR2，该基准测试旨在覆盖更广泛的长尾和具有挑战性的场景。OvisOCR2在比较的方法中获得了最佳的整体性能，进一步证明了其泛化能力和鲁棒性。OvisOCR2可在https://huggingface.co/ATH-MaaS/OvisOCR2上获取。

## 背景剖析

### 背景剖析  

**技术背景**：文档解析技术旨在将视觉丰富的文档图像（如扫描件、PDF或照片）转化为机器可理解的结构性格式（如Markdown）。这类技术广泛应用于数字化办公、知识管理、搜索引擎索引等场景，核心需求是准确提取文本、表格、公式等内容，并保留其原始布局和阅读顺序。例如，企业需要将纸质合同转为可搜索的电子文档，学术平台需从论文图像中提取结构化数据供检索。  

**之前的问题**：现有方法分为两类：  
1. **流水线方法**：分步骤处理（先分析布局，再识别内容，最后合并），虽在主流基准测试中表现较好，但部署复杂且易出错。例如，若表格边界识别错误，后续步骤无法修正；不同模块的运行时负载不均，增加系统开销。  
2. **端到端方法**：用单一模型直接生成结果，部署更简单，但性能落后于流水线方法。此前端到端模型的局限性在于难以处理长文档、复杂布局（如嵌套表格）或手写内容，导致在公开基准上得分较低。  

**本文的解法**：OvisOCR2提出了一种优化的端到端方案：  
- **数据引擎**：结合真实文档标注与合成数据（通过HTML模板生成图像和对应Markdown），提升模型对多样场景的适应性。  
- **训练策略**：采用监督微调、强化学习（基于4B参数模型）、策略蒸馏（压缩至0.8B）和模型融合，平衡性能与部署效率。  
- **目标**：在保持模型轻量化的同时，超越当前领先的流水线方法。  

**切入角度**：与前人工作相比，OvisOCR2的关键差异在于：  
1. **端到端设计的性能突破**：首次在主流基准（如OmniDocBench）上用单一模型超越流水线方法。  
2. **轻量化与高效训练**：基于Qwen3.5-0.8B小模型实现SOTA结果，适合资源受限场景。  
3. **综合数据策略**：通过合成数据弥补真实标注的不足，增强模型鲁棒性。  

这一工作证明了端到端模型在文档解析中的潜力，为实际应用提供了更高效的解决方案。

## 方法图解

![Figure 1: Performance of OvisOCR2 on OmniDocBench v1.6](fig1_1.webp)

> Figure 1: Performance of OvisOCR2 on OmniDocBench v1.6

这张图（图1）来自论文《OvisOCR2 Technical Report》，展示了OvisOCR2模型在OmniDocBench v1.6基准测试上的性能表现。我们可以将这张图分解为几个关键部分来理解：

首先，图的顶部是一个图例，列出了参与比较的多个文档解析模型及其对应的颜色和图标。这些模型包括OvisOCR2（蓝色V形图标）、PaddleOCR-VL-1.6（浅棕色）、MinerU2.5-Pro（浅蓝色）、GLM-OCR（米色）、PaddleOCR-VL-1.5（深蓝色）、HunyuanOCR-1.5（深青色）等，以及其他一些模型如Unlimited-OCR、Youtu-Parsing、Qwen3-VL-235B等。这个图例帮助我们识别图中不同颜色的柱状图分别代表哪个模型。

图的主体部分由四个子图组成，分别对应不同的评估维度：整体表现、文本得分（Text Score）、公式得分（Formula Score）、表格得分（Table Score）和阅读顺序（Reading Order）。每个子图都是一个柱状图，横轴代表不同的模型，纵轴代表得分（百分比）。

1.  **整体表现（最上方的完整柱状图）**：
    这个图表展示了所有模型在OmniDocBench v1.6上的综合得分。OvisOCR2（蓝色柱子）以96.6分位居榜首，紧随其后的是PaddleOCR-VL-1.6（96.3分）和MinerU2.5-Pro（95.8分）。其他模型如GLM-OCR（95.2分）、PaddleOCR-VL-1.5（94.9分）等得分依次降低。这个图表清晰地表明OvisOCR2在综合性能上领先于其他比较的模型。

2.  **文本得分（Text Score）**：
    这个子图专门评估模型识别和解析文本内容的能力。OvisOCR2（97.4分）再次表现出色，略高于PaddleOCR-VL-1.6（96.7分）和MinerU2.5-Pro（96.5分）。这表明OvisOCR2在文本处理方面具有很强的能力。

3.  **公式得分（Formula Score）**：
    此子图衡量模型解析数学公式的准确性。OvisOCR2（97.5分）与PaddleOCR-VL-1.6（97.5分）并列第一，显示出其在公式解析方面的卓越性能。

4.  **表格得分（Table Score）**：
    该图表评估模型解析表格数据的能力。OvisOCR2（94.8分）与PaddleOCR-VL（94.8分）得分相同，并列第一，表明其在表格处理方面也表现优异。

5.  **阅读顺序（Reading Order）**：
    这个子图考察模型按照自然阅读顺序输出内容的能力。OvisOCR2（88.9分）在此项评估中表现最佳，超过了其他模型如Youtu-Parsing（88.4分）和MinerU2.5-Pro（87.0分）。这说明OvisOCR2能够很好地理解文档的布局和结构，从而按正确的顺序输出信息。

**方法运作的揭示**：
虽然这张图本身主要展示的是结果，但结合论文摘要，我们可以理解OvisOCR2是如何达到这些高性能的：
*   **端到端设计**：OvisOCR2是一个端到端的文档解析模型，直接从文档图像生成Markdown表示，覆盖文本、公式、表格和视觉区域，并按自然阅读顺序输出。
*   **数据引擎**：构建了一个数据引擎，结合了过滤的真实文档标注和合成的页面。合成页面的渲染图像和Markdown目标都源自相同的HTML源，这有助于模型学习更真实和多样的文档表示。
*   **训练策略**：采用了多种先进的训练技术，包括监督微调、基于4B参数分支的强化学习（带有奖励设计）、策略梯度蒸馏到0.8B模型，以及模型融合。这些技术共同提升了模型的性能和泛化能力。

**结论**：
从图中可以清楚地看到，在OmniDocBench v1.6基准测试的各个评估维度上，OvisOCR2均取得了领先或并列领先的分数。这证明了OvisOCR2作为一个端到端文档解析模型的强大性能和有效性，它在之前主要由管道方法主导的排行榜上取得了最先进的整体分数（96.58），突显了端到端方法在文档解析领域的潜力。例如，在整体表现上，OvisOCR2（96.6分）高于其他所有比较模型；在文本、公式、表格和阅读顺序等具体任务上也均表现出色。

---

![Figure 2: Architecture of the data engine](fig2_1.webp)

> Figure 2: Architecture of the data engine

这张图展示了OvisOCR2的数据引擎架构，它由**真实世界数据管道（Real - World Data Pipeline）**和**合成数据管道（Synthetic Data Pipeline）**两部分组成，最终共同构建出高质量训练语料库（High - Quality Training Corpus, OvisOCR2）。下面我们分别解析这两个管道以及数据的流动过程：

### 真实世界数据管道（左侧，浅蓝色背景）
1. **起始点：真实世界文档图像（Real - World Document Images）**：这是数据的源头，即从现实世界中获取的各类文档图像。
2. **专门OCR解析（Specialized OCR Parsing）**：使用两种工具对文档图像进行解析，分别是`PaddleOCR - VL - 1.5`和`MinerU2.5 - Pro`。这一步的目的是从图像中提取出初步的文本或结构信息。
3. **基于规则的JSON转Markdown（Rule - Based JSON - to - Markdown）**：将上一步OCR解析得到的JSON格式数据，按照规则转换为Markdown格式。Markdown是一种轻量级的标记语言，便于后续处理和阅读。
4. **人工抽查与子集过滤（Manual Spot - Checking & Subset Filtering）**：通过人工检查的方式，对转换后的Markdown数据进行抽查，并过滤掉不符合要求的数据子集，以保证数据的质量。
5. **真实世界训练数据（Real - World Training Data）**：经过前面几步处理后，得到真实世界的训练数据。
6. **高质量训练语料库（OvisOCR2）**：真实世界训练数据最终流入这个语料库，成为其中的一部分。

### 合成数据管道（右侧，浅橙色背景）
1. **起始点：难例挖掘（Hard Sample Mining）**：这一步是挖掘出那些难以处理的样本，这些样本会导致两种失败情况：
    - **真实场景失败（In - the - Wild Failures）**：在实际应用场景中出现的问题样本。
    - **自测失败（Self - Test Failures）**：在模型自我测试过程中发现的问题样本。
2. **HTML模板生成（HTML Template Generation）**：使用**多模态大模型（Multimodal LLM）**来生成HTML模板。多模态大模型能够处理图像和文本等多种模态的信息，从而生成合适的HTML结构。
3. **基于Agent的HTML多样化（Agent - Based HTML Diversification）**：通过Agent（智能体）对生成的HTML进行多样化处理，以增加数据的多样性。
4. **两个并行的输出**：
    - **来自DOM的Markdown真实标签（Markdown GT from DOM）**：从文档对象模型（DOM）中提取出Markdown格式的真实标签（Ground Truth）。
    - **Playwright渲染（Playwright Rendering）**：使用Playwright工具对HTML进行渲染，得到对应的图像。
5. **图像 - 文本配对（Image - Text Pairing）**：将上一步得到的Markdown（文本）和渲染后的图像进行配对，形成图像 - 文本对。
6. **迭代质量控制（Iterative Quality Control）**：对图像 - 文本对进行迭代的质量控制，以确保数据的质量。
7. **合成训练数据（Synthetic Training Data）**：经过质量控制后，得到合成的训练数据。
8. **高质量训练语料库（OvisOCR2）**：合成训练数据最终也流入这个语料库，与真实世界训练数据共同构成高质量训练语料库。

### 数据流动与方法运作方式
- 真实世界数据管道从真实的文档图像开始，经过OCR解析、格式转换、人工过滤等步骤，得到高质量的真实训练数据。
- 合成数据管道则从难例挖掘开始，通过多模态大模型生成HTML模板，再经Agent多样化、渲染、配对和质量控制等步骤，得到高质量的合成训练数据。
- 最后，这两部分数据（真实训练数据和合成训练数据）共同组成了OvisOCR2的高质量训练语料库。这个语料库将被用于OvisOCR2模型的训练，以使其成为一个能够端到端解析文档（生成自然阅读顺序的Markdown表示，涵盖文本、公式、表格和视觉区域）的优秀模型。

### 总结
这张图清晰地展示了OvisOCR2的数据引擎是如何运作的：通过结合真实世界数据的精心处理和合成数据的创新生成，构建出高质量的训练语料库，为后续的模型训练（包括监督微调、强化学习、策略蒸馏和模型融合等步骤）提供数据支持，最终使OvisOCR2在多个文档解析基准测试中取得优异成绩。

---

![Figure 3: Two-branch training of OvisOCR2. The 4B branch produces an RL-aligned ](fig3_1.webp)

> Figure 3: Two-branch training of OvisOCR2. The 4B branch produces an RL-aligned teacher, while the 0.8B branch proceeds through SFT, OPD, and model fusion to obtain the final model.

这张图展示了OvisOCR2模型的**双分支训练流程**，清晰呈现了“教师分支（Teacher branch）”和“学生分支（Student branch）”的设计逻辑与数据/信息流动顺序，帮助我们理解模型如何通过两个分支的协作完成训练并得到最终模型：  

### 1. 教师分支（浅绿色区域）：生成RL对齐的教师模型  
教师分支的目标是训练一个“策略对齐”的教师模型，为后续学生分支的蒸馏提供指导。流程如下：  
- **第一步（4B SFT - Base parser）**：以“4B参数规模的基础解析器”为起点，通过**监督微调（SFT）**初始化模型，学习基础的文档解析能力（比如识别文本、公式、表格等结构）。  
- **第二步（4B RL - Structural feedback）**：在基础解析器的基础上，引入**强化学习（RL）**，并通过“结构反馈（Structural feedback）”优化模型。这里的“结构反馈”可能针对文档的结构合理性（如阅读顺序、元素层级等）设计奖励，让模型学习更符合人类阅读习惯的解析策略。  
- **第三步（4B Teacher - Aligned policy）**：经过RL训练后，得到“4B教师模型（Aligned policy）”，它的策略（即解析文档的方式）被对齐到更优的状态，将作为后续学生分支的“教师”，提供蒸馏的知识。  


### 2. 学生分支（浅紫色区域）：从SFT到最终模型（OvisOCR2）  
学生分支的目标是基于教师模型的知识，训练一个更轻量（0.8B参数）但性能优异的最终模型。流程如下：  
- **第一步（0.8B SFT - Student init）**：以“0.8B参数规模的学生初始化模型”为起点，同样通过**监督微调（SFT）**初始化，为后续蒸馏做准备。  
- **第二步（OPD - On - policy distillation）**：引入**在线策略蒸馏（On - policy distillation）**，这里的关键是**从教师分支的“4B Teacher Aligned policy”中获取知识**（箭头体现了知识的传递：教师模型的策略被用来指导学生模型的蒸馏）。在线策略蒸馏意味着学生在“模仿”教师的**实时策略**（而非预定义的静态知识），从而学习更灵活的解析能力。  
- **第三步（Model Fusion - Weighted averaging）**：通过**加权平均（Weighted averaging）**进行模型融合。这一步可能是将蒸馏后的学生模型与初始模型（或其他中间模型）进行加权合并，以平衡不同阶段的训练成果，提升模型的稳定性和性能。  
- **第四步（Final 0.8B - OvisOCR2）**：经过上述步骤后，得到最终的“0.8B模型（OvisOCR2）”，这就是论文中介绍的端到端文档解析模型。  


### 方法的核心逻辑（从图中可理解的运作方式）  
OvisOCR2的训练分为**“教师预训练（RL对齐）”**和**“学生轻量化蒸馏+融合”**两个核心阶段：  
- 教师分支通过“大参数（4B）+ 强化学习（RL）”的方式，学习到更优的文档解析策略（结构对齐的策略），解决了“如何解析出结构合理、符合人类阅读习惯的文档”这一问题。  
- 学生分支则通过“小参数（0.8B）+ 在线策略蒸馏（OPD）+ 模型融合”，在保持轻量化的同时，继承教师模型的优秀解析策略，并通过融合进一步提升性能。这种“大模型做教师，小模型做学生”的设计，既利用了大模型的能力（结构理解、强化学习优化），又通过轻量化让学生模型更适合实际部署，同时保证了性能（如论文中提到的在OmniDocBench、PureDocBench等基准上的SOTA表现）。  


### 补充说明（图中“看不清/不确定”的处理）  
图中箭头的方向清晰展示了**数据/知识的流动方向**：教师分支的输出（4B Teacher Aligned policy）作为学生分支“OPD”步骤的输入；学生分支内部则是“初始化→蒸馏→融合→最终模型”的顺序。所有组件的功能（如SFT、RL、OPD、模型融合）都通过标签明确，因此可以推断出整个训练流程的逻辑：**先训练一个强大的教师模型（4B分支），再用这个教师模型指导轻量学生模型的训练（0.8B分支），最终得到高性能的小模型（OvisOCR2）**。

---

![Figure 4: Training stability comparison between 4B RL and 0.8B RL. Panel (a) rep](fig4_1.webp)

> Figure 4: Training stability comparison between 4B RL and 0.8B RL. Panel (a) reports actor KL loss, with faint traces showing raw per-step values and bold curves showing 15-step centered rolling means. Panel (b) reports table TEDS on the validation set.

这张图（图4）来自论文《OvisOCR2 Technical Report》，用于比较4B参数规模和0.8B参数规模的强化学习（RL）训练过程的稳定性和性能。我们将其分为两个子图来详细解读：

首先看子图(a)，标题为“Policy divergence during RL”（强化学习过程中的策略分歧）。这个子图展示了**Actor KL loss**（演员KL损失）随**Training step**（训练步骤）的变化情况。图中有两条曲线：蓝色实线代表“4B RL”模型，红色虚线代表“0.8B RL”模型。图中的“faint traces”（浅色痕迹）显示的是每一步的原始值，而“bold curves”（粗曲线）则是15步中心滚动平均后的结果，这样可以更清晰地看到趋势。从图中可以看出，在训练的大部分步骤中，4B RL模型的KL损失（蓝色）保持在一个较低且稳定的水平，而0.8B RL模型的KL损失（红色）在训练后期（大约800到1000步之间）出现了显著的波动和峰值，这可能表明0.8B模型在强化学习过程中策略的分歧更大，训练稳定性较差。

接下来看子图(b)，标题为“Validation-set table quality”（验证集表格质量）。这个子图展示了**Table TEDS**（表格的某种质量评估指标，可能是Table Error Detection Score或其他相关指标）随**Training step**（训练步骤）的变化情况。同样有两条曲线：蓝色实线代表“4B RL”模型，红色虚线代表“0.8B RL”模型。从图中可以看出，4B RL模型的Table TEDS（蓝色）在训练过程中整体上保持在一个较高的水平（大约93到94之间），并且波动相对较小；而0.8B RL模型的Table TEDS（红色）在训练后期（大约600步之后）逐渐下降，并且在800步之后出现了明显的低谷，这表明0.8B模型在验证集上的表格质量随着训练步骤的增加而下降，而4B模型的表格质量则相对稳定且更高。

综合这两个子图，我们可以得出以下结论：在强化学习训练过程中，4B参数规模的模型（4B RL）比0.8B参数规模的模型（0.8B RL）具有更好的训练稳定性（表现为KL损失更低且波动更小）和更高的验证集表格质量（表现为Table TEDS更高且更稳定）。这可能意味着更大的模型在强化学习阶段能够更好地学习到有效的策略，从而在文档解析任务（特别是表格处理）中表现得更稳定和更好。

需要注意的是，图中的“Actor KL loss”通常用于衡量策略网络输出的分布与目标分布之间的差异，KL损失越低表示策略越稳定；而“Table TEDS”则用于评估模型生成的表格质量，分数越高表示表格质量越好。通过比较这两个指标在两种不同规模模型上的表现，我们可以清楚地看到4B RL模型在训练稳定性和表格质量方面都优于0.8B RL模型。

---

![Figure A.1: Qualitative comparison on a table document.](fig5_1.webp)

> Figure A.1: Qualitative comparison on a table document.

这张图（图A.1）展示了OvisOCR2在表格文档上的定性比较，通过四个不同的模型或系统（Image、OvisOCR2、PaddleOCR-VL-1.6、MinerU2.5-Pro）对同一份包含表格的文档图像进行解析，并展示其输出结果或相关配置信息。

首先，我们来看左上角的“Image”板块。这个板块展示了一份实际的文档图像，其中包含一个表格。这份图像是所有模型进行解析的输入数据。图像中的表格结构清晰，包含多行多列，用于测试模型对表格内容的识别和解析能力。

接下来是右上角的“OvisOCR2”板块。这个板块详细列出了OvisOCR2模型的相关信息。顶部是模型的基本信息，包括其名称“OvisOCR2”，以及一些版本和训练相关的元数据，如“Kubernetes 集群部署设计”、“生产环境: k8s v1.36, 基础镜像: 2024-03-15, 版本: v2.4”。下方是“组件版本表”，列出了模型依赖的各种软件包及其版本号，例如Kubernetes、containerd、etcd、CoreDNS等，这些是运行OvisOCR2所需的环境配置。再往下是“资源配额表 (ResourceQuota)”，详细说明了不同命名空间（如production、staging、monitoring、kubo-system）下的CPU和内存请求（Request）与限制（Limit），以及Pod上限和PVC上限。这表明OvisOCR2在部署时对计算资源有特定的需求。最底部是“基础资源限制 (BaseResourceQuota)”，提供了更宏观的资源限制信息。这个板块揭示了OvisOCR2的运行环境和资源配置，这是其能够正确解析文档的基础。

然后是左下角的“PaddleOCR-VL-1.6”板块。这个板块的结构与OvisOCR2的板块类似，也包含了模型的基本信息、组件版本表和资源配额表。它展示了另一个OCR模型PaddleOCR-VL-1.6的配置和资源需求。通过对比OvisOCR2和PaddleOCR-VL-1.6的资源配额表，可以观察到它们在资源分配上的差异，例如production命名空间下的CPU Limit，OvisOCR2是32 cores，而PaddleOCR-VL-1.6是64 cores。这可能影响模型的推理速度或处理复杂文档的能力。

最后是右下角的“MinerU2.5-Pro”板块。这个板块同样遵循了类似的格式，展示了MinerU2.5-Pro模型的基本信息、组件版本表和资源配额表。其资源配额表中的数值与其他模型有所不同，例如production命名空间下的CPU Request为32 cores，Memory Request为64 GiB。这表明每个模型都有其特定的资源配置需求。

这张图揭示了OvisOCR2方法运作的背景环境。虽然图中没有直接展示解析过程或结果的对比（如文字识别或表格结构还原的具体内容），但它通过展示四个模型的配置信息和资源分配，为理解OvisOCR2的运行环境和与其他模型的比较提供了一个框架。图中的“定性比较”可能体现在这些模型对同一份文档图像的解析质量上，而这种质量可能与它们的资源配置、模型架构和训练方法有关。通过观察这些模型的配置差异，可以推测OvisOCR2在设计上可能优化了资源利用效率，或者在特定配置下能够达到更好的解析效果。例如，OvisOCR2在某些资源限制上可能比其他模型更为严格，但仍然能够取得优异的性能，这表明其模型架构或训练策略的有效性。

总结来说，这张图通过展示四个模型（包括OvisOCR2）对同一份表格文档图像的解析配置和资源需求，为理解OvisOCR2的运行环境和与其他模型的比较提供了一个全面的视图。虽然具体的解析结果没有直接显示，但这些配置信息对于评估模型在实际应用中的性能和可行性至关重要。

---

![Figure A.2: Qualitative comparison on a table document (continued).](fig6_1.webp)

> Figure A.2: Qualitative comparison on a table document (continued).

这张图（图A.2）是论文《OvisOCR2 Technical Report》中的一个定性比较图，标题为“Figure A.2: Qualitative comparison on a table document ”，展示了不同OCR模型在处理表格文档时的表现对比。图中包含四个主要部分，分别对应不同的OCR模型或方法：Image、OvisOCR2、GLM-OCR和Unlimited-OCR。

1. **Image部分**：这是原始的表格文档图像，作为输入数据。图像显示了一个包含多行多列的表格，表格中有文本和一些视觉元素。这部分是所有OCR模型处理的起点，展示了需要解析的原始文档内容。

2. **OvisOCR2部分**：这部分展示了OvisOCR2模型对输入图像的解析结果。结果以结构化的方式呈现，包括表格的各个单元格内容和布局。OvisOCR2的输出看起来非常清晰，准确地还原了原始表格的结构和内容。这部分展示了OvisOCR2在处理表格文档时的高精度和准确性。

3. **GLM-OCR部分**：这部分展示了GLM-OCR模型对同一输入图像的解析结果。结果显示了一些表格内容和布局，但与OvisOCR2相比，可能存在一些差异或错误。这部分用于对比GLM-OCR与OvisOCR2在处理表格文档时的表现差异。

4. **Unlimited-OCR部分**：这部分展示了Unlimited-OCR模型对输入图像的解析结果。结果显示了表格内容和布局，但与OvisOCR2相比，可能存在更多的差异或错误。这部分用于进一步对比Unlimited-OCR与OvisOCR2在处理表格文档时的表现差异。

通过这张图，我们可以清楚地看到OvisOCR2在处理表格文档时的优势。OvisOCR2能够准确地解析表格的结构和内容，而其他模型可能在某些方面存在不足。这表明OvisOCR2在文档解析任务中具有较高的性能和准确性。

总结来说，这张图通过对比不同OCR模型在处理表格文档时的表现，展示了OvisOCR2在文档解析任务中的优势和准确性。OvisOCR2能够准确地还原原始表格的结构和内容，而其他模型可能在某些方面存在不足。这为OvisOCR2在文档解析任务中的应用提供了有力的证据。

---

![Figure A.3: Qualitative comparison on a table document.](fig7_1.webp)

> Figure A.3: Qualitative comparison on a table document.

这张图（图A.3）展示了四种不同OCR或文档解析系统在处理同一份包含表格的文档图像时的定性比较结果。图的标题“定性比较在表格文档上”准确地概括了其内容。这张图的核心目的是通过视觉化的方式，直观地展示各个系统在解析复杂表格结构时的表现差异。

图的结构被划分为四个主要区域，每个区域代表一个不同的系统或方法：
1.  **左上角：“Image”**：这个区域显示了原始的输入图像，即包含表格的文档页面。这是所有系统进行分析的原始数据。图像内容是一个典型的表格，包含多行多列，以及一些文本和可能的数字。这个区域作为基准，供其他系统的输出与之对比。

2.  **右上角：“OvisOCR2”**：这个区域展示了名为OvisOCR2的系统对输入图像的解析结果。OvisOCR2是本文介绍的0.8B参数文档解析模型。其输出看起来是一个结构化的文本表示，可能以Markdown格式呈现，试图重现原始表格的内容和布局。我们可以看到，解析结果尝试将表格的行和列内容清晰地组织起来，例如使用竖线（|）分隔列，或者使用某种形式的缩进和换行来表示行。这个区域展示了OvisOCR2在理解表格结构和提取内容方面的能力。

3.  **左下角：“PaddleOCR-VL-1.6”**：这个区域展示了另一个名为PaddleOCR-VL-1.6的系统（版本1.6）的解析结果。与OvisOCR2类似，这个区域也呈现了该系统对同一表格图像的文本表示。通过对比这个区域的输出与OvisOCR2的输出，可以观察到两者在表格内容识别准确性和结构还原度上的差异。例如，某些单元格的内容可能被正确识别，而另一些可能被遗漏、错误识别或格式化不当。

4.  **右下角：“MinerU2.5-Pro”**：这个区域展示了第三个系统“MinerU2.5-Pro”的解析结果。同样，这个区域呈现了该系统对输入表格图像的处理结果。通过与其他两个系统的输出进行比较，可以评估MinerU2.5-Pro在表格解析任务上的性能。

**数据或信息的流动顺序**：
这张图并不是展示一个动态的流程或数据流，而是展示了一个静态的比较结果。其逻辑顺序是：
*   首先，提供一个共同的输入（“Image”区域的原始表格图像）。
*   然后，并列展示三个不同系统（OvisOCR2、PaddleOCR-VL-1.6、MinerU2.5-Pro）对该输入的处理结果。
*   观众通过视觉比较这三个系统的输出，来评估它们在表格解析任务上的表现。

**这张图揭示了方法具体是怎么做的（从比较的角度）**：
虽然这张图本身不直接展示OvisOCR2的内部工作原理（如模型架构、训练过程等），但它通过与其他系统的定性比较，间接地展示了OvisOCR2的有效性。OvisOCR2被设计为一个端到端的解析器，能够从文档图像生成自然阅读顺序的Markdown表示，涵盖文本、公式、表格和视觉区域。这张图通过展示OvisOCR2的解析结果与其他系统（如PaddleOCR-VL-1.6和MinerU2.5-Pro）的结果，让读者能够直观地判断OvisOCR2在处理复杂表格结构时的准确性和清晰度。如果OvisOCR2的输出在结构完整性、内容准确性或可读性方面优于其他系统，那么这表明其设计方法是有效的。

**如果是结果图，说清坐标、对比对象和结论**：
这张图是一个定性比较的结果图。它没有具体的坐标数据，而是通过视觉对比来呈现结论。
*   **对比对象**：对比对象是三个不同的文档解析系统：OvisOCR2、PaddleOCR-VL-1.6和MinerU2.5-Pro。它们都处理同一个输入图像（左上角的“Image”）。
*   **结论**：通过观察图中各个系统的输出，可以得出关于它们在表格解析任务上性能的定性结论。例如，如果OvisOCR2的输出表格结构更清晰、内容识别更准确，那么可以得出结论OvisOCR2在该任务上表现更好。这张图旨在直观地展示OvisOCR2相对于其他系统的优势或特点，支持论文中关于OvisOCR2在文档解析任务上取得最先进性能的论断。具体来说，观众可以比较各个系统输出的表格是否完整地再现了原始图像中的行和列，文本是否正确无误，以及格式是否易于理解。虽然图中没有明确标注哪个输出对应哪个系统是最好的，但通过仔细观察，可以推断出作者希望展示OvisOCR2的解析结果在某种程度上优于或至少与其他系统相当。

---

![Figure A.4: Qualitative comparison on a table document (continued).](fig8_1.webp)

> Figure A.4: Qualitative comparison on a table document (continued).

这张图（图A.4）是论文《OvisOCR2 Technical Report》中的一个定性比较图，标题为“Figure A.4: Qualitative comparison on a table document (continued)”，即“图A.4：表格文档上的定性比较（续）”。它通过展示四个不同OCR或文档解析系统对同一个表格文档图像的处理结果，来直观地比较它们的性能。

图的布局分为四个主要部分，每个部分代表一个不同的系统或方法：

1.  **左上角：Image（原始图像）**
    *   这个板块展示了作为输入的原始表格文档图像。它包含一个表格，表格中有几行几列，内容涉及“UITableView”及其相关属性和方法，例如“Overview”、“Topics”、“Creating a Table View”等。这个图像是所有后续处理的基础。

2.  **右上角：OvisOCR2**
    *   这个板块展示了OvisOCR2模型对原始图像的解析结果。解析结果以结构化的文本形式呈现，试图重现原始表格的内容和结构。
    *   我们可以看到，OvisOCR2的输出包含了标题（如“UITableView”）、子标题（如“Overview”、“Topics”）以及列表项（如“Creating a Table View”、“Providing Data”等）。其格式试图模仿原始表格的层次结构和内容。
    *   从视觉上看，OvisOCR2的输出在文本识别和结构恢复方面表现良好，能够清晰地展示表格中的各个部分及其内容。

3.  **左下角：GLM-OCR**
    *   这个板块展示了GLM-OCR模型对同一原始图像的解析结果。
    *   其输出也是结构化文本，包含标题、子标题和列表项。例如，可以看到“UITableView”、“Overview”、“Creating a Table View”等元素。
    *   与OvisOCR2相比，GLM-OCR的输出在格式和内容完整性上可能略有不同，但同样试图提取表格中的关键信息。

4.  **右下角：Unlimited-OCR**
    *   这个板块展示了Unlimited-OCR模型对原始图像的解析结果。
    *   其输出同样是结构化文本，包含标题、子标题和列表项。例如，“UITableView”、“Overview”、“Creating a Table View”等。
    *   从图中可以看出，Unlimited-OCR的输出也尝试恢复表格的结构和内容，但其格式和内容的组织方式可能与OvisOCR2和GLM-OCR有所不同。

**图中揭示的方法运作方式：**

这张图本身并不直接展示OvisOCR2方法的具体运作机制（如训练过程或模型架构），而是通过**定性比较**的方式，展示OvisOCR2作为一个文档解析模型在处理表格文档时的**输出结果**。它暗示了OvisOCR2的方法能够将表格图像转换为结构化的文本表示，如Markdown或其他格式，从而保留原始文档的布局和内容信息。

**对比对象和结论：**

*   **对比对象：** 图中将OvisOCR2的输出与另外两个OCR系统（GLM-OCR和Unlimited-OCR）的输出进行了比较。原始输入图像是它们共同的解析对象。
*   **结论（基于图的视觉比较）：** 虽然图中没有明确的评分或定量指标，但通过视觉检查可以得出以下初步结论：
    *   OvisOCR2的输出在格式清晰度和内容完整性方面表现良好，能够较好地恢复原始表格的层次结构和内容。
    *   与其他两个系统相比，OvisOCR2的输出可能在文本识别的准确性、列表项的格式化或整体结构的组织上更具优势（这需要根据具体的视觉细节进行判断，但从图中整体来看，OvisOCR2的输出显得更为规整和易读）。
    *   这张图旨在通过视觉示例来支持论文中关于OvisOCR2在文档解析任务上取得优异性能的论断，特别是在表格这类结构化文档的处理上。

总而言之，这张图通过展示四个不同系统对同一表格文档的解析结果，直观地比较了它们的性能。OvisOCR2的输出在视觉上表现出色，表明其在文档解析，特别是表格内容的识别和结构化方面具有较高的准确性和可读性。

---

![Figure A.5: Qualitative comparison on a handwritten document.](fig9_1.webp)

> Figure A.5: Qualitative comparison on a handwritten document.

这张图是论文《OvisOCR2 Technical Report》中的**图A.5**，标题为“手写文档的定性比较”，用于直观展示不同OCR（光学字符识别）或文档解析模型在处理同一张手写文档图像时的表现差异，从而突出OvisOCR2的性能优势。

### 图的结构与组件说明：
图被划分为四个主要区域，每个区域对应一个不同的模型或方法，从左到右、从上到下依次是：
1. **左上角：原始手写文档图像（Image）**  
   这是被所有模型处理的输入，显示了一张包含中文手写文字的文档，顶部有“DATE / 118 / 484”的标注，内容是关于周末感受、社交互动和个人反思的手写文字。这个区域是所有模型的“输入源”，后续的三个区域展示了不同模型对该输入的“输出结果”。

2. **右上角：OvisOCR2的输出**  
   该区域展示了OvisOCR2模型对原始手写文档的解析结果，输出为结构化的文本（可能是Markdown格式），内容与原始手写文档的文字高度对应，排版清晰，能够准确识别并还原手写文字的内容和结构。这体现了OvisOCR2作为端到端文档解析模型的能力：给定文档图像，生成自然阅读顺序的Markdown表示（覆盖文本、公式、表格和视觉区域）。

3. **左下角：PaddleOCR-VL-1.6的输出**  
   该区域展示了另一个OCR模型（PaddleOCR-VL-1.6）的解析结果。与OvisOCR2的输出相比，这里的文本排版和识别准确性可能存在差异（例如，部分文字的识别或排版可能不够清晰或准确）。通过对比，可以观察到OvisOCR2在处理手写文档时的优势。

4. **右下角：MinerU2.5-Pro的输出**  
   该区域展示了第三个模型（MinerU2.5-Pro）的解析结果。同样，与OvisOCR2的输出对比，这里的文本识别或排版可能存在不足，进一步凸显OvisOCR2的性能。

### 方法运作方式的揭示（通过对比理解）：
这张图通过**定性对比**展示了OvisOCR2的工作方式：
- **输入**：一张手写文档图像（如左上角的“Image”区域）。
- **处理**：OvisOCR2作为端到端解析器，直接从图像中提取文本，并以自然阅读顺序生成结构化的Markdown表示（如右上角的输出）。
- **输出**：清晰的、与原始文档内容一致的文本，排版合理，能够准确还原手写文字的内容和结构。

与其他模型（PaddleOCR-VL-1.6和MinerU2.5-Pro）的输出对比，OvisOCR2的输出在**准确性**（文字识别正确）和**可读性**（排版清晰、符合自然阅读顺序）方面表现更优。这说明OvisOCR2的设计（结合过滤的真实文档注释和合成页面的数据引擎、监督微调、强化学习、策略蒸馏和模型融合等训练方法）使其能够更好地处理手写文档的复杂性。

### 结论（从图中得出的结果）：
- **对比对象**：OvisOCR2与PaddleOCR-VL-1.6、MinerU2.5-Pro三个模型。
- **坐标/区域**：四个区域分别对应输入和三个模型的输出。
- **结论**：OvisOCR2在处理手写文档时，能够生成更准确、更易读的文本输出，优于其他对比模型。这验证了OvisOCR2作为端到端文档解析模型的有效性和优越性，支持了论文中关于其在OmniDocBench v1.6和PureDocBench等基准测试中取得最先进结果的结论。

这张图通过直观的定性对比，让读者能够快速理解OvisOCR2在文档解析任务中的优势，即能够更准确地识别手写文字并生成结构化的输出，从而突出了端到端方法相对于传统管道方法的潜力。

---

![Figure A.6: Qualitative comparison on a handwritten document (continued).](fig10_1.webp)

> Figure A.6: Qualitative comparison on a handwritten document (continued).

这张图（图A.6）是论文《OvisOCR2 Technical Report》中的**定性比较图**，用于展示不同OCR（光学字符识别）或文档解析模型在处理**手写文档**时的表现差异，属于“继续”部分（即可能是系列比较中的一个子图）。我们逐个分析图中的四个板块（从左到右、从上到下）：

### 1. 左上角：原始手写文档（Image）
- **内容**：这是一张手写的中文文档图像，包含日期（2025年1月19日 21:05 周日）、页码（118/484）和一段手写文字，文字内容是关于情绪、社交、学习等个人思考（例如“愉快的周末结束啦……”）。
- **作用**：作为**输入样本**，展示需要被模型解析的原始手写文档的外观，包括文字的书写风格、布局（如段落、换行）、图像质量（可能有手写的连笔、模糊等）。

### 2. 右上角：OvisOCR2的输出
- **内容**：这是OvisOCR2模型对该手写文档的解析结果，以**文本形式**呈现（可能是Markdown或其他结构化格式，但这里主要是纯文本转录）。文本内容与原始手写文档的文字对应，尝试还原手写内容的准确性和格式（如换行、段落）。
- **作用**：展示OvisOCR2的**解析能力**，即从手写图像中识别并转录文字的准确性。通过对比原始图像和OvisOCR2的输出，可以评估模型对手写文字的识别精度（如是否正确识别连笔字、模糊字，是否保持段落结构等）。

### 3. 左下角：GLM-OCR的输出
- **内容**：这是另一个OCR模型（GLM-OCR）对该手写文档的解析结果，同样以文本形式呈现。文本中部分内容可能用**红色标注**（推测是识别错误或需要特别注意的部分，例如识别错误的文字、格式问题等）。
- **作用**：作为**对比对象**，与OvisOCR2的输出对比，展示GLM-OCR在手写文档解析上的表现。红色标注的部分可能反映了该模型的不足（如识别错误、遗漏或格式错误），从而突出OvisOCR2的优势。

### 4. 右下角：Unlimited-OCR的输出
- **内容**：这是第三个OCR模型（Unlimited-OCR）对该手写文档的解析结果，以文本形式呈现。文本的排版和内容与原始文档、OvisOCR2的输出进行对比。
- **作用**：作为另一个**对比对象**，展示Unlimited-OCR的解析结果，进一步与OvisOCR2对比，评估不同模型在手写文档解析上的性能差异（如准确性、格式还原度等）。

### 方法运作的揭示（通过对比）：
这张图通过**定性对比**展示了OvisOCR2在处理手写文档时的优势：
- **输入**：原始手写文档（Image）提供了需要解析的“真实场景”样本，包含手写文字的复杂性（如连笔、个人书写风格）。
- **模型输出**：OvisOCR2的输出（右上角）与其他模型（GLM-OCR、Unlimited-OCR）的输出（左下、右下）对比，重点观察：
  - **准确性**：OvisOCR2是否能更准确地识别手写文字（如正确的汉字、标点、段落结构）。
  - **格式还原**：是否能保持原始文档的段落、换行等格式。
  - **错误处理**：其他模型（如GLM-OCR）的红色标注部分（错误）在OvisOCR2的输出中是否被修正。

### 结论（从图中可观察到的）：
- OvisOCR2的输出（右上角）看起来更接近原始手写文档的内容和格式，而GLM-OCR的输出（左下）有红色标注的错误部分，Unlimited-OCR的输出（右下）可能在准确性或格式上也略逊于OvisOCR2。
- 这表明OvisOCR2在**手写文档解析**任务中具有更好的性能，能够更准确地识别手写文字并还原格式，验证了论文中提出的端到端文档解析方法的有效性（即OvisOCR2作为端到端模型，在复杂场景（如手写文档）下的表现优于其他对比模型）。

总结：这张图通过展示原始手写文档和三个模型（OvisOCR2、GLM-OCR、Unlimited-OCR）的解析输出，**定性比较**了它们在手写文档解析上的表现，突出了OvisOCR2的准确性和格式还原能力，支持了论文中关于OvisOCR2在手写文档解析任务中性能优越的结论。
