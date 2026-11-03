#!/usr/bin/env python3
"""Build the Allied Gardens Pool preview: the pool page, Aquatic Programs and Admission Fees, with every lap swim, rec
swim, class and team hour and every closure read live from Pool Relay by finder.js (#today, #week, data-live). Nothing
about WHEN the pool is open is typed here; only fees, ages, rules and facts about the water.
Run: python3 build.py"""
import hashlib, html, json

E = html.escape
V = {"ag": "wukjy7eHCAdsiElT58FrHm"}  # Pool Relay share token: Allied Gardens Pool, lane by lane
SITE = "https://www.sandiego.gov/park-and-recreation/centers/aquatics/alliedgardens"
POOLS = [
    dict(slug="ag", name="Allied Gardens Pool", short="Allied Gardens", facility="Allied Gardens Pool", area="Allied Gardens",
         kind="yearRound", address="6707 Glenroy St, San Diego, CA 92120", phone="619-235-1143", href="index.html"),
]

def live(mode, **kw):
    attrs = "".join(f' data-{k.replace("_", "-")}="{E(str(v))}"' for k, v in kw.items())
    return f'data-live="{mode}" data-view="{V["ag"]}" data-pool="ag"{attrs}'

MENU = [("Pools Home", None, 0), ("Allied Gardens Pool", "index.html", 1), ("Aquatic Programs", "programs.html", 0),
        ("Admission Fees", "fees.html", 0), ("Rules and Regulations", None, 0)]

VER = hashlib.sha1((open("finder.js").read() + open("style.css").read()).encode()).hexdigest()[:8]  # cache-busts both on change

def page(file, title, body, contact):
    menu = "".join(f'<a class="{"sub" if sub else ""}{" here" if href == file else ""}" href="{href or "#"}">{E(label)}</a>'
                   for label, href, sub in MENU)
    doc = f"""<!doctype html>
<!-- UNOFFICIAL PREVIEW. Not a City of San Diego website. A mock-up of {SITE}
     with the pool on one live Pool Relay schedule. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)} | City of San Diego Pools preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={VER}">
</head>
<body>
<div class="preview-note"><b>Unofficial preview.</b> Not a City of San Diego page &mdash; a mock-up of <a href="{SITE}" target="_blank" rel="noopener noreferrer">the Allied Gardens Pool page</a> with the pool on one live schedule.</div>
<header class="site"><div class="hdr">
  <a class="brand" href="index.html"><small>The City of San Diego</small><span>Pools</span></a>
  <div class="right"><div class="util"><span>Get It Done</span><span>Connect</span><span>Search</span></div>
    <nav aria-label="Main"><span>Residents</span><span>Business</span><span>Library</span><span>Public Safety</span><span>City Hall</span></nav></div>
</div></header>
<div class="page">
  <aside class="side"><h2>Pools</h2><nav aria-label="Pools">{menu}</nav></aside>
  <main class="main"><h1>{E(title)}</h1>{body}</main>
  <aside class="contact"><h2>Contact</h2>{contact}</aside>
</div>
<footer class="site"><div class="in">
  <div><h4>City of San Diego Parks &amp; Recreation</h4><p>Allied Gardens Pool<br>6707 Glenroy St, San Diego, CA 92120<br>619-235-1143</p></div>
  <div><h4>About this preview</h4><p>Built to demonstrate embedded <a href="https://www.poolrelay.com" target="_blank" rel="noopener">Pool Relay</a> schedules. Not operated by or affiliated with the City of San Diego. Schedule entered on November 2, 2026 from the City's Allied Gardens fall program sheet (effective October 5, 2026), pool closure calendar and event listings; how the pool's lanes are split between programs is our estimate.</p></div>
</div></footer>
<script>window.POOLS = {json.dumps(POOLS)};</script>
<script src="finder.js?v={VER}"></script>
</body>
</html>
"""
    open(file, "w").write(doc)

