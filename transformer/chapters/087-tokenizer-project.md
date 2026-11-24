# 專題本機Tokenizer與聊天模板

<figure class="tf-figure"><a href="assets/figures/29-tiny-lm-artifact.svg" target="_blank" rel="noopener"><img src="assets/figures/29-tiny-lm-artifact.svg" alt="原創語料到tokenizer模型訓練checkpoint生成設定評估證據六張卡沿環狀串接，各卡列保存欄位。" loading="lazy"></a><figcaption>從語料到可重現的Tiny LM交付。讓另一個人只用交付資料，就能重建token IDs、載入模型並核對同一個測試。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>依本頁專題追蹤資料、模型、固定輸入、數值比較與交付檔，寫出可重現的命令與限制。 本頁主題：專題本機Tokenizer與聊天模板。</p></div>

## 兩種本機詞表要先分清楚

本課有兩條可讀的實作：`ByteTokenizer`以固定byte+3映射，詞表259；`03_local_tokenizer.py`則使用Tokenizers套件訓練一個本機byte-level BPE。前者方便追蹤每個byte，後者讓你實際查看子詞合併。它們不是同一個詞表，ID也不能互換；不能把第二條產生的ID直接送進預設259詞表的TinyGPT，卻仍沿用原本的embedding。

這個專題交付`tokenizer.json`、特殊token與ID對照、訓練文字來源、正規化規則、round-trip案例及聊天模板。模型權重和tokenizer要成套版本化；即使兩個tokenizer的詞表大小相同，也可能把同一個ID解讀成不同片段。

## 在本機訓練BPE

從根目錄執行：

```text
python transformer/examples/03_local_tokenizer.py
```

程式使用`Tokenizer(models.BPE())`、ByteLevel前切分器與decoder，BpeTrainer預設納入完整256個byte字母表，再加入PAD、BOS、EOS。requested vocab_size=300是訓練設定，不應未查看輸出就宣稱實際一定學滿300個token。資料很小或可合併組合不足時，實際詞表數可不同。

完整byte字母表讓新文字仍能拆成基本bytes。以ASCII的A為例，UTF-8只需1 byte；「貓」有3 bytes，emoji也可能需要多個bytes。BPE可把常見片段合成較長token，但不會把byte、Unicode碼點與「畫面看起來一個字」變成同一單位。比較模型成本和context前，必須用該tokenizer實際編碼。

## Round-trip要對照哪一份文字

程式以原創小語料訓練，再編碼未在訓練字串出現的中文與emoji，驗證decode是否還原。這測試的是編解碼契約，不是語意理解。案例至少包含中文、英文、空白、換行、emoji和空字串；必要時另外測試特殊token字面內容和不完整byte序列。

本專題沒有開啟lowercase或Unicode normalization，所以以原始文字比較。如果你自行加入正規化，應把「原文→正規化後文字→tokens→decode」四者都記錄，驗收decode與預定的正規化結果一致。不能把有損正規化和任意原字串完全還原同時當成保證。

舉例：若將`AI`轉為`ai`，decode得到`ai`符合lowercase規則，但與原文不同。這不是decoder壞掉，而是你改了要保存的資訊。相似地，把連續空白折疊會影響程式碼、表格和精確字串任務，不能只因文字「看起來一樣」而略過。

## Chat template只負責序列化

`24_hf_offline_model.py`把本機tokenizer包裝成現行`TokenizersBackend`，加上教學模板，將messages轉為帶角色和特殊標記的一條文字／token序列。模板示例可讀成：每則訊息前有BOS、角色與冒號，內容後有EOS；`add_generation_prompt=True`再接一個assistant開頭，讓模型接續回答。

這些符號只有在訓練和推論契約一致時才有預期作用。隨機模型加上模板不會變成聊天助理；寫上system角色也不會由字串本身建立工具權限。模板是資料格式，角色權限與執行驗證由應用另外處理。

若先`apply_chat_template(..., tokenize=False)`取得文字，再另外encode，應檢查是否需要`add_special_tokens=False`以避免再插一次特殊標記。更直接的做法是讓模板處理tokenize，但仍要查看實際IDs。`add_generation_prompt`與`continue_final_message`回答不同需求，不能未理解模板就同時打開。

## 保存與模型詞表一致性

保存tokenizer時，同時保存chat template、特殊ID和正規化設定。重讀本機資料後，比較同一段文字的IDs、相同messages的模板結果，以及特殊token的ID。再檢查模型embedding列數、lm_head輸出維度與tokenizer最大ID；新增token後，模型對應權重也必須有明確處理。

模型config的vocab_size可以大於實際用到的token數，但不能小於輸入最大ID+1。若訓練資料從不使用某些ID，隨機模型仍可能輸出這些位置的分數，這是另一個需要限制或訓練處理的契約問題，不能靠decode默默丟掉來掩蓋。

## 練習與解析

**題目：** 一個模型原本使用詞表259，你換成requested vocab_size=300的BPE，文字decode仍正確。這樣能否不改模型直接訓練？

**解析：** 不能由decode成功推出模型相容。先查實際詞表、ID範圍與特殊ID，並比對模型embedding和輸出head的列數及語意。即使所有ID碰巧小於259，原權重每列代表的片段也可能不同。最簡單的課內方案是為新tokenizer建立一致的新模型設定，而不是把兩套ID混接。

## 參考與日期

查核日期：2026-11-24；案例與語料為原創。

- [Tokenizers 0.23.3從iterator訓練](https://huggingface.co/docs/tokenizers/v0.23.3/en/training_from_memory)
- [現行Chat templates官方說明](https://huggingface.co/docs/transformers/en/chat_templating)
- [Transformers 5.24 TokenizersBackend原始碼](https://raw.githubusercontent.com/huggingface/transformers/v5.24.0/src/transformers/tokenization_utils_tokenizers.py)

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 03_local_tokenizer.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:03_local_tokenizer.py -->

