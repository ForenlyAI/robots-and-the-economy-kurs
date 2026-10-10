"""Week 2 · Measuring the Economy — Lessons 2.1 to 2.4.
  python hafta2.py   ->  ekran/2.x/*.txt + *.png, OLCUMLER.json (d2_*)
Official series (veri/resmi, downloaded 2026-10-08): FRED GDP, GDPC1, GDPDEF, UNRATE, CPIAUCSL; World Bank (Türkiye) unemployment and
inflation. The cafe's sales, prices and the small town are EXAMPLE values."""
import numpy as np
import matplotlib.pyplot as plt
from ortak import measure, session, figure
from arac import ORANGE, BLUE, GREEN, PURPLE, GREY, INK, RED, official, worldbank, value_at, stamp, box, arrow, blank


def lesson_2_1():
    """GDP: value added of the cafe, the robot as investment, US GDP from FRED."""
    ns = session("2.1", "value-added", """
# EXAMPLE cafe, one year, dollars
sales = 180_000          # EXAMPLE: tea and food sold in a year
bought_inputs = 70_000   # EXAMPLE: tea leaves, milk, bread, power
value_added = sales - bought_inputs
value_added
robot = 60_000           # EXAMPLE: a new robot bought this year
# GDP by spending counts the robot as investment (I), the tea as consumption (C)
C, I = sales, robot
C + I
from arac import official
dates, gdp = official("GDP")             # FRED: billions of dollars, yearly rate
str(dates[-1]), gdp[-1]
""")
    d, g = official("GDP")
    m = d >= np.datetime64("2000-01-01")
    fig, ax = plt.subplots()
    ax.plot(d[m], g[m] / 1000, color=BLUE)
    ax.set_ylabel("trillions of dollars (yearly rate)"); ax.set_xlabel("quarter")
    ax.set_title("US nominal GDP, quarterly, seasonally adjusted annual rate")
    ax.text(0.02, 0.95, f"latest quarter {str(d[-1])[:7]}: {g[-1] / 1000:.2f} trillion dollars", transform=ax.transAxes, ha="left", va="top", fontsize=22, color=BLUE)
    stamp(ax, "Source: BEA via FRED, series GDP", GREEN)
    figure("2.1", "us-gdp")

    fig, ax = blank("Circular flow: where the cafe and the robot fit")
    box(ax, 0.05, 0.38, 0.25, 0.24, "households\n(customers,\nworkers)", BLUE)
    box(ax, 0.70, 0.38, 0.25, 0.24, "firms\n(the cafe,\nthe robot maker)", GREEN)
    arrow(ax, (0.32, 0.70), (0.68, 0.70), INK, label="spending on tea: C", off=(0, 0.06))
    arrow(ax, (0.68, 0.30), (0.32, 0.30), INK, label="wages, rent, profit: income", off=(0, -0.06))
    arrow(ax, (0.83, 0.86), (0.83, 0.64), ORANGE, label="", off=(0, 0))
    ax.text(0.83, 0.90, "the cafe buys a robot: I", ha="center", fontsize=24, color=ORANGE, weight="bold")
    ax.text(0.5, 0.08, "GDP = C + I + G + net exports  =  total income", ha="center", fontsize=26)
    figure("2.1", "circular-flow")
    measure(d2_1_sales=ns["sales"], d2_1_inputs=ns["bought_inputs"], d2_1_value_added=ns["value_added"], d2_1_robot=ns["robot"],
            d2_1_c_plus_i=ns["C"] + ns["I"], d2_1_gdp_last_date=str(d[-1]), d2_1_gdp_last_billion=float(g[-1]))


