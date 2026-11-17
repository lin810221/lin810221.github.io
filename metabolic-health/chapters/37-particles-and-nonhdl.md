# 血脂不只一個膽固醇：粒子與non-HDL

理解運輸系統，並計算non-HDL-C。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/19-particle-vessel-wall.svg" target="_blank" rel="noopener" aria-label="放大：脂蛋白粒子與動脈壁"><img src="assets/figures/19-particle-vessel-wall.svg" alt="左側粒子與右側動脈壁示意不同尺度；斑塊是壁內過程，不是油脂把管腔簡單塗滿。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 19｜脂蛋白粒子與動脈壁</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>辨識脂質核心、粒子與血中膽固醇量，再說明non-HDL-C是在同單位下的差值，不等於所有粒子數的直接計數。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.nhlbi.nih.gov/health/atherosclerosis">NHLBI：動脈粥狀硬化的血管壁過程</a> · <a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 脂質需要運輸

膽固醇參與細胞膜與合成，三酸甘油酯是能量儲存形式。它們在血中藉脂蛋白運送；LDL、HDL、VLDL等描述不同粒子群，檢驗的膽固醇濃度不等於粒子總數，也不是所有脂質共用一個換算因子。

## non-HDL的定義

總膽固醇減去HDL膽固醇，得到non-HDL-C，包含多種帶有致粥狀硬化潛力的脂蛋白所攜帶膽固醇。兩項必須同一單位與可比較檢體；不是拿總膽固醇減去三酸甘油酯。

## 算術和目標分開

TC=200、HDL-C=50 mg/dL時，non-HDL-C=150 mg/dL。這個差值本身不決定個人疾病或治療，目標需依風險與指南。若HDL大於總膽固醇，應查資料，而不是把負數截成零。

## 為何有多項指標

LDL-C、non-HDL-C和apoB各提供不同訊息，尤其在三酸甘油酯較高或代謝情境下可能不一致。2026指南說明何時補充指標有價值，而不是所有人每次都測完整套。缺少HDL時，程式輸出未知，不假定HDL正常。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 19_non_hdl.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:19_non_hdl.py -->

## 練習與解答

**先自己判斷：** TC200、HDL50、TG150，non-HDL是否為50？

<details><summary>展開驗算與理由</summary>

不是。non-HDL=TC−HDL=150 mg/dL，TG不在這個減式。這是同單位算術，不是個人治療目標判定。

</details>

## 官方來源與研究

- [2026血脂指南官方摘要](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/top-things-to-know)
- [2026血脂指南正式原文](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
