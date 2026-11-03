# 不可變預覽：綁定主體、內容與版本

讓使用者核准的變更，和伺服器真正執行的變更保持一致。

## 為什麼核准前先產生預覽

「關閉工單」看似簡單，實際上可能影響通知、報表與後續任務。預覽把操作、目標、原狀態、新狀態與資源版本具體列出，讓審核者確認。它不應直接執行正式變更，但可能保存待審核紀錄，因此也不一定是純唯讀工具。

本課 Server 產生隨機 preview_id，保存 issuer、tenant、subject、payload、digest、期限與狀態。模型只拿到識別與可顯示內容，不能在 commit 時重新提供任意 ticket_id 或目標狀態。

## 不可變的意義

如果使用者核准 T1，而提交時模型可以改成 T2，核准便失去意義。應保存或簽封原始 payload，並在執行時驗證它沒有改變。雜湊可以偵測內容變化，但若攻擊者能任意修改 payload 和 hash，單一 hash 不能保護整個資料庫；儲存本身仍需可信。

```text
預覽：operation + resource + version + proposed_change
綁定：issuer + tenant + subject + expiry
執行：preview_id + idempotency_key
```

對另一個使用者或租戶使用相同 preview_id，應被拒絕。隨機不可猜識別可以降低被猜中的機會，但不能取代主體綁定與權限檢查。

## 避免核准後資料已變

審核期間工單可能已被別人更新。執行時使用預覽保存的 version 做 optimistic concurrency check，只有目前版本符合時才套用變更。若版本改變，合理處理是建立新預覽、重新審核，而不是忽略衝突強行覆寫。

本課 UPDATE 同時檢查 tenant、ID、原狀態與 version，並確認恰好改一筆。這比先 SELECT 確認後，再做一個沒有版本條件的 UPDATE 更能避免時間差覆寫。

## 期限與使用後狀態

預覽有短期限，執行後標成 consumed。期限到後不應只在 UI 顯示過期，Server 必須拒絕；已 consumed 的預覽也不能換新冪等鍵再次執行。若是同一鍵重送，則走既有收據路徑，不重新使用核准。

## 練習與解答

在產生預覽後，把工單 version 從 1 改成 2，再提交核准預覽，應失敗且不留下 committed audit。另一個測試是修改保存的 payload 而不更新 hash，應在執行前拒絕。兩者分別驗證「資源仍是原版本」與「提案仍是原內容」。

## 官方閱讀

- [MRTR state protection](https://py.sdk.modelcontextprotocol.io/handlers/multi-round-trip/)
- [安全與狀態綁定](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