def lesson_2_2():
    """Unemployment: the rate, the three types, technological unemployment; US and Türkiye."""
    ns = session("2.2", "unemployment-rate", """
# EXAMPLE small town
employed, unemployed = 9_400, 600                # EXAMPLE small town
labor_force = employed + unemployed
round(100 * unemployed / labor_force, 1)           # unemployment rate, %
# 50 waiters lose their jobs to robots and look for other work
round(100 * (unemployed + 50) / labor_force, 1)
from arac import official, worldbank
d, u = official("UNRATE")                          # FRED / BLS, %
str(d[-1]), u[-1]
years, tur = worldbank("SL.UEM.TOTL.ZS")           # World Bank, Türkiye, %
int(years[-1]), round(tur[-1], 1)
""")
    d, u = official("UNRATE")
    y, tr = worldbank("SL.UEM.TOTL.ZS")
    m = d >= np.datetime64("2000-01-01")
    fig, ax = plt.subplots()
    ax.plot(d[m], u[m], color=BLUE, label="United States, monthly (BLS via FRED, UNRATE)")
    ax.plot([np.datetime64(f"{k}-07-01") for k in y], tr, "o-", color=ORANGE, label="Türkiye, yearly (World Bank, modelled ILO estimate)")
    ax.set_ylabel("unemployment rate (%)"); ax.set_ylim(0, 16); ax.legend(loc="upper left")
    ax.set_title("Unemployment rate: official series")
    figure("2.2", "unemployment")

    fig, ax = blank("Three types of unemployment, and where robots fit")
    box(ax, 0.02, 0.55, 0.30, 0.30, "frictional\nbetween two jobs,\nstill searching", BLUE, 23)
    box(ax, 0.35, 0.55, 0.30, 0.30, "structural\nskills do not match\nthe jobs: includes\ntechnological", ORANGE, 23)
    box(ax, 0.68, 0.55, 0.30, 0.30, "cyclical\nspending falls\nin a recession", PURPLE, 23)
    ax.text(0.5, 0.42, "natural rate = frictional + structural", ha="center", fontsize=26)
    ax.text(0.5, 0.18, "View 1: robots replace some tasks and cut local jobs\nView 2: robots also create new tasks and raise demand for other work",
            ha="center", fontsize=24, color=INK, linespacing=1.6)
    figure("2.2", "types")
    measure(d2_2_rate_town=100 * 600 / 10000, d2_2_rate_town_after=100 * 650 / 10000, d2_2_us_last_date=str(d[-1]),
            d2_2_us_last=float(u[-1]), d2_2_tur_year=int(y[-1]), d2_2_tur_last=float(tr[-1]))


def lesson_2_3():
    """Inflation: a cafe price index (EXAMPLE basket) and official CPI inflation."""
    ns = session("2.3", "price-index", """
# EXAMPLE basket of one customer: quantity, price last year, price this year (lira)
basket = {"tea": (10, 10.0, 12.0), "simit": (4, 15.0, 18.0),   # EXAMPLE
          "coffee": (2, 60.0, 66.0)}     # quantity, old price, new price
cost_base = sum(q * p0 for q, p0, p1 in basket.values())
cost_now = sum(q * p1 for q, p0, p1 in basket.values())
cost_base, cost_now
index_now = 100 * cost_now / cost_base
round(index_now, 1)                      # base year = 100
round(index_now - 100, 1)                # inflation rate, %
from arac import official, value_at, worldbank
d, cpi = official("CPIAUCSL")            # FRED / BLS, index 1982-84 = 100
us = 100 * (value_at(d, cpi, "2026-08-01") / value_at(d, cpi, "2025-08-01") - 1)
round(us, 1)                             # US, August 2025 to August 2026, %
y, tur = worldbank("FP.CPI.TOTL.ZG")
int(y[-1]), round(tur[-1], 1)            # Türkiye, consumer prices, %
""")
    d, cpi = official("CPIAUCSL")
    yoy = 100 * (cpi[12:] / cpi[:-12] - 1); dd = d[12:]
    m = dd >= np.datetime64("2000-01-01")
    y, tr = worldbank("FP.CPI.TOTL.ZG")
    fig, (a1, a2) = plt.subplots(1, 2, gridspec_kw=dict(width_ratios=[1.6, 1]))
    a1.plot(dd[m], yoy[m], color=BLUE); a1.axhline(0, color=GREY, lw=1.5)
    a1.set_title("US CPI, change from 12 months earlier (%)", fontsize=22); a1.set_ylabel("%")
    a1.text(0.02, 0.95, "BLS via FRED, CPIAUCSL", transform=a1.transAxes, fontsize=18, color=GREEN, va="top")
    a2.bar([str(k) for k in y], tr, color=ORANGE)
    for k, v in zip(y, tr):
        a2.text(str(k), v + 1.5, f"{v:.1f}", ha="center", fontsize=17)
    a2.set_title("Türkiye, consumer prices (% per year)", fontsize=22); a2.tick_params(axis="x", labelsize=16, rotation=45)
    a2.set_ylim(0, 85)
    a2.text(0.02, 0.95, "World Bank, FP.CPI.TOTL.ZG", transform=a2.transAxes, fontsize=18, color=GREEN, va="top")
    figure("2.3", "inflation")
    measure(d2_3_cost_base=ns["cost_base"], d2_3_cost_now=ns["cost_now"], d2_3_index=ns["index_now"], d2_3_inflation_basket=ns["index_now"] - 100,
            d2_3_us_cpi_yoy_aug2026=ns["us"], d2_3_tur_year=int(y[-1]), d2_3_tur_inflation=float(tr[-1]))


