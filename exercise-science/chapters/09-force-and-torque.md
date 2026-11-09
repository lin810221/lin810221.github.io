# 力、力臂與力矩：同重量為何難度不同

從向量與垂直距離推導力矩，學會清楚標單位。

## 力與質量

kg描述質量，N描述力；簡化地表重力可用F=mg，但加速、支撐與其他力還需另外處理。器材寫20kg不表示任何時刻、任何方向的手部或關節力都等於固定值。

## 力矩的幾何

$$
\tau=Fr\sin\theta
$$

F是外力、r是從轉軸到施力點的距離，θ是兩向量夾角；也可用外力乘垂直力臂。單位N·m，和同樣使用N·m的能量在概念上不同，力矩不是已做多少功。

## 手算與角度

100N、0.3m、90°得到30N·m；夾角30°時為15N·m。角度改變會改變有效力臂；不要用兩個向量長度相乘而漏sin。本課算的是大小，沒有完整正負方向、慣性或多肌肉協同。

## 不直接推出人體內力

肌肉的內部力臂可能與外力臂很不同，多條肌肉共同參與。外力矩模型幫助提問，但不能由30N·m直接宣稱某肌腱承受100N，也不能據此判姿勢是否造成傷害。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 05_lever_arm.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:05_lever_arm.py -->

## 練習與解答

**先自己判斷：** 100N、0.3m與30°算多少？能否把結果當肌腱受力？

<details><summary>展開理由與驗算</summary>

15N·m。這是簡化外力矩，肌腱內力需要額外幾何、協同與動態模型，不是同一個量。

</details>

## 官方來源與研究

- [OpenStax：神經控制與肌肉張力](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-4-nervous-system-control-of-muscle-tension)
- [OpenStax：肌纖維收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
