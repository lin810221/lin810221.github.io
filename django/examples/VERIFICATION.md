# 實測紀錄與界線

2026-11-26，Windows x64、Python3.15.2、Django6.1.3、DRF3.18.3、WhiteNoise6.12.0、Waitress3.0.2。完整七個相依見requirements-lock.txt。

## 已執行的核心

Python unittest與Django runner執行43項測試，涵蓋全部24個獨立實驗、Model與DB約束、migration、登入登出、密碼重設與token失效、ModelForm與tag範圍、HTML及API跨帳號拒絕、CSRF、私人附件、查詢數、回滾、on_commit、快取隔離、Tasks、async view及6.1 fetch modes。

實際Waitress loopback HTTP驗證健康、登入、取得表單、建立任務與API列表；使用本地測試設定及合成帳號，不是公開TLS部署。本次另檢查程式包內模板、CSS與migration並於解壓後的獨立目錄執行測試。

正式設定的check --deploy沒有ERROR，但保留security.W005與security.W021兩個HSTS條件警告。是否控制所有子網域、是否適合preload，需按真實網域決定；沒有隱藏或強制套用。collectstatic實際執行成功。

## 驗收限制

SQLite不提供與PostgreSQL相同的列鎖與競爭語意；本課沒有啟動真實PostgreSQL並行、外部SMTP、共享快取、外部storage或真正queue worker。ImmediateBackend同程序立即執行，locmem郵件不會真的寄出。

教材另有84單元閱讀器與8個JavaScript示意實驗的DOM檢查、28張SVG字型及邊界預覽、公式靜態KaTeX與下載包檢查。JavaScript示意不是Python runtime；DOM與SVG預覽也不等於真實瀏覽器的桌面／手機版面驗收。本次沒有可連線瀏覽器，該項版面驗收未完成。

GitHub Pages能提供教材，無法執行本Django專案。實際發布需Python服務、儲存、網域、TLS與維運配置。
