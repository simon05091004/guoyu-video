import re,html,json,sys,urllib.request,urllib.parse,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=30).read().decode("utf-8","ignore")
def rows(year,deg=6,press="康軒版"):
    u=("https://pedia.cloud.edu.tw/Bookmark/Textword?category=%E5%9C%8B%E8%AA%9E&year="+year+
       "&degree=%d&press=%s"%(deg,urllib.parse.quote(press)))
    s=get(u); out=[]
    for m in re.finditer(r'<td class="textname" id="(\d+)"[^>]*>\s*<strong>(.*?)</strong>',s,re.S):
        out.append({"id":m.group(1),"name":html.unescape(m.group(2)).strip()})
    return out
def words(tid):
    s=get("https://pedia.cloud.edu.tw/Bookmark/TCollection?TextNameId="+tid)
    t=html.unescape(re.sub(r'<[^>]+>','\n',s))
    lines=[l.strip() for l in t.split('\n') if l.strip()]
    w=[l for l in lines if len(l)==1 and '一'<=l<='鿿']
    seen=[];  [seen.append(x) for x in w if x not in seen]
    return seen
res={}
for year,label in (("115_1","六上"),("114_2","六下")):
    res[label]=[]
    for r in rows(year):
        ws=words(r["id"]); time.sleep(0.3)
        res[label].append({**r,"words":ws})
        print(label, r["name"], "生字%d:"%len(ws), "".join(ws), flush=True)
json.dump(res,open("pedia.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
