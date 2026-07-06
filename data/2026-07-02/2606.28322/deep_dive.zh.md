# PerceptionRubrics: Calibrating Multimodal Evaluation to Human Perception

[arXiv](https://arxiv.org/abs/2606.28322) · [HuggingFace](https://huggingface.co/papers/2606.28322) · ▲39

## 摘要（原文）

> We introduce PerceptionRubrics, a rubric-based evaluation framework that addresses the gap between saturated benchmark scores and real-world brittleness. Shifting evaluation from holistic semantic matching to rigorous atomic auditing, PerceptionRubrics pairs 1,038 information-dense images with over 12,000 instance-specific rubrics. These criteria are derived from golden captions constructed via a novel Circular Peer-Review consensus pipeline and then distilled into a dual-stream system of Must-Right (essential facts) and Easy-Wrong (fine-grained details) rubrics. Crucially, PerceptionRubrics implements a Gated Scoring mechanism: unlike linear averages, failure on mandatory visual facts triggers sharp binary penalties. Extensive evaluation yields critical insights: (1) The Reliability Gap: models often verify fragmented elements correctly yet fail strict conjunctive constraints, exposing brittleness in dense domains; (2) Open-Closed Stratification: contrary to reasoning trends, we reveal a persistent 8% perception deficit between open-source and proprietary frontiers; and (3) Human-Aligned Rigor: our gated metrics substantially out-align conventional benchmarks, validating that strict perceptual fidelity is the prerequisite for reliable generation.

## 摘要（中译）

我们引入了PerceptionRubrics，这是一种基于评分标准的评估框架，旨在解决饱和的基准分数与现实世界中的脆弱性之间的差距。将评估从整体语义匹配转向严格的原子审计，PerceptionRubrics将1,038张信息密集型图像与超过12,000个特定实例的评分标准配对。这些标准是通过一种新颖的循环同行评审共识管道构建的金色标题派生的，然后提炼成必须正确（基本事实）和容易错误（细粒度细节）的双流评分标准系统。关键的是，PerceptionRubrics实现了一种门控评分机制：与线性平均值不同，强制视觉事实的失败会触发急剧的二元惩罚。广泛的评估产生了关键的见解：（1）可靠性差距：模型通常正确验证分散的元素，但在严格的连接约束上失败，暴露了密集领域的脆弱性；（2）开放-封闭分层：与推理趋势相反，我们揭示了开源和专有前沿之间持续的8%的感知缺陷；（3）与人类对齐的严谨性：我们的门控指标在很大程度上超越了传统基准，验证了严格的感知保真度是可靠生成的前提条件。

## 背景剖析

### 背景剖析  

**技术背景**：多模态大模型（MLLMs）正被广泛应用于图像理解、内容生成等场景（如智能助手解析截图、AI生成报告校验），核心需求是让模型具备“人类级别的感知可靠性”——即不仅能回答问题，还要在复杂视觉信息中准确识别细节（如图表数据、空间关系）。例如，医疗影像分析需要模型精准定位病灶，而现有基准测试却无法有效验证这种能力。  

**之前的问题**：当前评估体系存在两大缺陷：一是**数据覆盖不足**，多数基准使用信息简单或领域狭窄的图像（如单一物体分类），导致模型依赖语言先验（而非真实视觉理解）；二是**评分机制失真**，传统指标（如CLIPScore）通过线性平均掩盖局部错误，例如模型即使误判表格数字仍能得高分，但这种错误在现实中是“零容忍”的。这导致排行榜高分模型在实际部署中表现脆弱（如漏看关键物体），形成“高分数≠高可靠性”的悖论。  

**本文的解法**：论文提出PerceptionRubrics框架，通过三步解决问题：首先，构建包含1,038张高信息量图像的数据集，并通过“循环同行评审”机制生成“黄金标准描述”（由多模型迭代优化并经人工验证）；其次，将这些描述拆解为12,000+条原子级规则，分为“必须正确”（如关键事实）和“容易错误”（如细节偏差）两类；最后，引入“门控评分”机制——若违反“必须正确”规则则直接扣分，确保评分与人类对严重错误的敏感度一致。  

**切入角度**：与先前工作不同，PerceptionRubrics不追求“整体语义匹配”，而是聚焦“细粒度感知审计”。它通过**数据驱动的规则提取**（从模型错误中学习）和**非线性评分**（区分致命错误与次要偏差），填补了基准测试与真实场景间的鸿沟。这种方法不仅揭示了模型在复杂域中的可靠性缺陷（如开源与闭源模型的8%感知差距），还为未来模型优化提供了可解释的诊断工具。

## 方法图解

![Figure 1 : Motivation of PerceptionRubrics . Top: An existing benchmark favors G](fig1_1.webp)

> Figure 1 : Motivation of PerceptionRubrics . Top: An existing benchmark favors GPT-4o despite key omissions, while humans prefer responses that capture more perceptually important details. Bottom: Compared with DetailCaps and DOCCI, PerceptionRubrics more clearly distinguishes model capabilities.

这张图是论文《PerceptionRubrics: Calibrating Multimodal Evaluation to Human Perception》中的Figure 1，旨在说明PerceptionRubrics方法的动机。我们可以将图分为上下两个主要部分来理解：

**上半部分：现有基准测试的局限性**

1.  **左侧图像**：展示了一张示例图片，内容是一条公路，右侧路肩上有一个年轻人在玩滑板（或类似活动）。这张图片是评估模型感知能力的视觉输入。
2.  **模型输出对比**：
    *   **Gemini-3-Pro** 的描述被高亮显示，它指出了图像右侧的一个关键元素：“最引人注目的是道路右侧，可能是一个匝道或路肩车道。一个年轻人正在玩滑板（看起来像长板），与高速公路交通平行。他穿着黑色长袖……” 这个描述提到了“路肩车道”和“滑板”等细节。
    *   **GPT-4o** 的描述则提到：“图像右侧，一个人在路肩上滑旱冰，穿着黑色上衣和浅色裤子。” 这个描述将活动误认为是“滑旱冰”，并且没有提到“路肩车道”这一重要背景信息。
3.  **DetailCaps 评分**：这是一个现有的基准测试。图中显示GPT-4o在DetailCaps上的得分为70.92（用绿色字体和对勾表示，似乎暗示其表现较好），而Gemini-3-Pro的得分为62.41。这表明在DetailCaps这样的基准测试中，GPT-4o获得了更高的分数。
4.  **人类判断 (Human Judge)**：这部分是关键，它展示了人类评估的结果。人类判断认为“Gemini-3-Pro 表现更好，因为它提到了：”
    *   一个年轻人在玩滑板
    *   高速公路/路肩车道
    *   红白相间的塑料施工护栏（图中未完全显示，但文本提及）
    这表明尽管GPT-4o在DetailCaps上得分更高，但人类更认可Gemini-3-Pro的描述，因为它捕捉到了更多重要的感知细节。这揭示了现有基准测试（如DetailCaps）可能与人类真实感知存在差距——模型可能在碎片化元素上正确，但在严格的逻辑约束（如同时正确识别关键背景和主体）上失败。

**下半部分：PerceptionRubrics 方法的有效性验证**

1.  **柱状图**：这是一个对比不同模型在三个不同基准测试上的性能表现的图表。
    *   **X轴**：代表三个不同的基准测试，分别是 `DetailCaps`、`DOCCI` 和 `PerceptionRubrics`。
    *   **Y轴**：代表“Performance”（性能），数值范围从0到80。
    *   **图例**：不同颜色的柱子代表不同的模型：
        *   蓝色：Gemini-3-Pro
        *   浅绿色：Qwen3-VL-235B
        *   粉色：GPT-4o
        *   黄色：GPT-5.4
        *   紫色：Qwen3-VL-8B
2.  **数据对比与结论**：
    *   在 `DetailCaps` 基准上，各模型的性能差异相对较小，柱子高度较为接近。例如，Gemini-3-Pro和GPT-4o的得分都在60分以上，其他模型也相差不远。
    *   在 `DOCCI` 基准上，所有模型的性能都显著低于DetailCaps，且模型间的差异也比较小，得分普遍在20分以下。
    *   在 `PerceptionRubrics` 基准上，模型间的性能差异变得非常明显。Gemini-3-Pro的得分最高（约70分），其次是GPT-5.4（约60分），Qwen3-VL-235B（约40分），Qwen3-VL-8B（约30分），而GPT-4o的得分最低（约10分）。
    *   这个对比表明，与DetailCaps和DOCCI相比，PerceptionRubrics能够更清晰地区分不同模型的能力。在PerceptionRubrics下，表现好的模型和表现差的模型之间的差距拉大了，这说明PerceptionRubrics作为一个评估框架，能更有效地衡量模型在严格感知任务上的表现。

**整体信息流与方法解释**：

1.  **问题提出**：上半部分通过一个具体的例子和人类判断，指出现有基准测试（如DetailCaps）可能无法准确反映人类的真实感知，因为它们可能奖励了某些不重要的细节而忽略了关键的、必须正确的视觉事实。
2.  **方法介绍**：虽然图中没有直接展示PerceptionRubrics的具体实现步骤（如Circular Peer-Review共识管道、Must-Right和Easy-Wrong rubrics、Gated Scoring机制），但它通过下半部分的实验结果暗示了该方法的设计目标：创建一个能更严格、更细致地评估模型感知能力的基准，特别是区分那些能准确捕捉关键视觉事实的模型和那些不能的模型。
3.  **结果展示**：下半部分的柱状图显示，PerceptionRubrics确实能够更好地分离不同模型的性能，这验证了该方法的优越性。它通过引入更精细的、基于人类感知的评估标准（即原子审计），实现了对模型能力的更准确校准。

总结来说，这张图通过对比现有基准测试（DetailCaps和DOCCI）和PerceptionRubrics在模型评估上的表现，揭示了PerceptionRubrics方法的核心动机和有效性：它旨在解决饱和基准分数与现实世界脆弱性之间的差距，通过更严格的原子级审计来校准多模态评估，使其更符合人类感知。

---

![Figure 4 : The PerceptionRubrics Construction Pipeline. Adopting a caption-centr](fig4_1.webp)

> Figure 4 : The PerceptionRubrics Construction Pipeline. Adopting a caption-centric approach, we first synthesize golden captions via circular peer-review (Top). These captions then serve as anchors to generate Must-Right and Easy-Wrong rubrics through domain-specific prompting (Bottom).

这张图展示了PerceptionRubrics的构建流程，整体分为**上方的“黄金描述生成”**和**下方的“规则（rubrics）生成”**两个核心阶段，信息按以下顺序流动：  


### 1. 黄金描述（Golden Captions）的生成（上方流程）  
- **输入**：一张信息密集的图像（左侧展示的拉斯维加斯街道场景）。  
- **初始候选（Initial Candidates）**：首先生成多个候选描述（如Candidate1、Candidate2、Candidate3），这些描述是对图像的不同初步解读（例如描述场景风格、建筑特征、标志等）。  
- **循环同行评审（Circular Peer Review）**：候选描述进入“循环同行评审”模块，该模块通过**Compare（比较）、Rank（排序）、Rewrite（重写）**三个步骤迭代优化：  
  - 多个AI（图中“AI”图标）和人类注释（“Human Annotations”）参与评审，对候选描述进行比较、排序，然后基于反馈重写，形成新的候选集\( C^{(i)} \)。  
  - 这个过程是“循环”的，即重写后的描述会再次进入比较-排序-重写，直到达成共识。  
- **输出：黄金描述（Golden Captions）**：经过多轮评审后，最终得到一个权威的“黄金描述”，它是对图像的精准、共识性解读（例如图中详细描述了街道场景、“LAS VEGAS”文本、标志等）。  


### 2. 规则（Rubrics）的生成（下方流程）  
黄金描述作为“锚点”，通过**领域特定提示（Domain-Specific Prompt）**生成两类规则：  

- **Must-Right（必须正确的事实）**：这类规则是图像的**核心、必要事实**，模型必须准确识别才能得分。例如：  
  - 识别场景为街道/商业区；  
  - 提到包含“LAS VEGAS”的标志、拱门或广告牌；  
  - 提到特定文本的位置等。  
  （图中“Must Right”板块列出了这些强制要求，若模型失败会触发“二进制惩罚”——即不得分）。  

- **Easy-Wrong（精细细节）**：这类规则是**易混淆、细粒度的细节**，模型容易错误判断。例如：  
  - 场景中无明显人群；  
  - 无双层巴士；  
  - 背景不是霓虹灯广告牌主导等。  
  （图中“Easy Wrong”板块列出了这些细节，用于测试模型的精细感知能力）。  

- **规则生成的触发**：通过“领域特定提示”（图中黄色灯泡图标下的文本），将黄金描述转化为“规则生成策略”（“Step 1: Rubric Generation Strategy...”），并结合“响应池（Response Pool）”中的示例（如不同风格的描述），最终生成“黄金规则（Golden Caption）”对应的规则集，同时还有“规则生成器（Rubric Generator）”（AI）参与优化。  


### 方法的核心逻辑  
PerceptionRubrics的核心是**从“整体语义匹配”转向“原子级审计”**：  
- 先通过“循环同行评审”构建权威的“黄金描述”（解决描述的主观性）；  
- 再基于黄金描述生成“必须正确”（强制事实）和“精细错误”（细粒度细节）的规则，用“门控评分（Gated Scoring）”机制评估模型：若模型未满足“必须正确”的事实，会直接扣分（二进制惩罚），而不仅仅是线性平均。  


### 流程的信息流动总结  
图像 → 初始候选描述 → 循环同行评审（AI+人类迭代优化）→ 黄金描述 → 领域特定提示 → 生成“必须正确”和“精细错误”规则（结合响应池和规则生成器）。  

这一流程确保了评估标准（规则）既基于人类共识（黄金描述），又覆盖了“核心事实”和“精细细节”，从而校准多模态评估与人类感知的差距。

---

![Figure 5 : Distribution of golden caption lengths in our benchmark. The histogra](fig5_1.webp)

> Figure 5 : Distribution of golden caption lengths in our benchmark. The histogram shows the word count frequency across the dataset.

这张图是论文《PerceptionRubrics: Calibrating Multimodal Evaluation to Human Perception》中的图5，标题为“Golden Caption Length Distribution”，即“黄金描述长度分布”。它展示了一个直方图，用于呈现我们基准测试集中“黄金描述”（golden captions）的单词数量频率分布。

首先，我们来理解图中的各个组件：

1.  **X轴（横轴）**：标记为“Words per golden caption”，表示每个“黄金描述”所包含的单词数量。刻度从0开始，向右延伸至3500，主要的刻度点包括500、1000、1500、2000、2500、3000和3500。这代表了描述的长度。
2.  **Y轴（纵轴）**：标记为“Number of images”，表示具有相应单词数量的“黄金描述”的图像数量。刻度从0开始，向上延伸至200，主要的刻度点包括25、50、75、100、125、150、175和200。这代表了对应长度的描述的频率。
3.  **直方图条形**：蓝色的垂直条形构成了直方图。每个条形的高度对应Y轴上的图像数量，其宽度代表X轴上一个特定的单词数量区间（bin）。例如，在X轴大约500的位置，有一个很高的条形，表明有大量图像的“黄金描述”长度接近500个单词。从左到右，条形的高度先升高后降低，形成一个峰值，然后逐渐平缓下降，说明大多数“黄金描述”的长度集中在某个范围内，而非常长或非常短的描述相对较少。
4.  **中位数（Median）**：一条橙色的虚线，垂直于X轴，标注为“Median = 569”。这条线表示所有“黄金描述”长度的中位数，即有一半的描述长度小于或等于569个单词，另一半则大于或等于569个单词。从图中可以看出，这个中位数位于直方图的峰值附近，表明数据的中心趋势。
5.  **平均值（Mean）**：一条绿色的虚线，垂直于X轴，标注为“Mean = 770.4”。这条线表示所有“黄金描述”长度的平均值。值得注意的是，这个平均值（770.4）明显高于中位数（569），这通常意味着数据分布是右偏的（正偏态），即存在一些较长的描述拉高了平均值，而大多数描述相对较短。这与直方图的形状相符，右侧有一些较矮但延伸较长的尾部。

这张图揭示了“黄金描述”的长度分布情况。这些“黄金描述”是通过论文中提到的“新颖的循环同行评审共识流程”（Circular Peer-Review consensus pipeline）构建的，是评估模型生成内容质量的基础。通过分析这些描述的长度，我们可以了解基准测试中文本标注的特性。例如，中位数约为569个单词，平均值为770.4个单词，说明大多数描述长度适中，但也存在一些较长的描述。这种分布信息对于后续的评估框架设计（如PerceptionRubrics）是重要的，因为它影响了评估标准的制定和模型的预期表现。例如，如果描述很长且包含很多细节，那么评估模型是否能够准确捕捉这些细节就变得至关重要。

总结来说，这张图通过直方图的形式清晰地展示了基准测试中“黄金描述”的单词数量分布，并通过中位数和平均值突出了数据的集中趋势和整体平均水平。这对于理解论文中所使用的评估数据集的特性至关重要。

---

![Figure 12 : Qualitative examples of the fine-grained rubrics across four categor](fig12_1.webp)

> Figure 12 : Qualitative examples of the fine-grained rubrics across four categories: Natural Scene, Document & OCR, Digital UI & UX, and Structured Data. Each example consists of an image and two tiers of rubrics: Must-Right (top group) focusing on core facts, and Easy-Wrong (bottom group) focusing on challenging details, negative constraints, and logical reasoning.

这张图（图12）来自论文《PerceptionRubrics: Calibrating Multimodal Evaluation to Human Perception》，它通过四个类别——自然场景（Natural Scene）、文档与OCR（Document & OCR）、数字UI与UX（Digital UI & UX）以及结构化数据（Structured Data）——展示了精细评估标准（rubrics）的定性示例。

该图的核心目的是说明PerceptionRubrics方法中使用的评估标准是如何构建和组织的。每个类别板块都包含一个示例图像和两组评估标准。这些标准分为“必须正确”（Must-Right，通常是顶部的一组）和“容易错误”（Easy-Wrong，通常是底部的一组）。

“必须正确”的标准关注核心事实，即图像中最基本、最关键的元素，模型必须正确识别这些元素才能通过评估。例如，在“自然场景”类别中，“必须正确”的标准包括：图像展示的是蔬菜或新鲜农产品，物品排列在架子、货架或多层展示架上，能识别出特定的蔬菜（如叶菜、卷心菜、西兰花、胡萝卜或芹菜），以及一些具体的空间关系（如某人指向或手势指向右臂等）和禁止性描述（如不得提及文本、标志或现代车辆）。

“容易错误”的标准则侧重于具有挑战性的细节、负面约束和逻辑推理。这些标准通常更细微，要求模型能够捕捉到更复杂的视觉信息或理解图像中的逻辑关系。例如，在“自然场景”类别中，“容易错误”的标准包括：底部的紫色卷心菜、底部架子上的圆形白色或浅绿色卷心菜、从顶部数第二层架子上的红色根茎蔬菜（如萝卜）等，以及一些禁止性描述（如不得将第二层的圆形蔬菜描述为黄色）。

这种方法的具体运作方式是：首先，通过一种名为“循环同行评审”（Circular Peer-Review）的共识管道构建“黄金标题”（golden captions），这些标题是图像的详细描述。然后，将这些标题提炼成“必须正确”和“容易错误”两类评估标准。这种双重流系统确保了评估的严谨性，不仅检查模型是否能识别基本事实，还能检查其是否能处理更精细的细节。

此外，论文中提到的“门控评分”（Gated Scoring）机制在这种评估中起着关键作用。与线性平均不同，如果在“必须正确”的视觉事实上失败，会触发严重的二元惩罚（即得零分）。这种机制强调了严格符合基本事实的重要性，这对于在密集领域（如图像理解）中实现可靠的生成至关重要。

通过这四个类别的示例，图中展示了PerceptionRubrics如何通过精细的评估标准来校准多模态评估，以使其更符合人类的感知。这种方法揭示了模型在处理碎片化元素时可能表现良好，但在严格的联结约束下可能失败，从而暴露了其在密集领域的脆弱性。

总之，这张图通过具体的示例清晰地展示了PerceptionRubrics方法的核心思想：通过构建精细的“必须正确”和“容易错误”评估标准，结合门控评分机制，来实现对多模态模型的更严格、更符合人类感知的评估。

---

![Figure 13 : Qualitative examples of the fine-grained rubrics across three additi](fig13_1.webp)

> Figure 13 : Qualitative examples of the fine-grained rubrics across three additional categories: Logic & Puzzle, STEM & Expert, and Creative & Cultural. Each example consists of an image and two tiers of rubrics: Must-Right (top group) focusing on core facts, and Easy-Wrong (bottom group) focusing on challenging details, negative constraints, and logical reasoning.

这张图来自论文《PerceptionRubrics: Calibrating Multimodal Evaluation to Human Perception》，展示了该方法中“精细评分标准（fine-grained rubrics）”在三个不同类别中的定性示例：逻辑与谜题（Logic & Puzzle）、STEM与专业领域（STEM & Expert）以及创意与文化（Creative & Cultural）。其核心目的是说明PerceptionRubrics框架如何通过具体的、分层的标准来评估图像内容。

这张图的结构清晰地分为三个主要板块，每个板块对应一个类别，并遵循一致的布局模式：

1.  **逻辑与谜题（Logic & Puzzle）**：
    *   **左侧文本区域**：这部分列出了该类别图像的“必须正确”（Must-Right）和“易错/难对”（Easy-Wrong）的评分标准。
        *   “必须正确”的标准包括：工作表的标题是“HOW MANY!”或包含计数形状的指示；中央区域散布着多种几何图形（如心形、星星、圆形、矩形、五边形）；底部答案区域由带有空框的特定形状对组成；指令文本是“Count the similar shapes and write the correct number”；黄色几何形状是矩形或倾斜条（非正方形）；黑色几何形状是三角形；中央有两个黑色三角形；深蓝色形状是八边形（或停止标志形状）；底部答案输入框为空或空白；并且答案输入框中不得出现深蓝色八边形出现在底部答案键区域的描述。
    *   **右侧图像区域**：展示了一个符合上述标准的示例图像，即一个包含各种颜色和形状的“HOW MANY!”工作表，以及一个用于填写答案的表格。
    *   **信息流动**：左侧的标准定义了图像应具备的特征，右侧的图像则是一个符合这些特征的实例。读者可以通过对比标准和图像来理解评分的具体要求。

2.  **STEM与专业领域（STEM & Expert）**：
    *   **左侧文本区域**：同样列出了“必须正确”和“易错/难对”的标准。
        *   “必须正确”的标准包括：层次化的营养级标签为“生产者”、“食草动物”、“食腐动物”和“食肉动物”；中央标签明确为“食肉动物和杂食动物”（或注明特定的杂食动物，如图像中可见的羚羊）；摄影缩略图中描绘了特定的物种（如金合欢树、长颈鹿、狮子、河马或秃鹫）；顶部的“食腐动物”层包含文本标签（如白蚁、细菌、真菌）而非照片；食物网或生态系统图包含五个层次；两个食腐动物被描绘为鬣狗和秃鹫；特定的物种在食草动物层，包括长颈鹿、羚羊和黑曼巴；特定的动物在食肉动物层，包括食草动物和食肉动物（此处原文可能有误，应为具体的食肉动物）；三个不同的树种被标记为金合欢树、猴面包树等。
    *   **右侧图像区域**：展示了一个生态系统的食物网图表，包含不同物种的照片和连接它们的线条，代表了能量流动。
    *   **信息流动**：左侧的标准定义了图像在科学内容和表示上应具备的准确性，右侧的图像则是一个符合这些标准的生态图示例。

3.  **创意与文化（Creative & Cultural）**：
    *   **左侧文本区域**：列出了针对电影海报的“必须正确”和“易错/难对”的标准。
        *   “必须正确”的标准包括：这是一部电影海报；标题文本为“BROTHERHOOD OF BLADES”；构图中有三个中心人物或男性；武器如剑和数字“3”；字幕文本为“INFERNO BATTLEFIELD”；罗马数字“III”为红色或深红色；中心人物的姿势是手臂伸展或张开。
        *   “易错/难对”的标准包括：演员名字（如张震、杨幂）位于顶部边缘；背景中的人物（左侧）戴着高顶礼帽；中文书法或字符覆盖在中心人物上；背景不得描述为温暖、阳光明媚或色彩鲜艳（而是冷色调/去饱和/灰色）。
    *   **右侧图像区域**：展示了一张《刀锋兄弟会》（Brotherhood of Blades）的电影海报，上面有演员、标题和符合描述的视觉元素。
    *   **信息流动**：左侧的标准定义了电影海报在内容和视觉表现上应具备的特征，特别是那些细微的、容易出错的细节，右侧的海报则是一个符合这些标准的实例。

**方法运作的解释**：
这张图揭示了PerceptionRubrics方法的具体运作方式。该方法的核心是将评估从整体的语义匹配转变为严格的原子级审计。它通过以下步骤实现：
*   **创建黄金标准说明（Golden Captions）**：首先，通过一种新颖的“循环同行评审”（Circular Peer-Review）共识流程构建详细的图像说明。这些说明捕捉了图像的所有关键事实和细节。
*   **提炼评分标准（Distilling Rubrics）**：然后，将这些黄金标准说明提炼成“必须正确”（Must-Right）和“易错/难对”（Easy-Wrong）两种类型的评分标准。
    *   **“必须正确”标准**：关注核心事实，是评估的强制性要求。如果模型未能满足这些标准，将会受到严厉的二进制惩罚（即得分为零或严重扣分）。
    *   **“易错/难对”标准**：关注具有挑战性的细节、负面约束和逻辑推理，这些是区分模型性能高低的关键点。
*   **实施门控评分机制（Gated Scoring Mechanism）**：与线性平均不同，该方法实施的门控评分机制意味着，如果在任何“必须正确”的视觉事实上失败，将会触发严重的惩罚，即使其他方面表现良好。这种机制强调了严格感知保真度的重要性。
*   **应用示例**：图中展示的三个类别（逻辑与谜题、STEM与专业领域、创意与文化）分别代表了不同类型的图像内容和评估重点。通过为每种类型的图像提供具体的、分层的标准，PerceptionRubrics能够对模型的感知能力进行细致、严格的评估。

这张图通过具体的例子展示了PerceptionRubrics如何运作：为每张图像定义一套详细的、分层次的评估标准（“必须正确”和“易错/难对”），然后用这些标准来衡量模型对图像内容的理解和再现能力。这种方法旨在解决传统基准测试在密集领域（如复杂图像理解）中的脆弱性问题，确保评估结果更能反映模型在真实世界场景中的可靠性。
