# 表單與CRUD驗收練習

讓成功、錯誤與越權各有可重跑的結果。

## 建立完整操作矩陣

測正常建立、空白標題、非法priority、別人的tag、別人的任務ID、刪除確認GET與刪除POST。列出應有狀態、資料庫變化與畫面訊息，不只測一筆理想輸入。

檢查建立後重新整理不重送原表單，無效提交仍保留輸入與錯誤，修改不能更換owner。對分頁加入篩選條件，確認第二頁沒有偷偷回到全部資料。

## 把框架抽象還原成流程

請用自己的話描述CreateView從取得表單到成功跳轉的步驟，再指出Mixin補了哪個user與資料範圍。若無法解釋某個super呼叫，回到該類別文件與測試，不以「框架會處理」當作答案。

本章交付表單白名單、View、模板與測試矩陣。下一章加入更完整的帳號與權限，你將沿用同一組資料與操作，觀察認證和授權如何進入每個入口。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener" aria-label="放大表單與CRUD驗收練習圖解"><img src="assets/figures/12.svg" alt="表單與CRUD驗收練習：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「表單與CRUD驗收練習」讀圖：沿POST、redirect與GET追蹤重新整理，核對分頁與狀態變更。再回答：測到表單拒絕外部tag後，還需測API嗎？</p></div>

## 自我檢查與解析

**題目：**測到表單拒絕外部tag後，還需測API嗎？

<details><summary>展開解析</summary><p>需要。HTML表單與Serializer是不同輸入入口，不能因為一條路安全就假設另一條也相同。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/forms/modelforms/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
