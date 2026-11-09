# 心率強度：HRmax、HRR與估計限制

用給定假設數值計算，不把年齡公式當實測最大心率。

## 不同分母

%HRmax是相對最大心率，%HRR則使用最大減休息的儲備。休息60、最大180時，60%HRmax為108；60%HRR則132。兩個60%不是同一強度，不應只寫60%心率。

$$
HR_{target}=HR_{rest}+f(HR_{max}-HR_{rest})
$$

## 數字從哪裡來

最大值可能來自合適測試或人口公式估計，兩者要分清；年齡公式有個體誤差，不能精準推某人的真正最大值。程式只接收虛構給定數值，不以讀者年齡生成安全區。

## 心率的其他影響

藥物、溫度、疲勞、體液與感測條件可能影響反應；短工作段還有時間延遲。某心率不一定對應同配速或同閾值，也不能因尚未達區域就忽略異常症狀。

## 如何使用示例

改比例看分母差異，保留來源和假設；沒有合適參考時可用其他適當線索與專業支持，而不是假造精準最大值。計算能驗算，不會替個人做運動許可。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 26_heart_rate_reserve.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:26_heart_rate_reserve.py -->

## 練習與解答

**先自己判斷：** 休息60、最大180，60%HRR是多少？是否等於60%HRmax？

<details><summary>展開理由與驗算</summary>

132次/min；60%HRmax是108，兩者不同。參考與適用性仍要確認，這是給定數值下的算術。

</details>

## 官方來源與研究

- [CDC：談話測試、絕對與相對強度](https://www.cdc.gov/physical-activity-basics/measuring/)
- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)
- [Exercise is Medicine：運動前篩檢表與背景](https://www.exerciseismedicine.org/wp-content/uploads/2021/04/EIM-exercise-preparticipation-screening.pdf)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
