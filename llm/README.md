# LLM 服務與 AI Agents

直接開啟 `index.html`；本機閱讀不需要伺服器、網路或 API Key。共 38 章，涵蓋 OpenAI Responses、Gemini Interactions、Claude Messages、功能參數、多模態、RAG 與 Agent 工程。

官方文件核對日期：2026-10-29。使用環境變數選擇模型，避免把會變動的模型可用性寫死。新版介面與舊教學的差異在章節內明確說明。

`chapters/*.md` 為教材原稿；`course.json` 為章節與分組；`assets/overview.js` 為本機參數與採樣實驗室。閱讀器、深色樣式、程式碼色彩與公式引擎共用根目錄 assets。

修改後從學習空間根目錄執行 `python tools/build.py llm`。`examples/README.md` 說明 12 份 Python 入口、共用模組、離線測試與明確開啟的 --live 模式。

閱讀進度與章節筆記使用獨立的 `learning-notes:llm:v1` 瀏覽器儲存，不與 LangGraph 混用。它不是跨裝置同步服務。
