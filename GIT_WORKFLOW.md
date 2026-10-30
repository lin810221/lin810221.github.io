# Learning Notes 的日常更新與自動發布

個人網站：<https://lin810221.github.io/>

GitHub repository：<https://github.com/lin810221/lin810221.github.io>

## 之後如何更新？

日常流程是：**本機修改 → Commit → Push → GitHub Actions 編譯與檢查 → GitHub Pages 更新網站**。

Commit 把一組修改存成有說明的版本；Push 把本機版本傳到 GitHub。GitHub Actions 接著執行已設定的工作，全部檢查通過後才更新網站。

這份專案的完整原始碼應保存在 repository，包括 `chapters/*.md`、`course.json`、範例、閱讀器、樣式與工具。網站訪客取得的是編譯後的靜態頁面和範例下載；自動發布時會先整理成 `dist/`。

## 第一次接上自動發布

第一次透過網頁拖曳上傳的是可發布檔案，因此網站已能顯示，但 repository 尚未包含全部 Markdown 原稿與編譯工具。要啟用新流程，需要先把這個本機原始碼專案提交並推送一次。

`.github/workflows/deploy-pages.yml` 已定義自動編譯、驗證、範例測試與發布。它在 `main` 收到 Push 時執行，也可以從 Actions 頁面手動啟動。沒有使用任何模型 API Key，範例測試使用離線資料或 mock。

只需要做一次的 GitHub 設定：

1. 打開 repository 的 **Settings → Pages**。
2. 將 **Build and deployment → Source** 選為 **GitHub Actions**。
3. 將這份完整原始碼和 workflow 提交並推送到 `main`。
4. 打開 repository 的 **Actions**，查看 **Build and deploy Learning Notes**。
5. Build 和 Deploy 都成功後，使用相同的網站網址查看更新。

Source 改成 GitHub Actions 後，分支和資料夾由 workflow 決定。若編譯或測試失敗，這次 workflow 不會進入 Deploy；先閱讀失敗步驟的訊息，修正後再 Push。

## 用 SourceTree 操作

本機已有 Git repository 後，可在 SourceTree 用 **Add / 新增現有工作目錄**，選擇：

```text
D:\DSPBD\10 - Software Development\11 - 需求\LearningNote
```

確認 Remote 是：

```text
https://github.com/lin810221/lin810221.github.io.git
```

第一次 Push 若要求登入，透過 SourceTree 的 GitHub 帳號登入流程完成；Commit 作者名稱與 email 也應使用你希望顯示在 GitHub 的身分。

每次更新：

1. 修改前先用 **Pull** 取得遠端最新版本。
2. 在本機修改 Markdown、程式或樣式。
3. 在 SourceTree 的 **File Status** 檢查變更，選取要提交的檔案。
4. 輸入清楚的訊息，例如 `新增 LLM 課程章節`，按 **Commit**。
5. 按 **Push**，將 `main` 推送到 `origin/main`。
6. 查看 GitHub Actions 的這次執行是否成功，再重新整理網站。

通常不需要重新拖曳網站檔案，也不需要為每次修改重新設定 Pages。

## 修改不同內容時要編輯哪裡？

| 修改內容 | 編輯位置 |
| --- | --- |
| 課程文字 | 各領域 `chapters/*.md` |
| 章節順序、標題與摘要 | 各領域 `course.json` |
| Python 範例 | 各領域 `examples/*.py` |
| 共用深色樣式 | `assets/style.css` |
| 共用閱讀互動 | `assets/reader.js` |
| LLM 互動實驗室 | `llm/assets/overview.js`、`llm/assets/course.css` |
| 學習首頁 | 根目錄 `index.html` |

`course-data.js` 和 `llm/examples.zip` 是產生檔；編譯會依原稿重建，不要只在產生檔修改教材。repository 可保留產生檔供離線閱讀；每次自動發布仍會重新編譯。

新增領域時，建立其 `course.json`、Markdown、頁面及需要的資產，再更新學習首頁連結。編譯器會發現第一層資料夾中的課程；發布工具會整理對應網站檔案。

## 本機預覽與檢查

閱讀網站仍可直接開啟 `index.html`。修改原稿後若要在本機預覽，先執行：

```powershell
python -m pip install -r tools/requirements.txt
python tools/build.py
python tools/validate.py
```

想完整重跑 CI 使用的 Python 測試，可在獨立虛擬環境安裝 `tools/requirements-ci.txt`，再執行 workflow 中的兩組測試。GitHub 會在乾淨環境自動執行這些步驟。

## `.nojekyll` 的用途

這個檔案告訴分支式 Pages 發布流程：不要用 Jekyll 產生器額外處理檔案。沒有它，許多靜態頁面仍然可以正常提供，因此它不是網站能顯示的必要條件。

新的 Actions 流程會直接發布 `dist/` 成品，沒有使用 Jekyll。保留 `.nojekyll` 仍適合這份靜態網站，且不用每次手動建立。

## 本機資料與發布成品

`.gitignore` 排除虛擬環境、`.qa/`、測試快取、`.env`、本機 SQLite、`github-upload/` 和 `dist/`。它們不屬於要提交的原始碼。

`python tools/prepare_pages.py --target pages` 產生自動部署的 `dist/`，沒有瀏覽器一次上傳 100 檔的限制。舊的 `python tools/prepare_pages.py` 仍可產生 `github-upload/`，留作臨時手動上傳用途。

筆記與閱讀進度仍保存在各自瀏覽器 localStorage。網址不變時，正常程式更新不會主動清除它們；它們仍不會跨裝置同步。

## 官方文件

- [GitHub Pages 自訂工作流程](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub Pages 發布來源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [將現有 repository 加入 SourceTree](https://support.atlassian.com/sourcetree/kb/add-an-existing-repository-into-sourcetree/)
