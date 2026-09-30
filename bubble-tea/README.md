# 珍珠奶茶搶答 · Bubble Tea Quiz

六上第六課〈珍珠奶茶〉的中英雙語搶答遊戲。學生用平板掃 QR code 就能玩，
不用安裝 App、不用登入、不用帳號。題目全部出自課堂簡報。

- **投影頁（老師）**：[`host.html`](host.html) — QR code、房號與即時排行榜
- **遊戲（學生）**：[`index.html`](index.html) — 平板掃碼後開啟的頁面
- **即時排行榜設定**：[`firebase-config.js`](firebase-config.js)（沒填就是單機模式）、[`sync.js`](sync.js)

線上版（GitHub Pages）：

```
https://simon05091004.github.io/guoyu-video/bubble-tea/host.html   ← 投影這一頁
https://simon05091004.github.io/guoyu-video/bubble-tea/            ← 學生玩的頁面
```

## 課堂流程

1. 老師用電腦或平板開 `host.html`，投影出來。
2. 需要的話，在 QR code 下面點選只玩某一關（QR code 會立刻換成那一關的網址）。
3. 學生用平板相機掃 QR code → 輸入暱稱、選頭像 → 開始作答。
4. 每個人自己的節奏作答，答完會看到成績、每一關的表現，以及全部題目的中英文解析。

QR code 是在頁面裡自己畫出來的（不是去外部服務要圖），所以校內網路擋掉外部網站也照樣能產生。
唯一的外部資源是 Google Fonts 的字型；連不到時會自動退回系統字型，遊戲功能不受影響。

## 內容

24 題，對應簡報的五個段落：

| 關卡 | 題數 | 對應課文 |
| --- | --- | --- |
| 一、風靡全球 | 2 | 第一段 |
| 二、誕生與演變 | 6 | 第二、三段（含粉圓製作排序題） |
| 三、美味關鍵 | 4 | 第四、五段（含「好搭檔」配對題） |
| 四、語詞與修辭 | 9 | 語詞 1／2、句型、修辭 |
| 五、創意與影響 | 3 | 第六、七段 |

題型有四種：單選、是非、**排序**（把粉圓做法排出順序）、**配對**（把「好搭檔」配成一對）。

## 雙語怎麼呈現

- 每一題的題幹與選項**同時**有中文和英文，不必切換就看得到兩種語言。
- 右上角的「中／EN」可以隨時把英文換成大字在前，中文變成小字輔助，遊戲進行中也能切。
- 題庫還留著一個 `ba` 欄位，需要時可以加第三語提示（例如班上有其他母語的學生），
  目前沒有任何一題使用，首頁那個「💬 母語提示」開關因此不會有作用。

## 即時全班排行榜

**要不要開都可以。** `firebase-config.js` 沒填的話，遊戲完全正常，只是每台平板各自記分；
填好之後，老師投影頁右邊會出現全班的即時排行榜，學生答題時也看得到自己目前第幾名。

### 運作方式

老師投影頁開啟時會產生一個四碼**房號**（例如 `A7K2`），並把它寫進 QR code。
掃同一個 QR code 的人就在同一個房間裡；每答完一題，成績就傳到 Firebase，
投影頁透過 SSE 即時更新，不用重新整理。換一個班級就按「新房間」，下課按「清空這個房間」。

沒有載入 Firebase SDK，只用瀏覽器內建的 `fetch` 與 `EventSource` 打 REST API，
所以學校網路擋掉 `gstatic.com` 之類的 CDN 也不影響。連不上時會自動退回單機模式，
遊戲本身不會中斷。

### 設定步驟（約五分鐘）

