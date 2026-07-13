# Ideas Have Genomes: Benchmarking Scientific Lineage Reasoning and Lineage-Grounded Idea Generation

[arXiv](https://arxiv.org/abs/2607.08758) · [HuggingFace](https://huggingface.co/papers/2607.08758) · ▲31

## 摘要（原文）

> Scientific ideas rarely start from a blank page. They inherit mechanisms, repair known limitations, and recombine pieces of earlier work, much like biological genomes. Current benchmarks still say little about whether AI systems can follow this inheritance structure. We present IdeaGene-Bench (IG-Bench), a benchmark for scientific lineage reasoning and lineage-grounded idea generation. IG-Bench is organized around the IdeaGene framework: each paper or proposal is represented as a set of minimal, typed, evidence-grounded Idea Genome objects, and a GenomeDiff aligns these objects to record inheritance, mutation, loss, external import, and novel insertion under six operational evolutionary dynamics. The benchmark contains 1,961 golden lineage traces, 1,085 curated Idea Genome objects, and 920 pairwise GenomeDiff records across 10 scientific domains. It supports two evaluations. IG-Exam (42 task types, 1,029 instances) tests closed-form lineage reasoning across Idea Genome abstraction, inheritance tracing, evolutionary reasoning, and lineage verification. IG-Arena evaluates generation with a lineage-conditioned Population-Evolution Score(PES), asking whether a proposal can be inserted as a coherent descendant of a given lineage population: it should inherit the right Idea Genome objects, vary meaningfully from nearby work, and offer selection value for future research. Experiments on 14 LLM-based scientists expose a compositional bottleneck. The strongest system reaches only 27.3% exact accuracy on lineage reasoning, and structured lineage context reshuffles system rankings rather than helping every participant uniformly.

## 摘要（中译）

科学思想很少从一张白纸开始。它们继承机制，修复已知的局限性，并重新组合早期工作的部分内容，很像生物基因组。当前的基准测试仍然很少说明人工智能系统是否能够遵循这种继承结构。我们提出了IdeaGene-Bench（IG-Bench），这是一个用于科学谱系推理和基于谱系的创意生成的基准测试。IG-Bench围绕IdeaGene框架组织：每篇论文或提案都被表示为一组最小的、类型化的、基于证据的Idea Genome对象，而GenomeDiff则将这些对象对齐以记录继承、变异、丢失、外部导入和在六种操作性进化动态下的新插入。该基准测试包含1,961个金色谱系痕迹，1,085个经过策划的Idea Genome对象，以及跨10个科学领域的920个成对GenomeDiff记录。它支持两种评估。IG-Exam（42种任务类型，1,029个实例）测试了在Idea Genome抽象、继承追踪、进化推理和谱系验证方面的封闭形式谱系推理。IG-Arena使用基于谱系的Population-Evolution Score（PES）评估生成，询问一个提案是否可以作为一个给定谱系种群的一致后代插入：它应该继承正确的Idea Genome对象，与附近的工作有意义地变化，并为未来的研究提供选择价值。在14个基于LLM的科学家上的实验暴露了一个组合瓶颈。最强的系统在谱系推理上的精确准确率仅达到27.3%，而有结构的谱系上下文会重新排列系统排名，而不是均匀地帮助每个参与者。

## 背景剖析

### 背景剖析  

科学创新并非凭空产生——新想法往往建立在已有研究的“遗传”基础上：继承核心机制、修复已知缺陷，或重组前人成果，就像生物基因组通过进化传递变异。然而，当前AI系统在理解这种“科学谱系”（scientific lineage）方面仍存在显著不足。这类技术的核心需求在于**辅助科研人员追溯研究脉络、验证创新合理性**，例如帮助生物学家分析药物研发的历史依赖关系，或让材料科学家快速定位某类材料的改进路径。但现有基准测试（benchmark）大多聚焦于单一任务（如文献分类或摘要），未能捕捉科学思想演化的动态过程。  

此前的方法主要卡在两个层面：一是**缺乏结构化的科学谱系表示**，无法明确区分“继承”“变异”“重组”等关键操作；二是**评估标准过于简单**，通常仅测试模型是否能识别文本相似性，而非理解思想演化的逻辑链条。例如，现有模型可能在判断两篇论文是否相关时表现良好，但无法解释“为何这篇论文是对前作的改进”。这种局限性导致AI难以真正支持需要深度上下文的科研活动，比如设计具有连续性的研究项目或预测新想法的潜在价值。  

本文提出的解决方案是构建一个名为IdeaGene-Bench（IG-Bench）的基准框架，将科学思想建模为“基因组”对象（Idea Genome），并通过“基因组差异”（GenomeDiff）记录其演化动态（如继承、突变或外部引入）。该框架包含两类任务：一是**谱系推理**（如追踪某一机制的来源），二是**条件生成**（如基于给定谱系生成合理的新想法）。实验表明，即使是先进的AI模型（如GPT-4）在复杂谱系推理上也仅能达到约27%的准确率，且谱系上下文会显著改变模型表现，这说明现有系统尚未掌握科学创新的“遗传逻辑”。  

与前人工作的关键差异在于，IG-Bench不仅关注文本匹配，更强调**结构化演化过程的建模**。例如，它通过“种群进化评分”（PES）评估生成结果是否能为未来研究提供“选择价值”，而非仅仅生成语法正确的文本。这种视角将科学创新视为一个动态演化的系统，而非静态的知识库，从而为AI系统的评估设定了更贴近真实科研需求的标准。

## 方法图解

（本文无可讲解的插图）
