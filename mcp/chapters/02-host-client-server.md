# Host、Client、Server：資料如何穿過系統

畫出控制流程與資料邊界，理解誰持有模型、連線及外部權限。

## 角色與實體不是一對一

Host 是使用者操作的 AI 應用，例如桌面助理、IDE 或你自己的網頁後端。Client 是 Host 內部用來連接某個 MCP Server 的元件。一個 Host 可以管理多個 Client；Server 則可以服務多個 Host。角色描述責任，不能直接等同於一個 Python 檔案或一台機器。

在本課，瀏覽器教材只是閱讀與互動示範，不會啟動你的工具。執行 Python 範例後，才會建立測試 Client 與 Server。模型 API 也不會因為建立 Client 而被偷偷呼叫；第一條實作路線完全不需要 API Key。

## 一次工具呼叫的路徑

使用者先提出問題，Host 選擇可用工具並將描述送給模型。模型產生工具名稱和參數後，Host 檢查允許清單與執行預算，再由 Client 發送 `tools/call`。Server 重新驗證輸入、身分及業務條件，執行後回傳結果。Host 將可用結果交回模型，最後呈現回答。

```text
使用者 → Host → 模型提出呼叫
             → Client → MCP Server → 工單系統
             ← 結果   ← 執行事實  ← 交易結果
             → 模型整理 → 使用者
```

同一條路上有不同類型的信任：模型的建議、傳輸過來的資料、驗證過的呼叫者身分，以及資料庫確認的交易結果。不能把其中一種當成另一種，尤其不能因為模型說「成功」就記錄結案成功。

## 整合數量的直覺

若有 $H$ 個 Host 與 $S$ 個能力系統，完全客製的成對整合最多需要 $H S$ 條介面；採用共同協定後，可把主要維護面收斂為 Host 端與 Server 端的實作：

$$
C_{pair}=H\times S,\qquad C_{standard}\approx H+S
$$

這是架構成本的示意，不是效能公式。不同 Host 對資源、授權與新版本的支援仍可能不同，因此共同協定能減少重複，不能消除相容性測試。

## 誰保管憑證

模型供應商 API Key 由呼叫模型的應用保管；MCP 存取 Token 用於 Host／Client 到 Server；Server 呼叫上游系統的憑證則屬於另一個授權關係。三者不應共用或互相轉送。Server 可以是代理人，但必須知道自己代表哪個主體，以及要操作哪個資源。

## 練習與解答

如果同一個工具被桌面助理與自製 Agent 使用，是否一定要建立兩個 Server？不必；可以共用符合契約的 Server，但兩個 Client 的使用者、允許範圍及 Token 可能不同。接著標出「工具清單快取」的位置：它可以在 Client 或 Host，但快取鍵需反映權限與版本，不能把甲的工具可見性直接重用給乙。

## 官方閱讀

- [架構](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
- [Client](https://py.sdk.modelcontextprotocol.io/client/)
