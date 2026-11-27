# 設定、環境變數與秘密

設定模組是Python程式，環境變數不會自動從.env讀入。

## 三種環境的界線

本課分本地、測試與正式設定。測試使用記憶體資料庫、記憶體郵件及儲存；正式設定關閉DEBUG並要求明確密鑰與hosts。不能因測試環境比較快，就把測試密碼雜湊器帶到正式網站。

```powershell
$env:DJANGO_SETTINGS_MODULE="studyhub.production"
$env:DJANGO_ALLOWED_HOSTS="your-domain.example"
```

實際密鑰應透過作業系統或部署平台注入，不寫進教材與公開設定。`os.environ` 讀取的是程序環境，本專案不會自動載入 `.env`；若加入相關工具，要明確記錄新的依賴與啟動方式。

## 不同設定要各自檢查

本地設定可以使用清楚標示的開發密鑰與本機hosts，正式模組則在缺必要值時中止。用 `--settings=studyhub.testing` 指定測試設定，避免管理命令不小心改到自己的練習資料。

檢查結果應附設定模組與資料庫位置，不能只寫「check通過」。後續正式部署還要確認HTTPS、反向代理、檔案與備份；單一設定檔無法替代整個環境驗收。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大設定、環境變數與秘密圖解"><img src="assets/figures/03.svg" alt="設定、環境變數與秘密：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「設定、環境變數與秘密」讀圖：沿路由比對順序找到View，再檢查reverse的參數與名稱。再回答：建立.env後設定沒有改變，可能是什麼原因？</p></div>

## 自我檢查與解析

**題目：**建立.env後設定沒有改變，可能是什麼原因？

<details><summary>展開解析</summary><p>本專案只讀程序環境，不會自動解析.env；應按文件注入環境變數，或明確加入並驗證載入工具。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/settings/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
