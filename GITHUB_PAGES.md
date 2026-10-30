# 用 GitHub Pages 發布 Learning Notes

這份網站使用 HTML、CSS、JavaScript 和已產生的課程資料，可以直接由 GitHub Pages 提供。閱讀時不需要 Python、Node.js、API Key 或後端服務。

網站目前已在 <https://lin810221.github.io/> 上線。**日常更新建議使用 Git / SourceTree 的 Commit、Push，加上 GitHub Actions 自動編譯與發布**，完整步驟見 [GIT_WORKFLOW.md](GIT_WORKFLOW.md)。下面保留第一次手動上傳與備用操作的說明。

## 選擇網址

- 個人主站：建立名稱為 `你的帳號.github.io` 的 repository，網址為 `https://你的帳號.github.io/`。
- 獨立學習網站：例如建立 `learning-notes` repository，網址為 `https://你的帳號.github.io/learning-notes/`。

目前使用個人主站 repository `lin810221.github.io`；網站採相對路徑，未來若調整部署路徑，也可依需求設定。

## 最少發布步驟

1. 在 GitHub 建立 repository。若使用 GitHub Free，GitHub Pages 需要公開 repository。
2. 將此專案加入版本控制並 push 到 repository 的 `main` 分支。也可以先用 GitHub 網頁上傳網站檔案。
3. 進入 repository 的 **Settings → Pages**。
4. 在 **Build and deployment → Source** 選擇 **Deploy from a branch**。
5. Branch 選 **main**，資料夾選 **/(root)**，按 **Save**。
6. 等待發布完成，再使用 Pages 設定頁顯示的網址。

根目錄的 `.nojekyll` 用來停用不需要的 Jekyll 處理；請保留這個檔案。入口是根目錄 `index.html`。

## 要上傳哪些檔案？

第一次透過 GitHub 網頁上傳時，建議先在本機執行：

```powershell
python tools/prepare_pages.py
```

這會產生 `github-upload/`，只包含可直接發布的網站檔案與範例下載，並檢查頁面連結、字型及 GitHub 網頁上傳限制。請開啟這個資料夾，將**裡面的全部內容**拖入 GitHub 上傳頁面；不要把 `github-upload` 外層資料夾一起上傳，根目錄應直接看到 `index.html`、`.nojekyll`、`assets/`、`langgraph/`、`llm/`。

上傳後按畫面的 Commit changes（儲存這次上傳），再設定 Pages 的 main / (root)。這種方式讓 GitHub 保存可發布版本，Markdown 原稿與編譯工具仍保留在你的本機學習資料夾。

如果 GitHub 的檔案列表沒有 `.nojekyll`，可點 Add file → Create new file，檔名填 `.nojekyll`，內容填 `# Serve static files without Jekyll.`，再 Commit changes。檔案存在即可停用 Jekyll；加入一行內容能讓它更容易透過網頁上傳。

若改用 Git / SourceTree 管理完整原始碼，可使用以下方式：

根目錄保留 `.nojekyll`、`index.html`、`.gitignore`、README 和發布說明；上傳 `assets/`、`langgraph/`、`llm/` 與 `tools/` 的原始碼及已產生檔案。保留 `llm/examples.zip`，供讀者下載完整範例。

使用 Git / SourceTree 時，現有 `.gitignore` 已排除 `.venv/`、`.qa/`、測試快取、`.env` 與本機 SQLite。若用 GitHub 網頁手動上傳，`.gitignore` 不會幫你過濾拖入的資料夾，請自行略過這些本機項目。

Python 範例只供閱讀或下載；GitHub Pages 不會替讀者執行 Python，也不會呼叫模型服務。

## 手動更新備用方式

一般更新依 [Git 自動發布流程](GIT_WORKFLOW.md)，不需要重複拖曳。以下供本機檢查或臨時手動上傳使用。

編輯 Markdown 與 `course.json` 後，在本機執行：

```powershell
python tools/build.py
python tools/validate.py
```

將原稿和更新後的 `course-data.js` 一起 commit / push；若 LLM 範例有改，編譯時會重新產生 `llm/examples.zip`。Pages 會依發布分支的更新重新發布。

若第一次是使用 `github-upload/` 上傳，則每次更新後再執行 `python tools/prepare_pages.py`，將整理好的網站檔案重新上傳到同一個 repository。

## 筆記與閱讀進度

網站公開後，讀者的筆記與進度仍只保存在自己的瀏覽器 localStorage，不會被上傳到 repository 或分享給其他讀者。

本機檔案與線上網址使用不同的儲存範圍，因此既有本機筆記不會自動移到線上。不同瀏覽器、裝置與網址之間也不會自動同步。

## 官方說明

- [What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
