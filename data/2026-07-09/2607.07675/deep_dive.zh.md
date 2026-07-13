# Scaling Mixture-of-Experts Video Pretraining for Embodied Intelligence

[arXiv](https://arxiv.org/abs/2607.07675) · [HuggingFace](https://huggingface.co/papers/2607.07675) · ▲53

## 摘要（原文）

> Despite the recent promise in robot control, video generative models suffer from a domain mismatch due to their primary focus on content creation. For example, their design inherently prioritizes visual fidelity and creativity over computational efficiency and physical realism. In this work, we present LingBot-Video, a DiT-based video pretraining paradigm specifically tailored for embodied intelligence. From the architecture perspective, we adopt the Mixture-of-Experts (MoE), instead of dense, framework to achieve a better trade-off between modeling capacity and inference efficiency, and manage to scale it up from scratch. From the data perspective, we construct a data profiling engine that augments standard internet videos with extensive robot-oriented footage, encompassing manipulation, navigation, and egocentric perspectives, to equip the base model with an intrinsic understanding of actions and world dynamics. From the training perspective, we develop a multi-dimensional reward system to enforce the alignment regarding physical rationality and task completion, going beyond standard criteria such as aesthetics, prompt-following, and motion consistency. Comprehensive evaluations validate its performance and efficiency as a video foundation model. We contribute LingBot-Video as the inaugural large-scale, open-source MoE video foundation model to the community, in a pioneering effort to bridge digital creativity and physical actuation.

## 摘要（中译）

尽管机器人控制领域近期取得了进展，但视频生成模型由于其主要关注内容创作而存在领域不匹配的问题。例如，它们的设计本质上优先考虑视觉保真度和创造力，而不是计算效率和物理真实性。在这项工作中，我们提出了LingBot - Video，这是一种基于DiT（可训练的图像变换器，Distributed Image Transformer）的视频预训练范式，专门为具身智能量身定制。从架构角度来看，我们采用混合专家（Mixture - of - Experts，MoE）框架而不是密集框架，以实现建模能力和推理效率之间的更好权衡，并设法从头开始对其进行扩展。从数据角度来看，我们构建了一个数据剖析引擎，该引擎用大量面向机器人的镜头（包括操作、导航和以自我为中心的视角）来增强标准的互联网视频，以使基础模型对动作和世界动态有内在的理解。从训练角度来看，我们开发了一个多维奖励系统，以强制实现物理合理性和任务完成方面的对齐，超越了美学、提示遵循和运动一致性等标准标准。全面的评估验证了其作为视频基础模型的性能和效率。我们将LingBot - Video作为首个大规模的开源MoE视频基础模型贡献给社区，在弥合数字创造力和物理驱动方面做出了开创性的努力。

## 背景剖析

要理解这篇论文的价值，首先需要明确它的应用场景：机器人控制领域正迫切需要一种能理解物理世界动态的视频预训练模型。比如让机器人学会开门、避障或模仿人类操作，这类任务需要模型既能理解动作逻辑，又能感知环境交互——但现有视频生成模型（如用于内容创作的工具）在这方面表现不佳。

过去的方法存在两个核心问题：一是过度追求视觉效果（如高清画质、创意内容），忽视了计算效率和物理真实性，导致模型在机器人任务中运行缓慢且不符合现实规律；二是缺乏针对机器人场景的专用数据，通用互联网视频多为人类的娱乐内容（如电影片段），缺少机器人视角的操作演示（如机械臂抓取、导航移动）。这使得模型难以学习到与物理世界交互的关键技能。

本文提出的解决方案是构建一个专为具身智能设计的视频预训练框架LingBot-Video。其核心思路有三点：首先，采用混合专家（MoE）架构替代传统的密集模型，在保持强大建模能力的同时提升推理效率，解决了以往模型“又慢又不实用”的问题；其次，通过数据增强引擎引入大量机器人相关视频（包括操作、导航和第一人称视角），弥补了通用数据的不足；最后，设计多维奖励系统，不仅要求视频内容合理，还要符合物理规律和任务目标（例如奖励模型预测“拿起杯子后水不会洒出”这类细节）。

与前人工作的关键差异在于，这项研究首次将MoE架构大规模应用于视频预训练，并特别针对机器人场景优化数据和训练目标。以往的视频模型要么专注内容创作，要么仅针对单一任务（如运动预测），而LingBot-Video试图成为一个通用的视频基础模型，既能支持机器人控制，又能作为具身智能研究的底层工具。这种从架构到数据再到训练目标的系统性优化，使其成为连接数字创造力与物理世界的首个开源MoE视频模型。

## 方法图解

（本文无可讲解的插图）
