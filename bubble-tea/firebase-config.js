/* ============================================================
   即時排行榜設定 · Live leaderboard settings
   ------------------------------------------------------------
   沒填 dbUrl 的話，遊戲照常運作，只是沒有即時排行榜
   （成績仍會存在各自的平板上）。設定步驟見 README.md。
   Leave dbUrl empty and everything still works — just without
   the live class board.
   ============================================================ */
window.BT_SYNC = {
  // Firebase Realtime Database 的網址，長得像
  // https://你的專案-default-rtdb.asia-southeast1.firebasedatabase.app
  dbUrl: "",

  // Firebase 專案設定裡的 Web API Key
  apiKey: "",

  // 匿名登入的端點，正常情況不用改（本機測試或用模擬器時才改）
  authUrl: "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
};
