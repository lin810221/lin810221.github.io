# 註冊、登入、登出與安全跳轉

優先使用框架表單與View，再補上你的流程。

## 帳號建立與登入

SignupForm沿用UserCreationForm的密碼確認與驗證，保存時使用正確雜湊。LoginView處理認證與錯誤，LogoutView以POST登出。不要將使用者提交的密碼原文記錄到日誌或回應頁面。

本課註冊成功後回登入頁，登入成功後進任務列表。這是明確的產品流程，可以日後加入信箱驗證，但不能在尚未實作時宣稱已驗證信箱持有人。

## Next參數不是任意外部網址

登入頁可能帶next，讓使用者回到原頁。必須驗證跳轉目標，避免攻擊者將網站變成開放跳轉器。本課使用內建LoginView並測試外部next不會被接受；自行改寫登入時也要保留這個條件。

將正常登入、錯密碼、停用帳號、外部next與登出後回訪列入測試。畫面上隱藏登入按鈕不是安全機制，伺服器仍需按每次請求判斷身分與權限。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大註冊、登入、登出與安全跳轉圖解"><img src="assets/figures/13.svg" alt="註冊、登入、登出與安全跳轉：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「註冊、登入、登出與安全跳轉」讀圖：區分身分驗證與物件授權，找出每次查詢的擁有者條件。再回答：建立帳號時直接將password欄位寫進User.password，會有什麼問題？</p></div>

## 自我檢查與解析

**題目：**建立帳號時直接將password欄位寫進User.password，會有什麼問題？

<details><summary>展開解析</summary><p>可能儲存明文或不符合雜湊格式。應使用create_user、set_password或內建建立表單。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/auth/default/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
