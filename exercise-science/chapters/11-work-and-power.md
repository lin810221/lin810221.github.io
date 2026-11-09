# 機械功、功率與代謝能量

知道kg-reps、J、W和kcal不能直接互換。

## 三個不同的量

功涉及力沿位移的累積，功率是做功速率；代謝能量則是身體消耗的化學能。等長保持外在位移接近零，不代表沒有肌肉用力或代謝需求；外在正功也未涵蓋全身全部能量。

$$
W_{external}=mgh,\qquad P_{average}=W_{external}/t
$$

## 算術例子

20kg外物上升0.5m，以g=9.80665m/s²，外在正功約98.07J。用1秒完成平均98.07W，2秒約49.03W；同功不同功率。這沒有計人體各節段、下降負功或效率。

## 噸數不是功

3組、8次、40kg得到960kg-reps，沒有位移和力方向，不能直接當J或熱量。不同器材與ROM的噸數不可無條件比大小後排適應效果；需同動作與記錄方式才有描述意義。

## 訓練用途

功率目標需要看速度、技術與可控負荷，不是所有動作都越快越好。功率儀、影片時間與外在位移的估計也有誤差，不能把小數精度當真實準確度。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 06_work_and_power.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:06_work_and_power.py -->

## 練習與解答

**先自己判斷：** 等長保持外物不動，外在功約零，是否代表人體沒消耗能量？

<details><summary>展開理由與驗算</summary>

不是。外在位移功與肌肉內部代謝不同，仍可能用力及消耗能量；不能由mgh的零推全身能量零。

</details>

## 官方來源與研究

- [OpenStax：肌纖維收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)
- [OpenStax：神經控制與肌肉張力](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-4-nervous-system-control-of-muscle-tension)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [Compendium：標準MET單位](https://pacompendium.com/unite-conversions/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
