# 起點、目的地與顯著控制：不能只看容易的一端

理解一個搬抬任務可能需要兩端評估。

## 為何終點也重要

若目的地需顯著控制負荷，例如較精確定位，手冊要求起點和目的地都評估。不是永遠只用起點，也不是所有搬運都能用同一端代表。

## 同一任務、不同參數

起點H25、V75，終點H40、V125cm，D50、A0，其餘示例假設相同。終點的HM、VM不同，兩端RWL可能有差異；需要時取較限制的端點，而非挑較漂亮值。

## 不把多任務平均

一端比較與整天多任務是不同問題。CLI有正式程序，不能把多個LI直接平均後改名CLI，也不能把高需求工作段用其他低值稀釋。

## 程式的範圍

範例明示兩端需求與FM／CM假設，輸出可核對算術，不替所有真實工作自動判定顯著控制或合規。未知條件仍應保留未知。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 29_rnle_endpoints.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:29_rnle_endpoints.py -->

## 練習與解答

**先想一想：** 兩端結果不同，可以只保留較低LI讓報告好看嗎？

<details><summary>展開驗算與理由</summary>

不可以。需按適用程序評估較限制條件，不能選擇性保留；多任務也不能用平均LI冒稱CLI。

</details>

## 正式來源與進一步閱讀

- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [NIOSH：2021修訂與短工時更正](https://stacks.cdc.gov/view/cdc/110725)
- [NIOSH：RNLE現行入口（2026頁面更新）](https://www.cdc.gov/niosh/ergonomics/about/rnle.html)
- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
