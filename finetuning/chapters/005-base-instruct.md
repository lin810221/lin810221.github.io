# 基底模型、指令模型與授權

起點不同，所需資料與可能退步的能力也不同。

## 選擇的是整套模型契約

基底模型主要學續寫分布；指令模型已經過某種後訓練，具有特定角色、停止符號與聊天模板。相同權重大小不代表能交換tokenizer或模板。選模型時記錄精確repository revision、config、tokenizer、授權及可用的推論格式。

本課的隨機初始化Llama只是架構實驗，沒有繼承任何大型預訓練模型的知識。真正專案常從已具語言能力的模型出發，評估領域語言、上下文長度、工具使用、硬體與授權條件，再決定完整微調或PEFT。

## 授權與成品必須一起看

公開可下載不等於任意再散布。檢查權重授權、衍生模型條款、訓練資料權利與服務限制；adapter也可能受基底條款約束。模型卡要交代訓練用途、限制、評估及資料來源，不應僅填一個模型名稱。

若把不同revision的同名模型當作同一基底，adapter可能可以載入卻產生不同結果。交付時保存可驗證的內容雜湊或不可變revision，並將tokenizer與聊天模板納入身分。模型能成功啟動只是第一道檢查，還需要固定輸入的行為回歸。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener"><img src="assets/figures/02.svg" alt="基底模型、指令模型與授權：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「基底模型、指令模型與授權」讀圖：沿版本身分走到成品，指出本單元需要保存的檢查紀錄。再回答：adapter檔很小，是否因此能不附基底模型資訊？</p></div>

## 自我檢查與解析

**題目：**adapter檔很小，是否因此能不附基底模型資訊？

<details><summary>展開解析</summary><p>不能。adapter依賴精確基底與tokenizer；也要核對衍生使用及再散布條件，不能由檔案大小推論授權。</p></details>

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/peft/v0.22.0/developer_guides/checkpoint)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
