# Django實作學習單

## 網站、後端與Django的角色

為什麼教材能放GitHub Pages，但StudyHub登入與儲存不能直接靠它執行？

「網站、後端與Django的角色」讀圖：追蹤瀏覽器與伺服器的請求及回應，指出靜態教材與Django程式各在哪裡執行。再回答：為什麼教材能放GitHub Pages，但StudyHub登入與儲存不能直接靠它執行？

[對應圖解](../assets/figures/01.svg)

作答：＿＿＿＿＿

## 安裝Django 6.1.3與隔離環境

終端顯示已安裝Django，程式卻說找不到模組，先查什麼？

「安裝Django 6.1.3與隔離環境」讀圖：追蹤瀏覽器與伺服器的請求及回應，指出靜態教材與Django程式各在哪裡執行。再回答：終端顯示已安裝Django，程式卻說找不到模組，先查什麼？

[對應圖解](../assets/figures/01.svg)

作答：＿＿＿＿＿

## Project、app與可重用功能

建立了desk資料夾就會自動出現資料表嗎？

「Project、app與可重用功能」讀圖：追蹤瀏覽器與伺服器的請求及回應，指出靜態教材與Django程式各在哪裡執行。再回答：建立了desk資料夾就會自動出現資料表嗎？

[對應圖解](../assets/figures/01.svg)

作答：＿＿＿＿＿

## 請求生命週期與MVT

health回傳200，是否代表整個網站都可用？

「請求生命週期與MVT」讀圖：區分project、app與設定，沿管理命令走到第一個頁面。再回答：health回傳200，是否代表整個網站都可用？

[對應圖解](../assets/figures/02.svg)

作答：＿＿＿＿＿

## 啟動第一個完整網站

重開01獨立算例後資料不見，但runserver資料還在，為什麼？

「啟動第一個完整網站」讀圖：區分project、app與設定，沿管理命令走到第一個頁面。再回答：重開01獨立算例後資料不見，但runserver資料還在，為什麼？

[對應圖解](../assets/figures/02.svg)

作答：＿＿＿＿＿

## 起步練習：畫出你正在執行的系統

看到ModuleNotFoundError與404，應採取相同排錯方式嗎？

「起步練習：畫出你正在執行的系統」讀圖：區分project、app與設定，沿管理命令走到第一個頁面。再回答：看到ModuleNotFoundError與404，應採取相同排錯方式嗎？

[對應圖解](../assets/figures/02.svg)

作答：＿＿＿＿＿

## 閱讀完整專案目錄

migration與db.sqlite3為什麼不能用相同方式管理？

「閱讀完整專案目錄」讀圖：沿路由比對順序找到View，再檢查reverse的參數與名稱。再回答：migration與db.sqlite3為什麼不能用相同方式管理？

[對應圖解](../assets/figures/03.svg)

作答：＿＿＿＿＿

## 設定、環境變數與秘密

建立.env後設定沒有改變，可能是什麼原因？

「設定、環境變數與秘密」讀圖：沿路由比對順序找到View，再檢查reverse的參數與名稱。再回答：建立.env後設定沒有改變，可能是什麼原因？

[對應圖解](../assets/figures/03.svg)

作答：＿＿＿＿＿

## URL、converter與reverse

使用UUID網址後，可以省掉物件權限檢查嗎？

「URL、converter與reverse」讀圖：沿路由比對順序找到View，再檢查reverse的參數與名稱。再回答：使用UUID網址後，可以省掉物件權限檢查嗎？

[對應圖解](../assets/figures/03.svg)

作答：＿＿＿＿＿

## View、狀態碼與回應內容

API回傳登入頁HTML，客戶端JSON解析失敗，應先查哪裡？

「View、狀態碼與回應內容」讀圖：依序讀middleware進入與返回路徑，指出本單元的檢查點。再回答：API回傳登入頁HTML，客戶端JSON解析失敗，應先查哪裡？

[對應圖解](../assets/figures/04.svg)

作答：＿＿＿＿＿

## Middleware的順序與責任

把View總耗時與其中資料庫耗時相加，會有什麼問題？

「Middleware的順序與責任」讀圖：依序讀middleware進入與返回路徑，指出本單元的檢查點。再回答：把View總耗時與其中資料庫耗時相加，會有什麼問題？

