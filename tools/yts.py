#!/usr/bin/env python3
import json, re, sys, urllib.parse, urllib.request, time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

def fetch(q):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&hl=zh-TW&gl=TW"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "zh-TW,zh;q=0.9"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")

def initial(html):
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        m = re.search(r'ytInitialData"\]\s*=\s*(\{.*?\});', html, re.S)
    return json.loads(m.group(1)) if m else None

def walk(o, out):
    if isinstance(o, dict):
        if "videoRenderer" in o:
            v = o["videoRenderer"]
            try:
                title = "".join(r.get("text","") for r in v["title"]["runs"])
            except Exception:
                title = v.get("title",{}).get("simpleText","")
            ch = ""
            try:
                ch = v["ownerText"]["runs"][0]["text"]
            except Exception:
                try: ch = v["longBylineText"]["runs"][0]["text"]
                except Exception: pass
            dur = v.get("lengthText",{}).get("simpleText","")
            views = v.get("viewCountText",{}).get("simpleText","") or v.get("shortViewCountText",{}).get("simpleText","")
            pub = v.get("publishedTimeText",{}).get("simpleText","")
            out.append({"id": v.get("videoId",""), "title": title, "ch": ch, "dur": dur, "views": views, "pub": pub})
        for val in o.values():
            walk(val, out)
    elif isinstance(o, list):
        for val in o:
            walk(val, out)

def search(q, n=8):
    try:
        data = initial(fetch(q))
    except Exception as e:
        return [{"id":"", "title":"[ERROR] %s" % e, "ch":"", "dur":"", "views":"", "pub":""}]
    out = []
    if data: walk(data, out)
    seen, res = set(), []
    for r in out:
        if not r["id"] or r["id"] in seen: continue
        seen.add(r["id"]); res.append(r)
        if len(res) >= n: break
    return res

if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("### " + q)
        for r in search(q, 8):
            print("  %s | %-52.52s | %-22.22s | %-7s | %s" % (r["id"], r["title"], r["ch"], r["dur"], r["views"]))
        print()
        time.sleep(0.6)
