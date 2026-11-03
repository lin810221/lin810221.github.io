# MCP Apps、Skills 與 Registry：下一步如何延伸

認識當前擴充生態與支援狀態，保持 UI、工作流程與執行權限的分離。

## Apps：工具結果也能有互動介面

MCP Apps 讓相容 Host 在對話內呈現表格、圖表、表單等互動 UI。查核時官方列為 Stable 擴充，但仍需 Host 與 Server 同時支援。普通工具回傳一段 HTML，不等於已完成 Apps 整合。

常見做法是註冊 UI 資源，將工具 metadata 連到它，再由 Host 按規範載入。資料與 UI 應有清楚邊界，包含內容來源、允許連線、CSP 與訊息傳遞。UI button 不能繞過 Server 的授權或自行把核准狀態改成可信。

## Skills：分發流程知識

Skills over MCP 讓 Host 探索與讀取工作流程指示和支援檔案。它描述怎麼做事，可以與工具互補；工具提供可執行能力，Skill 提供使用流程。查核時此擴充為 Beta，實際支援仍要查看官方 client matrix。

Skill 內容屬於需要信任管理的指示來源，不能因為它放在 MCP Resource 裡就無條件給最高權限。描述「部署流程」不代表使用者已同意部署，也不代表 Server 可以取得未授權憑證。

## Tasks 與其他擴充

Tasks 在查核時屬 Beta、規劃走向核心；Server Cards 與部分發現能力也有自己的狀態。擴充識別、版本與 capability 要由雙端處理，不應因為 Python SDK 的同名 module 存在，就假設某個 Host 一定能用。

對新功能，可以先做單獨能力探測與最小整合，再放入正式工具集合。若目標 Host 不支援，保留一般工具／資源的降級路線，並在 UI 說明缺少哪一種互動。

## Registry 提供發現，不提供信任保證

Registry 協助找到 Server 與相關 metadata，但套件來源、部署者、權限和實際執行內容仍需要審查。出現在公開列表，不等於可以直接把公司 Token 交給它；工具描述也不是完整安全審計。

導入第三方 Server 時，至少核對維護者、版本、需要的權限、資料流向、更新方式與撤銷方案。先用虛構資料與最小 scope 驗證，再決定是否接正式資源。

## 練習與解答

你要在對話中呈現工單核准表單，應使用 Apps 嗎？若 Host 支援，它可以改善介面；但核准仍要綁定可信審核者與不可變預覽。表單本身只是互動表面，不是授權事實。這個區分能讓未來新增 UI 時保留既有交易與安全模型。

## 官方閱讀

- [擴充狀態](https://modelcontextprotocol.io/extensions/overview)
- [Python SDK Apps](https://py.sdk.modelcontextprotocol.io/advanced/apps/)
- [Python SDK Skills](https://py.sdk.modelcontextprotocol.io/advanced/skills/)
- [MCP Registry](https://registry.modelcontextprotocol.io/)
