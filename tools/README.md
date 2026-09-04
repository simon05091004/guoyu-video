# 影音庫維護工具

`../index.html` 是產出的成品（單一 HTML、零相依，直接推 GitHub Pages）。
資料來源與重建流程都在這個資料夾。

## 每年開學前要做的事

1. **確認課次有沒有換**（康軒會改版，115 學年度六上第十二課就從〈祕密花園〉換成〈橘子〉）

   ```
   python3 pedia.py
   ```

   會抓教育部教育百科的生字詞彙表，印出六上（`115_1`）與六下（`114_2`）的課次、課名、
   完整生字，並寫進 `pedia.json`。要換學年度就改 `pedia.py` 最後的 `("115_1","六上"), ("114_2","六下")`。

2. **搜新影片**

   ```
   python3 yts.py "康軒 六上 國語 第十二課 橘子"
   ```

   直接爬 YouTube 搜尋結果，印出 videoId、標題、頻道、長度、觀看數。可以一次給多個查詢字串。

3. **檢查舊連結有沒有死掉**

   ```
   python3 verify.py ids.txt
   ```

   用 YouTube oembed 逐支檢查。`OK` 是還在且可嵌入，`HTTP401` 通常是被設為私人或停用嵌入，
   `HTTP404` 是已刪除。`verified.txt` 是上一次（2026-09-02）的檢查結果。

4. **重建頁面**

   影片的分課、分類與備註手寫在 `build.py` 的 `L` 字典裡（分類代碼：
   `read` 課文朗讀／`guide` 課文導讀／`lang` 語詞修辭／`class` 完整課堂／
   `ext` 延伸主題／`author` 作者背景／`genre` 文體寫作／`teach` 教師研習）。改完跑：

   ```
   python3 build.py      # 重建 data.json
   python3 assemble.py   # 組出 ../index.html
   ```

   `assemble.py` 做的事：把 `head.html`（樣式）＋ `body.html`（版型與程式，內含 `__DATA__` 佔位）
   合起來，`__DATA__` 換成 `data.json`，外面包上 doctype/html/head/body。
   要改版型或樣式就改 `body.html` / `head.html`，再跑一次 `assemble.py`。

## 注意

- 六下課次自 113 學年度改版後是 **9 課**（舊版 11–12 課），不要照舊版排。
- 文體標記是依課名與生字判讀的，不是官方分類。
- 影片全是他人上傳的公開內容，隨時可能下架，開學前跑一次 `verify.py` 比較保險。
