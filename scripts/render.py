"""Render a deterministic, self-contained contribution tank animation."""
import json, os, urllib.request, html
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
login = os.environ.get('PROFILE_LOGIN', 'jarredhj0214')
if os.environ.get('CONTRIBUTIONS_FILE'):
    data = json.loads(Path(os.environ['CONTRIBUTIONS_FILE']).read_text())
else:
    query = 'query { user(login: "%s") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount color } } } } } }' % login
    req = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query':query}).encode(), headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'], 'Content-Type':'application/json'})
    data = json.load(urllib.request.urlopen(req))
if data.get('errors'): raise RuntimeError(data['errors'])
cal = data['data']['user']['contributionsCollection']['contributionCalendar']
weeks = cal['weeks']
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1060" height="340" viewBox="0 0 1060 340" role="img" aria-label="Animated tank battle over real GitHub contributions">', '''<defs><pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M18 0H0V18" fill="none" stroke="#172739" stroke-width=".6"/></pattern><g id="tank"><rect x="-8" y="-9" width="5" height="18" rx="1" fill="#33465c"/><rect x="3" y="-9" width="5" height="18" rx="1" fill="#33465c"/><rect x="-5" y="-7" width="10" height="14" rx="2" fill="currentColor"/><rect x="-3" y="-3" width="6" height="6" fill="#e8faff"/><path d="M0 0V-13" stroke="currentColor" stroke-width="3"/></g></defs><style>text{font-family:monospace} .scan{animation:scan 8s linear infinite}@keyframes scan{from{transform:translateX(0)}to{transform:translateX(960px)}}@media(prefers-reduced-motion:reduce){.scan{animation:none}}</style>''', '<rect width="1060" height="340" rx="16" fill="#090f1c"/><rect x="1" y="1" width="1058" height="338" rx="16" fill="none" stroke="#263b53"/>', '<text x="32" y="38" fill="#60f0d5" font-size="19" font-weight="bold">JARRED / COMMIT COMBAT</text>', f'<text x="1028" y="37" text-anchor="end" fill="#9caec7" font-size="12">{cal["totalContributions"]:,} CONTRIBUTIONS · LAST 12 MONTHS</text>', '<text x="32" y="64" fill="#70839e" font-size="11">INSERT COMMIT  •  BUILD / SHIP / REPEAT</text>', '<rect x="32" y="83" width="996" height="186" rx="8" fill="#0d1726"/><rect x="32" y="83" width="996" height="186" fill="url(#grid)"/>']
# Use all returned calendar weeks; seven rows, one per weekday.
cell = 18
for w, week in enumerate(weeks):
    for day in week['contributionDays']:
        from datetime import date
        row = (date.fromisoformat(day['date']).weekday()+1)%7
        x,y = 48+w*cell, 108+row*cell
        n = day['contributionCount']
        color = '#172438' if not n else ('#165b59' if n<3 else '#208979' if n<7 else '#39bfa2' if n<15 else '#78f2bf')
        parts.append(f'<g><title>{day["date"]}: {n} contributions</title><rect x="{x}" y="{y}" width="15" height="15" rx="2" fill="{color}"/>')
        if n: parts.append(f'<path d="M{x} {y+7}h15m-8-7v7m4 0v8" stroke="#0b2630" stroke-width="1" opacity=".55"/>')
        parts.append('</g>')
parts.append('<rect class="scan" x="42" y="98" width="2" height="145" fill="#60f0d5" opacity=".18"/>')
# Tanks move in clear perimeter lanes; their shots enter the contribution field.
for idx,(color,ys,direction) in enumerate([('#60f0d5',252,1),('#b58aff',94,-1)]):
    coords = '64,0;976,0;64,0' if direction==1 else '976,0;64,0;976,0'
    parts.append(f'<g transform="translate(0 {ys})" color="{color}"><g><animateTransform attributeName="transform" type="translate" values="{coords}" dur="18s" repeatCount="indefinite"/><g transform="rotate({0 if direction==1 else 180})"><use href="#tank"/></g></g></g>')
for i in range(12):
    x = 90+i*76
    start,end = (240,130+(i%4)*18) if i%2==0 else (107,200-(i%4)*18)
    delay = i*.65
    parts.append(f'<rect x="{x}" y="{start}" width="3" height="8" rx="1" fill="{ "#60f0d5" if i%2==0 else "#b58aff" }" opacity="0"><animate attributeName="y" values="{start};{end};{end}" keyTimes="0;.22;1" dur="8s" begin="{delay}s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.21;.23;1" dur="8s" begin="{delay}s" repeatCount="indefinite"/></rect>')
    parts.append(f'<g transform="translate({x+1} {end})" opacity="0"><path d="M-9 0H9M0-9V9M-6-6L6 6M-6 6L6-6" stroke="#ffc76a" stroke-width="3"/><rect x="-3" y="-3" width="6" height="6" fill="#fff0bc"/><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;.21;.23;.3;1" dur="8s" begin="{delay}s" repeatCount="indefinite"/></g>')
parts += ['<path d="M488 270h84v12h-84z" fill="#263b53"/><text x="530" y="278" text-anchor="middle" fill="#60f0d5" font-size="9">JARRED HQ</text>', '<text x="32" y="308" fill="#9caec7" font-size="11">P1: DATA ENGINEER</text><text x="530" y="308" text-anchor="middle" fill="#60f0d5" font-size="11">JAVA → SQL → METADATA → LINEAGE</text><text x="1028" y="308" text-anchor="end" fill="#b58aff" font-size="11">AUTO PLAY / ∞</text>', '</svg>']
(ROOT/'assets/tank-battle.svg').write_text('\n'.join(parts))
(ROOT/'assets/header.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1060 260" width="1060" height="260"><defs><linearGradient id="bg"><stop stop-color="#101c32"/><stop offset="1" stop-color="#201630"/></linearGradient><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#60f0d5" opacity=".08"/></pattern></defs><rect width="1060" height="260" rx="16" fill="url(#bg)"/><rect width="1060" height="260" fill="url(#g)"/><g font-family="monospace"><text x="50" y="53" font-size="13" fill="#60f0d5">jarredhj0214 / developer terminal</text><text x="48" y="122" font-size="54" font-weight="bold" fill="#ecf6ff">Hello, I'm Jarred.</text><text x="50" y="162" font-size="20" fill="#afbdd1">Making sense of data. One system at a time.</text><text x="50" y="217" font-size="14" fill="#60f0d5">DATA PLATFORMS   /   SQL LINEAGE   /   OPEN SOURCE</text><path d="M960 55h-55v55h55v55h-55v55" stroke="#b58aff" stroke-width="2" fill="none"/><circle cx="960" cy="55" r="6" fill="#60f0d5"><animate attributeName="cy" values="55;220;55" dur="6s" repeatCount="indefinite"/></circle></g></svg>''')
print(f'Rendered {len(weeks)} weeks, {cal["totalContributions"]} contributions')
