# 動作地圖：關節、平面與基本模式

用結構語言描述動作，不以單一外觀判定每個人的最佳姿勢。

## 先找參與結構

骨提供支架，關節允許並限制相對移動，肌肉經肌腱施力，神經協調控制。韌帶、軟骨等也有角色；肌肉不是只向一個方向拉一根骨頭。完整動作需看多關節與任務。

## 平面和模式的用途

矢狀、額狀和橫斷面是描述工具，真實動作常跨平面。蹲、髖主導、推、拉、移動與攜帶是便於規劃的分類，不是人體唯一自然分法；不能由一個分類直接推算所有肌群劑量。

## 從畫面到分析

影片看得到角度與大致軌跡，卻未直接量到外力、關節內力或肌肉活化。先描述看到什麼，再列需要哪些測量；不要把膝蓋或軀幹某個角度自動判成組織損傷。

## 後續力學實驗

範例以簡化外力、力臂與夾角算力矩，讓你理解同重量在不同位置可能有不同要求。這不是人體完整模型，不能用它決定某個人的安全角度；動作選擇仍取決於目標、能力、耐受與教學。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 04_force_and_angle.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:04_force_and_angle.py -->

## 練習與解答

**先自己判斷：** 只看一張深蹲照片，能否精算每條肌腱的力？

<details><summary>展開理由與驗算</summary>

不能。照片不足以提供外力、速度、人體幾何、肌肉協同和模型條件；先描述觀察，不將外觀直接變成內部負荷或傷害結論。

</details>

## 官方來源與研究

- [OpenStax：神經控制與肌肉張力](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-4-nervous-system-control-of-muscle-tension)
- [OpenStax：肌纖維收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
