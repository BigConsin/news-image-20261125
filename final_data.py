"""Final story data - Wednesday 25 November 2026 (locked 26 Nov).

All market figures are CLOSES from LOCK_PACK_2026-11-26.md (verified
26 Nov morning, Beijing): Kospi -6.16%, Samsung -9.87%, SK hynix
-11.05%, Nikkei 57,011.62 -2.78%, Sensex 83,938.28 +1.82%, Stoxx 600
626.03 -1.06%, US close Dow +0.33% / S&P -0.25% / Nasdaq -0.62%,
core PCE +0.3% m/m and +3.3% y/y. Indonesia mine: 9 dead, 17 trapped.
Iowa detonation confirmed, zero airborne lead. Nor'easter written as
arriving (NJ emergency, 4,200+ flights delayed, parade postponed).
Real Madrid 5-1 PSV (24 Nov) is OUT; PSG 2-2 Roma (25 Nov night) is in.
"""

MASTHEAD = "Wednesday 25 November 2026"
SUBTITLE = ("Shenzhou-24 carries Pakistan's first astronaut  -  "
            "Kospi crashes 6.16% in the chip rout  -  Gaza strikes kill 7")
TOPLINE_LEFT = "THE WORLD IN ONE DAY - ONE PAGE"
TOPLINE_RIGHT = "36 STORIES - 6 REGIONS - ALL FROM WEDNESDAY 25 NOVEMBER 2026"

REGION_BAR = [
    ("EUROPE 9", "#274b9f"),
    ("MIDDLE EAST 5", "#c98a1b"),
    ("ASIA 8", "#b03a2e"),
    ("AMERICAS 5", "#1e8449"),
    ("AFRICA 6", "#7d3c98"),
    ("OCEANIA 3", "#117a8b"),
]

UTC_TICKER = ("UTC   00:30 NOAA G1 WATCH FOR NOV 26-27   -   08:18 SHENZHOU-24 "
              "LIFTS OFF   -   13:30 CORE PCE +3.3% Y/Y   -   16:35 STOXX ENDS "
              "-1.06%   -   GAZA AID TOLL REACHES 600")

LEADS = [
    dict(num=1, kicker="SHENZHOU-24 LAUNCH", place="JIUQUAN, CHINA - SPACE",
         cert="OFFICIAL", kind=("img", "rocket.webp"), banner="08:18 LIFTOFF",
         headline="China launches Shenzhou-24 with Pakistan's first astronaut aboard",
         body="Long March-2F rose at 08:18 Beijing time. Tang Hongbo and Wu Yi fly "
              "with Muhammad Zeeshan Ali, 40, the first foreigner on a Chinese "
              "crewed mission. (CGTN)"),
    dict(num=2, kicker="CHIP ROUT DEEPENS", place="SEOUL - MARKETS",
         cert="REPORTED", kind=("img", "chips.webp"), banner="KOSPI -6.16%",
         headline="Asia chip rout deepens: Kospi crashes 6.16% in a day",
         body="Samsung fell 9.87% and SK hynix 11.05% in Seoul; Tokyo's Nikkei lost "
              "2.78% to 57,012. Hong Kong bucked the rout, closing 1% higher. (AP)"),
    dict(num=3, kicker="GAZA STRIKES", place="GAZA CITY - WAR",
         cert="REPORTED", kind=("img", "gaza.webp"), banner="7 KILLED",
         headline="Israeli strikes kill 7 in Gaza, including Hamas's security chief",
         body="AFP counts seven dead, among them internal security director Naim Abu "
              "Nahal. Over 1,650 Palestinians have died since the October 2025 "
              "truce. (AFP)"),
]