[對應圖解](../assets/figures/04.svg)

作答：＿＿＿＿＿

## 請求處理練習：找出失敗在哪一層

把所有404改成200並顯示錯誤文字，會讓網站更容易使用嗎？

「請求處理練習：找出失敗在哪一層」讀圖：依序讀middleware進入與返回路徑，指出本單元的檢查點。再回答：把所有404改成200並顯示錯誤文字，會讓網站更容易使用嗎？

[對應圖解](../assets/figures/04.svg)

作答：＿＿＿＿＿

## Django模板語言與自動跳脫

使用safe之前，應先回答什麼？

「Django模板語言與自動跳脫」讀圖：追蹤模板繼承、context與輸出，指出哪些內容應保持自動跳脫。再回答：使用safe之前，應先回答什麼？

[對應圖解](../assets/figures/05.svg)

作答：＿＿＿＿＿

## 模板繼承與可重用版面

把完整HTML複製到每個頁面，長期會遇到什麼問題？

「模板繼承與可重用版面」讀圖：追蹤模板繼承、context與輸出，指出哪些內容應保持自動跳脫。再回答：把完整HTML複製到每個頁面，長期會遇到什麼問題？

[對應圖解](../assets/figures/05.svg)

作答：＿＿＿＿＿

## Context與模板中的隱藏查詢

模板裡只加一個owner名稱，為何也可能影響效能？

「Context與模板中的隱藏查詢」讀圖：追蹤模板繼承、context與輸出，指出哪些內容應保持自動跳脫。再回答：模板裡只加一個owner名稱，為何也可能影響效能？

[對應圖解](../assets/figures/05.svg)

作答：＿＿＿＿＿

## Static、media與collectstatic

為什麼不應把私人附件直接放進static？

「Static、media與collectstatic」讀圖：區分靜態資產、使用者檔案與頁面內容，找出可及性與保存位置。再回答：為什麼不應把私人附件直接放進static？

[對應圖解](../assets/figures/06.svg)

作答：＿＿＿＿＿

## 可及性、錯誤提示與深色介面

只把錯誤欄位邊框變紅，是否足夠？

「可及性、錯誤提示與深色介面」讀圖：區分靜態資產、使用者檔案與頁面內容，找出可及性與保存位置。再回答：只把錯誤欄位邊框變紅，是否足夠？

[對應圖解](../assets/figures/06.svg)

作答：＿＿＿＿＿

## 介面練習：把資料變成可操作的畫面

模板越少行就一定比較快嗎？

「介面練習：把資料變成可操作的畫面」讀圖：區分靜態資產、使用者檔案與頁面內容，找出可及性與保存位置。再回答：模板越少行就一定比較快嗎？

[對應圖解](../assets/figures/06.svg)

作答：＿＿＿＿＿

## Model欄位、驗證與資料庫型別

加了MinValueValidator，是否所有直接資料庫寫入都一定被擋下？

「Model欄位、驗證與資料庫型別」讀圖：數清楚一對多與多對多的方向，指出外鍵與中介表的角色。再回答：加了MinValueValidator，是否所有直接資料庫寫入都一定被擋下？

[對應圖解](../assets/figures/07.svg)

作答：＿＿＿＿＿

## 外鍵、多對多與刪除行為

外鍵能找到tag，是否代表目前使用者可以使用它？

「外鍵、多對多與刪除行為」讀圖：數清楚一對多與多對多的方向，指出外鍵與中介表的角色。再回答：外鍵能找到tag，是否代表目前使用者可以使用它？

[對應圖解](../assets/figures/07.svg)

作答：＿＿＿＿＿

## 在第一個migration前決定User

已經migrate並有真實帳號後，能直接修改AUTH_USER_MODEL嗎？

「在第一個migration前決定User」讀圖：數清楚一對多與多對多的方向，指出外鍵與中介表的角色。再回答：已經migrate並有真實帳號後，能直接修改AUTH_USER_MODEL嗎？

[對應圖解](../assets/figures/07.svg)

作答：＿＿＿＿＿

## Migration：schema演進與資料搬移

修改models.py後，資料庫為什麼沒有立刻改變？

