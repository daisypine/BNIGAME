import re, sys, base64, os
SITE = os.environ.get("SITE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src, logo, out = sys.argv[1], sys.argv[2], sys.argv[3]
orig = open(src, encoding="utf-8").read()
members_line = re.search(r'var MEMBERS=\[.*?\];', orig, re.S).group(0)
import json as _json
REMOVED_MEMBERS = {"Casey Li", "Francie Schildhauer", "Giti Majdy", "Michael Balistreri"}
_m = _json.loads(members_line[len("var MEMBERS="):-1])
_m = [x for x in _m if x["Name"] not in REMOVED_MEMBERS]
_m.append({"Name": "Marco Cerda", "Classification": "Insulation", "Contact Sphere": "Construction", "Company": "Insul-Techs Inc", "Phone": "707-287-5657", "Email": "", "Website": ""})
members_line = "var MEMBERS=" + _json.dumps(_m, ensure_ascii=False) + ";"
logo64 = base64.b64encode(open(logo, "rb").read()).decode()
VISIT = "https://bnisfbay.com/ca-santa-clara-premiere/en-US/visitorregistration?chapterId=2880"

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BNI Premiere | Member Directory</title>
<meta name="description" content="BNI Premiere chapter: weekly speakers and member directory.">
<link rel="icon" type="image/png" href="data:image/png;base64,__LOGO__">
<style>
:root{
  --red:#C4242A;--red-dark:#A11C21;--red-soft:#FBEDED;
  --white:#FFFFFF;--off:#F8F6F3;--line:#E9E4DF;
  --ink:#1C1C1C;--text:#3A3A3A;--muted:#7A7470;
}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;background:var(--white);color:var(--text);-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 32px}

/* nav */
.nav{background:var(--white);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;height:72px;gap:16px}
.brand{display:flex;align-items:center;gap:14px;text-decoration:none}
.brand img{height:30px;width:auto;display:block}
.brand-name{border-left:1px solid var(--line);padding-left:14px;font-size:14px;font-weight:600;color:var(--ink);letter-spacing:.2px;line-height:1.2}
.brand-name small{display:block;font-size:11.5px;font-weight:500;color:var(--muted)}
.btn{display:inline-flex;align-items:center;gap:8px;background:var(--red);color:#fff;text-decoration:none;font-weight:700;font-size:14px;padding:11px 20px;border-radius:999px;transition:background .2s}
.btn:hover{background:var(--red-dark)}

/* hero */
.hero{padding:64px 0 52px}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--red);margin-bottom:14px}
.hero h1{font-size:clamp(36px,5.4vw,60px);font-weight:800;color:var(--ink);letter-spacing:-1.5px;line-height:1.02;max-width:760px}
.hero h1 span{color:var(--red)}
.hero p{margin-top:18px;font-size:17px;line-height:1.6;color:var(--text);max-width:600px}
.hero-row{display:flex;align-items:flex-end;justify-content:space-between;gap:32px;flex-wrap:wrap}
.stats{display:flex;gap:36px;padding-bottom:6px}
.stat-num{font-size:40px;font-weight:800;color:var(--red);letter-spacing:-1px;line-height:1}
.stat-label{font-size:12px;font-weight:600;color:var(--muted);margin-top:6px;letter-spacing:.4px;text-transform:uppercase}
.notice{margin-top:30px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:var(--red-soft);border-left:3px solid var(--red);padding:14px 18px;border-radius:0 10px 10px 0;font-size:14.5px;color:var(--text);max-width:760px}
.notice a{color:var(--red);font-weight:700;text-decoration:none;white-space:nowrap}
.notice a:hover{text-decoration:underline}

