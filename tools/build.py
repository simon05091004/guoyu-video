#!/usr/bin/env python3
import json, glob, re, io

# --- metadata from verification (canonical title + channel) ---
meta = {}
for line in io.open("verified.txt", encoding="utf-8"):
    p = line.rstrip("\n")
    if " OK " not in p: continue
    vid = p[:12].strip(); rest = p[12:].strip()
    rest = rest[len("OK"):].strip()
    meta[vid] = {"t": rest[:58].strip(), "ch": rest[58:].strip()}
for vid, t, ch in [("ZMgxQ_vhZlw","廖科溢《我的非洲很有事》搶先看之馬達加斯加 猴麵包樹","亞洲旅遊台 - 官方頻道"),
                   ("ktwNY-U9nnQ","BBC地球的熱帶島嶼 1 馬達加斯加","Harvest Culture 百禾文化")]:
    meta[vid] = {"t": t, "ch": ch}

# --- durations harvested from search результата ---
dur = {}
for f in glob.glob("r*.json"):
    for q, rows in json.load(io.open(f, encoding="utf-8")).items():
        for r in rows:
            if r.get("dur"): dur.setdefault(r["id"], r["dur"])
dur.update({"lTR02f-yfks":"", "t9g1qz487ig":"", "26KqgIpwM-U":"", "ZMgxQ_vhZlw":"2:01", "ktwNY-U9nnQ":"3:00"})

words = json.load(io.open("pedia.json", encoding="utf-8"))

# category codes: read=課文朗讀 guide=課文導讀 lang=語詞修辭 class=完整課堂 ext=延伸主題 author=作者背景 genre=文體寫作
def V(vid, cat, note=""):
    m = meta.get(vid, {"t": "(未知)", "ch": ""})
    return {"id": vid, "t": m["t"], "ch": m["ch"], "d": dur.get(vid, ""), "c": cat, "n": note}

