# 正式靜態檔與儲存策略

資產收集、版本與私人檔案分別管理。

## 使用正式設定收集

正式模組使用CompressedManifestStaticFilesStorage，collectstatic產生帶內容版本的檔名與manifest。模板static標籤依儲存設定取得正確URL，瀏覽器快取才可跟版本協調。

WhiteNoise可服務適合的靜態資產，並不自動成為私人上傳檔案的授權儲存。MEDIA_ROOT與STATIC_ROOT不能只因都放檔案就共用；使用者內容有不同的大小、保存、刪除與權限需求。

## 發布順序與回復

新程式與manifest、CSS等資產必須相容。若HTML指向不存在的雜湊檔，會出現資產錯誤；不要用永遠停用快取掩蓋不完整發布。保留必要舊資產與版本回復策略。

本課可在本地收集並透過實際HTTP檢查CSS，但CDN、外部物件儲存與地區快取需要各自整合驗證。不要把檔案存在磁碟等同所有使用者都能載入。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大正式靜態檔與儲存策略圖解"><img src="assets/figures/23.svg" alt="正式靜態檔與儲存策略：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「正式靜態檔與儲存策略」讀圖：沿反向代理、WSGI及資料庫追蹤請求，指出各服務的責任。再回答：collectstatic完成後，私人附件也會自動安全提供嗎？</p></div>

## 自我檢查與解析

**題目：**collectstatic完成後，私人附件也會自動安全提供嗎？

<details><summary>展開解析</summary><p>不會。靜態資產建置與私人檔案授權是不同流程，後者仍需受控下載或相應儲存政策。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/howto/static-files/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
