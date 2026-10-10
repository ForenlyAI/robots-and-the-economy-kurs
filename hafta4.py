"""Week 4 · Money, Growth and Trade — Lessons 4.1 to 4.4.
  python hafta4.py   ->  ekran/4.x/*.txt + *.png, OLCUMLER.json (d4_*)
Official series (veri/resmi, downloaded 2026-10-08): FRED FEDFUNDS, CPIAUCSL, OPHNFB; IFR World Robotics 2025 press release figures
(kaynaklar.py). Robot price, wage, upkeep, money demand, loanable funds curves and exchange rates are EXAMPLE values."""
import numpy as np
import matplotlib.pyplot as plt
from ortak import measure, session, figure
from arac import ORANGE, BLUE, GREEN, PURPLE, GREY, INK, RED, EX, serve_stats, official, value_at, stamp
from kaynaklar import IFR_2025


def npv(rate, price, net, years):
    return -price + sum(net / (1 + rate) ** k for k in range(1, years + 1))


def lesson_4_1():
    """Money and interest rates: nominal and real rate, the money market."""
    ns = session("4.1", "real-interest-rate", """
from arac import official, value_at
d, ff = official("FEDFUNDS")                 # FRED: effective federal funds rate, %
str(d[-1]), ff[-1]
dc, cpi = official("CPIAUCSL")
inflation = 100 * (value_at(dc, cpi, "2026-08-01") / value_at(dc, cpi, "2025-08-01") - 1)
round(inflation, 1)
real_rate = ff[-1] - inflation               # real rate = nominal rate - inflation
round(real_rate, 1)
# EXAMPLE money market: demand for money M = 1000 - 100 * i, supply fixed by the central bank
i_eq = lambda supply: (1000 - supply) / 100  # EXAMPLE money market
i_eq(600), i_eq(650)                         # more money supply, lower interest rate
""")
    d, ff = official("FEDFUNDS"); dc, cpi = official("CPIAUCSL")
    yoy = 100 * (cpi[12:] / cpi[:-12] - 1); dy = dc[12:]
    fig, ax = plt.subplots()
    m = d >= np.datetime64("2000-01-01"); my = dy >= np.datetime64("2000-01-01")
    ax.plot(d[m], ff[m], color=BLUE, label="nominal: effective federal funds rate (FEDFUNDS)")
    ax.plot(dy[my], yoy[my], color=ORANGE, label="inflation: CPI change from a year earlier (CPIAUCSL)")
    ax.axhline(0, color=GREY, lw=1.5); ax.set_ylabel("% per year"); ax.legend(loc="upper right", fontsize=19)
    ax.set_title("When inflation is above the nominal rate, the real rate is negative")
    ax.text(0.01, 0.03, "Sources: Federal Reserve and BLS via FRED", transform=ax.transAxes, fontsize=19, color=GREEN)
    figure("4.1", "nominal-and-inflation")

    M = np.linspace(300, 900, 50)
    fig, ax = plt.subplots()
    ax.plot(M, (1000 - M) / 100, color=BLUE, label="money demand")
    ax.axvline(600, color=ORANGE, lw=3, label="money supply"); ax.axvline(650, color=ORANGE, lw=3, ls="--", label="money supply after the central bank buys bonds")
    ax.plot(600, 4, "o", color=INK, ms=14); ax.plot(650, 3.5, "o", color=PURPLE, ms=14)
    ax.text(590, 3.6, "4.0 %", fontsize=24, ha="right"); ax.text(660, 3.6, "3.5 %", fontsize=24, color=PURPLE)
    ax.set_xlabel("quantity of money"); ax.set_ylabel("nominal interest rate (%)"); ax.set_ylim(0, 7.5)
    ax.set_title("The money market")
    stamp(ax, "EXAMPLE model", ORANGE); ax.legend(loc="upper center", fontsize=19)
    figure("4.1", "money-market")
    measure(d4_1_ff_date=str(d[-1]), d4_1_ff=float(ff[-1]), d4_1_inflation=ns["inflation"], d4_1_real_rate=ns["real_rate"],
            d4_1_i_600=4.0, d4_1_i_650=3.5)


