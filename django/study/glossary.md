# Django術語表

## HTTP

瀏覽器與服務交換請求及回應的協定，方法、狀態與標頭具有語意。

## Request

一次傳入的請求，含方法、路徑、標頭與輸入資料。

## Response

伺服器回傳的狀態、標頭與本文。

## Project

組合整個Django網站的設定與入口。

## App

一組可組織或重用的Django功能。

## MVT

Model、View與Template的責任分工，不表示業務全部放View。

## View

協調請求、資料、授權與回應的程式入口。

## URLconf

依順序宣告路由與對應View的模組。

## Converter

將路由片段限制並轉成View參數的規則。

## Namespace

讓不同app的URL或資產名稱不互相衝突的範圍。

## Reverse

依路由名稱與參數產生網址，不硬編路徑。

## Middleware

包住請求處理、依順序進入並反向返回的共用層。

## Request ID

連接同一次請求紀錄的識別，不直接證明錯誤原因。

## Settings

Django程序的設定，常依本地、測試與正式環境分層。

## Environment variable

由程序環境提供的設定值，不代表自動讀取.env。

## DEBUG

開發除錯設定，正式網站應關閉並另保存錯誤證據。

## ALLOWED_HOSTS

可接受的HTTP主機範圍，不是一般使用者權限。

## SECRET_KEY

框架密碼學用途的機密設定，不應放在公開原始碼。

## Template

呈現資料的模板，不是任意Python執行環境。

## Context

傳入模板的資料契約，需知道是否會觸發查詢。

## Block

模板繼承中可替換的區塊。

## Autoescape

將輸出中的特殊字元跳脫，與允許任意HTML不同。

## Static

隨程式交付的CSS、JS與圖片等資產。

## Media

使用者上傳或產生的檔案，需另外保存與授權。

## Collectstatic

依設定收集程式資產，不處理私人檔案授權。

## Manifest storage

以內容版本對應資產檔名的儲存策略。

## Model

資料欄位、關係與部分規則的Python定義。

## ORM

以模型與QuerySet組織資料庫操作的工具。

## Field

Model或表單的欄位，兩者生命週期不同。

## Blank

通常影響表單是否允許空輸入。

## Null

資料庫欄位能否儲存NULL的條件。

## ForeignKey

指向另一列的單值關聯。

## ManyToManyField

透過中介資料表保存多對多關係。

## Related name

反向關聯存取名稱。

## On delete

被參照列刪除時的資料關係行為，不是使用者授權。

## AbstractUser

保留框架帳號能力並可擴充的User基礎類別。

## AUTH_USER_MODEL

指定專案帳號模型，宜在初始migration前決定。

## Migration

版本化schema及資料演進計畫。

## Makemigrations

由模型狀態差異產生migration原稿。

## Migrate

將migration套用到指定資料庫。

## Data migration

處理歷史資料轉換的migration，需使用對應歷史模型。

## CheckConstraint

由資料庫保護可檢查的資料條件。

## UniqueConstraint

由資料庫保護欄位組合唯一性。

## Index

協助特定查詢的資料結構，也增加寫入與儲存成本。

## QuerySet

可組合且通常惰性執行的資料查詢描述。

## Lazy evaluation

直到需要結果時才執行的行為，並非每次鏈式呼叫都查DB。

## Select related

以join載入適合的單值關聯。

## Prefetch related

以額外查詢批次載入關聯並在Python組合。

## Fetch mode

Django 6.1控制未載入欄位擷取行為的設定。

## FETCH_ONE

預設按單一物件取尚未載入欄位。

## FETCH_PEERS

為同批peers取尚未載入欄位，需理解批次與關聯條件。

## FETCH_RAISE

阻擋意外欄位擷取並拋出FieldFetchBlocked。

## Aggregate

回傳查詢集合的彙總。

## Annotate

為物件或群組附上計算結果。

## Atomic

將相關資料庫操作放在交易邊界。

## Savepoint

交易內可回復至的中間邊界。

## On commit

資料庫交易成功提交後才執行的callback。

## Select for update

在支援的資料庫與交易中鎖定選取列。

## Isolation

交易間可觀察資料與競爭的規則，依資料庫及設定而異。

## Form

輸入轉型、驗證與錯誤呈現的工具。

## Bound form

已綁定提交資料、可進行驗證的表單。

## Cleaned data

表單驗證後可使用的轉型資料。

## ModelForm

利用Model欄位資訊建立表單，仍需白名單與授權。

## PRG

POST成功後redirect再GET的互動流程，不是完整去重保證。

## CBV

以類別與生命週期方法組織的View。

## Mixin

提供特定方法或行為的可組合類別，順序影響MRO。

## Pagination

把完整篩選集合分段呈現的契約。

## Authentication

驗證請求者身分。

## Authorization

判斷該身分可對哪些資料執行什麼動作。

## Session

伺服器記錄多次請求間狀態的機制。

## Cookie

瀏覽器儲存並按規則附在請求的資料，不等於完整伺服器session。

## CSRF

防止利用自動附帶憑證發起未授權跨站修改的防護範圍。

## XSS

內容或腳本注入威脅，需正確插入與跳脫策略。

## CSP

限制資源載入等來源的瀏覽器政策，是額外防線。

## CORS

瀏覽器跨來源讀取回應的規則，不等於認證或CSRF。

## Staff

Admin使用資格的一部分，不代表全部模型權限。

## Superuser

具有高度管理權限的身分，應明確配置與使用。

## Permission

可執行某類動作的權限，仍要結合物件範圍。

## Group

可集合及指派模型權限的帳號群組。

## Admin

框架提供的管理介面，仍需資料範圍與欄位政策。

## Storage

檔案保存介面，本機或外部後端有不同可靠性條件。

## FileResponse

串流檔案回應，授權必須在開檔前確認。

## Serializer

DRF的輸出表示與輸入驗證工具。

## ViewSet

組織API動作的類別，常由router建立路由。

## Router

依API註冊資訊產生集合與詳情等路徑。

## SessionAuthentication

DRF使用session身分的認證方式，寫入仍需CSRF。

## Object permission

針對單一物件檢查的授權，不自動限制所有列表。

## TestCase

框架測試隔離工具，需理解交易及真正提交的差別。

## Test client

執行Django請求流程的測試客戶端，不是實際瀏覽器。

## Fixture

用於載入固定測試或參考資料的表示。

## Cache key

識別快取內容與範圍的鍵，私人資料常需包含user。

## TTL

快取存活限制，不是唯一失效策略。

## LocMemCache

程序內快取，不自動跨worker共享。

## Signal

事件通知機制，並非所有寫入路徑都觸發相同signals。

## Async view

非同步View，仍需核對同步I/O及服務入口。

## Tasks framework

Django定義與投遞工作的協定，真正worker需外部基礎設施。

## ImmediateBackend

同程序立即執行Tasks的本地與測試後端。

## Idempotency

按明確契約重複執行時不增加不期望副作用的性質。

## WSGI

Python同步Web應用介面。

## ASGI

可支援非同步等執行模型的Python服務介面。

## Reverse proxy

在應用前處理TLS、轉送與其他邊界工作的服務。

## Waitress

本課使用的WSGI服務套件，仍需實際網路與部署配置。

## HSTS

告知瀏覽器使用HTTPS的政策，範圍與preload需要條件。

## Restore

把備份還原成可用系統並核對資料的流程。
