# 版本原始論文與持續更新

<figure class="tf-figure"><a href="assets/figures/32-debug-decision-tree.svg" target="_blank" rel="noopener"><img src="assets/figures/32-debug-decision-tree.svg" alt="問題分成loss不下降生成異常cache不一致三條路，分別檢查shift更新、詞表解碼、位置與矩形遮罩。" loading="lazy"></a><figcaption>Transformer除錯路線。先定位資料、學習或推論哪一層失效，再選擇下一個能排除假說的測試。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>選本頁一個概念對照圖中shape、公式或除錯分支，說出下一個需要核對的條件。 本頁主題：版本原始論文與持續更新。</p></div>

## 這份版本表的時間意義

查核日期為2026-11-24，時區Asia/Taipei。本課依當日可用的正式發布、套件索引與固定tag建立基準；鎖定版本是為了讓你重現，不是宣稱它們未來仍是最新版。Nightly、RC和主分支文件另看，不能只因數字較大就選為穩定教材。

套件版本、文件證據與實際執行是三種紀錄。找到wheel表示有對應發行檔，不證明全部功能已驗證；讀到CUDA文件也不證明CPU有相同行為。課內CPU測試、DOM閱讀器測試與尚未測量的GPU／外部模型能力，應各有明確範圍，不由這張表互相替代。

## 軟體基準與正式來源

| 元件 | 穩定版本 | 發布日期 | 官方來源 |
|---|---|---|---|
| Python | 3.15.2 | 2026-10-25 | [Python發布頁](https://www.python.org/downloads/release/python-3152/) |
| PyTorch／torch | 2.15.0 | 2026-10-28 | [PyPI](https://pypi.org/project/torch/2.15.0/) |
| Transformers | 5.24.0 | 2026-11-21 | [PyPI](https://pypi.org/project/transformers/5.24.0/) |
| Tokenizers | 0.23.3 | 2026-10-09 | [PyPI](https://pypi.org/project/tokenizers/0.23.3/) |
| Safetensors | 0.8.0 | 2026-06-09 | [PyPI](https://pypi.org/project/safetensors/0.8.0/) |
| NumPy | 2.5.5 | 2026-11-15 | [PyPI](https://pypi.org/project/numpy/2.5.5/) |

Python使用一般GIL版本；平台、CPU架構與free-threaded分支不同時，應重新核對發行檔。Tokenizers的1.0.0rc5雖是較新的預覽序列，不取代本表0.23.3正式基準。需求檔鎖定直接相依，完整重現還需記錄實際解析的傳遞相依與平台。

## API證據採固定版本

PyTorch SDPA的bool True表示可參與attention；MultiheadAttention的bool遮罩True則表示阻擋。矩形`is_causal=True`的對齊方式也不能當成帶past offset的尾段query。本課以2.15官方文件和明確數值測試核對，不把名稱相似視為語意相同。

- [SDPA 2.15](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)
- [MultiheadAttention 2.15](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)
- [Lower-right因果bias](https://docs.pytorch.org/docs/2.15/generated/torch.nn.attention.bias.causal_lower_right.html)

Transformers的可讀文件可能隨預設版本移動；5.24部分版本化文件網址不完整時，以固定tag原始碼核對。當前Llama範例採`cache=`與`outputs.cache`，不把舊別名或未實際使用的參數當成新主線。

- [Llama 5.24 modeling](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/models/llama/modeling_llama.py)
- [DynamicCache 5.24](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/cache_utils.py)
- [TokenizersBackend 5.24](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/tokenization_utils_tokenizers.py)
- [Tokenizers 0.23.3官方API](https://huggingface.co/docs/tokenizers/v0.23.3/en/api/tokenizer)

## 原始架構與表示研究

下列年份表示研究首次提出或正式發表的歷史時點，不把存取日當成論文的新版本。讀完先重現一個小性質，再評估實驗結果是否可移植。

| 問題 | 原始資料 | 本課閱讀重點 |
|---|---|---|
| 注意力與encoder／decoder | [Attention Is All You Need，2017](https://arxiv.org/abs/1706.03762) | QKV、multi-head與架構分工 |
| BPE子詞 | [Sennrich等，2015／2016](https://arxiv.org/abs/1508.07909) | 詞表與合併規則，不混同byte和字 |
| 輸入輸出權重共享 | [Press與Wolf，2016／2017](https://arxiv.org/abs/1608.05859) | 共用參數與輸出分數 |
| RoPE | [RoFormer，2021](https://arxiv.org/abs/2104.09864) | 旋轉內積與相對位置 |
| GQA | [Ainslie等，2023](https://arxiv.org/abs/2305.13245) | query heads與KV heads分離 |
| 稀疏expert | [Switch，2021](https://arxiv.org/abs/2101.03961) | token路由與活躍／總參數 |

## 效率、後訓練與可靠性研究

| 問題 | 原始資料 | 本課閱讀重點 |
|---|---|---|
| IO-aware attention | [FlashAttention，2022](https://arxiv.org/abs/2205.14135) | 分塊和線上softmax，區分IO與算術 |
| KV分頁 | [PagedAttention，2023](https://arxiv.org/abs/2309.06180) | 邏輯頁、實體配置與服務狀態 |
| 草稿驗證 | [Speculative decoding，2022／2023](https://arxiv.org/abs/2211.17192) | 接受規則與目標分布 |
| 人類偏好 | [InstructGPT，2022](https://arxiv.org/abs/2203.02155) | 示範、獎勵與policy流程 |
| 直接偏好目標 | [DPO，2023](https://arxiv.org/abs/2305.18290) | policy相對reference的差值 |
| Attention可解釋性 | [Jain與Wallace，2019](https://arxiv.org/abs/1902.10186)及[Wiegreffe與Pinter，2019](https://arxiv.org/abs/1908.04626) | 明確定義解釋、介入與對照 |

這些研究是機制與方法的來源，不表示本課已複現其大規模訓練、硬體速度或benchmark。課內online softmax、量化與標量DPO例子提供可檢查的局部性質；真實服務或模型對齊還需額外資料、系統與評估。

## 下一次更新的具體流程

先查正式release與PyPI，再核對Python和平台wheel、直接相依範圍及重要破壞性變更。建立新的隔離環境，安裝鎖定組合，保存實際版本。接著跑數學、mask、shift、訓練、保存重讀、cache、HF離線與閱讀器驗收，對失敗項查固定tag和最小案例，不為了通過而直接放寬所有容差。

原創更新案例：假設未來framework將cache欄位改名，舊程式仍能輸出logits。更新者應檢查回傳狀態是否真的增長、mask和位置是否仍對齊，以及同一輸入cache／完整路徑是否一致；只改import後看到一段文字，證據不足。完成後同步改原稿、需求、範例、測試、下載包與版本說明，保留本次實際修改範圍。

舊課程日期仍代表它們當時的基準，不因本課更新就一律換成新日期。若外部權重、GPU或分散式功能沒有重跑，直接記錄條件和未驗證項目；穩定版查核、靜態檢查與實測通過分欄保存。

## 練習與解析

**題目：** 文件首頁顯示新API，但PyPI穩定版與版本tag仍是舊介面；你應把哪個寫成必裝基準？

**解析：** 先確認首頁是否指向main、nightly或RC，交叉查正式release、套件metadata與可安裝檔。教材主線採當日可安裝且實測通過的穩定組合；預覽功能另列版本與條件。不能只按文件頁面更新日期，推論讀者已能安裝該功能。