「Migration：schema演進與資料搬移」讀圖：沿schema變更與資料搬移的順序，說明哪些舊資料必須先處理。再回答：修改models.py後，資料庫為什麼沒有立刻改變？

[對應圖解](../assets/figures/08.svg)

作答：＿＿＿＿＿

## Unique、CheckConstraint與索引

UniqueConstraint能不能代替所有表單驗證？

「Unique、CheckConstraint與索引」讀圖：沿schema變更與資料搬移的順序，說明哪些舊資料必須先處理。再回答：UniqueConstraint能不能代替所有表單驗證？

[對應圖解](../assets/figures/08.svg)

作答：＿＿＿＿＿

## 資料模型練習：變更之前先問資料

本機資料庫有欄位，migration卻沒有，能直接交付嗎？

「資料模型練習：變更之前先問資料」讀圖：沿schema變更與資料搬移的順序，說明哪些舊資料必須先處理。再回答：本機資料庫有欄位，migration卻沒有，能直接交付嗎？

[對應圖解](../assets/figures/08.svg)

作答：＿＿＿＿＿

## QuerySet的惰性、篩選與SQL

filter接了三次，就一定執行三次SQL嗎？

「QuerySet的惰性、篩選與SQL」讀圖：比較逐列關聯查詢與批次載入，核對查詢次數及欄位範圍。再回答：filter接了三次，就一定執行三次SQL嗎？

[對應圖解](../assets/figures/09.svg)

作答：＿＿＿＿＿

## 建立、更新、刪除與驗證邊界

QuerySet.update後post_save沒有觸發，是Django壞了嗎？

「建立、更新、刪除與驗證邊界」讀圖：比較逐列關聯查詢與批次載入，核對查詢次數及欄位範圍。再回答：QuerySet.update後post_save沒有觸發，是Django壞了嗎？

[對應圖解](../assets/figures/09.svg)

作答：＿＿＿＿＿

## 關聯載入、額外查詢與6.1 fetch modes

select_related與prefetch_related可以不分關係全部互換嗎？

「關聯載入、額外查詢與6.1 fetch modes」讀圖：比較逐列關聯查詢與批次載入，核對查詢次數及欄位範圍。再回答：select_related與prefetch_related可以不分關係全部互換嗎？

[對應圖解](../assets/figures/09.svg)

作答：＿＿＿＿＿

## Count、annotate與統計分母

列表只顯示第一頁五筆，總任務數是否就應該是五？

「Count、annotate與統計分母」讀圖：沿交易邊界讀提交與回滾，指出跨資料庫不能直接推論的部分。再回答：列表只顯示第一頁五筆，總任務數是否就應該是五？

[對應圖解](../assets/figures/10.svg)

作答：＿＿＿＿＿

## Atomic、on_commit與併發界線

SQLite測試通過，就能保證select_for_update在PostgreSQL的所有併發行為嗎？

「Atomic、on_commit與併發界線」讀圖：沿交易邊界讀提交與回滾，指出跨資料庫不能直接推論的部分。再回答：SQLite測試通過，就能保證select_for_update在PostgreSQL的所有併發行為嗎？

[對應圖解](../assets/figures/10.svg)

作答：＿＿＿＿＿

## ORM練習：先手算，再看SQL

所有查詢結果正確，就代表效能也合格嗎？

「ORM練習：先手算，再看SQL」讀圖：沿交易邊界讀提交與回滾，指出跨資料庫不能直接推論的部分。再回答：所有查詢結果正確，就代表效能也合格嗎？

[對應圖解](../assets/figures/10.svg)

作答：＿＿＿＿＿

## Form、is_valid與cleaned_data

只限制前端下拉選單，是否就能防止提交別人的tag ID？

「Form、is_valid與cleaned_data」讀圖：追蹤輸入到cleaned_data，指出資料擁有權與欄位白名單在哪裡確認。再回答：只限制前端下拉選單，是否就能防止提交別人的tag ID？

[對應圖解](../assets/figures/11.svg)

作答：＿＿＿＿＿

## ModelForm與安全的欄位白名單

把所有Model欄位自動放進表單，可能帶來什麼維護風險？