L = {"六上": {}, "六下": {}}
L["六上"][1] = [
 V("ci03JKMmE6E","read","逐段朗讀，可直接當課文首讀"),
 V("sTqjrpLYb54","read","易讀版，資源班／差異化教學適用"),
 V("3as4FY4-tdQ","read","簡化版課文，1 分鐘掌握大意"),
 V("icwklFqGc2c","guide","課文欣賞與寫作特色，適合內容深究前"),
 V("P3I6aa0fV-U","lang","語詞解釋與例句"),
 V("ImazL4SVrvA","class","酷課雲完整課堂（舊版課次，內容深究可參考）"),
 V("tSrM3xy5F10","ext","引起動機：大隊接力逆轉勝，對照課文的競爭與友誼"),
]
L["六上"][2] = [
 V("oVDJRJ1PmPQ","read","一粥一飯"), V("nhQnp1ju6OE","read","未雨綢繆"),
 V("uNOL6fjOOfc","read","人有喜慶"), V("qWd5qrsptUs","read","器具質而潔"),
 V("xv8NIi_sHpw","read","一粥一飯・易讀版"), V("S9Z6mtsasi8","read","器具質而潔・易讀版"),
 V("PfoieDZH5-A","guide","課文導讀、寫作特色"),
 V("B_B_zkwrtVI","author","《朱子治家格言》作品與朱柏廬其人"),
 V("uKMDZMrmYYI","class","酷課雲完整課堂"),
 V("Y-UYWOxXllM","ext","全文朗讀版，可播放課本未選錄的段落"),
]
L["六上"][3] = [
 V("MsqhVJwU35o","read","課文朗讀"), V("UFNaFUYw5rM","read","簡化版課文"),
 V("-Kr2ReaFNks","guide","課文導讀、寫作特色"),
 V("T9mgEuoSf2U","lang","設問修辭教學（本課重點修辭）"),
 V("XA4aBpMlCfU","genre","認識議論文（他版統整單元，概念通用）"),
 V("-eQF-PfOYYQ","genre","議論文概說，酷課雲"),
 V("W2nPiDvHsRc","ext","成長型 vs 固定型思維，扣合「遇見更好的自己」"),
]
L["六上"][4] = [
 V("zivm29RpwoY","read","〈肉圓〉"), V("eGHAZoyHBjI","read","〈鼎邊趖〉"),
 V("NfbShTKScGg","guide","詩選導讀與寫作特色"),
 V("uTLGJKqZ7pk","ext","北斗肉圓的身世（呂捷），寫作素材"),
 V("DOCqfJAKgo0","ext","鄭成功發明蚵仔煎？49 秒暖身"),
 V("8dYYXwixY5Y","ext","台灣演義・台灣小吃（49 分，建議節選）"),
]
L["六上"][5] = [
 V("uH9Id_ENb00","read","課文朗讀"),
 V("YCMeNZPCd9A","guide","課文導讀、寫作特色"),
 V("0CCIEwH_04M","author","作者與作品簡介"),
 V("dsuvWFTWI_A","lang","語詞解釋及例句"),
 V("zcme9SdkXkw","lang","摹寫教學演示（本課核心修辭）"),
 V("AhwdxjJrGLA","lang","摹寫修辭速講"),
 V("WJPGMnGGSsw","genre","視覺摹寫寫作示範，酷課雲"),
]
L["六上"][6] = [
 V("lTI6C9K6eos","read","課文朗讀"), V("gPqiU3mLUXw","read","課文朗讀（另一版本）"),
 V("MrULDDzsFJQ","guide","課文導讀、說明文寫作特色"),
 V("BEey-h-Jshs","ext","珍奶由來，3 分鐘動畫，適合引起動機"),
 V("k7P79on2K6A","ext","珍奶台中發跡（民視新聞）"),
 V("ybQbUN35kR8","ext","珍奶如何走向國際（志祺七七），可延伸討論"),
]
L["六上"][7] = [
 V("LHQfDQcNX4Q","read","課文朗讀"), V("_ijfFNbPz1Q","read","簡化版課文"),
 V("7GoxR0_Sf7E","read","課文＋題目＋線上測驗，可當隨堂檢核"),
 V("BO4cvDaTgzY","guide","全課重點整理"),
 V("5PJ0xBEFerw","lang","語詞解釋及例句"),
 V("5h16DlomTJ0","class","酷課雲完整課堂（上）"),
 V("lJRe9mNONtQ","class","酷課雲完整課堂（下）"),
 V("K3xD30xHvmg","ext","緬甸仰光・蒲甘・曼德勒，補足課文背景"),
 V("YtgSHyov84c","ext","緬甸國家簡介，中英字幕，可跨科使用"),
]
L["六上"][8] = [
 V("IR3Ii1N4CB0","guide","題解：《戰國策》與寓言體"),
 V("JMFx8VgAaCs","guide","全課重點整理"),
 V("lwa2DK2S6fI","lang","成語「狐假虎威」用法解析"),
 V("yGMdxfa7wcI","ext","momokids 成語動畫，低門檻暖身"),
 V("GrTidIyIFfg","ext","東雨成語小學堂，3 分鐘"),
 V("aGk_1sFQKus","ext","熊貓博士版成語故事"),
 V("PS87z2g7-E0","ext","同出《戰國策》的〈鷸蚌相爭〉，本課生字含「鷸」"),
 V("rTuuny-itOE","ext","〈鷸蚌相爭〉動畫，可與本課對讀"),
]
L["六上"][9] = [
 V("Pr7Z_qibA5I","guide","全文概述"), V("t9g1qz487ig","guide","全課重點整理"),
 V("I2pedT6AroI","read","課文動畫，文白對照好用"),
 V("TNy5T4-ikpk","ext","三國演義動畫・空城計（3 分鐘）"),
 V("Wo-N5LwA6UI","ext","10 分鐘兒童歷史動畫版"),
 V("mN6443DWMsU","ext","動畫《三國演義》第 46 集全集（25 分）"),
]
L["六上"][10] = [
 V("NttOd_ujkkQ","read","課文朗讀"), V("eGfq-IdzvYU","guide","全課重點整理"),
 V("ZhcMHmoMcVc","lang","語詞：薄暮"),
 V("_7rsotmH28Y","lang","生字延伸成語：趁火打劫"),
 V("2Mv3knKBxPQ","lang","生字延伸成語：兵不厭詐"),
 V("yDU5yRYzip0","lang","生字延伸成語：孜孜不倦"),
 V("dg_oTB7b1Bs","lang","生字延伸成語：感激涕零"),
 V("_c2lbV7n03I","ext","耶誕節由來，2 分鐘，低年段也可用"),
]
L["六上"][11] = [
 V("0xlglHiM_UQ","guide","全課重點整理"),
 V("X_fonTfKJD8","genre","淺談劇本：認識劇本體例（酷課雲）"),
 V("4t8WV7RW9qE","ext","英式下午茶的歷史與由來"),
 V("auz9wWQsn6A","ext","台灣吧《偵茶事務所》，茶文化延伸"),
]
L["六上"][12] = [
 V("aJn7lXCTYHY","ext","〈橘子〉短片改編，5 分鐘看完全故事"),
 V("MpqOqHtIDFk","read","〈橘子〉中文朗讀全文"),
 V("859Rn5iF8Io","guide","篇章解析（香港 DSE 版本，分析架構可借用）"),
 V("JQtPPMGvJqw","ext","讀後感分享，可作討論引子"),
]
L["六下"][1] = [
 V("gBDxsy_0bxE","read","課文朗讀"), V("YFnY85YToQQ","read","簡化版課文"),
 V("cwjkPmimilI","guide","全課重點整理（含破音字更正）"),
 V("H4hHnxZf86s","ext","馬達加斯加獨特生態系（消失的國界）"),
 V("1SxaBJOoozE","ext","下課花路米：狐猴，兒童取向"),
 V("6UBQa9UWe5o","ext","馬達加斯加才有的狐猴"),
 V("ZMgxQ_vhZlw","ext","猴麵包樹，2 分鐘"),
 V("ktwNY-U9nnQ","ext","BBC《地球的熱帶島嶼》馬達加斯加"),
]
L["六下"][2] = [
 V("h8KNql6KE4s","read","課文朗讀"), V("--wRfs-JXgo","guide","全課重點整理"),
 V("ZFcg4U_iRNU","ext","國家地理《101 歷史教室：馬丘比丘》"),
 V("0CFWEubc3F4","ext","國家地理《遠古工程巡禮》馬丘比丘"),
 V("cKGMEAePYP4","ext","消失的國界：馬丘比丘鬼斧神工"),
]
L["六下"][3] = [
 V("KbVe-sPKNvE","guide","全課重點整理"),
 V("rvCIE32CO_Y","ext","聖城拉薩一日深度體驗"),
 V("_Eg0_2iAREc","ext","布達拉宮與大昭寺"),
 V("7r8q7keVRfM","teach","康軒官方：國語×自然跨域專題研習（2.5 小時）"),
]
L["六下"][4] = [
 V("lD0c5v4TUWA","read","注釋語譯篇"), V("8myh2JWl5tM","guide","賞析篇"),
 V("Tuw85iBnN2E","author","天才李白的背包客生涯"),
 V("_xw2tTN5jLM","guide","內容解析：作者李白"),
 V("ijaHcCa6WAA","author","李白（詩仙）介紹"),
 V("IqYr240EuUc","ext","《送友人》詩歌吟唱，可帶學生吟誦"),
 V("ArhyO3aXz1w","ext","一口氣看完李白一生（11 分）"),
]
L["六下"][5] = [
 V("Zp4ZgNSZB8Q","guide","全課重點整理"),
 V("PU-dvEQoPa8","guide","課文解析（一）"),
 V("n_rnsEqD84Q","lang","課文架構、修辭、句型"),
 V("c-mJUooaJpY","author","康軒官方「作家對我說」：作者賴鈺婷"),
 V("vnOx_0ldMVY","class","酷課雲完整課堂"),
 V("9CFttckk7_U","ext","一日蚵農：彰化蚵仔怎麼養"),
 V("33SJs-Eiaos","ext","潮間帶海牛採蚵，即將失傳的漁法"),
 V("NJ8K1xexw0s","ext","王功珍珠蚵（台灣第一等）"),
]
L["六下"][6] = [
 V("p-nIEnA6wkI","read","課文朗讀"), V("26KqgIpwM-U","read","課文朗讀（另一版本）"),
 V("S5WWF0E7ohc","guide","全課重點整理"),
 V("5DPwhw4RwNM","ext","棉花糖實驗，3 分鐘，可談延遲享樂"),
 V("89NoAtDovRo","ext","棉花糖實驗深談（14 分）"),
]
L["六下"][7] = [
 V("V2IEeM05cCU","guide","全課重點整理"),
 V("Ir2-jF5Zm2Q","author","劉墉：人生是小小又大大的一條河（1 分鐘）"),
 V("XJaWK20HDzk","author","文訊專訪劉墉"),
 V("sl7CQdeJBzM","ext","劉墉、劉軒父子對談（45 分，建議節選）"),
]
L["六下"][8] = [
 V("ezMLuy9XmPg","guide","全課重點整理"),
 V("m0NigTMBJEY","genre","議論文三要素：論點、論據、論證"),
 V("0R51Ee5SGv0","ext","《雜草的夢想》勵志動畫短片"),
 V("g8IzyXq-6B0","ext","夢想工作大調查，銜接生涯探索"),
]
L["六下"][9] = [
 V("zCqmeiQ6wAU","guide","全課重點整理"),
 V("4A1p1p_qx0s","ext","動畫短片《我的夢想》"),
 V("RKzwxDnvc8Y","ext","夢想雨果：看見自己的特質"),
]

