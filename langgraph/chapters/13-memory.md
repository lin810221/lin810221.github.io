## 記憶不是單一功能

把對話歷史存起來，只完成記憶的一部分。應用還要決定要記什麼、何時更新、哪些內容要送進模型，以及何時刪除。

| 面向 | 短期記憶 | 長期記憶 |
| --- | --- | --- |
| 常用元件 | Checkpointer + State | Store |
| 範圍 | 同一 thread 的執行狀態 | 應用定義，可跨 thread |
| 例子 | 本輪文件、對話訊息、待審核草稿 | 語言偏好、經驗證的使用者資訊 |
| 讀取方式 | 載入 thread 狀態 | 節點明確查詢 Store |

「長期」描述用途，**不保證底層儲存真的耐久**。`InMemoryStore` 和 InMemorySaver 一樣會隨程序結束遺失。

## Store 的基本讀寫

```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
namespace = ("users", "student-01", "preferences")
store.put(namespace, "language", {"value": "zh-TW", "confirmed": True})
item = store.get(namespace, "language")
if item is not None:
    print(item.value["value"])

# 與建好的圖一起使用：
# graph = builder.compile(store=store, checkpointer=checkpointer)
```

namespace 是用來分組的 tuple，key 識別其中的項目，value 是應用資料。要在節點使用，可從 `runtime.store` 取得 compile 時注入的 Store；但使用者識別應來自可信的 context。

namespace 不是自動的存取控制：如果服務允許任意使用者指定另一個人的 namespace，一樣會跨界。應由後端建立並檢查可用範圍。

## 保存與召回需要設計

使用者明確說「之後請用繁體中文」可以成為偏好候選，但「這次幫我用英文翻譯」不一定代表永久偏好。模型推論的記憶應有來源與確認機制，尤其不能把查到的外部文件當成使用者意願。

語意搜尋需要另外配置 embedding 與索引，不是呼叫 `put()` 後就自動理解所有文字。儲存的資料也不會自行出現在 prompt；節點必須選取與當輪問題相關的項目，再放入模型上下文。

## 對話長度如何控制？

保存整段訊息和送出整段訊息是兩件事。可以保留完整歷史供稽核，但只將模型需要的片段送進 context。常見策略有最近數輪、token budget、摘要加近期訊息，以及相關記憶召回。

不要直接任意截斷列表。工具請求與 ToolMessage 要保持配對，system 規則要保留，多模態內容也會占上下文。依模型的 tokenizer 與訊息規範做 trim，比數字元可靠。

摘要同樣可能遺漏資訊。保存摘要的來源範圍、更新時機與版本，並保留需要查回的原始紀錄。摘要不應被默認為比原始資料更可信。

## 刪除與更新

更新長期記憶時，選用穩定 key，避免每次都新增一份相互矛盾的偏好。清理資料時要考慮 Store、checkpoint、檢索索引與追蹤紀錄，不是只從 prompt 移除就等於刪除。

**練習：**讓同一個 user_id 使用兩條 thread，兩條都讀到同一份語言偏好，但對話訊息保持獨立。這能清楚展示 Store 與 checkpointer 的不同角色。

官方來源：[Memory](https://docs.langchain.com/oss/python/langgraph/add-memory)、[Stores](https://docs.langchain.com/oss/python/langgraph/stores)。