CONTACT = """<p><b>Allied Gardens Pool</b>6707 Glenroy St<br>San Diego, CA 92120<br>619-235-1143</p>
<p><b>Pool Manager</b>Lane Harris</p>
<p><b>Nearby</b>Allied Gardens Recreation Center and the Allied Gardens/Benjamin Branch Library.</p>"""

LANES = (f'<div class="frame"><iframe src="https://www.poolrelay.com/embed/{V["ag"]}" height="760" '
         f'title="Allied Gardens Pool, lane by lane" loading="lazy"></iframe></div>')
PROGRAMS = [("Lap Swim", "Lap Swim", "Lane sharing and circle swimming required."),
            ("Recreation Swim", "Rec Swim", "Diving board depends on staffing."),
            ("Aquatic Body Conditioning", "Aquatic Body Conditioning", "Shallow-water fitness class."),
            ("Youth Aquatic League Swim Team", "Youth Aquatic League Swim Team", "Ages 6–17."),
            ("Youth Water Polo", "Youth Water Polo", "Ages 9–17."),
            ("Junior Water Polo", "Junior Water Polo", "Ages 5–8 and 9–12.")]
rows = "".join(f'<tr><th>{E(n)}<div class="small muted" style="font-weight:400">{E(note)}</div></th>'
               f'<td class="when" {live("when", title=t)}>…</td></tr>' for n, t, note in PROGRAMS)
CLOSED = f'<div class="adjusted" {live("closures", ahead=200, label="Pool closed")} hidden></div>'

# ── Allied Gardens Pool ──────────────────────────────────────────────────────
page("index.html", "Allied Gardens Pool", f"""
    <p class="lede">The Allied Gardens Pool is nestled in the heart of the Allied Gardens community, with nearby access to the Allied Gardens
      Recreation Center and the Allied Gardens/Benjamin Branch Library. Every time on this page comes from the pool's live schedule, so when the
      pool staff change it, this page changes with it.</p>
    <div class="top2">
      <section class="now" aria-live="polite"><h2>Right now</h2>
        <div id="today" data-view="{V['ag']}" data-pool="ag"><p class="muted">Loading today’s schedule…</p></div></section>
      <aside class="hours"><h2>Lap swim</h2>
        <div {live("hours", format="dl", title="Lap Swim")}><p class="muted">…</p></div>
        <div class="adjusted" {live("exceptions", title="Lap Swim")} hidden></div>
      </aside>
    </div>
    {CLOSED}
    <h2>Programs</h2>
    <div class="tblwrap"><table class="prog">{rows}</table></div>
    <p class="small muted">Fees and ages on <a href="programs.html">Aquatic Programs</a> and <a href="fees.html">Admission Fees</a>.</p>
    <h2>This week</h2>
    <div id="week" data-view="{V['ag']}" data-pool="ag"><p class="muted">Loading the week…</p></div>
    <h2>Lane by lane</h2>
    <p class="small muted">Pick a day to see which of the 11 lanes each program is using, and how many are left for lap swim.</p>
    {LANES}
    <h2>About the pool</h2>
    <div class="facts">
      <div><h3>Main pool</h3><ul><li>25 yards long by 25 meters wide</li><li>3.5 to 12 feet deep</li><li>11 lanes</li><li>1-meter diving board</li></ul></div>
      <div><h3>Wading pool</h3><ul><li>2 feet deep</li></ul></div>
    </div>
    <p class="small">Amenities: restrooms; disabled access with ramp and lift; drinking fountain; outdoor heated showers; picnic tables;
      lockers (bring your own lock); outdoor lighting; indoor changing stalls; power outlets; bleachers with a shaded spectator area.
      No smoking, no alcohol.</p>

    <div class="replaces">
      <h2>What this replaces</h2>
      <ul>
        <li><b>A PDF in last year's folder.</b> The "Fall Program Guide" link opens <code>/sites/default/files/2024-04/alliedgardenspoolprogram.pdf</code>,
          a file in an April 2024 folder that now holds the fall 2026 schedule. Each season the City re-makes and re-posts it. Here the staff
          change the schedule once and the page follows.</li>
        <li><b>A closure notice from last spring.</b> The page still says <i>"Allied Garden Pool will be closed for maintenance from May 20th to May 27th"</i>.
          Here a closure shows only until it's over, and the next long maintenance closure is already on the calendar.</li>
        <li><b>Flyers that disagree with the schedule.</b> The City's free intro water polo flyer says Allied Gardens runs it
          <i>"Fri/Sat 3:00-4:00pm"</i>, and the pool's own fall program sheet disagrees with it. Here there is one schedule for flyers and
          pages to read from.</li>
        <li><b>"Limited lap lanes during some scheduled programs."</b> Lap swimmers can't tell how many lanes are left when classes and teams are in
          the water. Here every program holds its lanes, so the lane-by-lane view shows what's open.</li>
        <li><b>Sixteen pools, sixteen PDFs.</b> Every City of San Diego pool has this same page and its own program sheet. The same calendar and
          page format could run all of them, with one citywide view of every pool's lap swim.</li>
      </ul>
    </div>
""", CONTACT)

