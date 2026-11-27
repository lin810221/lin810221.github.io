# Class-based View與Mixin順序

使用框架生命週期，也要知道你覆寫哪一步。

## Generic View提供什麼

ListView、DetailView、CreateView、UpdateView與DeleteView提供常見流程；你仍需決定queryset、表單、模板與成功網址。它們不是自動知道你的資料擁有者與商業規則。

本課用OwnerQuerysetMixin將使用者範圍放進 `get_queryset`，用TaskFormMixin補user與owner。覆寫 `get_form_kwargs`、`form_valid` 時呼叫super，保留必要的生命週期，而不是不知情地跳過儲存與跳轉。

## 多重繼承要能解釋

Mixin順序影響方法解析，LoginRequiredMixin通常放在適當前側。不要為了減少行數堆疊一串無法說明的Mixin；遇到行為異常，查看MRO與每個方法的責任。

初學可以先寫清楚的函式View，再改成generic view比較。兩者是不同組織方式，不存在所有情境都應選同一種的規則；測試應驗證對外行為與權限，而不是只檢查類別名稱。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener" aria-label="放大Class-based View與Mixin順序圖解"><img src="assets/figures/12.svg" alt="Class-based View與Mixin順序：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Class-based View與Mixin順序」讀圖：沿POST、redirect與GET追蹤重新整理，核對分頁與狀態變更。再回答：使用UpdateView就會自動防止編輯別人的資料嗎？</p></div>

## 自我檢查與解析

**題目：**使用UpdateView就會自動防止編輯別人的資料嗎？

<details><summary>展開解析</summary><p>不會。預設資料範圍未必符合任務，必須限制get_queryset或實作相應物件授權。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/class-based-views/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
