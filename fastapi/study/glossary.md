# FastAPI與AI後端工程術語

## HTTP

客戶端與伺服器交換請求與回應的應用層協定。

## ASGI

以scope、receive、send連接非同步Python應用與伺服器的介面。

## FastAPI

整合型別、路由、依賴與OpenAPI的ASGI框架。

## Starlette

提供ASGI路由、回應、中介層與測試等底層工具。

## Uvicorn

接受網路連線並執行ASGI應用的伺服器。

## Pydantic

以明確模型驗證及序列化資料的套件。

## Path parameter

URL路徑中識別資源的變動部分。

## Query parameter

URL查詢部分的篩選、排序或分頁選項。

## Request body

請求承載內容，可採JSON、表單或其他編碼。

## Content-Type

描述body媒體型別的標頭，不是內容可信度保證。

## Status code

回應對本次HTTP操作結果的機器可讀分類。

## DTO

對外傳送的資料形狀，和ORM內部物件分開。

## Strict mode

拒絕不符合宣告型別的寬鬆轉換。

## Validator

補上欄位或跨欄位規則的驗證函式。

## Serialization

將內部資料轉成可傳輸格式的過程。

## OpenAPI

描述HTTP API介面、模型與安全方案的規格。

## JSON Schema

描述JSON值形狀與部分限制的規格。

## APIRouter

組織一組相關路由與共用設定的元件。

## App factory

依設定建立隔離應用實例的函式。

## Dependency

由框架在請求範圍解析的所需資源或責任。

## Depends

宣告FastAPI依賴關係的工具。

## Dependency cache

單次請求內重用同一依賴求值，不是跨使用者快取。

## Yield dependency

以yield交付資源並在結束時清理的依賴。

## Function scope

路由函式結束後、回應送出前清理的範圍。

## Request scope

涵蓋回應傳送期間的依賴範圍。

## Lifespan

ASGI應用啟動與關閉資源管理的生命週期。

## Event loop

協調可等待任務和I/O進度的事件迴圈。

## Coroutine

可在await邊界合作式暫停與恢復的非同步工作。

## Thread pool

有限執行緒執行同步阻塞工作的資源池。

## Cancellation

要求合作式工作停止，不保證撤回外部副作用。

## Timeout

某階段等待的時間界限。

## Deadline

跨階段與重試的總時間預算。

## Connection pool

保存並重用有限連線的機制。

## Keep-alive

連線完成一次請求後仍保留以供重用。

## HTTPX

本課明確建立同步與非同步HTTP客戶端使用的套件。

## HTTPX2

最新Starlette TestClient優先採用的客戶端套件。

## ASGITransport

直接把HTTP客戶端接到ASGI應用的測試傳輸。

## MockTransport

依固定程式回應HTTP請求的測試替身。

## SQLAlchemy

以Core與ORM操作關聯資料庫的套件。

## Engine

管理連線與資料庫方言的共用物件。

## Session

維護一組ORM狀態與交易的可變工作範圍。

## AsyncSession

供非同步資料庫驅動使用、每task獨立的Session。

## Flush

將待修改資料送到資料庫，但不等於交易提交。

## Commit

成功提交交易中的修改。

## Rollback

在失敗或明確要求時撤回尚未提交修改。

## Unique constraint

由資料庫保證指定欄位組合不重複。

## Foreign key

由資料庫約束資料列之間參照關係。

## Index

協助特定查詢存取資料、同時增加寫入成本的結構。

## Migration

按版本保存並執行schema演進的程式。

## Alembic

SQLAlchemy常用的migration工具。

## Keyset pagination

以穩定排序鍵續讀，而不是跳過任意筆數。

## ETag

識別資源表示版本的HTTP標頭。

## If-Match

要求目前版本符合客戶端條件才執行修改。

## Tombstone

保留刪除事實的標記，不等於物理抹除。

## Bearer token

持有者可用於驗證的憑證，需保護傳輸與保存。

## Opaque token

不直接承載可讀claims的隨機憑證。

## Authentication

確認呼叫者身分的過程。

## Authorization

判斷該身分可執行何操作與存取何資源。

## Tenant

資料與權限隔離的組織或使用者範圍。

## RBAC

依角色決定操作權限的模型。

## ACL

列出資源存取許可的權限控制方式。

## JWT

帶claims與簽章的token格式，通常不是加密內容。

## Issuer

發出token且須被信任的主體。

## Audience

token預期交付的受眾，API驗證時必須核對。

## OAuth

用token授權存取資源的框架。

## OIDC

建立在OAuth之上的登入身分層。

## PKCE

將授權碼交換綁定到原客戶端的驗證機制。

## JWKS

公開驗證金鑰的標準JSON集合。

## CORS

瀏覽器跨來源存取回應的政策，不是服務認證。

## CSRF

瀏覽器自動附帶憑證而遭跨站觸發的請求風險。

## SSRF

後端受不可信輸入誘導存取非預期網路目的地。

## Multipart

在同一body承載多個表單部分的編碼。

## UploadFile

FastAPI管理上傳檔案與暫存資源的物件。

## UTF-8

Unicode常用位元組編碼，bytes長度不同於字元數。

## Idempotency key

識別同一次意圖以找回既有結果的鍵。

## Fingerprint

由明確正規化內容計算的請求摘要。

## Provider adapter

將特定供應商介面映射到本地契約的邊界。

## Extractive answer

直接取自原文的答案，不保證通用語意理解。

## Citation

包含來源身份、區間與原文的引用。

## Abstention

資料不支持時明確拒絕作答的結果。

## Context window

模型可處理的輸入與相關token容量範圍。

## Retry

在明確政策內再次嘗試可能失敗的操作。

## Backoff

重試之前有限等待以減少故障放大。

## Circuit breaker

在失敗狀態下暫停新呼叫並有限探測恢復的機制。

## Job

有持久化識別、狀態與結果的業務工作。

## Worker

獨立取得和執行工作者，不等於HTTP連線。

## Claim

以原子狀態轉移取得工作執行資格。

## Lease

有截止時間的暫時執行權。

## Fencing token

區分不同持有者、拒絕舊worker提交的token。

## Attempt

一個工作的一次取得與執行嘗試。

## At-least-once

工作可能重投和重算，需要冪等或去重。

## SSE

使用HTTP文字事件向客戶端單向交付更新。

## Last-Event-ID

客戶端回報最後已處理事件的續讀游標。

## JSONL

每行一個獨立JSON值的逐筆資料格式。

## WebSocket

在連線中雙向傳輸訊息的協定。

## Backpressure

消費速率較慢時以等待、界限或拒絕控制產生端。

## Token bucket

以容量和補充率分開限制突發與長期流量的模型。

## Little law

穩定系統平均在途量等於平均抵達率乘平均停留時間。

## Percentile

排序觀察值後描述指定分位位置的方法。

## SLO

以明確範圍、分母與時間窗定義的服務目標。

## Readiness

服務是否準備好承接指定流量的狀態。

## Liveness

程序是否仍可回應的基本狀態。

## RPO

事故後可接受資料損失的時間目標。

## RTO

事故後恢復服務所需時間的目標。

## Graceful shutdown

停止接單、有限排空並依順序清理資源。

## Expand-contract

先擴充相容schema、切換程式、最後移除舊結構。

## GitHub Pages

提供本課靜態教材的服務，不執行Uvicorn後端。