GRID = [
    dict(num=4, kicker="112 DRONES", place="UKRAINE - WAR",
         cert="OFFICIAL", kind=("img", "drone.webp"), banner="88 OF 112 DOWNED",
         headline="Ukraine downs 88 of 112 drones in overnight barrage",
         body="A minibus was hit in the Kharkiv region: 1 killed, 7 injured. "
              "(Ukrinform)"),
    dict(num=5, kicker="GDP REVISED", place="BERLIN - ECONOMY",
         cert="OFFICIAL", kind=("chart", "gdp"), banner="+0.1% Q/Q",
         headline="Germany's Q3 GDP revised to +0.1% as investment falls",
         body="Destatis: +1.2% year on year; investment fell 1.2% in the quarter."),
    dict(num=6, kicker="SECURITY TREATY", place="CANBERRA - DIPLOMACY",
         cert="OFFICIAL", kind=("img", "treaty.webp"), banner="A$740M / 10 YEARS",
         headline="Australia signs A$740m treaty with Solomon Islands",
         body="A$670m in grants plus A$70m in loans; Canberra is named primary "
              "security partner. (Reuters)"),
    dict(num=7, kicker="MINE FLOOD", place="BOGOR - DISASTER",
         cert="REPORTED", kind=("img", "mine.webp"), banner="9 DEAD",
         headline="Flooded gold mine toll rises: 9 dead, 17 still trapped",
         body="Six more bodies were recovered on Wednesday from the flooded "
              "unauthorised Pongkor shafts. (AP)"),
    dict(num=8, kicker="CPI JUMPS", place="SYDNEY - ECONOMY",
         cert="OFFICIAL", kind=("chart", "cpi"), banner="4.9%",
         headline="Australia inflation jumps to 4.9%, fuel up 6.3%",
         body="ABS figures out Wednesday: up from 4.3%, trimmed mean 3.8%. (ABS)"),
    dict(num=9, kicker="259 SEATS", place="WASHINGTON - POLITICS",
         cert="REPORTED", kind=("img", "capitol.webp"), banner="MOST SINCE 1990",
         headline="Democrats clinch 259 House seats",
         body="A Tennessee call sealed at least 259 seats. (Reports)"),
    dict(num=10, kicker="NOR'EASTER", place="US EAST COAST - WEATHER",
         cert="REPORTED", kind=("img", "storm.webp"), banner="4,200+ FLIGHTS DELAYED",
         headline="Nor'easter slams East Coast",
         body="New Jersey declared an emergency from 6pm Wednesday. "
              "(Reuters)"),
    dict(num=11, kicker="494/7 vs 91", place="CENTURION - CRICKET",
         cert="CONFIRMED", kind=("img", "cricket.webp"), banner="LEAD: 403 RUNS",
         headline="South Africa 494/7 lead Bangladesh by 403",
         body="Bangladesh were bowled out for 91 on day one at Centurion. "
              "(LiveScore)"),
    dict(num=12, kicker="STOXX CLOSE", place="FRANKFURT - MARKETS",
         cert="REPORTED", kind=("chart", "stoxx"), banner="-1.06%",
         headline="European shares end lower: Stoxx 600 falls 1.06%",
         body="The index closed at 626.03 as banks and tech fell. (Dow Jones)"),
    dict(num=13, kicker="SENSEX CLOSE", place="MUMBAI - MARKETS",
         cert="REPORTED", kind=("chart", "sensex"), banner="+1.82%",
         headline="Sensex jumps 1,502 points to close at 83,938",
         body="Mumbai defied the rout; the Nifty rose 1.85%. (Moneycontrol)"),
]

