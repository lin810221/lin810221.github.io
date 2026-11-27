# 全站數學內容與排版修正

日期：2026-11-24。本輪覆蓋 **23 門課程、1840 個單元**，包含課文原稿、課程摘要及相關離線學習檔。

## 本輪處理的真正缺口

第一輪主要驗證「已標記為 LaTeX 的公式能否排版」，沒有充分攔住正文中尚未標記的算式，也沒有逐主題檢查定義公式是否缺漏。因此離散均勻分配沒有公式卡片，其他分配卻有；敘述中的平均數、變異數、條件機率、矩陣與導數也仍混有純文字記法。本輪以原稿內容與主題完整性為驗收對象，不以總公式數量作為完成依據。

## 內容修正

- **應用統計**：離散均勻、二項、超幾何及 Poisson 各自有機率質量函數、期望值、變異數、參數範圍、條件和算例。連續均勻補上分段密度與矩；補強平均數、變異數、期望、抽樣分配、信賴區間、檢定、ANOVA 與相關／迴歸等定義。密集公式改成有符號解釋的獨立段落。
- **PyTorch、機器學習與深度學習**：整理梯度、目標函數、矩陣、機率與效能算式；補上 BCE、MSE、SGD、卷積尺寸與 RMSNorm 的正式定義。明確標示平均分母、有效元素及模型條件。
- **Transformer、Embedding、RAG 與搜尋**：整理 attention、向量、距離、Token、快取及評估記法；補強距離與排序指標定義。API 呼叫、參數、程式切片及版本識別保持可複製的程式碼格式。
- **經濟學**：整理導數、彈性、預算、成本、折現、總體模型與會計恆等式；補強缺少的正式公式。現金流逐期折現，符號對應計算時點。
- **健康與生命科學各課**：整理原有比例、效果量、物理量與單位的數學排版；保留量測、診斷適用條件與資料來源。化學名稱、生理指標名稱、正式版本及 DOI 不當成除法；行動課不為湊數新增公式。

「間斷型均等分配」即離散均勻分配，主題已並列兩個名稱。有限等可能結果的通式，與連續整數端點的平均／變異數特例分開解釋；參數範圍與 SciPy 上界不包含的約定依 [randint 官方說明](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.randint.html) 核對。其餘分配並列 [binom](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binom.html)、[hypergeom](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html) 與 [Poisson](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html) 的對照來源。

