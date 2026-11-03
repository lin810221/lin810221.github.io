# 工具契約測試：成功之外也要驗證拒絕

把工具清單、Schema、錯誤與資源清理變成可以重複執行的驗收條件。

## 好的測試保護哪個承諾

工具契約包含名稱、參數形狀、輸出形狀與失敗行為。測試應關注呼叫者依賴的承諾，而不是只確認函式內部用了哪個變數。對搜尋工具而言，合法空結果、上限控制、錯誤型別與跨租戶隔離，比測試某行文字是否完全一樣更有價值。

先寫純領域測試，再透過真實 SDK Client 呼叫。前者較容易精確定位交易規則，後者能抓出 Schema、欄位名稱與 SDK 包裝行為的落差。兩者不應互相替代，也不必為每個印字或裝飾樣式建立脆弱測試。

## 建立最小契約案例

```python
async def check_search(client):
    tools = (await client.list_tools()).tools
    definition = next(tool for tool in tools if tool.name == "search_notes")
    assert "query" in definition.input_schema["required"]
    valid = await client.call_tool("search_notes", {"query": "MCP", "limit": 2})
    assert not valid.is_error
    assert len(valid.structured_content["matches"]) <= 2
    invalid = await client.call_tool("search_notes", {"query": "MCP", "limit": 0})
    assert invalid.is_error
```

這段測試同時確認「宣告什麼」與「實際怎麼做」。但它尚未測試 stdout 污染、HTTP Origin、驗證 Token 或目標 Host；測試報告要保留這個範圍。

## 拒絕案例比常見 happy path 更有辨識力

測試 limit=0、字串型數字、未知工具、無權限文件、過期預覽、同鍵不同操作，以及交易中斷。若所有案例都只確認成功結果含有一個字串，即使工具根本沒有執行權限檢查，也可能全部通過。

對於有副作用操作，測試應直接檢查資料狀態、版本、收據數與稽核數。看到一個「已執行」訊息不足以證明只執行一次；也不能只 mock 掉資料庫後宣稱交易回滾已驗證。

## 用故障注入檢查原子性

本課在狀態更新之後、收據寫入之前注入例外。如果交易邊界正確，工單狀態應回復，收據與 committed audit 也不應出現。這種測試能抓出「業務效果已發生但沒有收據」的危險窗口。

## 練習與解答

列出三個只測 happy path 會漏掉的問題。參考答案：其他租戶能讀到同名工單、逾時後重試產生第二次效果、模型可以直接傳 approved=true。為每項安排一個明確的反例，測試重點應是 Server 拒絕與狀態不變，而不是模型有沒有遵守提示。

## 官方閱讀

- [SDK 測試](https://py.sdk.modelcontextprotocol.io/get-started/testing/)
- [輸出契約](https://py.sdk.modelcontextprotocol.io/servers/structured-output/)
- [協定來源](https://modelcontextprotocol.io/specification/2026-07-28)
