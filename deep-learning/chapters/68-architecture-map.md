# 架構地圖：從CNN、Transformer到圖與生成模型

以資料結構、訊息交換方式與訓練目標整理架構，而非把所有名稱排成新舊名次。

## 兩個不同的分類軸

CNN、RNN、Transformer描述計算與連接方式；對比學習、分類、重建、去噪描述訓練目標。同一Transformer可做分類、對比或生成；Diffusion的denoiser也可採不同骨幹。因此看到模型名稱，先問它的輸入、主幹、目標及推論流程，避免把架構等同於應用能力。

## 卷積與patch Attention

CNN用局部共享權重處理規則網格，天然帶有某些位置結構；ViT把影像切成patch，映射成token，結合位置資訊與Attention。ViT不是「把像素丟給聊天模型」，CNN也未被所有任務淘汰。資料、預訓練、解析度、預算與歸納偏置共同影響結果，本課不宣稱任何架構是2026所有任務的最佳解。

## 遞迴、Attention與長度成本

RNN以狀態逐步壓縮歷史，標準dense self-attention則建立token兩兩互動。前者有逐步依賴，後者的注意力矩陣對長度是平方規模；具體效能仍受實作、記憶體與硬體影響。位置編碼、mask與cache改變使用方式，不能只看一個大O就宣布實機速度。

## 圖神經網路的起點

節點與邊表達不規則關係，message passing聚合鄰居訊息再更新節點。要考慮節點順序不應改變圖的語意、邊方向、聚合方式與多跳範圍。典型GCN以正規化鄰接矩陣聚合特徵；它不是將圖表圖片送進CNN，也不是LangGraph工作流程節點的同義詞。

$$
H^{(l+1)}=\sigma\!\left(\widetilde D^{-1/2}\widetilde A
\widetilde D^{-1/2}H^{(l)}W^{(l)}\right)
$$

此為加入self-loop後的典型GCN形式；不是所有GNN都使用這個公式。本課僅建立閱讀入口，沒有宣稱已實作完整圖學習課程。

## 生成模型與表示學習的交會

AE／VAE壓縮表示、對比學習塑造相似性、Diffusion和Flow學動態變換，彼此可組合但目標不同。更複雜的系統常同時含encoder、生成主幹與後處理。閱讀新論文時，把新模組放回資料—表示—目標—最佳化—評估這條線，會比背縮寫更有用。

## 練習與解答

「用了Transformer，所以是自回歸LLM」哪裡有問題？答案：主幹不能決定訓練目標、token種類或mask。它也可能是影像分類器、雙向encoder或去噪網路；需查看資料、loss與推論流程。

## 原始論文與官方來源

- [ViT原始論文](https://arxiv.org/abs/2010.11929)
- [GCN原始論文](https://arxiv.org/abs/1609.02907)
- [Transformer原始論文](https://arxiv.org/abs/1706.03762)