直接查看：[離散分配](applied-statistics/index.html#17-discrete-families/4-4-1)、[連續分配](applied-statistics/index.html#18-continuous-families)、[PyTorch 損失](pytorch/index.html#18-losses)。

## 防止後續課程重複漏掉

1. `tools/audit_math_prose.py --strict` 掃描所有課文和摘要，找出未受 LaTeX／程式碼標記保護的數學式，以及裸露的 TeX 指令。比較符號不再被誤認為 HTML。`1/k`、`(a+b)/2`、`np`、條件機率與分布記法均有回歸案例。
2. `tools/math-topic-coverage.json` 逐課、逐小節保護 **424 個公式段落**。刪掉離散均勻的公式，即使二項分配仍有公式，也不能通過。新定量主題須同步登記。
3. `tools/math-prose-literals.json` 只列有理由的文字名稱、單位及選項；真算式不得加入例外。程式參數、API、版本與 DOI 保持文字或程式碼角色。
4. 建置先驗證原稿，再產生靜態 KaTeX HTML 與 MathML。發布時使用 `--require-prerender`；無效公式、亂碼、控制字元或裸算式會擋下建置。
5. [AGENTS.md](AGENTS.md) 與 [COURSE_AUTHORING.md](COURSE_AUTHORING.md) 已記錄上述規格，GitHub Actions 加入內容檢查。自動檢查不會替作者發明原本漏寫的知識，新課仍需人工確認定量主題完整性。

## 驗證結果

- 23 門課程建置、連結、TOC、字型與離線資源檢查通過。
- 23 門閱讀器加編號專項，共 **24 組**隔離回歸測試通過；包含搜尋、互動、筆記、進度、下載與章內編號。
- 原稿數學內容 **10 項**、Markdown／LaTeX 邊界 **8 項**、全站品質 **6 項**測試通過。
- 教材與學習包 **122 項**、既有健康圖解 **11 項**測試通過。
- 直接檢查生成 HTML，確認四種離散分配各自的公式與矩、BCE／MSE、摘要及有限差分均有實際 KaTeX 排版；API 程式碼可複製。
- 修改範圍中原有 **160 段 fenced code** 內容比對一致；Python 範例未修改。
- 全站嚴格掃描剩餘裸算式：**0**。此數字指既定檢查規則；不等同數學內容不需要人工審查。

本次沒有可連線的真實瀏覽器，故驗證包含 DOM 與原稿檢查，**不宣稱桌面／手機實際版面或截圖已驗收**。也未重新執行既有課程的 GPU 訓練與外部 API 工作。

## 逐課紀錄

數學式欄包含正文與摘要中的出現次數，含重用；不是不同定理數量。原稿修改單元數以本輪備份對照計算。

| 課程 | 已掃描單元 | 修改原稿單元 | 已排版數學式 | 未解決裸算式 |
|---|---:|---:|---:|---:|
| 人體解剖與生理學 | 120 | 3 | 5 | 0 |
| 應用統計 | 70 | 61 | 744 | 0 |
| 深度學習 | 72 | 56 | 338 | 0 |
| 經濟學 | 84 | 59 | 408 | 0 |
| Embedding | 48 | 14 | 68 | 0 |
| 肌肉骨骼健康與人體工學 | 96 | 19 | 46 | 0 |
| 實證健康與醫學研究判讀 | 108 | 24 | 62 | 0 |
| 運動科學與訓練原理 | 96 | 18 | 43 | 0 |
| 急救與緊急應變 | 120 | 3 | 3 | 0 |
| 影像辨識 | 84 | 59 | 318 | 0 |
| LangGraph 完整教學 | 28 | 5 | 22 | 0 |
| LLM & Agents | 38 | 12 | 10 | 0 |
| 機器學習 | 60 | 40 | 164 | 0 |
| MCP 與工具整合 | 54 | 14 | 12 | 0 |
| 心理健康與壓力科學 | 96 | 2 | 7 | 0 |
| 代謝健康與慢性病預防 | 96 | 25 | 61 | 0 |
| 營養學與飲食科學 | 96 | 17 | 40 | 0 |
| 公共衛生與流行病學 | 120 | 13 | 61 | 0 |
| PyTorch | 48 | 30 | 75 | 0 |
| RAG | 42 | 7 | 60 | 0 |
| 搜尋與向量資料庫 | 60 | 23 | 30 | 0 |
| 睡眠科學與晝夜節律 | 108 | 7 | 15 | 0 |
| Transformer 與 LLM 原理 | 96 | 80 | 534 | 0 |
| **合計** | **1840** | **591** | **3126** | **0** |

## 後續更新流程

```powershell
python tools/audit_math_prose.py --strict
python tools/build.py --require-prerender
python -m unittest discover -s tools -p test_math_build.py -v
python -m unittest discover -s tools -p test_math_editorial.py -v
python -m unittest discover -s tools -p test_site_review.py -v
python tools/validate.py
python tools/prepare_pages.py --target pages
```

更新維持各課既有 ID、網址、筆記與進度鍵，原有軟體版本基準不因排版整理而一律換成新日期。修改在本機與待發布資料夾，尚未 commit 或 push。

## 2026-11-27：SQL與資料工程

新增108單元、58處KaTeX排版，含13個獨立公式區塊。加權平均、JOIN配對數、視窗累計、品質分母、有限重試、恢復目標與新鮮度等定量主題各自記錄於主題覆蓋清單，段落保留符號定義、條件與算例。SQL語法、欄位與API維持程式碼格式。全站嚴格數學文字稽核為零候選；空分母、同值視窗、複合游標等互動邊界另有DOM測試。上表保留原次檢查的歷史數量。

## 2026-11-27：多模態與文件AI

新增96單元、132處KaTeX排版，含22個獨立公式區塊。DPI、正規化與反向座標、IoU、切片數、CER、金額、餘弦相似度、對比損失、MaxSim、RRF、ANLS、F1、風險覆蓋、音訊取樣、半開時間、抽幀與像素預算均在對應主題定義符號、條件與算例。空參考、空保留集合、ANLS門檻邊界、零向量及原頁引用各自有明確政策與測試；API、MIME和檔案路徑維持程式碼格式，不擴大例外清單。全站原稿嚴格稽核與數學編輯回歸通過。
