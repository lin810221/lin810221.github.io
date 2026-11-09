# 最大肌力：負荷特異性與估計公式

讀懂高負荷證據，分清研究最佳化和初學者當下需要。

## 最大力量的任務性

動作、ROM、器材和技術共同定義測試；練習較接近測試需求可能提高相應表現。ACSM2026對健康成人最大力量的最佳化支持較高負荷等條件，但不是要求所有初學者第一天就測最大或直接上高負荷。

## 相對強度的前提

以%1RM安排需有可靠且相符的參考；公式估計、舊測值或另一器材的值都可能不適用。相對負荷不包含所有努力與疲勞，仍要看實際完成與技術。

## 兩個估計

$$
\widehat{1RM}_{Epley}=L(1+r/30),\qquad
\widehat{1RM}_{Brzycki}=36L/(37-r)
$$

60kg做5次分別70與67.5kg。本課只用1–10次作教育比較，單次直接保留重量；公式不是保證個人真正最大值，也不推薦拿估值立即試舉。

## 訓練決策

先建立可控制動作、持續紀錄與合適監督；再依目標逐步安排阻力。把估計、實測與訓練重量分欄，可避免一個推估數字變成自動指令。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 22_estimated_one_rm.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:22_estimated_one_rm.py -->

## 練習與解答

**先自己判斷：** 估1RM70kg，是否表示下一堂應直接舉70kg？

<details><summary>展開理由與驗算</summary>

不是。估值有條件和誤差，訓練與測試目的不同，還需技術、準備、健康與保護條件。

</details>

## 官方來源與研究

- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [ACSM：2026正式更新與適用範圍](https://acsm.org/resistance-training-guidelines-update-2026/)
- [Exercise is Medicine：運動前篩檢表與背景](https://www.exerciseismedicine.org/wp-content/uploads/2021/04/EIM-exercise-preparticipation-screening.pdf)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
