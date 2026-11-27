# WSGI、ASGI與正式服務入口

Django應用程式需要服務程序與網路邊界。

## 開發與正式服務

runserver提供本機除錯與重新載入，不是正式服務器。WSGI是同步Web應用介面，ASGI可支援非同步執行等模式；選擇的服務器、middleware與I/O共同決定實際行為。

下載包提供wsgi與asgi入口。Windows可使用已鎖版Waitress啟動WSGI；正式公開網站通常另有TLS反向代理，負責憑證、主機轉送、請求限制與連線管理，不能只把開發埠打開。

```powershell
waitress-serve --listen=127.0.0.1:8000 studyhub.wsgi:application
```

## 不將不同部署面混在一起

教材依舊可發佈到GitHub Pages，Django實作需另外的Python服務與資料儲存。把程式推GitHub是版本管理，不會自動配置資料庫、TLS與worker。

依實際平台配置啟動、健康檢查、日誌、程序重啟與保存位置。此處不替你開付費服務或發布私人資料；先以本機HTTP驗證，再在目標環境驗收。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大WSGI、ASGI與正式服務入口圖解"><img src="assets/figures/23.svg" alt="WSGI、ASGI與正式服務入口：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「WSGI、ASGI與正式服務入口」讀圖：沿反向代理、WSGI及資料庫追蹤請求，指出各服務的責任。再回答：把runserver綁到公開IP，是否等於正式部署？</p></div>

## 自我檢查與解析

**題目：**把runserver綁到公開IP，是否等於正式部署？

<details><summary>展開解析</summary><p>不是。正式服務還需適當服務器、TLS、主機與代理設定、資料保存、日誌及回復流程。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/howto/deployment/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