# ── Aquatic Programs ─────────────────────────────────────────────────────────
page("programs.html", "Aquatic Programs", f"""
    <p class="lede">Classes and Youth Aquatic League teams at Allied Gardens Pool. Days and times come from the live schedule.</p>
    <h2>Youth Aquatic League</h2>
    <div class="tblwrap"><table class="prog">
      <tr><th>Swim Team<div class="small muted" style="font-weight:400">Ages 6–17 · $35/month</div></th><td class="when" {live("when", title="Youth Aquatic League Swim Team")}>…</td></tr>
      <tr><th>Youth Water Polo<div class="small muted" style="font-weight:400">Ages 9–17 · $28/month</div></th><td class="when" {live("when", title="Youth Water Polo")}>…</td></tr>
      <tr><th>Junior Water Polo<div class="small muted" style="font-weight:400">Ages 5–8 and 9–12 · $21/month</div></th><td class="when" {live("when", title="Junior Water Polo")}>…</td></tr>
    </table></div>
    <h2>Water fitness</h2>
    <div class="tblwrap"><table class="prog">
      <tr><th>Aquatic Body Conditioning<div class="small muted" style="font-weight:400">Shallow water · $5 daily or $39 for 10 classes</div></th><td class="when" {live("when", title="Aquatic Body Conditioning")}>…</td></tr>
    </table></div>
    <div class="adjusted" {live("exceptions", title="Aquatic Body Conditioning")} hidden></div>
    {CLOSED}
    <h2>Lane by lane</h2>
    {LANES}
""", CONTACT)

# ── Admission Fees ───────────────────────────────────────────────────────────
page("fees.html", "Admission Fees", f"""
    <p class="lede">Daily admission for lap swim and recreation swim at Allied Gardens Pool.</p>
    <div class="tblwrap"><table class="prog">
      <tr><th>Adult</th><td>$5.00 daily</td></tr>
      <tr><th>Child, senior or disabled</th><td>$2.25 daily</td></tr>
      <tr><th>Aquatic Body Conditioning</th><td>$5 daily or $39 for 10 classes</td></tr>
    </table></div>
    <p class="small">The City's Activity Fee Waiver Program can cover fees for eligible residents.</p>
    <h2>When you can swim</h2>
    <div class="tblwrap"><table class="prog">
      <tr><th>Lap Swim</th><td class="when" {live("when", title="Lap Swim")}>…</td></tr>
      <tr><th>Recreation Swim</th><td class="when" {live("when", title="Rec Swim")}>…</td></tr>
    </table></div>
    {CLOSED}
""", CONTACT)
print("built 3 pages, assets", VER)