「ModelForm與安全的欄位白名單」讀圖：追蹤輸入到cleaned_data，指出資料擁有權與欄位白名單在哪裡確認。再回答：把所有Model欄位自動放進表單，可能帶來什麼維護風險？

[對應圖解](../assets/figures/11.svg)

作答：＿＿＿＿＿

## CRUD與POST Redirect GET

使用PRG後，是否就不用處理重複付款或重複命令？

「CRUD與POST Redirect GET」讀圖：追蹤輸入到cleaned_data，指出資料擁有權與欄位白名單在哪裡確認。再回答：使用PRG後，是否就不用處理重複付款或重複命令？

[對應圖解](../assets/figures/11.svg)

作答：＿＿＿＿＿

## Class-based View與Mixin順序

使用UpdateView就會自動防止編輯別人的資料嗎？

「Class-based View與Mixin順序」讀圖：沿POST、redirect與GET追蹤重新整理，核對分頁與狀態變更。再回答：使用UpdateView就會自動防止編輯別人的資料嗎？

[對應圖解](../assets/figures/12.svg)

作答：＿＿＿＿＿

## 分頁、穩定排序與篩選

十二筆資料每頁五筆，最後一頁應有幾筆？

「分頁、穩定排序與篩選」讀圖：沿POST、redirect與GET追蹤重新整理，核對分頁與狀態變更。再回答：十二筆資料每頁五筆，最後一頁應有幾筆？

[對應圖解](../assets/figures/12.svg)

作答：＿＿＿＿＿

## 表單與CRUD驗收練習

測到表單拒絕外部tag後，還需測API嗎？

「表單與CRUD驗收練習」讀圖：沿POST、redirect與GET追蹤重新整理，核對分頁與狀態變更。再回答：測到表單拒絕外部tag後，還需測API嗎？

[對應圖解](../assets/figures/12.svg)

作答：＿＿＿＿＿

## 認證、Session與Cookie

用force_login測到頁面可開，是否已驗證密碼登入正確？

「認證、Session與Cookie」讀圖：區分身分驗證與物件授權，找出每次查詢的擁有者條件。再回答：用force_login測到頁面可開，是否已驗證密碼登入正確？

[對應圖解](../assets/figures/13.svg)

作答：＿＿＿＿＿

## 註冊、登入、登出與安全跳轉

建立帳號時直接將password欄位寫進User.password，會有什麼問題？

「註冊、登入、登出與安全跳轉」讀圖：區分身分驗證與物件授權，找出每次查詢的擁有者條件。再回答：建立帳號時直接將password欄位寫進User.password，會有什麼問題？

[對應圖解](../assets/figures/13.svg)

作答：＿＿＿＿＿

## 物件授權與資料擁有者

detail有owner檢查，API列表是否就自然只顯示自己的任務？

「物件授權與資料擁有者」讀圖：區分身分驗證與物件授權，找出每次查詢的擁有者條件。再回答：detail有owner檢查，API列表是否就自然只顯示自己的任務？

[對應圖解](../assets/figures/13.svg)

作答：＿＿＿＿＿

## CSRF、XSS、CSP與CORS的不同責任

測試Client的POST成功，是否表示CSRF設定已驗收？

「CSRF、XSS、CSP與CORS的不同責任」讀圖：追蹤cookie、CSRF token及來源，說明哪些防護不能互相取代。再回答：測試Client的POST成功，是否表示CSRF設定已驗收？

[對應圖解](../assets/figures/14.svg)

作答：＿＿＿＿＿

## 群組、模型permission與Admin身分

使用者有export_task，是否代表能匯出所有帳號資料？

「群組、模型permission與Admin身分」讀圖：追蹤cookie、CSRF token及來源，說明哪些防護不能互相取代。再回答：使用者有export_task，是否代表能匯出所有帳號資料？

[對應圖解](../assets/figures/14.svg)

作答：＿＿＿＿＿

## 帳號與授權驗收矩陣

越權測試回404，但資料真的被更新了，算通過嗎？

「帳號與授權驗收矩陣」讀圖：追蹤cookie、CSRF token及來源，說明哪些防護不能互相取代。再回答：越權測試回404，但資料真的被更新了，算通過嗎？

[對應圖解](../assets/figures/14.svg)

