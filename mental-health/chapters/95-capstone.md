# 完整專題：原創案例、資料與證據一起交付

完成一次不過度推論的學習報告。

## 專題任務

使用本課全部合成資料，輸出CSV、SVG、JSON，再寫一頁說明目的、欄位、缺漏、來源版本與可回答的問題。不得加入真實個人敏感資料到公開倉庫。

## 執行順序

先看metadata和README，跑第一份觀察與測試，再以48_complete_project.py指定新的輸出資料夾。保留五個雜湊與程式版本，讓他人能從ZIP獨立重跑。

## 至少驗證三件事

原創尺度沒有被改成診斷；兩筆缺漏和計畫B未知保留；假設篩檢與效果量沒有冒充個人或具名量表資料。可以手算一個值並對照輸出。

## 學習問題

可問三日窗口遇缺漏如何處理、假設盛行率改變PPV怎麼變、切換成本假設如何影響總時長。這些由明確模型回答，不需私人病史或治療判斷。

## 交付標準

看單位、來源、假設、隱私、可重跑與結論邊界，不看曲線是否往理想方向走。能誠實說未知，是學會判讀的重要部分，而不是報告失敗。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 48_complete_project.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:48_complete_project.py -->

## 練習與解答

**先想一想：** 專題的好成績是否取決於圖看起來壓力一路下降？

<details><summary>展開示範答案與理由</summary>

不是。品質在資料與解釋可追溯，合成曲線不代表治療效果；缺漏與限制應保留，不為美觀改數字。

</details>

## 來源與進一步閱讀

- [Python3.15.2官方正式發布](https://www.python.org/downloads/release/python-3152/)
- [OpenStax：相關、實驗與證據](https://openstax.org/books/psychology-2e/pages/2-3-analyzing-findings)
- [WHO：Doing What Matters壓力技能手冊（2020）](https://www.who.int/publications/i/item/9789240003927)
- [NICE NG225：自傷照護及風險工具限制](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)
- [WHO：工作心理健康正式指南（2022）](https://www.who.int/publications/i/item/9789240053052)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
