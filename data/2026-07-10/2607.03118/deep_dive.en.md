# Vidu S1: A Real-Time Interactive Video Generation Model

[arXiv](https://arxiv.org/abs/2607.03118) · [HuggingFace](https://huggingface.co/papers/2607.03118) · ▲127

## Abstract (verbatim)

> We introduce Vidu S1, a real-time interactive video generation model supporting voice control of digital characters. Users can control video generation content at any moment through voice instructions. Vidu S1 supports infinite-length real-time video generation without blurring, drift, or visual distortion. Built with TurboDiffusion and TurboServe, Vidu S1 outputs 540p real-time videos at up to 42 FPS on regular consumer GPUs. Users can upload custom images of real people, anime, and pets, and choose different voice tones for personalized experiences. Experiments show that Vidu S1 achieves the best performance across all test metrics while fully meeting real-time inference requirements. A playable online demo is available at https://vidu.com/vidu-stream.

## Background

### Background Analysis  

With the increasing popularity of digital content creation, real-time interactive video generation technology has shown great potential in fields like entertainment, education, and virtual assistants. For instance, users may want to engage in natural conversations with virtual characters or dynamically adjust video content (e.g., changing scenes or character actions) via voice commands. The core requirements for such technology are **low-latency, high-fidelity** real-time generation, while also supporting personalized inputs (e.g., custom images) and multimodal interactions (e.g., voice control). However, existing methods still face significant challenges in these areas.  

Previous research was mainly limited by two key issues: first, the **trade-off between generation efficiency and quality**—traditional models either generated content too slowly (failing to meet real-time requirements) or suffered from blurring, drifting, or distortion during prolonged generation; second, **insufficient interactivity flexibility**—most systems relied on pre-defined scripts or static inputs, making it difficult to respond to dynamic voice commands or user-uploaded personalized content. These limitations made it hard for existing technologies to deploy on consumer-grade hardware and provide a smooth user experience.  

The core innovation of Vidu S1 lies in **breaking the real-time and quality bottleneck through the TurboDiffusion and TurboServe architectures**. Specifically, TurboDiffusion optimizes the computational efficiency of diffusion models, enabling them to generate 540p videos at 42 FPS on regular consumer GPUs; meanwhile, TurboServe further reduces latency through an efficient inference pipeline. Additionally, the model supports users uploading custom images (e.g., real people, anime characters, or pets) and controlling content in real time via voice commands, addressing the interactivity limitations of traditional methods.  

Compared to previous work, the key difference of Vidu S1 is its **"end-to-end real-time interaction" design philosophy**. It not only pursues generation speed but also ensures stability during prolonged generation (without blurring or drifting), while achieving true personalization through multimodal fusion of voice and images. Experiments show that Vidu S1 achieves state-of-the-art performance across all test metrics while fully meeting real-time inference requirements, marking an important step toward the practical deployment of real-time interactive video generation technology.

## Method, Figure by Figure

(No figures to walk through.)