作答：＿＿＿＿＿

## Admin的模型管理與操作體驗

啟用staff旗標，是否就自動取得所有模型修改權限？

「Admin的模型管理與操作體驗」讀圖：沿staff、模型權限與資料範圍三道檢查，找出後台可看的資料。再回答：啟用staff旗標，是否就自動取得所有模型修改權限？

[對應圖解](../assets/figures/15.svg)

作答：＿＿＿＿＿

## 管理後台的資料範圍與關聯選項

主列表已限制owner，還要檢查關聯欄位嗎？

「管理後台的資料範圍與關聯選項」讀圖：沿staff、模型權限與資料範圍三道檢查，找出後台可看的資料。再回答：主列表已限制owner，還要檢查關聯欄位嗎？

[對應圖解](../assets/figures/15.svg)

作答：＿＿＿＿＿

## 上傳文字附件：驗證與儲存

檔名結尾是.txt，是否就能信任內容？

「上傳文字附件：驗證與儲存」讀圖：沿staff、模型權限與資料範圍三道檢查，找出後台可看的資料。再回答：檔名結尾是.txt，是否就能信任內容？

[對應圖解](../assets/figures/15.svg)

作答：＿＿＿＿＿

## 私人下載、回應標頭與刪除

FileResponse設為as_attachment，是否就保證只有owner能下載？

「私人下載、回應標頭與刪除」讀圖：沿私人檔案的上傳及下載路徑，指出哪裡再次檢查擁有者。再回答：FileResponse設為as_attachment，是否就保證只有owner能下載？

[對應圖解](../assets/figures/16.svg)

作答：＿＿＿＿＿

## 郵件後端與密碼重設流程

測試的mail.outbox有一封信，能否證明SMTP正式配置正常？

「郵件後端與密碼重設流程」讀圖：沿私人檔案的上傳及下載路徑，指出哪裡再次檢查擁有者。再回答：測試的mail.outbox有一封信，能否證明SMTP正式配置正常？

[對應圖解](../assets/figures/16.svg)

作答：＿＿＿＿＿

## 後台與附件驗收練習

交易回滾後，若檔案已被永久刪除，表示哪個邊界設計錯了？

「後台與附件驗收練習」讀圖：沿私人檔案的上傳及下載路徑，指出哪裡再次檢查擁有者。再回答：交易回滾後，若檔案已被永久刪除，表示哪個邊界設計錯了？

[對應圖解](../assets/figures/16.svg)

作答：＿＿＿＿＿

## REST API與HTTP資源

JsonResponse是否自動提供Serializer、物件權限與分頁？

「REST API與HTTP資源」讀圖：追蹤JSON輸入到Serializer，再檢查哪些欄位由伺服器決定。再回答：JsonResponse是否自動提供Serializer、物件權限與分頁？

[對應圖解](../assets/figures/17.svg)

作答：＿＿＿＿＿

## Serializer的輸入驗證與唯讀欄位

把owner設成唯讀後，建立時應由誰填入？

「Serializer的輸入驗證與唯讀欄位」讀圖：追蹤JSON輸入到Serializer，再檢查哪些欄位由伺服器決定。再回答：把owner設成唯讀後，建立時應由誰填入？

[對應圖解](../assets/figures/17.svg)

作答：＿＿＿＿＿

## ViewSet、router與共享服務

額外complete action可直接只憑主鍵取得任務嗎？

「ViewSet、router與共享服務」讀圖：追蹤JSON輸入到Serializer，再檢查哪些欄位由伺服器決定。再回答：額外complete action可直接只憑主鍵取得任務嗎？

[對應圖解](../assets/figures/17.svg)

作答：＿＿＿＿＿

## API驗證、Session CSRF與物件權限

只寫IsOwner.has_object_permission，是否已保護列表內容？

「API驗證、Session CSRF與物件權限」讀圖：依API回應狀態與分頁內容，指出驗證、授權及錯誤的差異。再回答：只寫IsOwner.has_object_permission，是否已保護列表內容？

[對應圖解](../assets/figures/18.svg)

作答：＿＿＿＿＿

## API分頁、驗證錯誤與一致回應

count為十二、results只有五筆，是錯誤嗎？

