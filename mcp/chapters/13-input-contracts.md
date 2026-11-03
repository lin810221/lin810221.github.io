# 輸入契約：JSON Schema、型別與限制

把可接受的輸入寫清楚，避免將模型輸出直接視為可信參數。

## Schema 是可被機器檢查的承諾

工具輸入通常是 object，properties 描述欄位，required 描述哪些必填。型別還不夠：字串可能需要最小長度，數字需要範圍，選項需要 enum，物件可能需要禁止額外欄位。這些限制同時幫助模型產生參數，以及 Server 在執行前阻止無效輸入。

MCP 對未聲明 dialect 的 Schema 以 JSON Schema 2020-12 為預設。Host 和 Server 必須知道支援哪一種方言；不能因為某個模型只支援簡化 Schema，就悄悄改掉 Server 的正式契約。必要時建立 adapter，並保留伺服器端完整驗證。

## Python 型別如何轉為 Schema

官方高階 Server 能從函式型別和 Pydantic `Field` 產生輸入 Schema。`query` 用長度限制，`limit` 用 strict integer 和上下限，會比只寫「請提供合理頁數」更可靠。必填、帶預設值與允許 null 是三個不同概念，不能互相替代。

```python
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

class Query(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(min_length=1, max_length=100)
    limit: Annotated[int, Field(strict=True, ge=1, le=10)] = 5
```

若採巢狀模型作為工具參數，線上輸入也會出現對應巢狀結構，不應假設 SDK 自動把模型欄位攤平。修改前先看 `list_tools()` 所回傳的 input schema。

## 型別轉換可能掩蓋問題

某些驗證器會把字串 `"2"` 轉成數字 2。這可能方便一般表單，但對需要嚴格契約的工具，應明確選擇是否允許。Python 的 bool 還是 int 的子型別，因此純 `isinstance(value, int)` 可能接受 True；本課範例以 strict integer 防止這種意外。

Schema 驗證之後還有業務規則。字串長度合法，不表示工單存在；工單存在，不表示屬於此租戶。輸入驗證、授權與狀態檢查應依序發生，避免在檢查權限前把敏感資料回傳給模型。

## 練習與解答

分別傳入 limit=2、0、11、`"2"`、True。只有 2 符合此範例契約。再試傳入空白 query：長度限制可能仍讓空白通過，因此若業務要求非空白內容，需在領域層 strip 後檢查。Schema 與業務驗證各自有責任，不能假設其中一個涵蓋全部。

## 可執行範例

在 `examples` 目錄執行 `python 07_input_schema.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:07_input_schema.py -->

## 官方閱讀

- [工具輸入](https://py.sdk.modelcontextprotocol.io/servers/tools/)
- [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation)
