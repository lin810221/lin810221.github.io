# 全身振動與乘坐設備：方法不同，不能混算

把座椅、地面、車輛與暴露類型分清。

## 接觸與來源

車輛、設備與地面可透過座位、腳或其他接觸傳遞振動；路況、速度、懸吊、座椅調整與維護都可能影響。不能只憑車型或座椅品牌判定實際暴露。

## WBV不是HAV換名稱

全身振動有不同各軸權重和評估方法，不能拿手－手臂三軸合成直接套用。姿勢、時間、衝擊與其他條件也需按正式方法處理。

## 地區法規

HSE說明英國WBV行動值0.5、限值1.15m/s² A(8)，和HAV不同。這些不是台灣統一通行線，也不是低於就完全沒有健康需求的保證。

## 改善的來源

路面、設備維護、操作安排、速度與合適座椅等可成為評估方向。單靠更厚墊子不一定改善所有頻率，還需實際方法與新風險確認。

## 本課的界線

瀏覽器和Python只實作HAV已加權輸入的算術，WBV作概念及來源介紹，不冒稱已建完整評估器。需要現場時由適當受訓人員與工具處理，不能用手機曲線生成安全認證。

## 練習與解答

**先想一想：** HAV和WBV都用m/s²，所以可直接共用同一算法與界線嗎？

<details><summary>展開驗算與理由</summary>

不能。暴露來源、軸向權重、方法與法規背景不同，單位相同不等於評估等效。

</details>

## 正式來源與進一步閱讀

- [HSE：英國全身振動的不同方法](https://www.hse.gov.uk/vibration/wbv/regulations.htm)
- [HSE L140：手－手臂振動正式方法](https://www.hse.gov.uk/pubns/priced/l140.pdf)
- [HSE：英國HAV行動值與限值](https://www.hse.gov.uk/vibration/HAV/responsibilities.htm)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)
- [台灣職安法：現行第6條](https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=N0060001&flno=6)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
