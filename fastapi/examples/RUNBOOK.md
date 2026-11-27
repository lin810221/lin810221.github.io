# RelayDesk操作手冊

## 正常操作

在examples目錄建立環境，先跑測試與socket_smoke。啟動API，檢查health/live、health/ready；以manage.py provision建立隨機token，啟動manage.py work。依README從本機client建立文件、提交工作、查結果、回放事件。

## 憑證與秘密

token只在佈建時顯示；資料庫只保存摘要。token不得放URL、Git、ZIP或截圖。reader只讀；editor可新增與取消。若要撤銷，可在可信任本機程式呼叫Store.revoke，或使用manage.py revoke的隱藏輸入。JWT實驗與正式OIDC分開；本服務沒有自架登入提供者。

## 重送、取消與恢復

同一次意圖保留原鍵和相同body；回409先確認是否改了問題。queued取消直接終止；running取消在worker呼叫前及發布時檢查，不保證中止已送出的模型推論或撤回費用。訂閱斷線不取消工作。計算後未發布的當機等租約到期重領，舊worker由fencing拒絕。最多三次claim，之後記attempt_limit；沒有自動人工重開介面。

## 常見故障

- queued不動：查worker、DB絕對路徑、migration與權限。
- 401：查Bearer、摘要是否存在、token是否已撤銷；不要把憑證印進log。
- 412／428：重新讀文件ETag，再決定如何處理修改衝突。
- 413：核對整體bytes、multipart overhead和檔案內容限制。
- 400表單錯誤：檢查是否超過1個檔案或帶了文字欄位。
- stale_lease：查attempt、截止與token；不可關閉fencing來強制覆寫。
- SSE不即時：先分辨本機事件尚未提交與代理緩衝，再核對idle期限。
- 已刪文件不能重傳：本課tombstone政策，409不是儲存失敗。

## 正式環境還需完成

在實際資料庫驗證鎖與時間，單獨協調migration，配置TLS與可信代理、秘密輪替、租戶配額、事件與資料保留、用量對帳、備份還原、負載與警報。SQLite只適合本課單機教學，不宣稱分散式高可用。容器與外部服務原稿需自行驗收，不能以文件存在當作部署成功。

## 關閉

先停止接單、有限排空，最後關閉HTTP client和engine。work模式Ctrl+C會退出；未提交工作的租約可供下一worker恢復。不要為了重啟隨意刪除資料庫或named volume。
