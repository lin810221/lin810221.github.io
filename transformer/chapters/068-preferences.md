# 偏好資料獎勵與RLHF

<figure class="tf-figure"><a href="assets/figures/24-preference-relative-policy.svg" target="_blank" rel="noopener"><img src="assets/figures/24-preference-relative-policy.svg" alt="prompt連到chosen和rejected兩回答，DPO計算policy序列logprob差減reference差，再用負log sigmoid beta delta。" loading="lazy"></a><figcaption>偏好、reference與DPO的相對比較。DPO不是只最大化chosen的單獨分數；比較的是同prompt的偏好差與reference差。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出資料、模型、參考或回饋的角色，說明本頁目標改善什麼，以及仍不能保證什麼。 本頁主題：偏好資料獎勵與RLHF。</p></div>

理解「比較哪個答案較好」如何變成可學分數，以及獎勵、KL 約束與真實品質之間的差距。

## 示範與偏好提供不同訊號

SFT 給一個希望模型模仿的答案；偏好資料則在同一問題下比較多個答案，指出哪個較符合評分規則。偏好可能反映正確性、清楚、簡潔、禮貌或安全，但這些面向有時衝突，必須先制定標準，不能把一個「較好」標籤當作客觀真理。

評分者可能看不出細微事實錯誤，也可能偏愛長篇、流暢或與自己觀點一致的說法。資料要保存題目、候選、選擇規則、平手與分歧，並檢查來源及族群覆蓋。將評分者偏好學得更準，不等於模型對世界事實的理解必然更準。

## 從成對比較建立獎勵模型

一種常見的 Bradley–Terry 形式，以兩答案的獎勵分數差預測被選中的機率。對同一問題 x，較佳答案為 y_w，較差答案為 y_l，記為：

$$
P(y_w\succ y_l\mid x)
=\sigma\big(r_\phi(x,y_w)-r_\phi(x,y_l)\big)
$$

若分數分別為 2、0，機率約 0.8808，該偏好對的負對數損失約 0.1269。兩個分數都加 100，差仍是 2，偏好機率不變；因此原始 reward 的絕對值沒有天然的真實品質單位。先看它學的比較與校驗，再解讀數值。

## 以獎勵調整生成策略

一個簡化的正則化目標是提升期望 reward，同時限制策略相對參考模型的偏離：

$$
J(\theta)=\mathbb E_{y\sim\pi_\theta(\cdot\mid x)}
[r_\phi(x,y)]
-\beta D_{\mathrm{KL}}\big(\pi_\theta(\cdot\mid x)\Vert
\pi_{\mathrm{ref}}(\cdot\mid x)\big)
$$

參考策略提供行為錨點，KL 是一種偏離懲罰，不是事實檢查器。真實 RLHF 還有抽樣、優勢估計、最佳化及資料配方等細節；本單元建立目標與風險，不把簡式冒稱完整訓練演算法。

## 原創的兩答案算例

假設只有 A、B 兩個可能答案，參考分布為 0.5、0.5，目前策略為 0.8、0.2，reward 分別為 2、0。期望 reward 是 1.6，KL 約為 \(0.8\log1.6+0.2\log0.4=0.1927\)。若  $\beta =0.5$ ，目標值約 \(1.6-0.0964=1.5036\)。

這個目標偏好提高 A 的機率，但如果 reward 模型誤把錯誤 A 給高分，最佳化也會朝錯誤方向走。計算正確的目標值，不等於選對品質標準。應另外檢查事實、任務成功與不被獎勵模型覆蓋的失敗情境。

## Reward hacking 與分布偏移

策略持續最佳化後，可能生成獎勵模型未見過的答案，利用其弱點取得高分，例如冗長、迎合、重複特定措辭或表面格式。這是代理目標與真正需求之間的落差，不只發生在惡意行為；即使資料出於善意，過度最佳化也可能暴露缺口。

可以用獨立人工評估、不同驗證方法、對照候選及專項失敗集觀察。不要用同一 reward 模型同時做訓練目標與唯一驗收者，再把分數上升當作所有能力進步。偏好分數、事實正確率與使用者任務成功率應分別報告。

## 練習與解析

**題目：** 將 reward 的兩個分數同加十，成對偏好機率會改變嗎？如果 reward 上升但外部查證錯誤更多，應該相信哪個指標？

**解析：** 分數差不變，成對機率不變。Reward 是被最佳化的代理，不能推翻外部任務證據；應分析錯誤類型、分布與評分規則，修正資料及驗收。RLHF 可以改變模型行為，但不保證真實性或消除偏差。

## 原始來源

[InstructGPT／RLHF 原論文，2022](https://arxiv.org/abs/2203.02155) 提供示範、偏好與策略調整的公開研究案例；[HF Reward Trainer](https://huggingface.co/docs/trl/en/reward_trainer) 可對照偏好資料。所有兩答案分布與數值為原創，本課沒有執行外部 RLHF 模型或重現論文成績。
