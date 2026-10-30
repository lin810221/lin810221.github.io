# 自監督、預訓練與微調：目標如何塑造表示

比較重建、遮罩預測、對比與蒸餾式方法的共同資料邊界。

## 沒有人工作業label仍有訓練目標

自監督從資料構造target，例如遮罩內容、不同view對應或下一位置。它降低對某種人工標籤的依賴，不代表完全沒有假設、清理成本或資料權限。模型可學到來源捷徑，也可能從預訓練資料記住評估內容。

## 幾種目標的差別

重建偏好保留可重建資訊，對比依positive／negative拉開關係，遮罩預測依上下文補內容，teacher-student方式依目標表示與穩定化策略。不同架構與目標可結合，不宜只用一個新方法名字代替流程說明。

## Collapse與防護機制

若所有表示相同仍能滿足某個過度簡單目標，會失去資訊。負例、停止梯度、動量teacher、variance／covariance限制等可在不同方法中使用，各有假設；不是只加detach就自動得到有效自監督學習。需要看原始目標與實際評估。

## 表示與適應的評估

linear probe固定backbone只學線性head，fine-tune更新更多層，二者回答不同問題。公平比較要記預訓練資料、算力、下游label量與調參預算；較少下游epochs不代表總訓練成本較低。group/time與資料污染仍要檢查。

## 與本課範例的關係

第33例只測in-batch對比數學與grad，不宣稱重現完整SimCLR；AE／VAE篇實際學低維重建；第60章以小teacher/student示範distillation。這些讓你看見目標差異，之後可沿原始論文與獨立Embedding課深化。

## 自己設計一個檢查

若表示只記住拍攝設備，使用同設備的linear probe可能很好，換設備就失效。可以按資料來源分組切分，再比較within-source與held-out-source結果；同時查看表示是否幾乎相同、是否只分出來源而沒有任務訊號。這比只展示一張漂亮的二維投影更直接回答「表示是否有用」。預訓練中沒有下游label，也不會自動消除來源偏差或資料污染。

## 練習與解答

用同一圖片增強產生兩view，若增強改掉label語意，positive仍合理嗎？答案：不一定，會要求模型忽略你真正關心訊號。解答要連回下游任務、失敗樣本與表示評估，而不只看對比loss下降。模型學的是你設計的目標，不是自動知道你的用途。

## 原始論文與官方來源

- [SimCLR](https://arxiv.org/abs/2002.05709)
- [Representation learning](https://www.deeplearningbook.org/contents/representation.html)
