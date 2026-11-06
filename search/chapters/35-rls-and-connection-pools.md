# RLS、角色與連線池：資料隔離不只一個 WHERE

將可信身分映射到交易範圍，明確檢查管理者、擁有者與連線重用的例外。

## 雙層資料資格

應用層仍加入 tenant Filter，資料庫可再使用 Row-Level Security 保護讀寫。Policy 的 USING 控制可見行，WITH CHECK 控制新值是否可寫。RLS 不是一個開關就萬無一失；superuser、BYPASSRLS 與 table owner 有特殊行為，需依官方規則以真正 app role 測試。

## 交易內設定主體

本課 policy 參考 current_setting('app.tenant_id',true)，查詢前用 set_config(...,true) 作 transaction-local 設定。連線池重用後不應殘留前一位使用者租戶。tenant 必須由已驗證的請求邊界產生，模型不可獲得可執行任意 SQL 或自行更改租戶設定的權限。

## FORCE RLS 的限制

FORCE ROW LEVEL SECURITY 影響 owner 的一般行為，但不能拿來限制真正 superuser 或 BYPASSRLS。若以管理者執行測試，看到所有資料可能是預期的例外；不能因此宣稱 policy 壞掉，也不能用管理者通過的查詢來證明隔離正確。測試角色、grant 與連線參數都要記錄。

## 驗收真實部署

以 app role 連線，開交易設定 alpha、查同名 doc，再以同一池連線設定 beta；測未設定、錯誤設定與寫入另一租戶，確認沒有殘留。離線入口只展示安全識別字組合與 policy 契約，不建立角色或驗證 server RLS；需自行啟動受控服務才能完成這一層。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 22_pg_roles.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:22_pg_roles.py -->

## 練習與解答

**請先嘗試：** 把 tenant 設成 session-level，再把連線還給池，有什麼風險？

<details><summary>展開解答與判斷依據</summary>

下一個請求可能沿用上一租戶狀態。採交易內設定並確保交易結束、池重置與異常回滾；仍要測試連線重用。資料庫角色也不能擁有繞過 RLS 或任意執行模型 SQL 的能力。

</details>

## 官方文件與延伸閱讀

- [PostgreSQL Row Security](https://www.postgresql.org/docs/18/ddl-rowsecurity.html)
- [Psycopg 3 官方文件](https://www.psycopg.org/psycopg3/docs/)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
