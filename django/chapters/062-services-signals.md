# 服務層、Signals與副作用

讓動作有明確入口，避免重要規則藏在隱性連動。

## 顯式服務的用途

HTML與API都要標記完成，可以共用complete_task，集中授權、交易、命令識別與revision規則。服務函式的參數與結果應清楚，不能只是把原View全部搬到另一個檔案而沒有責任界線。

Signals適合部分解耦通知，但呼叫端不容易看見所有副作用。本課用signal安排Task快取失效與附件提交後清理，並以測試確認；沒有把主要業務交易全部藏在signals裡。

## 不同寫入路徑的差異

QuerySet.update不等同逐一save，可能不觸發相同signal。新增批次管理action時，要重新處理updated_at、快取與副作用，不能假設原本接收器會涵蓋全部修改。

外部寄信或工作失敗不應不知情地讓資料狀態混亂。依需求設計可重試事件、對帳或outbox，而不是把任意網路呼叫放進post_save後宣稱可靠交付。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener" aria-label="放大服務層、Signals與副作用圖解"><img src="assets/figures/21.svg" alt="服務層、Signals與副作用：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「服務層、Signals與副作用」讀圖：沿使用者範圍與快取鍵，說明命中、失效與資料隔離。再回答：一項重要規則只放post_save，所有更新都一定遵守嗎？</p></div>

## 自我檢查與解析

**題目：**一項重要規則只放post_save，所有更新都一定遵守嗎？

<details><summary>展開解析</summary><p>不一定。批次update等路徑可能不觸發，需明確選擇服務入口、約束與副作用策略。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/signals/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
