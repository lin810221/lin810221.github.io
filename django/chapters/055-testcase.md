# TestCase、測試資料庫與隔離

測試必須能在乾淨環境重建，而非依賴本機資料。

## 正常使用框架測試生命週期

Django TestCase提供資料庫測試隔離，Test runner準備測試資料庫；setUpTestData建立類別共用初始資料，setUp處理每項測試的狀態。不要用正式資料庫試刪除，或依賴開發者曾手動建立的帳號。

本課另提供Python unittest入口，先以測試設定建立記憶體schema，再執行相同測試。標準Django runner也可使用：

```powershell
python manage.py test desk --settings=studyhub.testing
python -m unittest -v test_examples.py
```

## 選擇符合問題的測試類型

TestCase常以交易包住測試，和真正提交、鎖定或多連線行為不同。需要提交與鎖定語意時，研究TransactionTestCase及目標資料庫的並行測試。不能用一種快速測試替代所有部署保證。

測試設定使用快雜湊與記憶體郵件，只是速度與隔離選擇，不能帶進正式設定。測試報告附版本、設定與資料庫後端，讓通過的範圍清楚可見。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大TestCase、測試資料庫與隔離圖解"><img src="assets/figures/19.svg" alt="TestCase、測試資料庫與隔離：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「TestCase、測試資料庫與隔離」讀圖：由資料模型到HTTP層讀測試範圍，指出這個單元能驗證的責任。再回答：Django TestCase通過，是否代表真實多程序列鎖已驗證？</p></div>

## 自我檢查與解析

**題目：**Django TestCase通過，是否代表真實多程序列鎖已驗證？

<details><summary>展開解析</summary><p>不能。它的交易與連線條件不同，需要在目標資料庫使用適合的測試與真正並行情境。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/testing/overview/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
