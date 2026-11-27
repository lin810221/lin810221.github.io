# 版本來源、實測與界線

把教材日期、軟體版本與驗證環境明確連起來。

## 本課基準

2026-11-26查核Django官方下載、PyPI與相容表，主線使用Django 6.1.3、Python 3.15.2、DRF 3.18.3、WhiteNoise 6.12.0與Waitress 3.0.2。完整相依、來源與可選PostgreSQL驅動版本見 `study/versions.json` 與程式包鎖版。

官方文件使用6.1系列，實際API以安裝的6.1.3測試確認。其他既有課程保留其原更新日與版本，不能因新課完成而宣稱全站套件同時升級。

## 驗證內容

程式包實測Model、migration、表單、認證、擁有者、CSRF、附件、API、查詢、交易、Tasks、async view及fetch mode。Django Client與實際HTTP各有範圍；DOM、SVG點陣預覽與真實瀏覽器版面也分開記錄。

外部PostgreSQL、SMTP、共享快取及真正背景worker沒有因本地替身通過就被標為已整合。正式雲端發布與網域設定也需目標環境驗收。

## 教材維護

課文是UTF-8 Markdown，公式用LaTeX，圖解是可放大的原創SVG，下載包附學習單與解析。修改後同步原稿、實作、鎖版、測試與生成檔，並檢查模板及CSS確實在程式包內，避免只有作者工作目錄可跑。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/28.svg" target="_blank" rel="noopener" aria-label="放大版本來源、實測與界線圖解"><img src="assets/figures/28.svg" alt="版本來源、實測與界線：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「版本來源、實測與界線」讀圖：沿版本、測試與回復流程，指出交接前最後需要確認的內容。再回答：查核官方文件就足以宣稱範例已實測嗎？</p></div>

## 自我檢查與解析

**題目：**查核官方文件就足以宣稱範例已實測嗎？

<details><summary>展開解析</summary><p>不夠。需在對應環境執行並保存結果；文件查核、靜態檢查與實際執行是不同證據。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/intro/install/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
