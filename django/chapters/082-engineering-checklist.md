# Django工程完成清單

用可重跑的成果確認這門課真正串起來。

## 功能與資料

確認環境可重建、migration可建立schema、帳號流程正常、CRUD與分頁可操作。資料表約束、跨帳號拒絕、tag範圍、私人附件與API都具有對應測試，不只看成功頁面。

## 工程與維護

確認快取包含owner且會失效，交易與on_commit用途清楚，Tasks的inline與真正worker分開，async沒有掩蓋同步阻塞。記錄SQLite已測與PostgreSQL待測範圍，避免不正確的併發結論。

## 交付與部署

程式包包含模板、CSS、migration與測試，沒有帶入私人資料。正式設定檢查、資產收集、資料與檔案備份、日誌與回復方案都有說明；真實網域及外部服務由目標環境驗收。

最後以乾淨環境重做安裝、migrate、建立帳號、seed、啟動與測試。這張清單用於本課成果，不取代實際產品的需求與審查；它讓下一次擴充知道從哪個已驗證基準開始。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/28.svg" target="_blank" rel="noopener" aria-label="放大Django工程完成清單圖解"><img src="assets/figures/28.svg" alt="Django工程完成清單：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Django工程完成清單」讀圖：沿版本、測試與回復流程，指出交接前最後需要確認的內容。再回答：程式包漏掉templates，但原作者電腦能開網站，哪項驗收會發現？</p></div>

## 自我檢查與解析

**題目：**程式包漏掉templates，但原作者電腦能開網站，哪項驗收會發現？

<details><summary>展開解析</summary><p>乾淨環境解壓與啟動測試，以及下載包內容對照。不能只在原工作目錄測試。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
