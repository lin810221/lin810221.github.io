## 記憶至少有三種

對話歷史記錄說過什麼；工作狀態記錄任務做到哪裡；長期偏好記錄可跨對話使用的應用資料。把它們全部塞進一個 messages 列表，會讓更新、刪除與權限難以管理。

模型上下文是當輪看見的資訊，不等於完整資料庫。你可以保存長期紀錄，再按需召回相關內容，而不是每次全部送入模型。

## 一份簡單的 SQLite 儲存

此範例將對話以 owner + thread 隔離，偏好則以 owner 共享。它使用參數化 SQL，並在配置序號時使用寫入交易。

<!-- example:memory_store.py -->

## 關閉後重新開啟

<!-- example:10_memory.py -->

範例先關閉連線再重新開啟，驗證資料確實來自 SQLite，而不是 Python 物件仍然活著。預設使用臨時資料夾，示範結束後清理；正式資料請選擇明確持久路徑。

## 身分範圍不等於登入系統

資料查詢都有 owner，不代表應用已有認證。服務端必須從可信登入身分取得 owner，不能讓使用者任意填入另一個人的值。

同一人的兩條 thread 可共享偏好，但聊天歷史不同。不同人即使剛好有同名 thread，也不能互相讀到紀錄。

## 什麼值得記住？

明確的語言偏好、經確認的使用者資訊或工作設定可以保存；模型猜測、暫時要求和外部網頁指令不應自動成為永久偏好。

保存來源、確認狀態和更新時間，避免衍生記憶比原始資料更難追溯。記憶更新本身也可能需要審核或撤銷機制。

## 召回和長度管理

小型偏好可直接按 key 取得；大量知識可使用檢索。送入 prompt 的資料應和任務相關，並保留權限範圍。摘要能縮短歷史，但可能遺漏細節，必要時要能回查原文。

清除記憶時，也要考慮對話、索引、checkpoint、快取和追蹤紀錄。只是不再把一段文字送進模型，不等於資料已刪除。

**練習：**加入第二個 thread，確認能讀到同一人的語言偏好，但看不到另一條完整聊天。再用另一個 owner 測隔離。

官方來源：[OpenAI conversation state](https://developers.openai.com/api/docs/guides/conversation-state)、[Gemini Interactions](https://ai.google.dev/gemini-api/docs/interactions-overview)、[LangGraph memory](https://docs.langchain.com/oss/python/langgraph/add-memory)。
