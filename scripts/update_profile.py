"""Render first-party GitHub profile cards; Python standard library only."""
import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.request

OWNER = "QiuuDev"
ASSETS = Path(__file__).resolve().parents[1] / "assets"


def api(path, body=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "QiuuDev-profile"}
    if os.getenv("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request("https://api.github.com/" + path, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if isinstance(result, dict) and result.get("errors"):
        raise RuntimeError("GitHub GraphQL query failed; existing cards were preserved")
    return result


def public_repos():
    repos = []
    page = 1
    while True:
        batch = api(f"users/{OWNER}/repos?type=owner&sort=pushed&per_page=100&page={page}")
        repos.extend(r for r in batch if not r["private"])
        if len(batch) < 100:
            return repos
        page += 1


def text(x, y, value, size=14, color="var(--fg)", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{html.escape(str(value))}</text>'


def svg(body, height, mode, title):
    colors = ("#080e1d", "#eef5ff", "#95a9c9", "#50e8ed", "#a792ff", "#263650") if mode == "dark" else ("#f2f7ff", "#15223c", "#526780", "#007e88", "#7354cf", "#cddaea")
    bg, fg, muted, cyan, violet, line = colors
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img"><title>{html.escape(title)}</title>
<style>:root{{--bg:{bg};--fg:{fg};--muted:{muted};--cyan:{cyan};--violet:{violet};--line:{line}}}text{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}.signal{{animation:breathe 5s ease-in-out infinite}}@keyframes breathe{{50%{{opacity:.55}}}}@media(prefers-reduced-motion:reduce){{.signal{{animation:none}}}}</style>
<rect x="1" y="1" width="958" height="{height-2}" rx="16" fill="{bg}" stroke="{line}"/>{body}</svg>'''


def render(user, repos, calendar, stamp):
    repos = [r for r in repos if not r["private"]]
    original = [r for r in repos if not r["fork"]]
    recent = sorted((r for r in original if r["name"] != OWNER and r["size"] > 0), key=lambda r: r.get("pushed_at") or "", reverse=True)[:3]
    languages = sorted({r["language"] for r in original if r.get("language")})
    body = text(30, 38, "PUBLIC WORKSPACE / TELEMETRY", 12, "var(--cyan)", 'letter-spacing="2"')
    for x, value, label in [(32,len(repos),"PUBLIC REPOS"),(269,sum(r["stargazers_count"] for r in original),"STARS / OWN WORK"),(506,user["followers"],"FOLLOWERS"),(743,len(languages),"PRIMARY LANGUAGES")]:
        body += text(x, 97, value, 40) + text(x, 122, label, 11, "var(--muted)")
    body += '<path d="M30 146H930" stroke="var(--line)"/>'
    body += text(30, 179, "RECENT PUBLIC REPOSITORY PUSHES", 11, "var(--violet)", 'letter-spacing="1.4"')
    for i, r in enumerate(recent):
        y = 208 + i*28
        body += text(32, y, r["name"][:42], 15) + text(927, y, (r.get("pushed_at") or "")[:10], 12, "var(--muted)", 'text-anchor="end"')
    body += text(30, 300, "PRIMARY LANGUAGES / " + (" · ".join(languages) or "—"), 12, "var(--muted)")
    body += text(30, 327, "UPDATED " + stamp + " UTC · SOURCE: GITHUB", 10, "var(--muted)")
    output = {f"activity-{mode}.svg": svg(body, 350, mode, "Public GitHub repository statistics. Updated " + stamp) for mode in ("dark", "light")}
    weeks = calendar["weeks"]
    all_days = [day for week in weeks for day in week["contributionDays"]]
    counts = [day["contributionCount"] for day in all_days]
    peak = max(counts, default=0)
    for mode in ("dark", "light"):
        colors = ["#152238", "#124b55", "#14838a", "#24b8be", "#50e8ed"] if mode == "dark" else ["#dfe8f4", "#b7e6e5", "#71cbcd", "#2da4af", "#087c88"]
        matrix = text(30, 38, "CONTRIBUTION MATRIX / LAST YEAR", 12, "var(--cyan)", 'letter-spacing="1.5"')
        matrix += text(30, 81, f'{calendar["totalContributions"]:,}', 34) + text(190,81,"contributions",14,"var(--muted)")
        matrix += text(929, 80, f'{sum(c > 0 for c in counts)} active days', 14, "var(--muted)", 'text-anchor="end"')
        # Preserve GitHub week/day positions, including partial boundary weeks.
        cell = min(16, 864/max(1,len(weeks)))
        previous_month = None
        for w, week in enumerate(weeks):
            for day in week["contributionDays"]:
                count = day["contributionCount"]
                level = 0 if count == 0 else min(4, 1 + int(3*(count/max(1,peak))))
                x, y = 48 + w*cell, 120 + day["weekday"]*18
                matrix += f'<rect x="{x:.2f}" y="{y}" width="{cell-3:.2f}" height="13" rx="2" fill="{colors[level]}"><title>{html.escape(day["date"])}: {count} contributions</title></rect>'
            if week["contributionDays"]:
                month = week["contributionDays"][0]["date"][5:7]
                if month != previous_month:
                    matrix += text(round(48+w*cell,2),111,dt.date(2000,int(month),1).strftime("%b"),9,"var(--muted)")
                    previous_month=month
        matrix += text(30, 270, "Less", 10, "var(--muted)")
        for i, color in enumerate(colors):
            matrix += f'<rect x="{68+i*17}" y="260" width="12" height="12" rx="2" fill="{color}"/>'
        matrix += text(160,270,"More",10,"var(--muted)")
        matrix += text(929,270,"UPDATED " + stamp + " UTC",10,"var(--muted)",'text-anchor="end"')
        matrix += '<circle class="signal" cx="914" cy="34" r="4" fill="var(--cyan)"/>'
        output[f"contributions-{mode}.svg"] = svg(matrix, 292, mode, "GitHub contribution calendar. Updated " + stamp)
    return output


def main():
    user = api(f"users/{OWNER}")
    repos = public_repos()
    query = '''query($login:String!){ user(login:$login){ contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date weekday contributionCount } } } } } }'''
    calendar = api("graphql", {"query": query, "variables": {"login": OWNER}})["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    output = render(user, repos, calendar, stamp)
    # All requests and rendering complete before overwriting any existing cards.
    ASSETS.mkdir(exist_ok=True)
    for filename, content in output.items():
        (ASSETS / filename).write_text(content, encoding="utf-8")
    print("Updated four SVG cards from GitHub data.")


if __name__ == "__main__":
    main()
