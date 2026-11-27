# RelayDesk資料字典

## Credential

digest是高熵隨機token的SHA-256 hex摘要，tenant是受信任租戶識別，role只有reader或editor。它是服務金鑰模型，不是使用者密碼保存方案。真正token只在佈建輸出，資料庫沒有可反解的原文。

## Document

id是資料庫整數主鍵；tenant與digest共同唯一；title最多120字元；text是不可變原文、最多4096字元。version由1開始，每次標題更新或邏輯刪除增加；ETag使用帶雙引號的版本。deleted為0或1的應用旗標；邏輯刪除保留原文與摘要，查詢與worker選取會隱藏。這不是完整隱私資料清除。

## Job

id是隨機32字元hex，不能代替授權。tenant加key共同唯一；fingerprint為已正規化request_json的SHA-256。request包含問題與視為集合的排序文件ID。state為queued、running、succeeded、failed或cancelled。attempt為claim次數；lease_until是Unix整數秒；lease_token每次claim更新；cancel_requested為0或1。result_json只在成功且未取消時保存。時間由同機時鐘提供，本課沒有跨機器續租治理。

## Event

id是全表整數主鍵，單一工作內不保證連號。job_id外鍵連到Job，kind與data_json保存安全狀態。每批最多100筆，按id升序且只取大於cursor。沒有自動保留清除政策；正式刪除歷史時需另外定義過期cursor的回復方式。

## Answer與Citation

status為answered或abstained；text為有限文字；citations列document_id、start、end和quote。offset是Python Unicode字串位置，零起算、起點含而終點不含，不是UTF-8 bytes也不是視覺字形數。quote必須等於同一原文切片。抽句provider額外要求答案等於引用句；遠端自由改寫仍需語意評估。

## 合成資料與能力邊界

預設政策只有Warranty lasts 12 months與Delivery takes 7 days。unicorns沒有證據而拒答。沒有真實客戶資料、模型權重或正式API key。抽句以簡單詞交集挑原文行，不是BM25或Embedding；MockTransport只驗證供應商介面，不代表雲端品質。
