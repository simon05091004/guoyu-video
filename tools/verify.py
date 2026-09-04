#!/usr/bin/env python3
import json, sys, urllib.request, urllib.parse, concurrent.futures as cf
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"
def chk(vid):
    u="https://www.youtube.com/oembed?format=json&url="+urllib.parse.quote("https://www.youtube.com/watch?v="+vid,safe="")
    try:
        d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=20).read().decode())
        return vid,"OK",d.get("title",""),d.get("author_name","")
    except urllib.error.HTTPError as e:
        return vid,"HTTP%d"%e.code,"",""
    except Exception as e:
        return vid,"ERR",str(e)[:40],""
ids=[l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
with cf.ThreadPoolExecutor(12) as ex:
    for vid,st,t,a in ex.map(chk, ids):
        print("%-12s %-7s %-58.58s %s" % (vid, st, t, a))