/* speakers */
.speakers{background:var(--off);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:52px 0}
.sec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:24px}
.sec-head h2{font-size:clamp(26px,3.4vw,34px);font-weight:800;color:var(--ink);letter-spacing:-.6px}
.when{display:inline-flex;align-items:center;gap:9px;background:var(--white);border:1px solid var(--line);color:var(--ink);font-size:14px;font-weight:600;padding:9px 16px;border-radius:999px}
.when::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--red)}
.sp-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.sp-card{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:24px;display:flex;gap:18px;align-items:center;transition:border-color .2s,box-shadow .2s,transform .2s}
.sp-card:hover{border-color:var(--red);box-shadow:0 10px 30px rgba(196,36,42,.10);transform:translateY(-2px)}
.sp-card .avatar{width:76px;height:76px;font-size:24px}
.sp-tag{font-size:11px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.sp-name{font-size:20px;font-weight:800;color:var(--ink);letter-spacing:-.3px;line-height:1.15}
.sp-class{font-size:14px;font-weight:600;color:var(--red);margin-top:4px}
.sp-co{font-size:13px;color:var(--muted);margin-top:2px}
.sp-info{margin-top:34px;display:grid;grid-template-columns:1.4fr 1fr;gap:16px}
.info-card{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:22px 24px}
.info-card h3{font-size:18px;font-weight:800;color:var(--ink);letter-spacing:-.3px;margin-bottom:14px}
.steps{list-style:none;display:grid;gap:12px}
.steps li{display:flex;gap:12px;align-items:flex-start;font-size:14.5px;line-height:1.5;color:var(--text)}
.steps li strong{color:var(--ink)}
.step-n{flex-shrink:0;width:26px;height:26px;border-radius:50%;background:var(--red-soft);color:var(--red);font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center}
.backup-card{background:var(--red);border-color:var(--red);color:#fff;display:flex;flex-direction:column;justify-content:space-between;gap:16px}
.backup-card h3{color:#fff}
.backup-card p{font-size:14.5px;line-height:1.55;color:rgba(255,255,255,.9)}
.btn-white{display:inline-flex;align-self:flex-start;align-items:center;gap:8px;background:#fff;color:var(--red);text-decoration:none;font-weight:700;font-size:14px;padding:11px 20px;border-radius:999px;transition:transform .15s}
.btn-white:hover{transform:translateY(-1px)}
@media(max-width:860px){.sp-info{grid-template-columns:1fr}}
.next{margin-top:34px}
.next h3{font-size:13px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
.next-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.next-item{background:var(--white);border:1px solid var(--line);border-radius:14px;padding:14px 16px;display:flex;gap:14px;align-items:flex-start}
.cal{flex-shrink:0;width:52px;text-align:center;border-radius:10px;background:var(--red-soft);padding:7px 0}
.cal-m{font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--red)}
.cal-d{font-size:22px;font-weight:800;color:var(--ink);line-height:1.05}
.next-names{display:flex;flex-direction:column;gap:10px;padding-top:2px;min-width:0;flex:1}
.np{display:flex;gap:10px;align-items:center;min-width:0}
.np .avatar{width:36px;height:36px;font-size:12px}
.np-name{font-size:14px;font-weight:700;color:var(--ink);line-height:1.25}
.np-what{font-size:12.5px;line-height:1.35;color:var(--muted)}
.np-what b{font-weight:600;color:var(--red)}

/* avatars */
.avatar{position:relative;flex-shrink:0;border-radius:50%;background:var(--red-soft);color:var(--red);font-weight:800;display:flex;align-items:center;justify-content:center;overflow:hidden;letter-spacing:.5px}
.avatar img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}

/* directory */
.dir-head{padding:52px 0 0}
.controls{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.96);backdrop-filter:blur(6px);border-bottom:1px solid var(--line);padding:16px 0;margin-top:18px}
.controls .wrap{display:flex;flex-direction:column;gap:12px}
.search-row{display:flex;gap:14px;align-items:center}
.search{position:relative;flex:1}
.search svg{position:absolute;left:15px;top:50%;transform:translateY(-50%);color:var(--muted)}
#search{width:100%;padding:13px 16px 13px 44px;border:1px solid var(--line);border-radius:999px;font:inherit;font-size:15px;background:var(--off);color:var(--ink);outline:none;transition:border-color .2s,background .2s}
#search:focus{border-color:var(--red);background:#fff}
.count{font-size:14px;color:var(--muted);white-space:nowrap}.count strong{color:var(--ink)}
.filters{display:flex;gap:8px;overflow-x:auto;padding-bottom:2px;scrollbar-width:none}
.filters::-webkit-scrollbar{display:none}
.chip{flex-shrink:0;padding:7px 14px;border:1px solid var(--line);border-radius:999px;background:#fff;font:inherit;font-size:13px;font-weight:600;color:var(--text);cursor:pointer;transition:all .15s}
.chip:hover{border-color:var(--red);color:var(--red)}
.chip.active{background:var(--red);border-color:var(--red);color:#fff}
.directory{padding:28px 0 72px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:18px}
.card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px;display:flex;flex-direction:column;transition:border-color .2s,box-shadow .2s,transform .2s}
.card:hover{border-color:var(--red);box-shadow:0 10px 30px rgba(196,36,42,.08);transform:translateY(-2px)}
.card-top{display:flex;gap:14px;align-items:center;margin-bottom:14px}
.card .avatar{width:56px;height:56px;font-size:18px}
.card-sphere{font-size:10.5px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:var(--muted);margin-bottom:3px}
.card-name{font-size:17px;font-weight:800;color:var(--ink);letter-spacing:-.2px;line-height:1.2}
.card-class{font-size:14px;font-weight:600;color:var(--red)}
.card-co{font-size:13px;color:var(--muted);margin-top:1px}
.card-links{display:flex;flex-direction:column;gap:6px;margin:14px 0 16px;padding-top:14px;border-top:1px solid var(--line);flex:1}
.link{display:flex;align-items:center;gap:9px;font-size:13px;color:var(--text);text-decoration:none;word-break:break-all}
.link:hover{color:var(--red)}.link svg{flex-shrink:0;color:var(--muted)}
.save{display:flex;align-items:center;justify-content:center;gap:8px;padding:10px;border:1px solid var(--red);border-radius:999px;background:#fff;color:var(--red);font:inherit;font-size:13.5px;font-weight:700;cursor:pointer;transition:all .15s}
.save:hover{background:var(--red);color:#fff}.save.saved{background:#2E7D4F;border-color:#2E7D4F;color:#fff}
.empty{grid-column:1/-1;text-align:center;padding:70px 20px;color:var(--muted)}.empty h3{color:var(--ink);font-size:19px;margin-bottom:6px}


/* meeting card */
.meet{background:var(--white);border:1px solid var(--line);border-radius:18px;padding:22px 24px;min-width:280px;max-width:340px;box-shadow:0 6px 24px rgba(28,28,28,.05)}
.meet-label{font-size:12px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;color:var(--red);margin-bottom:10px}
.meet-when{font-size:22px;font-weight:800;color:var(--ink);letter-spacing:-.4px}
.meet-mode{display:inline-block;margin-top:8px;font-size:12px;font-weight:700;color:var(--red);background:var(--red-soft);padding:4px 10px;border-radius:999px}
.meet-place{margin-top:14px;padding-top:14px;border-top:1px solid var(--line);font-size:14.5px;line-height:1.55;color:var(--text)}
.meet-place strong{color:var(--ink);font-weight:700}
.meet-map{display:inline-block;margin-top:10px;font-size:14px;font-weight:700;color:var(--red);text-decoration:none}
.meet-map:hover{text-decoration:underline}
.hero-stats{display:flex;gap:36px;margin-top:30px}
.navlinks{display:flex;align-items:center;gap:22px}
.navlink{font-size:14px;font-weight:600;color:var(--text);text-decoration:none}
.navlink:hover{color:var(--red)}
.text-link{font-size:14px;font-weight:700;color:var(--red);text-decoration:none}
.text-link:hover{text-decoration:underline}

/* leadership */
.leaders{background:var(--off);border-top:1px solid var(--line);padding:56px 0 60px}
.ld-group{font-size:13px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;color:var(--muted);margin:28px 0 12px}
.ld-group:first-of-type{margin-top:4px}
.ld-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.ld-grid-big{grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.ld{background:var(--white);border:1px solid var(--line);border-radius:14px;padding:16px;display:flex;gap:14px;align-items:center;transition:border-color .2s}
.ld:hover{border-color:var(--red)}
.ld .avatar{width:48px;height:48px;font-size:15px}
.ld-big{padding:22px}.ld-big .avatar{width:68px;height:68px;font-size:21px}
.ld-body{min-width:0}
.ld-role{font-size:11.5px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:var(--red)}
.ld-name{font-size:16px;font-weight:800;color:var(--ink);margin-top:2px}.ld-big .ld-name{font-size:19px}
.ld-co{display:block;font-size:13px;color:var(--muted);text-decoration:none;margin-top:1px}
a.ld-co:hover{color:var(--red);text-decoration:underline}
.ld-prof{display:inline-block;font-size:12.5px;font-weight:700;color:var(--red);text-decoration:none;margin-top:6px}
.ld-prof:hover{text-decoration:underline}

/* sites + footer */
.sites{padding:48px 0 8px}
.sites h2{font-size:clamp(22px,3vw,28px);font-weight:800;color:var(--ink);letter-spacing:-.5px;margin-bottom:18px}
.site-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.site{border:1px solid var(--line);border-radius:16px;padding:22px;text-decoration:none;color:var(--text);display:block;transition:border-color .2s,box-shadow .2s}
a.site:hover{border-color:var(--red);box-shadow:0 10px 30px rgba(196,36,42,.08)}
.site-tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;padding:4px 10px;border-radius:999px;background:var(--red-soft);color:var(--red);margin-bottom:12px}
.site-tag.here{background:var(--off);color:var(--muted)}
.site-title{font-size:17px;font-weight:800;color:var(--ink)}
.site-url{font-size:13.5px;color:var(--red);font-weight:600;margin-top:2px;word-break:break-all}
.site p{font-size:14px;line-height:1.55;margin-top:10px}
@media(max-width:860px){.navlink{display:none}}
@media(max-width:720px){.meet{max-width:none;width:100%}.hero-stats{gap:26px}}

/* footer */
.footer{background:var(--white);border-top:1px solid var(--line);padding:30px 0;margin-top:44px}
.footer .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--muted)}
.footer img{height:20px;display:block}
.footer a{color:var(--red);font-weight:700;text-decoration:none}

@media(max-width:720px){
  .wrap{padding:0 18px}.nav .wrap{height:62px}.brand img{height:24px}.brand-name{display:none}.btn{padding:9px 16px;font-size:13px}
  .hero{padding:40px 0 36px}.stats{gap:26px}.stat-num{font-size:32px}
  .speakers{padding:38px 0}.sp-card{padding:18px}.sp-card .avatar{width:62px;height:62px;font-size:20px}
  .search-row{flex-direction:column;align-items:stretch}.count{text-align:right}
}
</style></head><body>

<nav class="nav"><div class="wrap">
  <a class="brand" href="#"><img src="data:image/png;base64,__LOGO__" alt="BNI"><div class="brand-name">Premiere Chapter<small>Santa Clara &middot; San Jose</small></div></a>
  <div class="navlinks"><a class="navlink" href="#speakers">Speakers</a><a class="navlink" href="#directory">Members</a><a class="navlink" href="#leadership">Leadership</a><a class="navlink" href="agenda/">Meeting agenda</a><a class="navlink" href="__OFFICIAL__" target="_blank" rel="noopener">Official BNI page</a>
  <a class="btn" href="__VISIT__" target="_blank" rel="noopener">Visit as a guest</a></div>
</div></nav>

<header class="hero"><div class="wrap">
  <div class="hero-row">
    <div>
      <div class="eyebrow">BNI Premiere</div>
      <h1>Business owners who send each other <span>referrals</span>.</h1>
      <p>Meet the members, see who's presenting this week, and save anyone's contact in one tap.</p>
      <div class="hero-stats">
        <div><div class="stat-num" id="total-count">-</div><div class="stat-label">Members</div></div>
        <div><div class="stat-num" id="sphere-count">-</div><div class="stat-label">Categories</div></div>
      </div>
    </div>
    <div class="meet">
      <div class="meet-label">Meeting details</div>
      <div class="meet-when">Wednesdays, 7:00 AM</div>
      <span class="meet-mode">In person</span>
      <div class="meet-place"><strong>Bogey's Pizza Co</strong><br>5039 Almaden Expy<br>San Jose, CA 95118</div>
      <a class="meet-map" href="__MAPS__" target="_blank" rel="noopener">Get directions &rarr;</a>
    </div>
  </div>
</div></header>

<section class="speakers" id="speakers" hidden><div class="wrap">
  <div class="sec-head"><div><div class="eyebrow">Weekly presentations</div><h2>This week's speakers</h2></div><div class="when" id="sp-date"></div></div>
  <div class="sp-grid" id="sp-grid"></div>
  <div class="next" id="sp-next"><h3>Coming up</h3><div class="next-list" id="sp-list"></div></div>
  <div class="sp-info">
    <div class="info-card"><h3>Presenting soon? Here's what to bring</h3>
      <ol class="steps">
        <li><span class="step-n">1</span><span><strong>A door prize.</strong> A product, service or gift card that shows off your business.</span></li>
        <li><span class="step-n">2</span><span><strong>Your introduction.</strong> Send Daisy 2&ndash;3 sentences so the person introducing you has it ready.</span></li>
        <li><span class="step-n">3</span><span><strong>Your slides (optional).</strong> Email them to Daisy by the Monday before you present.</span></li>
      </ol>
    </div>
    <div class="info-card backup-card"><div><h3>Be a backup speaker</h3>
      <p>Speakers sometimes can't make it last minute. Sign up as a backup and you could get the spotlight sooner.</p></div>
      <a class="btn-white" href="https://docs.google.com/forms/d/e/1FAIpQLSd-RNljUII5pYu9IDIevcw1jgkjow37q0V-nNVfhvKy-5QOdA/viewform" target="_blank" rel="noopener">Sign up as a backup &rarr;</a>
    </div>
  </div>
</div></section>

<div class="dir-head" id="directory"><div class="wrap"><div class="eyebrow">Directory</div><h2 style="font-size:clamp(26px,3.4vw,34px);font-weight:800;color:var(--ink);letter-spacing:-.6px">Our members</h2></div></div>
<div class="controls"><div class="wrap">
  <div class="search-row">
    <div class="search"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
    <input type="text" id="search" placeholder="Search by name, business or category" autocomplete="off"></div>
    <div class="count">Showing <strong id="showing-count">0</strong></div>
  </div>
  <div class="filters" id="filter-wrap"><button class="chip active" data-sphere="all">All</button></div>
</div></div>
<main class="directory"><div class="wrap"><div class="grid" id="members-grid"></div></div></main>

<section class="leaders" id="leadership"><div class="wrap">
<div class="sec-head"><div><div class="eyebrow">Who runs the chapter</div><h2>Chapter leadership</h2></div><a class="text-link" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/index#Chapter_leaders" target="_blank" rel="noopener">See it on BNI SF Bay &rarr;</a></div>
<h3 class="ld-group">Leadership team</h3><div class="ld-grid ld-grid-big"><div class="ld ld-big"><div class="avatar" data-name="Maria Nunez"></div><div class="ld-body"><div class="ld-role">President</div><div class="ld-name">Maria Nunez</div><a class="ld-co" href="http://www.homepros.casa/" target="_blank" rel="noopener">Home Pros</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=lGOlpWBzlPMoS8g3YP11sA%3D%3D&name=Maria+Nunez" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld ld-big"><div class="avatar" data-name="Bethany Black"></div><div class="ld-body"><div class="ld-role">Vice President</div><div class="ld-name">Bethany Black</div><div class="ld-co">Strata Shield Insurance Solutions</div><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=i5dTp7Y1DAn4gxN4RRv%2B8w%3D%3D&name=Bethany+Black" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld ld-big"><div class="avatar" data-name="Daisy Pineda"></div><div class="ld-body"><div class="ld-role">Secretary / Treasurer</div><div class="ld-name">Daisy Pineda</div><a class="ld-co" href="http://kaizenagency.org/" target="_blank" rel="noopener">Kaizen Agency</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=Afv43WL6Jh5mRwD4fdACfA%3D%3D&name=Daisy+Pineda" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div></div>
<h3 class="ld-group">Visitor hosts</h3><div class="ld-grid"><div class="ld"><div class="avatar" data-name="Colin Clancy"></div><div class="ld-body"><div class="ld-name">Colin Clancy</div><a class="ld-co" href="http://www.colinclancy.com/" target="_blank" rel="noopener">Colin Clancy Realtor</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=qn6z9UNVfM3woILZI6nrgA%3D%3D&name=Colin+Clancy" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Jay Shergill"></div><div class="ld-body"><div class="ld-name">Jay Shergill</div><a class="ld-co" href="https://virtualadmins.org/" target="_blank" rel="noopener">Virtual Admins</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=E8%2BFVNW0%2FZYkluho%2FDUW9g%3D%3D&name=Jay+Shergill" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Joseph Barghouthi"></div><div class="ld-body"><div class="ld-name">Joseph Barghouthi</div><a class="ld-co" href="http://www.homexinc.com/" target="_blank" rel="noopener">HEX Construction dba HOMEX</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=efw53ohip7cKthfDW2y9Qg%3D%3D&name=Joseph+Barghouthi" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Thi Kelley"></div><div class="ld-body"><div class="ld-name">Thi Kelley</div><div class="ld-co">Dignity Memorial</div><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=W09xdK66NZ3syitwdSRn6A%3D%3D&name=Thi+Kelley" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Mike Caulkins"></div><div class="ld-body"><div class="ld-name">Mike Caulkins</div><div class="ld-co">LPL Financial</div></div></div><div class="ld"><div class="avatar" data-name="Jason Smith"></div><div class="ld-body"><div class="ld-name">Jason Smith</div><div class="ld-co">Blue Moon Estate Sales</div></div></div></div>
<h3 class="ld-group">Membership committee</h3><div class="ld-grid"><div class="ld"><div class="avatar" data-name="John Jorgensen"></div><div class="ld-body"><div class="ld-name">John Jorgensen</div><div class="ld-co">Johnny Windows</div><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=9Bt7NPKdJOOA5v1QZP%2FBQQ%3D%3D&name=John++Jorgensen" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="John Wheeler"></div><div class="ld-body"><div class="ld-name">John Wheeler</div><a class="ld-co" href="http://www.wheelergrp.net/" target="_blank" rel="noopener">John Wheeler&#x27;s State Farm Agency</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=TeFLajRFMhNIH4ygr5lpuw%3D%3D&name=John+Wheeler" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Marie Zandian"></div><div class="ld-body"><div class="ld-name">Marie Zandian</div><a class="ld-co" href="https://rainbowrestores.com/san-jose" target="_blank" rel="noopener">Rainbow Restoration of San Jose</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=2kk2N30GZXCEbA%2BHG%2FWefQ%3D%3D&name=Marie+Zandian" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Elizabeth Popova"></div><div class="ld-body"><div class="ld-name">Elizabeth Popova</div><div class="ld-co">Plush Communications LLC</div><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/index#Chapter_leaders" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Tom Pavicic"></div><div class="ld-body"><div class="ld-name">Tom Pavicic</div><a class="ld-co" href="https://www.newyorklife.com/agent/tmpavicic" target="_blank" rel="noopener">New York Life Insurance Company</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=aVt%2Bb0Trzu3xk%2FduDZYCZQ%3D%3D&name=Tom+Pavicic" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div></div>
<h3 class="ld-group">Supporting leaders</h3><div class="ld-grid"><div class="ld"><div class="avatar" data-name="Bryan Russell"></div><div class="ld-body"><div class="ld-role">Education Coordinator</div><div class="ld-name">Bryan Russell</div><div class="ld-co">Flagstar Bank</div><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=D6Nm9C2W6SkmKsUX43orsA%3D%3D&name=Bryan+Russell" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Shannon Sevor"></div><div class="ld-body"><div class="ld-role">Education Coordinator</div><div class="ld-name">Shannon Sevor</div><a class="ld-co" href="https://www.gymguyz.com" target="_blank" rel="noopener">GYMGUYZ Silicon Valley</a></div></div><div class="ld"><div class="avatar" data-name="Phil Lonardo"></div><div class="ld-body"><div class="ld-role">Events Coordinator</div><div class="ld-name">Phil Lonardo</div><div class="ld-co">Organizing Pros</div><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=c6QbPSxwB%2FD2fnLA0jtKHA%3D%3D&name=Phil+Lonardo" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Roxanne Salazar"></div><div class="ld-body"><div class="ld-role">Events Coordinator</div><div class="ld-name">Roxanne Salazar</div><a class="ld-co" href="https://www.handnhandseniorplacement.com/" target="_blank" rel="noopener">HandnHand Senior Placement</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=Dzdjc8MnVa%2Fuv8pQFzynUg%3D%3D&name=Roxanne+Salazar" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Denise Artache"></div><div class="ld-body"><div class="ld-role">Mentor Coordinator</div><div class="ld-name">Denise Artache</div><a class="ld-co" href="http://www.sunwestpainting.net/" target="_blank" rel="noopener">Sunwest Painting</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=CpBlo%2FsK9ebw43C8u7Qa5w%3D%3D&name=Denise+Artache" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Shawna Rodriguez"></div><div class="ld-body"><div class="ld-role">Mentor Coordinator</div><div class="ld-name">Shawna Rodriguez</div><a class="ld-co" href="http://bayareacaremanagement.com/" target="_blank" rel="noopener">Bay Area Care Management, LLC</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=VzJN20nHDIIeusu0gkQEVQ%3D%3D&name=Shawna+Rodriguez" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Sonia Shah"></div><div class="ld-body"><div class="ld-role">Mentor Coordinator</div><div class="ld-name">Sonia Shah</div><a class="ld-co" href="http://www.cocoacumin.com/" target="_blank" rel="noopener">CocoaCumin LLC</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=KUtQJB36pinSk6johUtRug%3D%3D&name=Sonia+Shah" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Elliot Foad"></div><div class="ld-body"><div class="ld-role">Growth Coordinator</div><div class="ld-name">Elliot Foad</div><a class="ld-co" href="http://positivemotionhealth.com/" target="_blank" rel="noopener">Positive Motion Chiropractic</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=4wDCNLeTpW0%2BIBFXD6a4iw%3D%3D&name=Elliot+Foad" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div><div class="ld"><div class="avatar" data-name="Ken Wong"></div><div class="ld-body"><div class="ld-role">Growth Coordinator</div><div class="ld-name">Ken Wong</div><a class="ld-co" href="https://www.sfoundation.io/" target="_blank" rel="noopener">sFoundation Inc.</a><a class="ld-prof" href="https://bnisfbay.com/ca-santa-clara-premiere/en-US/memberdetails?encryptedMemberId=l8D3OCU%2FUyX4xvVSKHQY9g%3D%3D&name=Ken+Wong" target="_blank" rel="noopener">BNI profile &rarr;</a></div></div></div>
</div></section>
<section class="sites"><div class="wrap">
  <div class="eyebrow">Find us online</div><h2>Visit, connect, join</h2>
  <div class="site-grid">
    <div class="site"><span class="site-tag here">You are here</span><div class="site-title">Our chapter website</div><div class="site-url">bnipremierchapter.com</div>
      <p>Built and kept up by our members: weekly speakers, the member directory and chapter leadership.</p></div>
    <a class="site" href="__OFFICIAL__" target="_blank" rel="noopener"><span class="site-tag">Official BNI page</span><div class="site-title">BNI Premiere on BNI SF Bay &rarr;</div><div class="site-url">bnisfbay.com/ca-santa-clara-premiere</div>
      <p>Our listing on the official BNI SF Bay Region site, with member profiles and visitor sign-up.</p></a>
    <a class="site" href="https://bnisfbay.com/en-US/apply" target="_blank" rel="noopener"><span class="site-tag">Join us</span><div class="site-title">Apply to become a member &rarr;</div><div class="site-url">bnisfbay.com/en-US/apply</div>
      <p>Ready to join BNI Premiere? Start your membership application on the official BNI SF Bay site.</p></a>
  </div>
</div></section>
<footer class="footer"><div class="wrap">
  <img src="data:image/png;base64,__LOGO__" alt="BNI">
  <div>BNI Premiere &middot; Wednesdays 7:00 AM at Bogey's Pizza Co, San Jose &middot; Part of BNI SF Bay Region</div>
  <div style="display:flex;gap:18px;flex-wrap:wrap"><a href="__VISIT__" target="_blank" rel="noopener">Visit as a guest &rarr;</a><a href="https://bnisfbay.com/en-US/apply" target="_blank" rel="noopener">Apply to join &rarr;</a></div>
</div></footer>

<script>
__MEMBERS__
/* PHOTOS: put headshots in a "photos" folder named like first-last.jpg (e.g. photos/daisy-pineda.jpg).
   Anyone without a photo shows their initials. */
var PHOTO_DIR='photos/', PHOTO_EXT='.jpg';

/* WEEKLY SPEAKERS: edit this list (date as YYYY-MM-DD, names as they appear in the directory) */
var SPEAKERS=[
 {date:"2026-10-14",names:["Mike Caulkins","Stephen Hartman","Tom Pavicic"]},
 {date:"2026-10-21",names:["Daisy Pineda","Sailosi Taunaholo","Felipe Miguel Mejia"]},
 {date:"2026-10-28",names:["Thi Kelley","Angelo DeSando","David Nasseri"]},
 {date:"2026-11-04",names:["Marcus Araiza","Marie Zandian","Marco Cerda"]},
 {date:"2026-11-11",names:["John Jussen","Phil Lonardo","Shannon Sevor"]},
 {date:"2026-11-18",names:["Shawna Rodriguez","Clifford Shaw","Angela Cearns"]},
 {date:"2026-12-02",names:["Lino Martire","Jennifer Isensee","John Wheeler"]},
 {date:"2026-12-09",names:["Bethany Black","Michael McIlrath","Mario Renteria"]},
 {date:"2026-12-16",names:["Robert Min","Jay Shergill","Bryan Russell"]},
 {date:"2027-01-06",names:["John Jorgensen","Ramji Digumarthi","Ken Wong"]}
];

var all=MEMBERS.slice().sort(function(a,b){return a.Name.localeCompare(b.Name)});var activeFilter='all';
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function pd(p){return (p||'').replace(/[^0-9]/g,'')}
function slug(n){return (n||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}
function initials(n){var p=(n||'').replace(/\(.*?\)/g,'').trim().split(/\s+/);return ((p[0]||'')[0]||'')+((p.length>1?p[p.length-1][0]:'')||'')}
var LOCAL=""" + __import__("json").dumps(sorted(f[:-4] for f in __import__("os").listdir(__import__("os").path.join(SITE,"photos")) if f.endswith(".jpg"))) + r""";
var PHOTOS={"Shannon Sevor": "photos/shannon-sevor.jpg", "Maria Nunez": "https://bniconnectglobal.com/web/open/networkViewProfileImage/6ac5dadb217e120001e0973f.jpg", "Bethany Black": "https://bniconnectglobal.com/web/open/networkViewProfileImage/55cce182f0f0e33b902c32e5.jpg", "Daisy Pineda": "https://bniconnectglobal.com/web/open/networkViewProfileImage/62cc60f5e4b0165f2a05c6b7.jpg", "Colin Clancy": "https://bniconnectglobal.com/web/open/networkViewProfileImage/5b983109663cad000142bc19.jpg", "Jay Shergill": "https://bniconnectglobal.com/web/open/networkViewProfileImage/6963230df4936d000136d262.jpg", "Joseph Barghouthi": "https://bniconnectglobal.com/web/open/networkViewProfileImage/65eb36b0868a6c0001577e8c.jpg", "Thi Kelley": "https://bniconnectglobal.com/web/open/networkViewProfileImage/6a98432d8ea062000177bb30.jpg", "Elizabeth Popova": "https://bniconnectglobal.com/web/open/networkViewProfileImage/6709a807059d970001bcefd9.jpg", "John Jorgensen": "https://bniconnectglobal.com/web/open/networkViewProfileImage/64deac0fe4b01b5a8c17cdff.jpg", "John Wheeler": "https://bniconnectglobal.com/web/open/networkViewProfileImage/66be7fb0e4b0869983281eb6.jpg", "Marie Zandian": "https://bniconnectglobal.com/web/open/networkViewProfileImage/641cc6bbe4b0c2b5512624fc.jpg", "Tom Pavicic": "https://bniconnectglobal.com/web/open/networkViewProfileImage/62f68c4de4b0165f2a0687c3.jpg", "Bryan Russell": "https://bniconnectglobal.com/web/open/networkViewProfileImage/68c1c11f01d9a400017199fd.jpg", "Phil Lonardo": "https://bniconnectglobal.com/web/open/networkViewProfileImage/694ebbd537f61500019e79b2.jpg", "Roxanne Salazar": "https://bniconnectglobal.com/web/open/networkViewProfileImage/6a2321929882230001c72b37.jpg", "Denise Artache": "https://bniconnectglobal.com/web/open/networkViewProfileImage/66fccf7be4b0147dce9c7397.jpg", "Shawna Rodriguez": "https://bniconnectglobal.com/web/open/networkViewProfileImage/6a979c5d549e85000145a8d9.jpg", "Sonia Shah": "https://bniconnectglobal.com/web/open/networkViewProfileImage/6a2b2ccff10c170001ace7c7.jpg", "Elliot Foad": "https://bniconnectglobal.com/web/open/networkViewProfileImage/6a6a17b3acc6a6000165e919.jpg", "Ken Wong": "https://bniconnectglobal.com/web/open/networkViewProfileImage/680135c08202c20001cfd670.jpg"};
function avatar(n){var s1=slug(n),s2=slug((n||'').replace(/^Cliff /,'Clifford ')),loc=LOCAL.indexOf(s1)>-1?s1:(LOCAL.indexOf(s2)>-1?s2:'');var src=loc?(PHOTO_DIR+loc+PHOTO_EXT):(PHOTOS[n]||PHOTOS[(n||'').replace('Clifford','Cliff')]||(PHOTO_DIR+slug(n)+PHOTO_EXT));return '<div class="avatar">'+esc(initials(n).toUpperCase())+'<img src="'+src+'" alt="" loading="lazy" onerror="this.remove()"></div>'}
function vc(m){var l=['BEGIN:VCARD','VERSION:3.0','FN:'+m.Name,'ORG:'+(m.Company||''),'TITLE:'+(m.Classification||'')];var d=pd(m.Phone);if(d)l.push('TEL;TYPE=WORK,VOICE:'+d);if(m.Email)l.push('EMAIL:'+m.Email);if(m.Website)l.push('URL:https://'+m.Website);l.push('END:VCARD');return l.join('\r\n')}
function save(btn,idx){var m=all.filter(function(x){return x._idx===idx})[0];if(!m)return;var b=new Blob([vc(m)],{type:'text/vcard'});var u=URL.createObjectURL(b);var a=document.createElement('a');a.href=u;a.download=m.Name.replace(/\s+/g,'_')+'.vcf';a.click();URL.revokeObjectURL(u);btn.textContent='Saved';btn.classList.add('saved');setTimeout(function(){btn.textContent='Save contact';btn.classList.remove('saved')},2500)}
var IC_PHONE='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.6 3.38 2 2 0 0 1 3.57 1h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.54a16 16 0 0 0 6.29 6.29l.91-.91a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>';
var IC_MAIL='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>';
var IC_WEB='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>';
function card(m){var d=pd(m.Phone);var o='<div class="card"><div class="card-top">'+avatar(m.Name)+'<div><div class="card-sphere">'+esc(m['Contact Sphere'])+'</div><div class="card-name">'+esc(m.Name)+'</div></div></div>';
 o+='<div class="card-class">'+esc(m.Classification)+'</div><div class="card-co">'+esc(m.Company)+'</div><div class="card-links">';
 if(m.Phone)o+='<a class="link" href="tel:'+d+'">'+IC_PHONE+'<span>'+esc(m.Phone)+'</span></a>';
 if(m.Email)o+='<a class="link" href="mailto:'+esc(m.Email)+'">'+IC_MAIL+'<span>'+esc(m.Email)+'</span></a>';
 if(m.Website&&m.Website.trim())o+='<a class="link" href="https://'+esc(m.Website.replace(/^https?:\/\//,''))+'" target="_blank" rel="noopener">'+IC_WEB+'<span>'+esc(m.Website)+'</span></a>';
 o+='</div><button class="save" onclick="save(this,'+m._idx+')">Save contact</button></div>';return o}
function render(){var q=document.getElementById('search').value.toLowerCase();var f=all.filter(function(m){var ms=activeFilter==='all'||(m['Contact Sphere']||'')===activeFilter;var mq=!q||[m.Name,m.Classification,m.Company,m['Contact Sphere']].some(function(v){return (v||'').toLowerCase().indexOf(q)>-1});return ms&&mq});
 document.getElementById('showing-count').textContent=f.length;var g=document.getElementById('members-grid');g.innerHTML=f.length?f.map(card).join(''):'<div class="empty"><h3>No members found</h3><p>Try a different search or category.</p></div>'}
function setFilter(s,btn){activeFilter=s;document.querySelectorAll('.chip').forEach(function(x){x.classList.remove('active')});btn.classList.add('active');render()}
function init(){all.forEach(function(m,i){m._idx=i});var sp=[];all.forEach(function(m){var s=m['Contact Sphere']||'';if(s&&sp.indexOf(s)===-1)sp.push(s)});sp.sort();
 document.getElementById('total-count').textContent=all.length;document.getElementById('sphere-count').textContent=sp.length;var w=document.getElementById('filter-wrap');
 sp.forEach(function(s){var b=document.createElement('button');b.className='chip';b.textContent=s;b.onclick=function(){setFilter(s,b)};w.appendChild(b)});
 var allBtn=document.querySelector('[data-sphere="all"]');allBtn.onclick=function(){setFilter('all',allBtn)};
 document.getElementById('search').addEventListener('input',render);render()}

function spFind(n){var l=n.toLowerCase();var m=MEMBERS.filter(function(x){return x.Name.toLowerCase()===l})[0];
 if(!m){var last=l.split(' ').pop();var c=MEMBERS.filter(function(x){return x.Name.toLowerCase().split(' ').pop()===last});if(c.length===1)m=c[0]}
 return m||{Name:n,Classification:'',Company:''}}
function spDate(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2])}
function initSpeakers(){var t=new Date();t.setHours(0,0,0,0);
 var now=Date.now();var up=SPEAKERS.filter(function(w){return spDate(w.date).getTime()+8.5*3600e3>now}).sort(function(a,b){return spDate(a.date)-spDate(b.date)});
 if(!up.length)return;var cur=up[0],d=spDate(cur.date);
 document.getElementById('sp-date').textContent=(d.getTime()===t.getTime()?'Today, ':'')+d.toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric'});
 document.getElementById('sp-grid').innerHTML=cur.names.map(function(n,i){var m=spFind(n);
  return '<div class="sp-card">'+avatar(m.Name)+'<div><div class="sp-tag">Speaker '+(i+1)+'</div><div class="sp-name">'+esc(m.Name)+'</div>'+(m.Classification?'<div class="sp-class">'+esc(m.Classification)+'</div>':'')+(m.Company?'<div class="sp-co">'+esc(m.Company)+'</div>':'')+'</div></div>'}).join('');
 var rest=up.slice(1,6);
 if(rest.length){document.getElementById('sp-list').innerHTML=rest.map(function(w){var x=spDate(w.date);
  return '<div class="next-item"><div class="cal"><div class="cal-m">'+x.toLocaleDateString('en-US',{month:'short'})+'</div><div class="cal-d">'+x.getDate()+'</div></div><div class="next-names">'+w.names.map(function(n){var m=spFind(n);var what=(m.Classification?'<b>'+esc(m.Classification)+'</b>':'')+(m.Classification&&m.Company?' &middot; ':'')+(m.Company?esc(m.Company):'');return '<div class="np">'+avatar(m.Name)+'<div style="min-width:0"><div class="np-name">'+esc(m.Name)+'</div>'+(what?'<div class="np-what">'+what+'</div>':'')+'</div></div>'}).join('')+'</div></div>'}).join('')}
 else document.getElementById('sp-next').style.display='none';
 document.getElementById('speakers').hidden=false}

init();initSpeakers();
document.querySelectorAll('.ld .avatar').forEach(function(el){var n=el.getAttribute('data-name');el.outerHTML=avatar(n)});
</script></body></html>
"""
h = HTML.replace("__MAPS__", "https://www.google.com/maps/search/?api=1&query=Bogey%27s+Pizza+Co+5039+Almaden+Expy+San+Jose+CA+95118").replace("__OFFICIAL__", "https://bnisfbay.com/ca-santa-clara-premiere/en-US/index").replace("__LOGO__", logo64).replace("__VISIT__", VISIT).replace("__MEMBERS__", members_line)
open(out, "w", encoding="utf-8").write(h)
print("written", len(h))
