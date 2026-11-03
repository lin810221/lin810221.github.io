# 舊能力與新擴充：Roots、Sampling、Tasks

辨識核心、棄用功能與選用擴充，不把規範存在誤認為整個生態已支援。

## 為什麼這些名詞仍會出現

早期 MCP 教材常介紹 Roots、Sampling、logging 與 Tasks。這些名詞有各自用途，但在新協定中的位置與生命週期已不同。閱讀文章時先核對協定日期，再看 SDK 版本，最後確認目標 Host 的實際支援，避免把不同時期的範例拼在一起。

Roots 是 Client 告知 Server 可考慮的檔案根目錄；它從來不是作業系統強制沙箱。Sampling 則曾讓 Server 請 Client 代為使用模型能力；它需要明確的政策、成本控制和內容檢查，不能視為 Server 免費取得任意模型的保證。

## 新版中的棄用與相容性

2026-07-28 將 Roots、Sampling 與協定 logging 列為棄用能力，ping 已移除。棄用不等於當天所有舊 Client 都停止運作，也不表示可以依賴它們做新系統的唯一主線。若為了既有 Host 保留舊模式，應清楚列在相容性矩陣與測試中。

需要使用者輸入時，優先考慮當前推薦的 Resolve／Elicitation 與 MRTR；需要應用日誌時，使用正常的結構化日誌與 tracing。不要為了沿用某段舊教學而讓整個服務永遠停在 legacy mode。

## Tasks 是正式擴充路線

Tasks 用於長時間非同步工作、可保存的 handle、查詢狀態與中途輸入。現代規範已將它從核心拆為選用擴充；查核時官方列為 Beta、預計走向核心。它不等於隨便回傳一個 job_id，也不等於讓工具請求一直開著。

本課不假設 Python SDK 2.3.0 已完成 Tasks 擴充的全部行為，因此採一般工作佇列概念說明，並將支援狀態交給官方 roadmap 和兩端功能測試確認。自己實作的背景工作 API 應明確稱為應用層 job 介面，不能冒稱協定 Tasks 相容。

## 擴充有自己的生命週期

擴充通常有帶 vendor prefix 的識別，並需 Client 與 Server 明確支援。Experimental、Beta、Stable 的變更承諾不同，擴充版本也不必與 SDK 主版本同步。未宣告的選用擴充，不能只因為工具 metadata 出現某個鍵就假設已協商成功。

## 練習與解答

看到 Server 宣稱支援 Tasks，Host 卻只能一般 tools/call，是否能直接開始長任務？不應；要先確認兩端能力、處理方式、取消及保存語意。再問 Roots 能否阻止 Server 讀其他磁碟？不能，還需要程序權限、檔案開啟限制與實際沙箱。

## 官方閱讀

- [Deprecated features](https://py.sdk.modelcontextprotocol.io/deprecated/)
- [擴充總覽與狀態](https://modelcontextprotocol.io/extensions/overview)
- [Python SDK roadmap](https://github.com/modelcontextprotocol/python-sdk/blob/main/ROADMAP.md)
