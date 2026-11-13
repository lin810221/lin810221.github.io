# 上肢重複作業：分布、峰值和恢復

用窗口資料理解平均和仍缺少的資訊。

## 循環的定義

一次循環可能包含多個動作，也可能左右手不同。先說計數方式和哪隻手、哪個工作段，不能把產品數直接當手部動作數。

## 平均掩蓋的差異

同樣每分鐘9次，可能有不同峰值、施力、腕肩位置與節奏。恢復也需看是否真的換到不同需求，而不是名稱改了仍做相同動作。

## 原創窗口範例

本課12個10分鐘組裝觀察有一段未知，程式列前幾段的率與活動比例。這不是正式ART表或全部工作日暴露，也不把缺漏當休息。

## 改善方向

流程、輔具、物件位置、施力與工作安排可以一起評估。訓練與提醒能補充，但不能只要求快一點再多伸展來抵銷設計問題。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 24_repeated_task_record.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:24_repeated_task_record.py -->

## 練習與解答

**先想一想：** 輪換到名稱不同但仍同樣緊握的小任務，就一定有恢復效果嗎？

<details><summary>展開驗算與理由</summary>

不一定。需看實際力、動作、部位與時間是否改變，工作名稱不是暴露或恢復的證明。

</details>

## 正式來源與進一步閱讀

- [HSE ART：上肢重複作業工具](https://www.hse.gov.uk/msd/uld/art/index.htm)
- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)
- [HSE：工作安排與休息的適用條件](https://www.hse.gov.uk/msd/dse/work-routine.htm)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