「API分頁、驗證錯誤與一致回應」讀圖：依API回應狀態與分頁內容，指出驗證、授權及錯誤的差異。再回答：count為十二、results只有五筆，是錯誤嗎？

[對應圖解](../assets/figures/18.svg)

作答：＿＿＿＿＿

## REST API專題練習

API建立成功後只檢查201，還漏掉什麼？

「REST API專題練習」讀圖：依API回應狀態與分頁內容，指出驗證、授權及錯誤的差異。再回答：API建立成功後只檢查201，還漏掉什麼？

[對應圖解](../assets/figures/18.svg)

作答：＿＿＿＿＿

## TestCase、測試資料庫與隔離

Django TestCase通過，是否代表真實多程序列鎖已驗證？

「TestCase、測試資料庫與隔離」讀圖：由資料模型到HTTP層讀測試範圍，指出這個單元能驗證的責任。再回答：Django TestCase通過，是否代表真實多程序列鎖已驗證？

[對應圖解](../assets/figures/19.svg)

作答：＿＿＿＿＿

## HTTP測試Client與CSRF反例

為什麼要保留一個預期403的測試？

「HTTP測試Client與CSRF反例」讀圖：由資料模型到HTTP層讀測試範圍，指出這個單元能驗證的責任。再回答：為什麼要保留一個預期403的測試？

[對應圖解](../assets/figures/19.svg)

作答：＿＿＿＿＿

## API測試與越權回歸

用戶提交另一個owner，API忽略它並建立自己的資料，測試應檢查什麼？

「API測試與越權回歸」讀圖：由資料模型到HTTP層讀測試範圍，指出這個單元能驗證的責任。再回答：用戶提交另一個owner，API忽略它並建立自己的資料，測試應檢查什麼？

[對應圖解](../assets/figures/19.svg)

作答：＿＿＿＿＿

## 測試資料、fixtures與可讀性

測試資料越多，越能證明正確嗎？

「測試資料、fixtures與可讀性」讀圖：比較正常與越權案例，確認測試真的會攔住錯誤行為。再回答：測試資料越多，越能證明正確嗎？

[對應圖解](../assets/figures/20.svg)

作答：＿＿＿＿＿

## 查詢數、on_commit與外部副作用

測試註冊了on_commit但未執行，可以宣稱檔案已清除嗎？

「查詢數、on_commit與外部副作用」讀圖：比較正常與越權案例，確認測試真的會攔住錯誤行為。再回答：測試註冊了on_commit但未執行，可以宣稱檔案已清除嗎？

[對應圖解](../assets/figures/20.svg)

作答：＿＿＿＿＿

## 測試驗收：讓錯誤真的會被抓到

測試很多但全是正常成功案例，最可能漏掉什麼？

「測試驗收：讓錯誤真的會被抓到」讀圖：比較正常與越權案例，確認測試真的會攔住錯誤行為。再回答：測試很多但全是正常成功案例，最可能漏掉什麼？

[對應圖解](../assets/figures/20.svg)

作答：＿＿＿＿＿

## 快取範圍、TTL與失效策略

快取命中率很高，但不同使用者看到同一份摘要，代表什麼？

「快取範圍、TTL與失效策略」讀圖：沿使用者範圍與快取鍵，說明命中、失效與資料隔離。再回答：快取命中率很高，但不同使用者看到同一份摘要，代表什麼？

[對應圖解](../assets/figures/21.svg)

作答：＿＿＿＿＿

## 服務層、Signals與副作用

一項重要規則只放post_save，所有更新都一定遵守嗎？

「服務層、Signals與副作用」讀圖：沿使用者範圍與快取鍵，說明命中、失效與資料隔離。再回答：一項重要規則只放post_save，所有更新都一定遵守嗎？

[對應圖解](../assets/figures/21.svg)

作答：＿＿＿＿＿

## Async View、非同步ORM與同步邊界

把View改成async def後，裡面的同步資料庫與CPU工作會自動變成非阻塞嗎？

「Async View、非同步ORM與同步邊界」讀圖：沿使用者範圍與快取鍵，說明命中、失效與資料隔離。再回答：把View改成async def後，裡面的同步資料庫與CPU工作會自動變成非阻塞嗎？

