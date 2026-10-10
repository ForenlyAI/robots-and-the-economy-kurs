"""Week 3 · National Income and Policy — Lessons 3.1 to 3.4.
  python hafta3.py   ->  ekran/3.x/*.txt + *.png, OLCUMLER.json (d3_*)
All curves, the MPC, the gap sizes and the robot spending are EXAMPLE values; the robot's serve time comes from the simulation recording."""
import numpy as np
import matplotlib.pyplot as plt
from ortak import measure, session, figure
from arac import ORANGE, BLUE, GREEN, PURPLE, GREY, INK, RED, EX, serve_stats, stamp

Y = np.linspace(600, 1000, 50)


def lesson_3_1():
    """AD-AS: equilibrium, then more investment in robots shifts AD right."""
    ns = session("3.1", "ad-as", """
# EXAMPLE linear model: output Y in billions, price level P
AD = lambda P, shift=0: 1000 + shift - 2 * P   # EXAMPLE model
SRAS = lambda P: 400 + 4 * P
LRAS = 800                              # full-employment output
P0 = (1000 - 400) / (2 + 4)
P0, AD(P0)                              # short-run equilibrium
# firms buy robots: investment rises, AD shifts right by 60 at every price level
P1 = (1000 + 60 - 400) / (2 + 4)
P1, AD(P1, 60)
AD(P1, 60) - LRAS                       # output above full employment
""")
    P = np.linspace(60, 160, 50)
    fig, ax = plt.subplots()
    ax.plot(1000 - 2 * P, P, color=BLUE, label="AD")
    ax.plot(1060 - 2 * P, P, color=BLUE, ls="--", label="AD after robot investment")
    ax.plot(400 + 4 * P, P, color=ORANGE, label="SRAS")
    ax.axvline(800, color=GREEN, lw=3, label="LRAS (full employment)")
    ax.plot(800, 100, "o", color=INK, ms=14); ax.plot(840, 110, "o", color=PURPLE, ms=14)
    ax.text(745, 103, "E0 (800, 100)", fontsize=22, ha="right"); ax.text(850, 108, "E1 (840, 110)", fontsize=22, color=PURPLE)
    ax.set_xlabel("real output Y"); ax.set_ylabel("price level P"); ax.set_xlim(650, 1000); ax.set_ylim(60, 160)
    ax.legend(loc="upper center"); ax.set_title("AD–AS: more investment pushes output and prices up")
    stamp(ax, "EXAMPLE model", ORANGE)
    figure("3.1", "ad-as-graph")
    measure(d3_1_p0=ns["P0"], d3_1_y0=ns["AD"](ns["P0"]), d3_1_p1=ns["P1"], d3_1_y1=ns["AD"](ns["P1"], 60), d3_1_gap=ns["AD"](ns["P1"], 60) - 800)


def lesson_3_2():
    """The spending multiplier, round by round."""
    ns = session("3.2", "multiplier", """
mpc = 0.8                     # EXAMPLE marginal propensity to consume
multiplier = 1 / (1 - mpc)
round(multiplier, 2)
spend = 60_000                # EXAMPLE: one cafe buys one robot, dollars
rounds = [spend * mpc ** k for k in range(10)]
[round(r) for r in rounds[:4]]
round(sum(rounds))            # after 10 rounds
round(spend * multiplier)     # after all rounds
""")
    r = np.array(ns["rounds"]); c = np.cumsum(r)
    fig, ax = plt.subplots()
    k = np.arange(1, len(r) + 1)
    ax.bar(k, r / 1000, color=ORANGE, label="new spending in this round")
    ax.plot(k, c / 1000, "o-", color=BLUE, label="total so far")
    ax.axhline(300, color=GREEN, ls="--", lw=2.5); ax.text(0.6, 295, "limit: 300", fontsize=22, color=GREEN, ha="left", va="top")
    ax.set_xticks(k); ax.set_xlabel("round of spending"); ax.set_ylabel("thousand dollars"); ax.set_ylim(0, 330)
    ax.legend(loc="center right"); ax.set_title("One robot purchase of 60,000 becomes 300,000 of spending when MPC = 0.8")
    stamp(ax, "EXAMPLE values", ORANGE)
    figure("3.2", "rounds")
    measure(d3_2_mpc=ns["mpc"], d3_2_multiplier=ns["multiplier"], d3_2_spend=ns["spend"], d3_2_first_rounds=[round(x) for x in r[:4]],
            d3_2_ten_rounds=float(c[-1]), d3_2_total=ns["spend"] * ns["multiplier"])