GENERAL = [
 V("IOhmfthRgxg","teach","康軒官方研習：用圖卡與聲音玩轉國語課－以六上第二單元為例"),
 V("bxkQeo2rutg","teach","楊裕貿教授：故事文體的教學重點"),
 V("gpM1tow1GGg","teach","麗雲老師：中高年級教學升級"),
 V("i2F2Iae16Yg","genre","記敘文概說（酷課雲）"),
 V("-eQF-PfOYYQ","genre","議論文概說（酷課雲）"),
 V("X_fonTfKJD8","genre","淺談劇本（酷課雲）"),
 V("AhwdxjJrGLA","genre","摹寫修辭"),
 V("Bfa_PIhJATY","genre","擬人修辭"),
 V("lh1XlXXkqSA","genre","譬喻修辭"),
]

TITLES = {"六上": [], "六下": []}
GENRE = {
 "六上": ["記敘文","古典格言","議論文","現代詩","記敘文","說明文","記敘文","文言寓言","章回小說","記敘文","劇本","小說"],
 "六下": ["遊記","遊記","遊記","唐詩","記敘文","抒情文","記敘文","議論文","議論文"],
}
NOTE = {("六上",8):"選自劉向編纂《戰國策》",("六上",9):"改寫自羅貫中《三國演義》",
        ("六上",12):"115 學年度新換課文；依生字（廂・袱・隧・欄柵・岔・扔）判讀應為芥川龍之介〈橘子〉（原題〈蜜柑〉）",
        ("六下",4):"李白・五言律詩",("六下",5):"作者賴鈺婷",("六下",7):"作者劉墉"}

out = {"sem": {}}
for sem in ("六上","六下"):
    rows = []
    for i, w in enumerate(words[sem]):
        no = i + 1
        name = w["name"].split("：",1)[1]
        rows.append({"no": no, "name": name, "genre": GENRE[sem][i],
                     "words": w["words"], "note": NOTE.get((sem,no),""),
                     "vids": L[sem].get(no, []), "pedia": w["id"]})
    out["sem"][sem] = rows
out["general"] = GENERAL
json.dump(out, io.open("data.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
n = sum(len(r["vids"]) for s in out["sem"].values() for r in s) + len(GENERAL)
print("課數 六上=%d 六下=%d ; 影片連結總數=%d" % (len(out["sem"]["六上"]), len(out["sem"]["六下"]), n))
for sem in ("六上","六下"):
    for r in out["sem"][sem]:
        print("  %s L%-2d %-12s %s 影片%d" % (sem, r["no"], r["name"], r["genre"], len(r["vids"])))
