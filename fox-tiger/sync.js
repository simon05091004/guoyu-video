/* ============================================================
   即時排行榜的同步層 · live leaderboard sync
   Firebase Realtime Database REST + SSE，不載入 Firebase SDK。
   沒設定或連不上時，所有方法都安靜地失敗，遊戲不受影響。
   ============================================================ */
(function () {
  "use strict";
  var CFG = window.BT_SYNC || {};
  var token = null, room = null;

  function configured() { return !!(CFG.dbUrl && CFG.apiKey); }
  function base() { return String(CFG.dbUrl).replace(/\/+$/, ''); }
  function q(path) { return base() + path + '.json' + (token ? '?auth=' + encodeURIComponent(token) : ''); }

  // 匿名登入，換一個 id token（Firebase 規則用 auth != null 擋掉外人亂寫）
  function signIn() {
    var url = (CFG.authUrl || 'https://identitytoolkit.googleapis.com/v1/accounts:signUp') +
              '?key=' + encodeURIComponent(CFG.apiKey);
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ returnSecureToken: true })
    }).then(function (r) {
      if (!r.ok) throw new Error('auth ' + r.status);
      return r.json();
    }).then(function (d) {
      if (!d.idToken) throw new Error('auth: no token');
      token = d.idToken;
      return token;
    });
  }

  // 401/403 時重新登入再試一次
  function withAuth(run) {
    return run().catch(function (e) {
      if (!/\b(401|403)\b/.test(String(e && e.message))) throw e;
      token = null;
      return signIn().then(run);
    });
  }

  function jsonFetch(url, opts) {
    return fetch(url, opts).then(function (r) {
      if (!r.ok) throw new Error('http ' + r.status);
      return r.status === 204 ? null : r.json();
    });
  }

  var API = {
    /** 有沒有設定好可以用 */
    ready: configured,

    /** 目前的房號 */
    room: function () { return room; },

    /** 加入一個房間（會先匿名登入） */
    join: function (code) {
      if (!configured()) return Promise.reject(new Error('not configured'));
      room = String(code).toUpperCase();
      return (token ? Promise.resolve(token) : signIn()).then(function () { return room; });
    },

    /** 寫入／更新自己的成績 */
    save: function (playerId, data) {
      if (!configured() || !room) return Promise.resolve(null);
      return withAuth(function () {
        return jsonFetch(q('/rooms/' + room + '/players/' + playerId), {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
      });
    },

    /** 讀一次目前的排行榜，回傳已排序的陣列 */
    list: function () {
      if (!configured() || !room) return Promise.resolve([]);
      return withAuth(function () {
        return jsonFetch(q('/rooms/' + room + '/players'), { method: 'GET' });
      }).then(toRows);
    },

    /**
     * 清空房間裡的所有成績。
     * 逐一刪除每位玩家，而不是砍掉整個 players 節點 —— 這樣 Firebase 規則
     * 只要開放 players/$player 一層，沒有人能用一次請求把整個房間洗掉。
     */
    clear: function () {
      if (!configured() || !room) return Promise.resolve(null);
      return API.list().then(function (rows) {
        return Promise.all(rows.map(function (r) {
          return withAuth(function () {
            return fetch(q('/rooms/' + room + '/players/' + r.id), { method: 'DELETE' })
              .then(function (res) {
                if (!res.ok) throw new Error('http ' + res.status);
                return null;
              });
          });
        }));
      }).then(function () { return null; });
    },

    /**
     * 持續接收排行榜變動（給老師投影頁用）。
     * onRows 會在每次變動時收到排序好的陣列；回傳值呼叫後停止接收。
     */
    stream: function (onRows, onState) {
      if (!configured() || !room) { if (onState) onState('off'); return function () {}; }
      var es = null, stopped = false, players = {}, retry = 0, timer = null;

      function open() {
        if (stopped) return;
        if (onState) onState('connecting');
        es = new EventSource(q('/rooms/' + room + '/players'));
        es.addEventListener('put', function (ev) { apply(ev, true); });
        es.addEventListener('patch', function (ev) { apply(ev, false); });
        es.onopen = function () { retry = 0; if (onState) onState('on'); };
        es.onerror = function () {
          if (stopped) return;
          if (onState) onState('error');
          try { es.close(); } catch (e) {}
          retry = Math.min(retry + 1, 6);
          timer = setTimeout(open, 500 * Math.pow(2, retry - 1));
        };
      }

      function apply(ev, isPut) {
        var msg;
        try { msg = JSON.parse(ev.data); } catch (e) { return; }
        if (!msg || typeof msg.path !== 'string') return;
        var p = msg.path === '/' ? [] : msg.path.replace(/^\//, '').split('/');
        if (p.length === 0) {
          players = (isPut ? (msg.data || {}) : Object.assign(players, msg.data || {}));
        } else {
          var id = p[0];
          if (msg.data === null) delete players[id];
          else if (p.length === 1) players[id] = isPut ? msg.data : Object.assign(players[id] || {}, msg.data);
          else { players[id] = players[id] || {}; players[id][p[1]] = msg.data; }
        }
        if (onState) onState('on');
        onRows(toRows(players));
      }

      open();
      return function () {
        stopped = true;
        if (timer) clearTimeout(timer);
        if (es) { try { es.close(); } catch (e) {} }
        if (onState) onState('off');
      };
    }
  };

  /** 物件 → 排序後的陣列：分數高的在前，同分先看答對題數，再看誰先到 */
  function toRows(obj) {
    var rows = [];
    Object.keys(obj || {}).forEach(function (id) {
      var v = obj[id];
      if (!v || typeof v !== 'object') return;
      rows.push({ id: id, n: v.n || '?', a: v.a || '🧋', s: +v.s || 0,
                  c: +v.c || 0, t: +v.t || 0, d: !!v.d, u: +v.u || 0 });
    });
    rows.sort(function (x, y) { return (y.s - x.s) || (y.c - x.c) || (x.u - y.u); });
    return rows;
  }

  API.toRows = toRows;
  window.BTSync = API;
})();
