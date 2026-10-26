"""Make the Instagram "Meet this week's speakers" flyers (story 1080x1920 + feed 1080x1350).

Usage:  python3 make_flyers.py 2026-11-04 "Marcus Araiza" "Marie Zandian" "Marco Cerda"
Writes: <site>/flyers/nov4-story.png and nov4-feed.png
Names must match the member directory (index.html MEMBERS) - e.g. "Clifford Shaw", "Robert Min", "Ramji Digumarthi".
Photos come from <site>/photos/<first-last>.jpg; members without one get a red initials circle.
"""
import base64, datetime, html, json, os, re, sys, tempfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get("SITE", os.path.dirname(TOOLS))

date = datetime.date.fromisoformat(sys.argv[1])
names = sys.argv[2:5]
assert len(names) == 3, "need exactly 3 speaker names"

home = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
members = json.loads(re.search(r"var MEMBERS=(\[.*?\]);", home, re.S).group(1))


def slug(n):
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", n.lower()))


def find(n):
    for m in members:
        if m["Name"].lower() == n.lower():
            return m
    last = [m for m in members if m["Name"].lower().split()[-1] == n.lower().split()[-1]]
    if len(last) == 1:
        return last[0]
    sys.exit("Not in member directory: " + n)


def photo(n):
    p = os.path.join(SITE, "photos", slug(n) + ".jpg")
    if os.path.exists(p):
        return "file://" + p
    ini = "".join(w[0] for w in [n.split()[0], n.split()[-1]]).upper()
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><circle cx="100" cy="100" r="100" fill="#C4242A"/>'
           '<text x="100" y="122" font-family="Helvetica Neue,Arial" font-size="72" font-weight="700" fill="#fff" text-anchor="middle">%s</text></svg>' % ini)
    print("  no photo for %s - using initials" % n)
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


vals = {"DATE": date.strftime("%b ") + str(date.day), "LOGO": "file://" + os.path.join(TOOLS, "bni-logo.png")}
for i, n in enumerate(names, 1):
    m = find(n)
    vals["NAME%d" % i] = html.escape(m["Name"])
    vals["CAT%d" % i] = html.escape(m.get("Classification", ""))
    vals["BIZ%d" % i] = html.escape(m.get("Company", ""))
    vals["PHOTO%d" % i] = photo(m["Name"])

tag = date.strftime("%b").lower() + str(date.day)
os.makedirs(os.path.join(SITE, "flyers"), exist_ok=True)
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for kind, w, h in [("story", 1080, 1920), ("feed", 1080, 1350)]:
        t = open(os.path.join(TOOLS, "flyers", kind + ".html"), encoding="utf-8").read()
        for k, v in vals.items():
            t = t.replace("{{%s}}" % k, v)
        tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
        tmp.write(t); tmp.close()
        p = b.new_page(viewport={"width": w, "height": h})
        p.goto("file://" + tmp.name); p.wait_for_timeout(800)
        out = os.path.join(SITE, "flyers", "%s-%s.png" % (tag, kind))
        p.screenshot(path=out, clip={"x": 0, "y": 0, "width": w, "height": h})
        print("wrote", out)
    b.close()
