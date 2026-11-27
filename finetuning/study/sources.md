# 來源、版本與驗收範圍

查核：2026-11-25。軟體採當日穩定版；歷史研究保留原出版時間。

- [torch 2.15.0](https://pypi.org/project/torch/2.15.0/)
- [transformers 5.24.1](https://pypi.org/project/transformers/5.24.1/)
- [peft 0.22.0](https://pypi.org/project/peft/0.22.0/)
- [trl 1.18.2](https://pypi.org/project/trl/1.18.2/)
- [accelerate 1.16.0](https://pypi.org/project/accelerate/1.16.0/)
- [datasets 5.2.0](https://pypi.org/project/datasets/5.2.0/)
- [safetensors 0.8.0](https://pypi.org/project/safetensors/0.8.0/)
- [tokenizers 0.23.3](https://pypi.org/project/tokenizers/0.23.3/)
- [numpy 2.5.5](https://pypi.org/project/numpy/2.5.5/)
- [pyarrow 26.0.1](https://pypi.org/project/pyarrow/26.0.1/)

- [Python正式版本](https://www.python.org/downloads/)
- [LoRA原始研究](https://arxiv.org/abs/2106.09685)
- [QLoRA原始研究](https://arxiv.org/abs/2305.14314)
- [DPO原始研究](https://arxiv.org/abs/2305.18290)
- [DoRA原始研究](https://arxiv.org/abs/2402.09353)
- [rsLoRA原始研究](https://arxiv.org/abs/2312.03732)
- [Soft prompt原始研究](https://arxiv.org/abs/2104.08691)
- [蒸餾原始研究](https://arxiv.org/abs/1503.02531)
- [領域持續預訓練](https://arxiv.org/abs/2004.10964)
- [GRPO：DeepSeekMath](https://arxiv.org/abs/2402.03300)
- [SFTTrainer鎖版文件](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)
- [DPOTrainer鎖版文件](https://huggingface.co/docs/trl/v1.18.2/dpo_trainer)
- [PEFT量化指南](https://huggingface.co/docs/peft/v0.22.0/developer_guides/quantization)
- [OpenAI微調](https://developers.openai.com/api/docs/guides/supervised-fine-tuning)
- [Gemini API微調狀態](https://aistudio.google.com/docs/model-tuning)
- [Google Cloud監督調整](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/tuning/supervised-tuning)

CPU主線使用原創合成資料與本地初始化小模型，實測資料、模板、SFT、PEFT、DPO、續訓與成品。GPU四位元、分散式與付費雲端工作未執行，須依實際平台驗收；原創圖中數字不代表大型模型效能。

Transformers與Accelerate連結採本次可讀的官方穩定文件入口，頁面可能隨未來版本更新；實測API與重現基準以本課鎖版及程式測試為準，不把動態文件頁當作不可變版本。
