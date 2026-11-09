# 衝量、快速產力與跳躍

從力時關係理解起跳，不把高度直接當整段產力能力。

## 力與時間

$$
J=\int F_{net}\,dt=\Delta p
$$

衝量單位N·s，需明確是淨外力。平均淨力200N維持0.2秒，衝量40N·s；真實起跳需要完整力時資料、體重與起始條件，不把地面反力總量無聲當淨力。

## 產力速率的界線

快速產力關注很短時間內力的變化，測量會受取樣、起點和訊號處理影響。峰值力量、衝量和跳高各看不同特徵，不能只憑一個跳高數字反推完整神經肌肉狀態。

## 技能也影響高度

擺臂、起始姿勢、下蹲深度、接觸規則與測量方法會改變結果。前後比較需同協定；若改了擺臂，就不能全把差值歸因腿部產力適應。

## 教學與執行

介紹公式不要求讀者做最大跳躍測試。選擇練習需考慮落地控制、表面、目前能力和適當指導；量的記錄需寫次數、接觸與任務，不以一個衝量值判安全。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 23_impulse.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:23_impulse.py -->

## 練習與解答

**先自己判斷：** 200N是總地面反力卻未扣重力，可以直接叫起跳淨衝量嗎？

<details><summary>展開理由與驗算</summary>

不能。公式需明確淨外力和時間條件，總反力、體重與其他外力要分清；否則動量解讀會錯。

</details>

## 官方來源與研究

- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [OpenStax：神經控制與肌肉張力](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-4-nervous-system-control-of-muscle-tension)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [ACSM：2026正式更新與適用範圍](https://acsm.org/resistance-training-guidelines-update-2026/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