[對應圖解](../assets/figures/21.svg)

作答：＿＿＿＿＿

## Django Tasks與真正的背景worker

看到TaskResult成功，能否證明工作是在背景worker執行？

「Django Tasks與真正的背景worker」讀圖：區分request、佇列與worker，指出ImmediateBackend的執行位置。再回答：看到TaskResult成功，能否證明工作是在背景worker執行？

[對應圖解](../assets/figures/22.svg)

作答：＿＿＿＿＿

## 重試、冪等與命令識別

相同命令識別回傳相同結果，是否保證外部郵件只寄一次？

「重試、冪等與命令識別」讀圖：區分request、佇列與worker，指出ImmediateBackend的執行位置。再回答：相同命令識別回傳相同結果，是否保證外部郵件只寄一次？

[對應圖解](../assets/figures/22.svg)

作答：＿＿＿＿＿

## 進階工程練習：速度與可靠性一起檢查

快取、async與queue一次全開後出錯，應如何縮小範圍？

「進階工程練習：速度與可靠性一起檢查」讀圖：區分request、佇列與worker，指出ImmediateBackend的執行位置。再回答：快取、async與queue一次全開後出錯，應如何縮小範圍？

[對應圖解](../assets/figures/22.svg)

作答：＿＿＿＿＿

## WSGI、ASGI與正式服務入口

把runserver綁到公開IP，是否等於正式部署？

「WSGI、ASGI與正式服務入口」讀圖：沿反向代理、WSGI及資料庫追蹤請求，指出各服務的責任。再回答：把runserver綁到公開IP，是否等於正式部署？

[對應圖解](../assets/figures/23.svg)

作答：＿＿＿＿＿

## 正式設定、DEBUG與安全檢查

check --deploy沒有ERROR，就能宣稱正式網站安全完成嗎？

「正式設定、DEBUG與安全檢查」讀圖：沿反向代理、WSGI及資料庫追蹤請求，指出各服務的責任。再回答：check --deploy沒有ERROR，就能宣稱正式網站安全完成嗎？

[對應圖解](../assets/figures/23.svg)

作答：＿＿＿＿＿

## 正式靜態檔與儲存策略

collectstatic完成後，私人附件也會自動安全提供嗎？

「正式靜態檔與儲存策略」讀圖：沿反向代理、WSGI及資料庫追蹤請求，指出各服務的責任。再回答：collectstatic完成後，私人附件也會自動安全提供嗎？

[對應圖解](../assets/figures/23.svg)

作答：＿＿＿＿＿

## 從SQLite到PostgreSQL

切到PostgreSQL後執行migrate，原SQLite資料會自動出現嗎？

「從SQLite到PostgreSQL」讀圖：區分程式、資料、靜態檔與備份，確認更新與回復的順序。再回答：切到PostgreSQL後執行migrate，原SQLite資料會自動出現嗎？

[對應圖解](../assets/figures/24.svg)

作答：＿＿＿＿＿

## 日誌、健康檢查、備份與回復

有Git repo就等於有完整網站備份嗎？

「日誌、健康檢查、備份與回復」讀圖：區分程式、資料、靜態檔與備份，確認更新與回復的順序。再回答：有Git repo就等於有完整網站備份嗎？

[對應圖解](../assets/figures/24.svg)

作答：＿＿＿＿＿

## 部署提案與驗收清單

正式方案尚未決定網域，應直接開啟所有HSTS子網域選項嗎？

「部署提案與驗收清單」讀圖：區分程式、資料、靜態檔與備份，確認更新與回復的順序。再回答：正式方案尚未決定網域，應直接開啟所有HSTS子網域選項嗎？

[對應圖解](../assets/figures/24.svg)

作答：＿＿＿＿＿

## StudyHub專題：先定義交付範圍

哪些功能最適合先做成可驗證基準？

「StudyHub專題：先定義交付範圍」讀圖：沿專題的資料到評估路徑，列出每一階段應留下的成果。再回答：哪些功能最適合先做成可驗證基準？

[對應圖解](../assets/figures/25.svg)

作答：＿＿＿＿＿

## 合成資料與管理命令

為什麼不在教材提供大家共用的admin密碼？

