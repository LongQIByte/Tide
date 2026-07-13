# Scaling Mixture-of-Experts Video Pretraining for Embodied Intelligence

[arXiv](https://arxiv.org/abs/2607.07675) · [HuggingFace](https://huggingface.co/papers/2607.07675) · ▲53

## Abstract (verbatim)

> Despite the recent promise in robot control, video generative models suffer from a domain mismatch due to their primary focus on content creation. For example, their design inherently prioritizes visual fidelity and creativity over computational efficiency and physical realism. In this work, we present LingBot-Video, a DiT-based video pretraining paradigm specifically tailored for embodied intelligence. From the architecture perspective, we adopt the Mixture-of-Experts (MoE), instead of dense, framework to achieve a better trade-off between modeling capacity and inference efficiency, and manage to scale it up from scratch. From the data perspective, we construct a data profiling engine that augments standard internet videos with extensive robot-oriented footage, encompassing manipulation, navigation, and egocentric perspectives, to equip the base model with an intrinsic understanding of actions and world dynamics. From the training perspective, we develop a multi-dimensional reward system to enforce the alignment regarding physical rationality and task completion, going beyond standard criteria such as aesthetics, prompt-following, and motion consistency. Comprehensive evaluations validate its performance and efficiency as a video foundation model. We contribute LingBot-Video as the inaugural large-scale, open-source MoE video foundation model to the community, in a pioneering effort to bridge digital creativity and physical actuation.

## Background

To appreciate this paper's significance, it’s essential to first clarify its application context: the field of robotics urgently needs a video pretraining model capable of understanding physical world dynamics. For instance, enabling robots to perform tasks like opening doors, avoiding obstacles, or imitating human actions requires the model to grasp both action logic and environmental interactions—but existing video generation models (designed for content creation) struggle with such needs.

Previous approaches faced two core limitations: 1) They prioritized visual quality (e.g., high-resolution graphics, creative content) over computational efficiency and physical realism, resulting in slow, impractical models for robotic tasks; 2) They lacked robot-specific data. Generic internet videos (e.g., movie clips) focus on human entertainment, not robot-centric perspectives (e.g., manipulations, navigation). This gap left models ill-equipped to learn skills critical for physical interaction.

The paper’s solution is LingBot-Video, a video pretraining framework tailored for embodied intelligence. Its key innovations include: 1) Adopting the Mixture-of-Experts (MoE) architecture to balance modeling capacity and efficiency, addressing the "slow and inefficient" shortcomings of dense models; 2) Building a data profiling engine to augment generic videos with robot-oriented footage (e.g., manipulation, navigation, egocentric views), filling the void in specialized data; 3) Designing a multi-dimensional reward system that enforces physical rationality and task alignment (e.g., rewarding predictions where "water doesn’t spill when picking up a cup").  

The critical difference from prior work lies in its systematic optimization across architecture, data, and training objectives. Unlike models focused solely on content creation or single tasks (e.g., motion prediction), LingBot-Video is the first open-source MoE video foundation model designed for embodied intelligence. By scaling MoE from scratch and tailoring it to robotic scenarios, it bridges the gap between digital creativity and physical actuation, serving as a foundational tool for research in this field.

## Method, Figure by Figure

(No figures to walk through.)
