# 內外負荷與session-RPE

用一致量表描述整堂感受，知道AU不是不同運動的精準等價劑量。

## 內外負荷

重量、次數、距離與時長是外在描述，主觀感受與心率等反映部分內在反應。相同外在量可有不同感受，兩者都值得記，不必強迫轉成同一生理單位。

## 整堂負荷示例

$$
L_{session}=duration_{min}\times sRPE_{CR10}
$$

45分鐘×5得到225AU；30分鐘×7.5也是225AU。這個相同乘積不表示兩種活動的肌肉、能量或傷害風險相同，只在明示量表與收集方法下提供描述。

## 收集問題要一致

問整堂而非某一組，記何時收集、量表版本與作答方式。原始session-RPE研究有其程序，不能把工作途中某個最高RPE、Borg6–20或單組RIR直接搬進同欄。

## 紀錄的使用

用來看自身同方法的趨勢和計畫完成，結合任務、恢復與功能。工具不把225AU轉為熱量、肌肉刺激或可訓練許可；若有未知時長或感受，完整負荷也保留未知。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 37_session_load.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:37_session_load.py -->

## 練習與解答

**先自己判斷：** 兩堂都225AU，是否可認定對力量和心肺的刺激完全一樣？

<details><summary>展開理由與驗算</summary>

不能。乘積相同不代表任務結構或生理作用相同；AU是描述，需同量表方法與其他背景。

</details>

## 官方來源與研究

- [Foster等：session-RPE原始研究](https://pubmed.ncbi.nlm.nih.gov/11708692/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Impellizzeri等：ACWR概念與方法陷阱](https://pubmed.ncbi.nlm.nih.gov/32502973/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
