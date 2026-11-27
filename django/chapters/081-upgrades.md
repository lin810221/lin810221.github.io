# 更新Django與相依套件

查當日穩定版，再在隔離環境驗證遷移。

## 不把版本標籤當作升級

本課以Django 6.1.3與Python 3.15.2為基準。未來更新時查官方release notes、相容Python、資料庫與相依套件，再建立獨立環境安裝。舊教材的API只在閱讀與遷移情境解釋，不直接當現行主線。

先處理deprecated警告與破壞性變更，跑Model、表單、認證、API、檔案及部署檢查。新版新功能如fetch modes也需實際套件驗證匯入與行為，不只從文章記憶複製名稱。

## 資料與回復一起考慮

確認migration能在資料副本套用，資產與模板相容，測試及操作主線仍成立。若有schema或資料語意變更，程式回退未必足夠；先規劃回復與相容期。

更新完成後同步鎖版、原稿、程式包、來源日期與驗證紀錄。不能只改首頁寫最新版本，卻讓讀者安裝到未測的相依組合。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/27.svg" target="_blank" rel="noopener" aria-label="放大更新Django與相依套件圖解"><img src="assets/figures/27.svg" alt="更新Django與相依套件：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「更新Django與相依套件」讀圖：從症狀選最小反例，說明要蒐集什麼證據才能判定原因。再回答：只將requirements裡版本加大，其他測試都沒跑，算完成更新嗎？</p></div>

## 自我檢查與解析

**題目：**只將requirements裡版本加大，其他測試都沒跑，算完成更新嗎？

<details><summary>展開解析</summary><p>不算。還要驗證API、資料、相依與部署行為，並同步教材與實測紀錄。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/howto/upgrade-version/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
