import json, re, base64, sys, os
TOOLS = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get("SITE", os.path.dirname(TOOLS))
logo = base64.b64encode(open(sys.argv[1],'rb').read()).decode()
out = sys.argv[2]
home = open(os.path.join(SITE,'index.html'), encoding='utf-8').read()
speakers = re.search(r'var SPEAKERS=\[.*?\];', home, re.S).group(0)
ag = json.load(open(os.path.join(TOOLS,'agendas.json')))
H = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>BNI Premiere | Meeting Agendas</title>
<style>
:root{--red:#C4242A;--red-soft:#FBEDED;--off:#F6F4F1;--line:#E6E1DC;--ink:#161616;--text:#3A3A3A;--muted:#7A7470}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;color:var(--ink);background:#fff;-webkit-font-smoothing:antialiased}
.wrap{max-width:860px;margin:0 auto;padding:36px 20px 64px}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:44px}
header img{height:34px}
header a{font-size:14px;font-weight:700;color:var(--muted);text-decoration:none}
.kicker{font-size:12px;font-weight:700;letter-spacing:2.2px;text-transform:uppercase;color:var(--red);margin-bottom:10px}
h1{font-size:clamp(34px,6vw,52px);letter-spacing:-1.5px;line-height:1.05}
h1 em{font-style:normal;color:var(--red)}
.lead{font-size:17px;color:var(--text);margin-top:12px;line-height:1.5}
.cur{display:block;margin-top:32px;background:var(--red);color:#fff;border-radius:18px;padding:28px 30px;text-decoration:none;transition:transform .15s}
.cur:hover{transform:translateY(-2px)}
.cur .lbl{font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;opacity:.85}
.cur .d{font-size:clamp(26px,4.5vw,36px);font-weight:700;letter-spacing:-.8px;margin-top:6px}
.cur .s{font-size:15px;margin-top:8px;opacity:.92}
.cur .go{display:inline-block;margin-top:18px;background:#fff;color:var(--red);font-weight:700;font-size:14px;padding:10px 18px;border-radius:999px}
h2{font-size:13px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin:44px 0 12px}
.list a{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 18px;border:1px solid var(--line);border-radius:12px;margin-bottom:10px;text-decoration:none;color:var(--ink);background:#fff}
.list a:hover{border-color:var(--red)}
.list b{font-size:16px}
.list span{font-size:13px;color:var(--muted);display:block;margin-top:3px}
.list i{font-style:normal;color:var(--red);font-weight:700;font-size:14px;white-space:nowrap}
.empty{font-size:14px;color:var(--muted)}
</style></head><body><div class="wrap">
<header><img src="data:image/png;base64,__LOGO__" alt="BNI"><a href="../">&larr; bnipremierchapter.com</a></header>
<div class="kicker">BNI Premiere</div><h1>Meeting <em>agendas</em></h1>
<p class="lead">Every Wednesday's slides, saved by date. Open this week's to put it on the screen, or look back at a past meeting.</p>
<div id="cur"></div>
<h2>Past meetings</h2><div class="list" id="past"></div>
</div><script>
__SPEAKERS__
var AGENDAS=__AGENDAS__;
function sd(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2])}
function fmt(d){return d.toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'})}
function who(date){var w=SPEAKERS.filter(function(x){return x.date===date})[0];return w?w.names.join(', '):''}
var t=new Date();t.setHours(0,0,0,0);
var A=AGENDAS.slice().sort(function(a,b){return sd(b.date)-sd(a.date)});
var up=A.filter(function(a){return sd(a.date)>=t}).sort(function(a,b){return sd(a.date)-sd(b.date)});
var cur=up[0]||A[0];var past=A.filter(function(a){return sd(a.date)<t&&a!==cur});
if(cur){var isUp=sd(cur.date)>=t;document.getElementById('cur').innerHTML='<a class="cur" href="'+cur.slug+'/"><div class="lbl">'+(isUp?'This week':'Most recent')+'</div><div class="d">'+fmt(sd(cur.date))+'</div>'+(who(cur.date)?'<div class="s">Speakers: '+who(cur.date)+'</div>':'')+'<span class="go">Open agenda &rarr;</span></a>'}
document.getElementById('past').innerHTML=past.length?past.map(function(a){return '<a href="'+a.slug+'/"><div><b>'+fmt(sd(a.date))+'</b>'+(who(a.date)?'<span>'+who(a.date)+'</span>':'')+'</div><i>View &rarr;</i></a>'}).join(''):'<p class="empty">Past agendas will show up here after each meeting.</p>';
</script></body></html>"""
H = H.replace('__LOGO__', logo).replace('__SPEAKERS__', speakers).replace('__AGENDAS__', json.dumps(ag))
open(out,'w',encoding='utf-8').write(H); print('written', len(H))