def lesson_4_2():
    """Should the cafe borrow to buy a robot? Net present value at different interest rates; loanable funds."""
    sph = round(serve_stats()["serves_per_hour"], 1)
    ns = session("4.2", "robot-investment", f"""
price, upkeep, life = 60_000, 3_000, 5      # EXAMPLE dollars, dollars per year, years
serves_per_year = 200 * 360                 # EXAMPLE serves the cafe needs
labor_cost_per_serve = 10 / 40              # EXAMPLE wage 10 per hour, 40 serves per hour
saving = serves_per_year * labor_cost_per_serve - upkeep
saving                                      # net saving per year
round({sph} * 10 * 360)                     # most the robot could serve in a year, 10 hours a day
npv = lambda r: -price + sum(saving / (1 + r) ** k for k in range(1, life + 1))
[round(npv(r)) for r in (0.03, 0.05, 0.08, 0.10)]
round(price / saving, 1)                    # payback in years, no interest
""")
    saving = ns["saving"]; price = ns["price"]; life = ns["life"]
    rates = np.linspace(0, 0.14, 141)
    vals = np.array([npv(r, price, saving, life) for r in rates])
    be = float(rates[np.argmin(np.abs(vals))])
    fig, ax = plt.subplots()
    ax.plot(100 * rates, vals / 1000, color=BLUE); ax.axhline(0, color=INK, lw=1.5)
    ax.fill_between(100 * rates, vals / 1000, 0, where=vals > 0, color=GREEN, alpha=0.2)
    ax.fill_between(100 * rates, vals / 1000, 0, where=vals < 0, color=RED, alpha=0.2)
    ax.axvline(100 * be, color=PURPLE, ls="--", lw=2.5); ax.text(100 * be + 0.2, 10, f"break-even ≈ {100 * be:.1f} %", fontsize=24, color=PURPLE)
    ax.text(1, -8, "buy: value of savings > price", fontsize=22, color=GREEN); ax.text(9.5, 8, "do not buy", fontsize=22, color=RED)
    ax.set_xlabel("real interest rate (% per year)"); ax.set_ylabel("net present value (thousand dollars)")
    ax.set_title("The robot pays off only if the interest rate is low enough")
    stamp(ax, "EXAMPLE values", ORANGE)
    figure("4.2", "npv")

    Q = np.linspace(100, 900, 50)
    fig, ax = plt.subplots()
    ax.plot(Q, 10 - Q / 100, color=BLUE, label="demand for loans (investment)")
    ax.plot(Q, Q / 100 - 2, color=ORANGE, label="supply of loans (saving)")
    ax.plot(Q, Q / 100 - 3, color=ORANGE, ls="--", label="supply after saving rises")
    ax.plot(600, 4, "o", color=INK, ms=14); ax.plot(650, 3.5, "o", color=PURPLE, ms=14)
    ax.text(560, 5.2, "4.0 %", fontsize=24, ha="center"); ax.text(690, 2.4, "3.5 %", fontsize=24, ha="center", color=PURPLE)
    ax.set_xlabel("quantity of loanable funds"); ax.set_ylabel("real interest rate (%)"); ax.set_ylim(0, 9)
    ax.set_title("Loanable funds: more saving lowers the real rate and raises investment")
    stamp(ax, "EXAMPLE model", ORANGE); ax.legend(loc="upper center", fontsize=19)
    figure("4.2", "loanable-funds")
    measure(d4_2_price=price, d4_2_upkeep=ns["upkeep"], d4_2_life=life, d4_2_serves_per_year=ns["serves_per_year"],
            d4_2_labor_cost_per_serve=ns["labor_cost_per_serve"], d4_2_saving=saving, d4_2_robot_capacity_year=round(sph * 10 * 360),
            d4_2_npv=[round(npv(r, price, saving, life)) for r in (0.03, 0.05, 0.08, 0.10)], d4_2_breakeven_pct=100 * be,
            d4_2_payback_years=price / saving)