# (num, bold lead-in, rest) - lead-ins print bold like the v8 ALSO list.
ALSO = [
    (14, "Khartoum:", " Sudan rejects Ethiopia's offer to host Sudan talks (Reuters)"),
    (15, "Athens:", " Greeks strike nationwide over wages, 3rd walkout in weeks"),
    (16, "London:", " CMA says remedies could clear $25bn AkzoNobel-Axalta merger"),
    (17, "Madrid:", " Spain votes Nov 29; 368 enquiries chase each Catalan home"),
    (18, "Rafah:", " Gaza aid-worker toll reaches 600, incl. 397 UNRWA staff (OCHA)"),
    (19, "Hodeidah:", " Saudi-led coalition strikes port; Houthis threaten ports"),
    (20, "Samara:", " Kyiv strikes two Russian oil refineries, Kyiv says [CLAIM]"),
    (21, "Hormuz:", " Iran warns ships off unauthorised routes [CLAIM] (Gulf News)"),
    (22, "Ras Tanura:", " Saudi defences intercept 4 drones, Houthis claim [CLAIM]"),
    (23, "Seoul:", " births jump 12.2% in September; Q3 fertility rate 0.90"),
    (24, "Tokyo:", " 1 in 5 firms to cut graduate clerical hiring over AI (Kyodo)"),
    (25, "Hong Kong:", " Wang Fuk Court survivors mourn 168 dead, a year on"),
    (26, "India:", " AI funding hits $1.6bn in 9 months, nearly double [CLAIM]"),
    (27, "Dakar:", " CAS reinstates Senegal as AFCON champions; Morocco to appeal"),
    (28, "Abuja:", " Nigeria holds its rate at 23%; Dangote allotment cleared"),
    (29, "Kampala:", " Uganda gold exports more than double to $8.9bn (Reuters)"),
    (30, "Bamako:", " Sahel insurgents fly FPV drones costing a few hundred dollars"),
    (31, "Canberra:", " Australia apologises to LGBTQ veterans in parliament"),
    (32, "Washington:", " core PCE +0.3% m/m, 3.3% y/y, highest since Nov 2023 (BEA)"),
    (33, "New York:", " Dow +0.33% to 50,183 at the close; S&P -0.25%, Nasdaq -0.62%"),
    (34, "Iowa:", " Army blasts 9,500lb of lead azide; zero airborne lead found (CNN)"),
    (35, "Paris:", " PSG held 2-2 by Roma; holders' perfect UCL run ends (Reports)"),
    (36, "Geneva:", " Gukesh draws Sindarov in Game 1 of the world title match"),
]

DATE_CHECK = ("Every numbered story happened, or was first reported, on Wednesday "
              "25 November 2026. Left out as earlier news: Monday's Nvidia-led rally, "
              "Tuesday's US consumer-confidence jump to 103.3 and Real Madrid's 5-1 "
              "win over PSV (both 24 Nov). Stories 20-22 and 26 are one side's claim.")
LEGEND = ("REPORTED = carried by wires or officials  -  OFFICIAL = an authority's own "
          "word  -  CLAIM = one side says  -  CONFIRMED = result verified  -  "
          "Sources: Reuters, AP, AFP, Al Jazeera, Destatis, ABS, NOAA, as tagged")

MAP_ROWS = [
    "            #####  ##           ##########  #####                      ",
    "    #############  #####     ################  #######     ##########  ",
    "   ###############  ###     ####################  #######   ########## ",
    "    #############           #####################  #####     ########  ",
    "     ##########              ####################            ######    ",
    "      ########                ##################              ####     ",
    "       ######                  ################                ##      ",
    "        ####                    ##############                             ",
    "         ##                      ############            ##              ",
    "                                  ##########            ####             ",
    "                                   ########            ########          ",
    "                                    ######              ######     ##    ",
    "                                     ####                ####       ##   ",
    "                                     ##                                  ",
]

PINS_LONLAT = {
    1: (100.3, 39.9),
    2: (127.0, 37.6),
    3: (34.3, 31.4),
    4: (30.5, 50.4),
    5: (13.4, 52.5),
    6: (149.1, -35.3),
    7: (106.8, -6.6),
    8: (151.2, -33.9),
    9: (-77.0, 38.9),
    10: (-74.0, 40.7),
    11: (28.2, -25.9),
    12: (8.7, 50.1),
    13: (72.9, 19.1),
}