def lesson_2_4():
    """Real versus nominal: the GDP deflator from FRED, real growth, the cafe's sales."""
    ns = session("2.4", "real-and-nominal", """
from arac import official, value_at
d, nominal = official("GDP")          # billions of current dollars
_, real = official("GDPC1")           # billions of chained 2017 dollars
_, deflator = official("GDPDEF")      # index, 2017 = 100
q = "2026-04-01"
round(100 * value_at(d, nominal, q) / value_at(d, real, q), 1), value_at(d, deflator, q)
nominal_growth = 100 * (value_at(d, nominal, q) / value_at(d, nominal, "2025-04-01") - 1)
real_growth = 100 * (value_at(d, real, q) / value_at(d, real, "2025-04-01") - 1)
round(nominal_growth, 1), round(real_growth, 1)
# EXAMPLE cafe: sales rise from 180,000 to 216,000 lira, prices rise 25 %
round(100 * (216_000 / 1.25 / 180_000 - 1), 1)  # EXAMPLE cafe: real change, %
""")
    d, real = official("GDPC1")
    g = 100 * (real[4:] / real[:-4] - 1); dd = d[4:]
    m = dd >= np.datetime64("2000-01-01")
    fig, ax = plt.subplots()
    ax.bar(dd[m], g[m], width=80, color=np.where(g[m] < 0, RED, BLUE))
    ax.axhline(0, color=INK, lw=1.5)
    ax.set_ylabel("real GDP, change from a year earlier (%)"); ax.set_xlabel("quarter")
    ax.set_title("Business cycle: US real GDP growth (red = shrinking)"); ax.set_ylim(-9, 14)
    ax.text(0.99, 0.03, "Source: BEA via FRED, series GDPC1", transform=ax.transAxes, ha="right", va="bottom", fontsize=19, color=GREEN,
            weight="bold", bbox=dict(fc="#ffffff", ec=GREEN, boxstyle="round,pad=0.3"))
    figure("2.4", "business-cycle")
    measure(d2_4_quarter="2026-04-01", d2_4_deflator_computed=100 * value_at(d, official("GDP")[1], "2026-04-01") / value_at(d, real, "2026-04-01"),
            d2_4_deflator_fred=value_at(*official("GDPDEF"), "2026-04-01"), d2_4_nominal_growth=ns["nominal_growth"],
            d2_4_real_growth=ns["real_growth"], d2_4_cafe_real_change=100 * (216000 / 1.25 / 180000 - 1))


if __name__ == "__main__":
    lesson_2_1(); lesson_2_2(); lesson_2_3(); lesson_2_4()