1. 到 [Firebase 主控台](https://console.firebase.google.com/) 建立一個專案
   （沿用現有專案也可以，但建議另開一個，跟其他資料分開）。
2. 左側 **建構 Build → Realtime Database** → 建立資料庫 →
   位置選 `asia-southeast1`（新加坡，離臺灣最近）→ 先選「**以鎖定模式啟動**」。
3. 複製資料庫網址，長得像
   `https://你的專案-default-rtdb.asia-southeast1.firebasedatabase.app`。
4. 左側 **建構 Build → Authentication** → 開始使用 → 登入方式 →
   啟用「**匿名**」。（學生不用註冊，這只是讓 Firebase 規則擋掉外人亂寫。）
5. **專案設定 → 一般 → 你的應用程式** → 新增網頁應用程式（`</>`）→ 複製 `apiKey`。
6. 把這兩個值填進 [`firebase-config.js`](firebase-config.js)：

   ```js
   window.BT_SYNC = {
     dbUrl: "https://你的專案-default-rtdb.asia-southeast1.firebasedatabase.app",
     apiKey: "AIza……",
     authUrl: "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
   };
   ```

7. 回到 **Realtime Database → 規則**，貼上下面這段再按「發布」：

   ```json
   {
     "rules": {
       "rooms": {
         "$room": {
           ".read": "auth != null",
           "players": {
             "$player": {
               ".write": "auth != null",
               ".validate": "newData.hasChildren(['n','s','c','t','u'])",
               "n": { ".validate": "newData.isString() && newData.val().length <= 20" },
               "a": { ".validate": "newData.isString() && newData.val().length <= 8" },
               "s": { ".validate": "newData.isNumber() && newData.val() >= 0 && newData.val() <= 200000" },
               "c": { ".validate": "newData.isNumber() && newData.val() >= 0 && newData.val() <= 100" },
               "t": { ".validate": "newData.isNumber() && newData.val() >= 0 && newData.val() <= 100" },
               "d": { ".validate": "newData.isBoolean()" },
               "u": { ".validate": "newData.isNumber()" },
               "$other": { ".validate": false }
             }
           }
         }
       }
     }
   }
   ```

8. 推上 GitHub Pages，投影 `host.html`，房號和排行榜就會出現。

### 這樣夠安全嗎

規則只允許「登入過的人」寫入 `rooms/<房號>/players/<某個人>`，而且限定欄位、
型別與數值上限，寫不進別的路徑，也沒有人能用一次請求把整個房間洗掉
（「清空」是逐一刪除）。**但匿名登入人人可拿**，所以拿到網址的人理論上仍能在房間裡
亂寫分數。這裡存的只有暱稱、頭像和分數，換個房號或按清空就沒了 —— 對課堂用途夠用，
但**不要拿這個專案存任何其他資料**。

流量也很省：一個 30 人的班級跑完 24 題大約 800 次讀寫，Firebase 免費額度是每天 10 GB 傳輸，
遠遠用不完。

## 計分

答對得 600–1000 分（越快分數越高），連續答對第 2 題起每題多 100 分、最多加到 500 分。
成績存在各自的平板上（`localStorage`），同一台平板會累積排行榜。
有開即時排行榜的話，成績另外會送到你自己的 Firebase 專案；沒開的話不會傳到任何地方。
按「再玩一次」就重來。

## 要改題目？

題庫在 [`index.html`](index.html) 裡，用註解標出來的區塊：

```
/* ===== 課程內容開始 · LESSON CONTENT START ===== */
   ... ROUNDS（關卡）、QS（題庫）、AVATARS（頭像）、GRADES（等級稱號）、TIME（秒數）
/* ===== 課程內容結束 · LESSON CONTENT END ===== */
```

這個區塊以外都是遊戲引擎、QR 產生器與即時排行榜，換課時不用動。
題庫是 `QS` 陣列，一題一個物件，直接改文字即可：

```js
{ r:1,                      // 第幾關（對應 ROUNDS）
  t:'mc',                   // mc 單選 / tf 是非 / order 排序 / match 配對
  src:'第一段 ¶1',           // 顯示在題目上方，方便對照簡報
  zh:'中文題目', en:'English question',
  ba:'第三語小提示',          // 可省略，目前沒有題目使用
  o:[['正確答案','correct'],['錯的','wrong'], …],   // mc：第一個就是答案，畫面上會自動打散
  why:['中文解析','English explanation'] }
```

- `tf` 用 `ans:true` 或 `ans:false` 代替 `o`。
- `order` 用 `it:[…]`，照**正確順序**寫，畫面上會自動打散。
- `match` 用 `pr:[[左,右],[左,右],…]`，同樣會自動打散右欄。
- 作答時間在 `TIME`：單選 25 秒、是非 15 秒、排序與配對 45 秒。

改完存檔、推上去就好，沒有建置步驟。
