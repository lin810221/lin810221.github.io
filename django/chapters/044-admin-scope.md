# 管理後台的資料範圍與關聯選項

Admin也不能成為跨帳號查詢的捷徑。

## 一般staff與superuser分開

TaskAdmin對superuser保留跨帳號管理，對一般staff限制owner。readonly owner與save_model共同避免建立或編輯時偽造擁有者。後台選取tags也要限制queryset，不只篩選主列表。

這是本專題的管理政策，不是Django所有網站的預設。若團隊需要跨部門角色，應明確建立新的授權模型，不能把superuser當作每種工作需求的通用解法。

## 後台搜尋同樣需要審查

列表、搜尋、關聯下拉、自動完成與批次action都可能暴露資料。新增功能時測試每個入口，而非只看主畫面。顯示欄位也不要放不必要的敏感內容或密鑰。

本課測試一般staff在Admin查不到Bob的任務。這是實際查詢範圍驗證，不只是CSS隱藏；正式專案若覆寫更多Admin元件，也要同步擴充測試。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener" aria-label="放大管理後台的資料範圍與關聯選項圖解"><img src="assets/figures/15.svg" alt="管理後台的資料範圍與關聯選項：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「管理後台的資料範圍與關聯選項」讀圖：沿staff、模型權限與資料範圍三道檢查，找出後台可看的資料。再回答：主列表已限制owner，還要檢查關聯欄位嗎？</p></div>

## 自我檢查與解析

**題目：**主列表已限制owner，還要檢查關聯欄位嗎？

<details><summary>展開解析</summary><p>需要。外鍵或多對多選單可能是另一條資料曝光與關聯寫入路徑。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
