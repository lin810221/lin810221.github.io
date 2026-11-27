# 從零建立位元組BPE

<figure class="tf-figure"><a href="assets/figures/04-bpe-merges.svg" target="_blank" rel="noopener"><img src="assets/figures/04-bpe-merges.svg" alt="lower先分l o w e r，按順位合併l加o成lo，再lo加w成low，最後low e r。" loading="lazy"></a><figcaption>BPE：從較小片段到子詞。相同文字在不同詞表和規則下會有不同token數；版本需與模型一起保存。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿文字、byte與ID的轉換追蹤，說明哪些邊界、特殊符號或padding會影響本頁方法。 本頁主題：從零建立位元組BPE。</p></div>

## 先分清本課兩個不同基線

核心小模型使用固定ByteTokenizer： $\mathrm{PAD}=0$ 、 $\mathrm{BOS}=1$ 、 $\mathrm{EOS}=2$ ，原始byte值b映射到`b+3`，因此詞彙大小是259。它沒有學合併，優點是簡單、可核對且不需外部資料。本單元另做教學BPE：從同一組byte與保留ID出發，再增加合併Token；BPE詞彙大小會隨合併數增加，不能把它直接塞給仍只有259列Embedding的模型。

輸入先以UTF8轉bytes，不做lowercase、Unicode正規化或空白折疊。每個一般Token都對應一串bytes，merge只是把兩串連在一起。完整合法輸入的encode/decode往返，依賴保存全部規則與不改寫原始bytes；特殊Token如何加入與跳過也要明定。

## 訓練迴圈的四個決策

只讀train文件，各文件維持自己的符號序列，不跨文件結尾數pair。每輪統計相鄰pair次數，選最高頻pair，建立新ID，再從左到右做非重疊替換，重複到預定預算或沒有可合併pair。若多pair同頻，使用固定破局規則，例如按pair ID字典序；這樣同一語料順序與版本才容易重現。

原創語料只有`abab`與`ab`。a的byte值97，ID100；b值98，ID101。第一輪pair(100,101)出現三次，合併成新ID259，對應bytes `b"ab"`。兩段變`[259,259]`與`[259]`。沒有出現在train的`ac`仍可退回byte IDs100與102，不需要UNK才能表示它。

## 重複pair與編碼次序

`aaa`有兩個相鄰(a,a)位置，但一次從左到右非重疊合併只能得到`aa|a`，不能同時把共享中間a的兩對都合成兩個aa。統計候選次數與真正替換的結果要依明確規則處理；寫測試涵蓋這種重疊，避免只用不重複英文單字驗證。

編碼新文字時使用已學的merge順位，不能再依這段新文字的局部頻率重新學規則。也不能把「詞彙表中最長字串匹配」當成所有BPE編碼器的通用替代，因為合併歷史與限制可能讓結果不同。凍結Tokenizer後，validation/test只做encode與decode，不更新pair統計。

## 解碼先拼bytes，再解Unicode

一般Token ID先查到bytes，按順序串接；依政策移除PAD/BOS/EOS等控制ID，再對完整byte序列做UTF8解碼。不要每個Token分別解碼，因為一個中文字的bytes可能分在多個Token。對非法或不完整序列，strict解碼應明確報錯；若產品選替代字元顯示，也要承認該輸出不再是原樣還原。

```text
一般ID序列
  → 每ID對應的byte片段
  → 依序串接完整bytes
  → UTF8 strict decode
  → 原始文字
```

生成模型可能輸出任意byte組合，並非每段都合法UTF8；即使Tokenizer能無損編碼有效文字，也不保證未訓練模型的任意輸出可讀。這兩個保證應分開測試與描述。

## 工件與測試不是只存vocab

保存特殊ID、初始byte映射、合併pair與順位、新ID對應bytes、正規化政策、文件邊界、訓練資料清單與雜湊。原始bytes若寫JSON，可用整數陣列或明確編碼格式，不隨意當Unicode字串儲存所有片段。

至少測空字串、空白與換行、中文、組合重音、emoji、字面特殊Token字串、重疊pair、未知字及凍結後編碼。再檢查每次合併的新ID只引用已存在Token，decode往返一致，固定語料重跑產物相同，validation內容變動不改Tokenizer工件。

## 練習與解析

若合併10次，從259個初始項目出發、每次確實新增一項，詞彙大小應269。若模型Embedding仍是`[259,D]`，新ID會越界；應在模型建立前固定詞彙，或以明確的擴表／重訓流程處理，不把新ID取餘數硬塞回舊表。

歷史子詞BPE見[Sennrich等人論文](https://arxiv.org/abs/1508.07909)，官方實作對照見[Tokenizers BPE原始碼](https://github.com/huggingface/tokenizers/tree/v0.23.3/tokenizers/src/models/bpe)。本課為原創簡化教學器，未複刻特定商用Tokenizer的regex、特殊Token與全部效能細節。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 02_byte_bpe.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:02_byte_bpe.py -->