def lesson_3_3():
    """Fiscal policy: closing a recessionary gap with spending or with a tax cut."""
    ns = session("3.3", "fiscal-policy", """
mpc = 0.8                                  # EXAMPLE
gap = 100                                  # EXAMPLE recessionary gap, billions
spending_multiplier = 1 / (1 - mpc)
tax_multiplier = -mpc / (1 - mpc)
round(spending_multiplier, 2), round(tax_multiplier, 2)
round(gap / spending_multiplier, 1)        # extra government spending needed
round(gap / -tax_multiplier, 1)            # tax cut needed
# retraining grants for workers who lost jobs to robots: a spending rise of 20
round(20 * spending_multiplier, 1)
""")
    fig, ax = plt.subplots()
    names = ["government spending\n+20", "tax cut\nof 25"]
    yy = np.arange(2)
    ax.barh(yy + 0.2, [20, 25], 0.38, color=GREY, label="size of the policy")
    ax.barh(yy - 0.2, [100, 100], 0.38, color=GREEN, label="change in real output")
    for i, v in enumerate([20, 25]):
        ax.text(v + 2, i + 0.2, f"{v}", va="center", fontsize=24); ax.text(102, i - 0.2, "100 = the gap", va="center", fontsize=24, color=GREEN)
    ax.set_yticks(yy, names); ax.set_xlabel("billions (EXAMPLE)"); ax.set_xlim(0, 135); ax.legend(loc="center right")
    ax.set_title("Same gap, different tools: spending multiplier 5, tax multiplier −4")
    stamp(ax, "EXAMPLE values", ORANGE)
    figure("3.3", "two-tools")
    measure(d3_3_mpc=ns["mpc"], d3_3_gap=ns["gap"], d3_3_spending_multiplier=ns["spending_multiplier"], d3_3_tax_multiplier=ns["tax_multiplier"],
            d3_3_spending_needed=ns["gap"] / ns["spending_multiplier"], d3_3_tax_cut_needed=ns["gap"] / -ns["tax_multiplier"],
            d3_3_retraining_effect=20 * ns["spending_multiplier"])


def lesson_3_4():
    """An automation shock: productivity rises, SRAS and LRAS shift right."""
    sph = round(serve_stats()["serves_per_hour"], 1)
    ns = session("3.4", "productivity-shock", f"""
waiter_alone = 40                          # EXAMPLE serves per hour
robot = {sph}                              # serves per hour, simulation recording
round(100 * robot / waiter_alone)          # robot output as % of a waiter's
# one waiter plus one robot: serves per worker-hour
round((waiter_alone + robot) / waiter_alone, 2)
# EXAMPLE economy: productivity +5 %, so SRAS and LRAS move right by 5 % of 800
shift = 0.05 * 800                         # EXAMPLE: +5 % of 800
P_new = (1000 - 400 - shift) / (2 + 4)
round(P_new, 2), round(1000 - 2 * P_new, 1), 800 + shift
""")
    P = np.linspace(60, 160, 50)
    fig, ax = plt.subplots()
    ax.plot(1000 - 2 * P, P, color=BLUE, label="AD")
    ax.plot(400 + 4 * P, P, color=ORANGE, label="SRAS before")
    ax.plot(440 + 4 * P, P, color=ORANGE, ls="--", label="SRAS after")
    ax.axvline(800, color=GREEN, lw=3, label="LRAS before"); ax.axvline(840, color=GREEN, lw=3, ls="--", label="LRAS after")
    pn = ns["P_new"]
    ax.plot(800, 100, "o", color=INK, ms=14); ax.plot(1000 - 2 * pn, pn, "o", color=PURPLE, ms=14)
    ax.text(852, 88, f"new short-run point ({1000 - 2 * pn:.0f}, {pn:.1f})", fontsize=22, color=PURPLE)
    ax.set_xlabel("real output Y"); ax.set_ylabel("price level P"); ax.set_xlim(650, 1000); ax.set_ylim(60, 160)
    ax.set_title("Automation as a positive supply shock")
    stamp(ax, "EXAMPLE model", ORANGE); ax.legend(loc="upper center", fontsize=18, ncol=2)
    figure("3.4", "supply-shock")
    measure(d3_4_robot_share_of_waiter=100 * sph / 40, d3_4_team_ratio=(40 + sph) / 40, d3_4_shift=ns["shift"], d3_4_p_new=pn,
            d3_4_y_new=1000 - 2 * pn, d3_4_lras_new=800 + ns["shift"])


if __name__ == "__main__":
    lesson_3_1(); lesson_3_2(); lesson_3_3(); lesson_3_4()