「合成資料與管理命令」讀圖：沿專題的資料到評估路徑，列出每一階段應留下的成果。再回答：為什麼不在教材提供大家共用的admin密碼？

[對應圖解](../assets/figures/25.svg)

作答：＿＿＿＿＿

## 從登入到附件的一次完整操作

兩個頁面都顯示不同使用者名稱，足夠證明資料隔離嗎？

「從登入到附件的一次完整操作」讀圖：沿專題的資料到評估路徑，列出每一階段應留下的成果。再回答：兩個頁面都顯示不同使用者名稱，足夠證明資料隔離嗎？

[對應圖解](../assets/figures/25.svg)

作答：＿＿＿＿＿

## 專題報告：查詢、快取與限制

查詢從二十一次變一次，就能宣稱網站快二十一倍嗎？

「專題報告：查詢、快取與限制」讀圖：依端到端操作找出帳號、CRUD、附件與API共用的權限邊界。再回答：查詢從二十一次變一次，就能宣稱網站快二十一倍嗎？

[對應圖解](../assets/figures/26.svg)

作答：＿＿＿＿＿

## API客戶端與共用業務流程

Django Client API測試成功，能否證明另一個網域的前端已完成CORS及Cookie整合？

「API客戶端與共用業務流程」讀圖：依端到端操作找出帳號、CRUD、附件與API共用的權限邊界。再回答：Django Client API測試成功，能否證明另一個網域的前端已完成CORS及Cookie整合？

[對應圖解](../assets/figures/26.svg)

作答：＿＿＿＿＿

## 交接專題：乾淨環境重新啟動

交接時最不應放進公開程式包的是什麼？

「交接專題：乾淨環境重新啟動」讀圖：依端到端操作找出帳號、CRUD、附件與API共用的權限邊界。再回答：交接時最不應放進公開程式包的是什麼？

[對應圖解](../assets/figures/26.svg)

作答：＿＿＿＿＿

## 排錯指南：環境、路由、資料與資產

CSRF失敗後直接加csrf_exempt，是否算找出原因？

「排錯指南：環境、路由、資料與資產」讀圖：從症狀選最小反例，說明要蒐集什麼證據才能判定原因。再回答：CSRF失敗後直接加csrf_exempt，是否算找出原因？

[對應圖解](../assets/figures/27.svg)

作答：＿＿＿＿＿

## 常見威脅與反例清單

使用Django ORM後，能否把使用者字串任意拼進raw SQL？

「常見威脅與反例清單」讀圖：從症狀選最小反例，說明要蒐集什麼證據才能判定原因。再回答：使用Django ORM後，能否把使用者字串任意拼進raw SQL？

[對應圖解](../assets/figures/27.svg)

作答：＿＿＿＿＿

## 更新Django與相依套件

只將requirements裡版本加大，其他測試都沒跑，算完成更新嗎？

「更新Django與相依套件」讀圖：從症狀選最小反例，說明要蒐集什麼證據才能判定原因。再回答：只將requirements裡版本加大，其他測試都沒跑，算完成更新嗎？

[對應圖解](../assets/figures/27.svg)

作答：＿＿＿＿＿

## Django工程完成清單

程式包漏掉templates，但原作者電腦能開網站，哪項驗收會發現？

「Django工程完成清單」讀圖：沿版本、測試與回復流程，指出交接前最後需要確認的內容。再回答：程式包漏掉templates，但原作者電腦能開網站，哪項驗收會發現？

[對應圖解](../assets/figures/28.svg)

作答：＿＿＿＿＿

## 術語與三條學習路線

已有API經驗，哪部分仍值得優先補？

「術語與三條學習路線」讀圖：沿版本、測試與回復流程，指出交接前最後需要確認的內容。再回答：已有API經驗，哪部分仍值得優先補？

[對應圖解](../assets/figures/28.svg)

作答：＿＿＿＿＿

## 版本來源、實測與界線

查核官方文件就足以宣稱範例已實測嗎？

「版本來源、實測與界線」讀圖：沿版本、測試與回復流程，指出交接前最後需要確認的內容。再回答：查核官方文件就足以宣稱範例已實測嗎？

[對應圖解](../assets/figures/28.svg)

作答：＿＿＿＿＿