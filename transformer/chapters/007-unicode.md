# Unicode字元與UTF8位元組

<figure class="tf-figure"><a href="assets/figures/03-unicode-bytes-tokens.svg" target="_blank" rel="noopener"><img src="assets/figures/03-unicode-bytes-tokens.svg" alt="A貓包含兩個Unicode碼點U0041 U8C93，UTF8則是41 E8 B2 93四bytes，再由tokenizer規則映射成不同ID。" loading="lazy"></a><figcaption>字、byte與token不是相同單位。比較長度或計費前，先說清楚採用bytes、碼點還是特定tokenizer。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿文字、byte與ID的轉換追蹤，說明哪些邊界、特殊符號或padding會影響本頁方法。 本頁主題：Unicode字元與UTF8位元組。</p></div>

## 「一個字」可能有四種不同的計數

使用者看到的一個字形、Unicode碼位、UTF8位元組與模型Token，不是同一單位。「中」是一個常見碼位，UTF8編碼有三個位元組；Tokenizer可能把它保留成一個Token，也可能拆成多個片段。若以Python的`len(text)`代表某模型Token數，會混淆軟體字串與模型詞彙表。

更細地看，可見字形也不一定對應單一碼位。`é`可以用預組字元 $U+00E9$ ，也可以用`e`加結合重音。兩者在畫面上常相同，碼位與位元組卻不同。Unicode的字素叢集規則用來描述某些使用者感知的字元邊界，與Tokenizer的子詞分割另有目的。

## 用位元組核對原創小例子

```python
text = "中"
raw = text.encode("utf-8")
assert len(text) == 1
assert list(raw) == [0xE4, 0xB8, 0xAD]
assert len(raw) == 3
assert raw.decode("utf-8", errors="strict") == text

composed = "\u00e9"
decomposed = "e\u0301"
assert len(composed) == 1 and len(decomposed) == 2
assert len(composed.encode("utf-8")) == 2
assert len(decomposed.encode("utf-8")) == 3
```

這段只檢查編碼事實，不依賴某個外部模型。UTF8位元組值範圍0到255；byte tokenizer把每個位元組映射成ID後，可以覆蓋所有可編碼文字，不必替每個完整中文字先建立詞彙項目。代價是某些語言會使用較多Token，並影響序列長度與計算。

## 正規化會改變「可逆」的定義

NFC等Unicode正規化可以把某些等價序列轉成一致形式；lowercase、空白折疊、全半形轉換也可能出現在前處理。這些步驟可幫某些任務降低變異，但不保證保留原始文字。若Tokenizer做過大小寫折疊，decode後不應宣稱能還原原始大小寫。

本課自寫byte主線不做正規化，encode有效Unicode字串為UTF8，再依固定ID對照儲存；完整byte序列以strict解碼，才能驗證`decode(encode(text)) == text`。這個保證不延伸到任意截斷Token、任意新增特殊符號或非法UTF8輸出，也不等於每個單獨Token都可獨立顯示成完整字元。

## 串流輸出可能切在一個字元中間

「中」的三個位元組若被不同Token輸出，第一個片段`E4`單獨不是完整UTF8字元。直接每個Token各自strict解碼會報錯；用`errors="replace"`又可能永久插入替代字元，無法恢復原文。串流應保存尚未完整的位元組，使用增量解碼或在完整序列組合後解碼，並明確處理最終非法序列。

這也影響截斷策略：按byte或Token長度切斷，可能停在字元中間；若用途是提供可讀文字，需要適當的解碼與邊界政策。若用途是模型訓練的任意Token片段，則應承認片段可能不是完整可讀字串，而不要悄悄替換後再聲稱資料完全一致。

## 安全顯示與身分辨識是另一層

外觀相近的字元、不可見控制字、零寬連接與方向標記，可能讓畫面與實際字串不同。做資料去重、程式碼分析或帳號辨識時，需依任務定義比較與顯示規則；不能因兩段文字看起來一樣就直接認定bytes相同，也不能不經用途評估地把所有差異正規化。

練習：兩份文件看起來都是`é`，原始SHA不同，是否能斷言檔案損壞？不能。先比較碼位與正規化形式；若原文保真重要，保存原始檔與另存正規化版本，並記錄轉換。再問：中文一個字三bytes是否代表永遠三Tokens？也不能，Token數由特定Tokenizer的分割規則決定。

## 原始標準與API

字素邊界查[Unicode UAX #29 revision 49](https://www.unicode.org/reports/tr29/tr29-49.html)，正規化查[UAX #15](https://www.unicode.org/reports/tr15/)，字串編碼與解碼查[Python codecs](https://docs.python.org/3/library/codecs.html)。標準與執行時採用的Unicode資料版本也可能不同，真正需要版本敏感行為時應一併記錄。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 01_unicode_bytes.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:01_unicode_bytes.py -->

