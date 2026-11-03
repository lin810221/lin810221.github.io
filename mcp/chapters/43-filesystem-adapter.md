# 檔案工具：限制目錄、格式與讀取量

把檔案存取包成有邊界的能力，避免任意路徑與超大文件讀取。

## 先決定要分享哪一組文件

若需求是讀取專案手冊，適合的介面通常是文件 ID 或受控相對路徑，而不是任意絕對路徑。Server 管理固定 root，確認目標仍在其內，再檢查格式、大小與呼叫者 ACL。模型不應自行決定可以讀取整個使用者目錄。

本課只允許 root 內的 .txt，並以有上限的 binary read 取得內容後解碼。這是最小檔案 adapter，不是完整文件管理平台；正式平台還需版本、資料分類與主體權限。

## 路徑穿越與 prefix 陷阱

`../outside.txt` 可以離開表面目錄。單純做字串 startswith 也不安全，例如 docs 與 docs-private 可能有共同前綴。應使用解析後的路徑關係檢查，並考慮絕對路徑、Windows drive、symlink、null bytes 與平台差異。

SDK 的 URI 模板提供部分 path safety 保護，但自訂讀檔程式仍要維護自身邊界。MCP Roots 更不是檔案系統沙箱，不應因為 Client 告知 root 就讓 Server 跳過實際存取控制。

## 有界讀取與格式驗證

先 stat 再讀完整檔案，可能在檔案變大時超出限制。本課最多讀 `max_bytes + 1`，若多一個 byte 就拒絕。這能控制一次取得的資料量，但不替你保證文字編碼正確；解碼失敗應回傳可理解錯誤，不應隨便替換後宣稱內容完整。

對 PDF、Office、圖片等格式，還需要獨立 parser、資源上限與隔離策略。不要把檔名副檔名當成內容一定安全的證據，也不要在閱讀文件時自動執行內嵌程式。

## 時間差與更強隔離

解析安全路徑後到 open 之前，若攻擊者能修改 symlink 或目錄，仍可能有 race。教學函式假設 root 不能被不可信程序同時修改。正式需求若不滿足此假設，需用平台支援的安全開啟策略、檔案描述符相對存取或隔離容器與唯讀掛載。

這個限制要寫進部署條件，不能只因測試成功拒絕一次 ../，就宣稱所有檔案攻擊都已解決。

## 練習與解答

範例在臨時目錄建立可分享文件與外部文件，正常讀取應成功，路徑穿越應拒絕。再測超過大小、錯誤副檔名與絕對路徑。解答應檢查「未讀取外部資料」與「失敗後沒有部分內容被回傳」，而不是只看錯誤訊息包含安全兩字。

## 可執行範例

在 `examples` 目錄執行 `python 27_filesystem.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:27_filesystem.py -->

## 官方閱讀

- [URI 模板安全](https://py.sdk.modelcontextprotocol.io/servers/uri-templates/)
- [本機 Server 安全](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