def lesson_4_3():
    """Productivity and long-run growth: output per hour from FRED, rule of 70, robot stock from IFR."""
    ns = session("4.3", "productivity-growth", """
from arac import official, value_at
d, prod = official("OPHNFB")       # FRED / BLS: output per hour, nonfarm business, index 2017 = 100
str(d[-1]), prod[-1]
start, end = value_at(d, prod, "2016-04-01"), value_at(d, prod, "2026-04-01")
growth = 100 * ((end / start) ** (1 / 10) - 1)
round(growth, 2)                   # average % per year over 10 years
round(70 / growth)                 # rule of 70: years to double
round(70 / 3)                      # at 3 % per year
from kaynaklar import IFR_2025
IFR_2025["operational_stock_2024"], IFR_2025["stock_growth_pct"]
""")
    d, prod = official("OPHNFB")
    m = d >= np.datetime64("2000-01-01")
    fig, ax = plt.subplots()
    ax.plot(d[m], prod[m], color=BLUE)
    ax.set_ylabel("index, 2017 = 100"); ax.set_xlabel("quarter")
    ax.set_title("US labor productivity: output per hour, nonfarm business sector")
    stamp(ax, "Source: BLS via FRED, series OPHNFB", GREEN)
    figure("4.3", "productivity")
    measure(d4_3_last_date=str(d[-1]), d4_3_last_index=float(prod[-1]), d4_3_growth_10y=ns["growth"], d4_3_double_years=70 / ns["growth"],
            d4_3_double_years_3pct=70 / 3, d4_3_ifr_stock=IFR_2025["operational_stock_2024"], d4_3_ifr_stock_growth=IFR_2025["stock_growth_pct"])


def lesson_4_4():
    """Trade and exchange rates: a robot priced in dollars, paid in lira; world robot installations from IFR."""
    ns = session("4.4", "exchange-rate", """
price_usd = 60_000                  # EXAMPLE robot price in dollars
for rate in (40, 45):               # EXAMPLE lira per dollar
    print(rate, price_usd * rate)   # cost in lira
round(100 * (45 / 40 - 1), 1)       # lira weaker: robot costs this % more in lira
# a tea exported for 2 dollars: lira received per cup
2 * 40, 2 * 45
from kaynaklar import IFR_2025
IFR_2025["installations_2024"], IFR_2025["china_installations_2024"], IFR_2025["china_share_pct"]
""")
    fig, (a1, a2) = plt.subplots(1, 2)
    a1.bar(["40 lira\nper dollar", "45 lira\nper dollar"], [2.40, 2.70], color=[BLUE, ORANGE])
    for i, v in enumerate([2.40, 2.70]):
        a1.text(i, v + 0.05, f"{v:.2f} million lira", ha="center", fontsize=22)
    a1.set_ylim(0, 3.2); a1.set_title("Robot of 60,000 dollars, cost in lira", fontsize=22)
    a1.text(0.02, 0.95, "EXAMPLE values", transform=a1.transAxes, fontsize=19, color=ORANGE, va="top", weight="bold")
    k = IFR_2025
    a2.pie([k["china_installations_2024"], k["installations_2024"] - k["china_installations_2024"]],
           labels=[f"China\n{k['china_installations_2024']:,}", f"rest of the world\n{k['installations_2024'] - k['china_installations_2024']:,}"],
           colors=[PURPLE, GREY], startangle=90, textprops=dict(fontsize=20), wedgeprops=dict(width=0.45))
    a2.set_title(f"Industrial robots installed in 2024: {k['installations_2024']:,}", fontsize=22)
    a2.text(0, -1.45, "Source: IFR, World Robotics 2025 press release", ha="center", fontsize=18, color=GREEN)
    figure("4.4", "exchange-and-trade")
    measure(d4_4_price_usd=60000, d4_4_cost_40=2400000, d4_4_cost_45=2700000, d4_4_pct=100 * (45 / 40 - 1), d4_4_export_lira=[80, 90],
            d4_4_ifr_installations=k["installations_2024"], d4_4_ifr_china=k["china_installations_2024"], d4_4_ifr_china_share=k["china_share_pct"])


if __name__ == "__main__":
    lesson_4_1(); lesson_4_2(); lesson_4_3(); lesson_4_4()
