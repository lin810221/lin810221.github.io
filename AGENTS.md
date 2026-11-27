# 課程網站維護

先閱讀 `COURSE_AUTHORING.md`。課程保留獨立資料夾、深色閱讀器、離線資源及可編輯 Markdown；單元 ID 與筆記／進度儲存鍵必須穩定。

## 數學內容是原稿責任

- 公式寫在原稿，以 `$...$`／`\(...\)` 表示行內式，以 `$$...$$`／`\[...\]` 表示獨立式。不要期待閱讀器猜測普通文字中的算式，也不要用反引號替代數學排版。
- 分配、損失、距離、估計式等定量主題，須在該主題下定義公式、符號、取值範圍、適用條件與算例。其他小節已有公式不能代替本節缺少的定義。
- 新增或修改定量主題時同步維護 `tools/math-topic-coverage.json`。純概念或行動課程不需要為了數量門檻硬塞公式。
- 程式 API、參數、路徑與可複製的程式碼保持程式碼格式。`tools/math-prose-literals.json` 只允許有理由的單位、正式名稱及文字選項，不能加入真正的算式來繞過檢查。
- 中文檔案明確使用 UTF-8；避免將含中文的程式碼經 Shell 標準輸入傳遞。修正後讀回，檢查問號亂碼與不可見控制字元。

## 驗證與交付

1. 執行 `python tools/audit_math_prose.py --strict`。
2. 建置全部課程；發布時使用 `python tools/build.py --require-prerender`。只有 Python 的環境須透過可用 Node 執行 `tools/render_math_cli.mjs` 完成靜態排版後，才能宣稱發布公式已驗收。
3. 執行 `test_math_build.py`、`test_math_editorial.py`、`test_site_review.py`、相關教材下載包測試與 `tools/validate.py`。
4. 執行全站閱讀器測試，核對實際輸出的公式及回歸互動。依修改範圍同步更新離線學習檔、ZIP 與 `dist`。
5. 瀏覽器可用時檢查實際頁面；不可用時清楚區分 DOM／原稿檢查與尚未完成的版面驗收。
