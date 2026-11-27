# 合成資料與管理命令

可重跑示例，不預先建立通用密碼。

## 只對既有使用者加入資料

seed_demo要求username，若帳號不存在就停止；不自動建立容易被誤用的固定管理密碼。它用既定合成標題與get_or_create加入任務及tag，重跑不重複固定資料。

```powershell
python manage.py createsuperuser
python manage.py seed_demo --username 你的帳號
```

這是本地練習資料，不是生產初始化與備份匯入的萬用工具。正式資料載入應另外處理來源、唯一條件、失敗回復與核對，不能直接覆蓋既有帳號。

## 管理命令的契約

命令接受明確參數、顯示可理解結果，缺資料時以非成功狀態結束。自動化呼叫應能判斷失敗，而不是任何例外都捕捉後印出「完成」。

本課測試連續執行兩次，確認資料數穩定。若新增命令會修改真實內容，先定義範圍、預覽與稽核方式，避免方便工具成為不易追查的隱性修改入口。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/25.svg" target="_blank" rel="noopener" aria-label="放大合成資料與管理命令圖解"><img src="assets/figures/25.svg" alt="合成資料與管理命令：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「合成資料與管理命令」讀圖：沿專題的資料到評估路徑，列出每一階段應留下的成果。再回答：為什麼不在教材提供大家共用的admin密碼？</p></div>

## 自我檢查與解析

**題目：**為什麼不在教材提供大家共用的admin密碼？

<details><summary>展開解析</summary><p>避免被直接帶到公開網站，也讓帳號來源清楚。使用者自行建立帳號，種子命令只加入合成內容。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/howto/custom-management-commands/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
