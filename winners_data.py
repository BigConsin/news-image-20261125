"""Data for the winners-style layout (modelled on the 24 Nov #1 and #2).

Stories 1-36 are the LOCK_PACK-verified set from final_data.py.
Stories 37-40 are additional 25 Nov items verified in this chat's own
research files on 25 Nov (each with dated evidence):
  37 NOAA space weather, issued 2026 Nov 25 0030 UTC (OFFICIAL)
  38 EasyJet profit GBP 71m vs GBP 87.7m expected (Reuters, 25 Nov slug)
  39 NZ Miss Universe 4th runner-up (25 Nov-dated reports)
  40 Ghana GHc 28.58bn bond buyback closing 25 Nov (single roundup
     source in the research file, so it carries [CLAIM])
Regions are split finer than the draft: East / Southeast / South Asia
and North America separated, 9 regions in all.
"""

import final_data as F

TOP_LEFT = "THE WORLD IN ONE DAY"
TOP_RIGHT = "40 STORIES - 9 REGIONS - EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
TAGLINE = F.SUBTITLE

STATS = [
    ("-6.16%", "Kospi crash: worst day of the Asia chip rout"),
    ("88/112", "Russian drones downed by Ukraine overnight"),
    ("4.9%", "Australia inflation jumps, up from 4.3%"),
    ("A$740m", "Australia-Solomon Islands security treaty"),
    ("81.5m", "Americans travel for Thanksgiving week"),
    ("600", "aid workers killed in Gaza, incl. 397 UNRWA"),
]

UTC_BAR = ("WEDNESDAY IN UTC   00:30 NOAA G1 watch for Nov 26-27   -   "
           "08:18 Shenzhou-24 lifts off   -   13:30 Core PCE +3.3% y/y   -   "
           "16:35 Stoxx ends -1.06%   -   21:00 PSG held 2-2 by Roma")

REGIONS = [
    ("EUROPE 10", "#274b9f"),
    ("EAST ASIA 5", "#b03a2e"),
    ("MIDDLE EAST 5", "#c98a1b"),
    ("AFRICA 7", "#7d3c98"),
    ("N. AMERICA 5", "#1e8449"),
    ("OCEANIA 4", "#117a8b"),
    ("S. ASIA 2", "#2e6da4"),
    ("SE ASIA 1", "#4d908e"),
    ("GLOBAL 1", "#555555"),
]

# fact = the red banner across the bottom of the card's picture
LEADS = []
for _s, _fact, _src in [
    (F.LEADS[0], "FIRST FOREIGNER ON A CHINESE CREWED MISSION",
     "CGTN - Xinhua - Arab News"),
    (F.LEADS[1], "KOSPI -6.16% - SAMSUNG -9.87%", "AP - Seoul Economic Daily"),
    (F.LEADS[2], "7 KILLED - SECURITY CHIEF AMONG THEM", "AFP - Al Jazeera"),
]:
    _d = dict(_s)
    _d["fact"] = _fact
    _d["src"] = _src
    LEADS.append(_d)

_GRID_EXTRA = [
    ("88 OF 112 DOWNED", "Ukrinform - General Staff"),
    ("+0.1% Q/Q - INVESTMENT -1.2%", "Destatis, release 409"),
    ("A$740M OVER 10 YEARS", "Reuters - AFP"),
    ("9 DEAD - 17 TRAPPED", "AP - Arab News"),
    ("4.9% - FUEL +6.3%", "ABS - RBA"),
    ("259 SEATS CLINCHED", "Reports"),
    ("4,200+ FLIGHTS DELAYED", "NOAA - Reuters - FlightAware"),
    ("LEAD: 403 RUNS", "LiveScore - IANS"),
    ("CLOSE 626.03", "Dow Jones - Morningstar"),
    ("+1,502 POINTS", "Moneycontrol - ET Now"),
]
GRID = []
for _s, (_fact, _src) in zip(F.GRID, _GRID_EXTRA):
    _d = dict(_s)
    _d["fact"] = _fact
    _d["src"] = _src
    GRID.append(_d)

ALSO = list(F.ALSO) + [
    (37, "Space:", " NOAA: solar wind 368 km/s, Kp 3.0; G1 storm watch Nov 26-27"),
    (38, "London:", " EasyJet profit GBP 71m misses the GBP 87.7m forecast (Reuters)"),
    (39, "Auckland:", " NZ's Waddington 4th runner-up at Miss Universe, best in 33 yrs"),
    (40, "Accra:", " Ghana's GHc 28.58bn bond buyback closes Wednesday [CLAIM]"),
]

DATE_CHECK = ("Every numbered story happened, or was first reported, on Wednesday "
              "25 November 2026. Left out as earlier news: Monday's Nvidia-led rally, "
              "Tuesday's US consumer-confidence jump to 103.3 and Real Madrid's 5-1 "
              "win over PSV (all 24 Nov). Stories 20-22, 26 and 40 are one side's claim.")
SOURCES_LINE = ("Compiled Wednesday 25 November 2026 (UTC). Sources: Reuters, AP, AFP, "
                "Al Jazeera, Destatis, ABS, NOAA, UN OCHA and the day's wires, as tagged.")
HOW_SURE = [
    ("OFFICIAL", "= on the record"),
    ("REPORTED", "= wires / outlets"),
    ("CLAIM", "= one side's account"),
]

PINS_LONLAT = F.PINS_LONLAT
MAP_ROWS = F.MAP_ROWS
MASTHEAD = F.MASTHEAD
