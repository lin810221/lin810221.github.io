# 自我調節、雙重漸進與觀察條件

示範規則如何支持討論，不讓程式直接替真人加量。

## 規則不是生理定律

雙重漸進可先在指定區間追次數，再考慮負荷；自我調節則使用當下反應等資訊。不同目標與情境有不同方法，不能以一個達標條件取代技術、耐受和健康背景。

## 虛構判定

給定區間上界10，實做10、10、10但RIR為2、2、未知；工具回所有組達上界、努力資料不完整。它不因次數夠就輸出「加5kg」，因其他條件尚未確認。

## 另一個情境

實做10、9、8且RIR皆2，表示指定次數條件未全達，並不等於必須退步或方案失敗。還需休息、順序、目標與趨勢；同一規則只適用自己定義的任務和資料。

## 應保留的紀錄

規則版本、實際組次、RIR不確定、ROM、技術與調整理由。自我調節的價值在明確回饋，不是保證每堂完美最佳化。課內範例只回觀察狀態，不開個人處方。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 29_progression_observation.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:29_progression_observation.py -->

## 練習與解答

**先自己判斷：** 三組都做十次但RIR缺一筆，是否程式應自動判準備好加量？

<details><summary>展開理由與驗算</summary>

不應。只可描述次數條件達到和RIR不完整；技術、反應及適用背景仍需確認，不能由缺值給出增加許可。

</details>

## 官方來源與研究

- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [ACSM：2026正式更新與適用範圍](https://acsm.org/resistance-training-guidelines-update-2026/)
- [Foster等：session-RPE原始研究](https://pubmed.ncbi.nlm.nih.gov/11708692/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
