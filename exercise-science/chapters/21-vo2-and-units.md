# VO₂max、VO₂peak與單位

理解絕對與相對耗氧，區分實測最大與測到的峰值。

## 同一量的兩種表達

絕對耗氧常用L/min或mL/min，相對體重用mL/kg/min。2500mL/min除70kg約35.71mL/kg/min；分母改變會影響相對值，即使絕對值不變也可能不同。

$$
\dot V O_{2,relative}=\dot V O_{2,absolute}/m
$$

## max與peak

測試協定、量測與受試者達到的條件影響能否稱最大值；peak是該測試觀察的峰值，不能未說明就改名max。穿戴估計、場地公式與實驗室量測也不是同一資料等級。

## 不只一個指標

相同相對耗氧的人，耐力表現仍可能因經濟性、可維持比例、配速、技能和環境不同。不要把一個穿戴估值當競賽時間或全部心血管健康的保證。

## 變化如何解讀

記同協定、設備、準備與體重基準，保留估計誤差。若數字變動，先查測試條件和是否實測，再討論適應；本課只示範單位，不替讀者產生個人VO₂測試或最大強度要求。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 11_oxygen_units.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:11_oxygen_units.py -->

## 練習與解答

**先自己判斷：** 絕對耗氧不變但體重變了，相對耗氧可能變嗎？

<details><summary>展開理由與驗算</summary>

可能，因分母改變。需同時保留絕對值、體重與測量條件，不把相對值增加自動全歸為心肺適應。

</details>

## 官方來源與研究

- [Compendium：標準MET單位](https://pacompendium.com/unite-conversions/)
- [2024成人身體活動Compendium與年齡範圍](https://pacompendium.com/adult-compendium/)
- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)
- [OpenStax：運動與肌肉表現](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-6-exercise-and-muscle-performance)
- [OpenStax：心臟生理與心輸出量](https://openstax.org/books/anatomy-and-physiology-2e/pages/19-4-cardiac-physiology)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
