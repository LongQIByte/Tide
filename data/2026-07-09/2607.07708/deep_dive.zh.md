# Accurate, Interdisciplinary and Transparent Structure-property Understanding with Deep Native Structural Reasoning

[arXiv](https://arxiv.org/abs/2607.07708) · [HuggingFace](https://huggingface.co/papers/2607.07708) · ▲84

## 摘要（原文）

> Structure-property relationships are foundational to biology, chemistry and materials science, where function, reactivity and physical response emerge from spatial, chemical and periodic organization. Mechanistically explaining these relationships requires interpreting structural evidence through scientific principles and physical constraints, from stereochemistry and bonding to symmetry, energetics and periodic order. However, applying artificial intelligence to this process presents a joint challenge of representation and reasoning: models must preserve domain-native structural information while showing how specific evidence supports predictions under these constraints. Here we introduce SciReasoner, a multimodal scientific foundation model for native structural reasoning across proteins, small molecules and inorganic crystals. SciReasoner discretizes coordinates, topologies and periodic connectivities into a unified structure-aware vocabulary, treating structural tokens as addressable evidence units during reasoning. In homology-controlled Gene Ontology prediction, SciReasoner improves Cellular Component annotation for low-homology and orphan-like proteins, increasing F_{max} from 0.42 to 0.55. In chemistry, it raises single-step retrosynthesis accuracy from 0.63 to 0.72 while generating fragment-level disconnection and precursor-verification traces. In materials science, its representations separate elemental and compound phases and resolve high- and low-band-gap regimes. Across 86 benchmarks, SciReasoner achieves state-of-the-art performance on 67 tasks. Double-blind expert evaluation rates its reasoning traces as preferred or at least comparable to those of a frontier large language model in 98% of cases. By making structure an inspectable substrate for reasoning under scientific constraints, SciReasoner connects accurate prediction with interpretable scientific inference.

## 摘要（中译）

结构-性质关系是生物学、化学和材料科学的基础，在这些学科中，功能、反应性和物理响应源于空间、化学和周期性组织。从立体化学和键合到对称性、能量学和周期性秩序，通过科学原理和物理约束来解释这些关系的机制需要解释结构证据。然而，将人工智能应用于这一过程面临着表示和推理的共同挑战：模型必须在保持领域原生结构信息的同时，展示特定证据如何在这些约束下支持预测。在这里，我们介绍了 SciReasoner，这是一个多模态科学基础模型，用于蛋白质、小分子和无机晶体的原生结构推理。SciReasoner 将坐标、拓扑和周期性连接离散化为统一的 结构感知词汇表，在推理过程中将结构令牌视为可寻址的证据单元。在同源控制的基因本体预测中，SciReasoner 提高了低同源性和孤儿样蛋白质的细胞组分注释，将 F_{max} 从 0.42 提高到 0.55。在化学领域，它将单步逆合成准确性从 0.63 提高到 0.72，同时生成片段级断开和前体验证痕迹。在材料科学中，其表示分离了元素和化合物相，并解决了高带隙和低带隙区域。在 86 个基准测试中，SciReasoner 在 67 个任务上实现了最先进的性能。双盲专家评估认为，在 98% 的情况下，其推理痕迹优于或至少与前沿大型语言模型的推理痕迹相当。通过使结构成为在科学约束下进行推理的可检查基质，SciReasoner 将准确预测与可解释的科学推断联系起来。

## 背景剖析

### 背景剖析  

**技术背景**：在生物学、化学和材料科学中，物质的“结构-性质关系”是核心问题——例如蛋白质如何通过三维结构决定功能，药物分子如何通过化学键合影响反应活性，或材料如何通过晶体排列决定导电性。科学家需要从这些复杂的空间、化学或周期性组织中提取规律，但手动分析海量结构数据（如蛋白质序列、分子构象或晶体结构）既耗时又容易出错。人工智能的介入有望自动化这一过程，但需要同时满足两个关键需求：准确预测性质（如蛋白质功能或材料能带隙），并能解释“为什么”得出该结论（即推理过程需符合科学原理）。  

**之前的问题**：现有AI模型在结构-性质关系建模中存在两大瓶颈。首先，**表示不足**：传统方法（如深度学习或图神经网络）常将结构信息简化为数值特征，丢失了领域特有的科学约束（例如化学键的立体化学规则或晶体的周期性对称性）。其次，**推理不透明**：即使某些模型能预测结果（如蛋白质功能分类），其决策过程往往是“黑箱”，无法说明哪些结构特征是关键依据，导致科学家难以信任或验证其结论。例如，低同源性蛋白质的功能预测常因缺乏相似结构参考而准确率低下，而材料科学中能带隙的预测则难以区分元素相与化合物相的影响。  

**本文的解法**：论文提出的SciReasoner模型通过三个创新点解决上述问题。其一，**统一结构表示**：将蛋白质、小分子和晶体的坐标、拓扑和周期性连接转化为一种“结构感知词汇表”，使模型能以类似人类专家的方式解析结构证据（例如将分子中的化学键或晶体中的原子排列视为可追溯的“证据单元”）。其二，**约束感知推理**：在推理过程中显式引入科学原理（如化学键合规则或能量优化），确保预测结果符合物理约束。例如，在药物合成路径预测中，模型不仅输出目标分子，还生成每一步反应的化学断键依据。其三，**可解释性增强**：通过生成详细的推理轨迹（如标注哪些结构特征支持特定预测），使科学家能验证模型的逻辑是否符合领域知识。  

**切入角度**：与前人工作相比，SciReasoner的核心差异在于**将结构本身作为推理的“可解释基底”**。以往模型要么专注于预测准确性（如忽略物理约束的纯数据驱动方法），要么依赖人工设计的规则（如缺乏泛化能力的专家系统）。而SciReasoner首次实现了“结构-性质关系”的端到端建模，既保留了领域原生信息（如分子的立体化学或晶体的周期性），又通过透明的推理过程连接了预测与科学解释。这种结合使它在跨领域任务中（如蛋白质功能注释、化学合成规划和材料相分析）显著优于现有方法，并获得了专家对其推理逻辑的高度认可。

## 方法图解

（本文无可讲解的插图）
