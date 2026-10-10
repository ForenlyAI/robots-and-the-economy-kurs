"""Week 1 · Basic Economic Concepts — Lessons 1.1 to 1.4 (and the overview figure of the introduction lesson).
  python hafta1.py   ->  ekran/1.x/*.txt + *.png, ekran/0.1/*.png, OLCUMLER.json (d0_*, d1_*)
Serve time comes from the simulation recording. Brewing rates, the waiter's rates and the tea market are EXAMPLE values."""
import numpy as np
import matplotlib.pyplot as plt
from ortak import recording, measure, session, figure
from arac import ORANGE, BLUE, GREEN, PURPLE, GREY, INK, SIM, EX, serve_stats, stamp, box, arrow


def lesson_0_1():
    rec = recording(); s = serve_stats(rec); t = rec["t"]
    fig, (a1, a2) = plt.subplots(2, 1, sharex=True)
    a1.plot(t, rec["cup_z"], color=BLUE); a1.set_ylabel("cup height (m)")
    a1.set_title(f"One serve in the {SIM}: {s['duration_s']:.1f} s")
    a2.plot(t, s["speed"], color=ORANGE); a2.fill_between(t, 0, s["speed"].max() * 1.05, where=s["moving"], color=ORANGE, alpha=0.12)
    a2.set_ylabel("cup speed (m/s)"); a2.set_xlabel("time (s)")
    a2.text(2, s["speed"].max() * 0.85, f"cup moving: {s['moving_s']:.1f} s of {s['duration_s']:.1f} s", fontsize=22, color=ORANGE)
    figure("0.1", "recording-overview")
    measure(d0_duration_s=s["duration_s"], d0_serves_per_hour=s["serves_per_hour"])


def lesson_1_1():
    """Scarcity and opportunity cost: the robot's time is limited; one serve costs time."""
    ns = session("1.1", "serve-time", """
from ortak import recording
from arac import serve_stats
rec = recording()
len(rec["t"]), rec["t"][-1]              # samples, seconds
s = serve_stats(rec)
round(s["duration_s"], 1)                # one serve, seconds
round(s["moving_s"], 1), round(s["moving_share"], 2)
round(s["distance_m"], 2)                # start to end of the cup, metres
serves_per_hour = 3600 / s["duration_s"]
round(serves_per_hour, 1)                # if every serve took this long
round(8 * serves_per_hour)               # serves in an 8-hour day
""")
    s = ns["s"]; sph = ns["serves_per_hour"]
    rec = ns["rec"]; t = rec["t"]
    fig, ax = plt.subplots()
    ax.plot(t, s["speed"], color=ORANGE)
    ax.fill_between(t, 0, 0.45, where=s["moving"], color=ORANGE, alpha=0.12)
    ax.fill_between(t, 0, 0.45, where=~s["moving"], color=GREY, alpha=0.10)
    ax.set_ylim(0, 0.45); ax.set_xlabel("time (s)"); ax.set_ylabel("cup speed (m/s)")
    ax.text(2, 0.40, f"cup still (waiting, lifting, placing): {s['duration_s'] - s['moving_s']:.1f} s", fontsize=22, color=GREY,
            bbox=dict(fc="#ffffff", ec="none"))
    ax.text(2, 0.355, f"cup moving: {s['moving_s']:.1f} s", fontsize=22, color=ORANGE, bbox=dict(fc="#ffffff", ec="none"))
    ax.set_title(f"Every serve uses {s['duration_s']:.1f} s of the robot's time · {SIM}")
    figure("1.1", "time-of-a-serve")

    # opportunity cost of one hour of the robot
    ns = session("1.1", "opportunity-cost", """
brews_per_hour = 20      # EXAMPLE: cups of tea the robot could brew in one hour
serves_per_hour_robot = round(serves_per_hour, 1)
# one hour spent serving gives up one hour of brewing
serves_per_hour_robot, brews_per_hour
cost_of_one_serve = brews_per_hour / serves_per_hour_robot
round(cost_of_one_serve, 2)            # brews given up for one serve
round(1 / cost_of_one_serve, 2)        # serves given up for one brew
""", ns)
    measure(d1_1_samples=len(t), d1_1_duration_s=s["duration_s"], d1_1_moving_s=s["moving_s"], d1_1_moving_share=s["moving_share"],
            d1_1_distance_m=s["distance_m"], d1_1_serves_per_hour=sph, d1_1_serves_per_day=round(8 * sph),
            d1_1_example_robot_brews_per_hour=ns["brews_per_hour"], d1_1_opportunity_cost_serve_in_brews=ns["cost_of_one_serve"],
            d1_1_opportunity_cost_brew_in_serves=1 / ns["cost_of_one_serve"])


def ppc_points(serves_h, brews_h, hours):
    return serves_h * hours, brews_h * hours


def lesson_1_2():
    """Production possibilities curve: robot, waiter, and the cafe with both."""
    sph = round(serve_stats()["serves_per_hour"], 1); H = EX["hours_per_day"]
    rs, rb = ppc_points(sph, EX["robot_brews_per_hour"], H)
    ws, wb = ppc_points(EX["worker_serves_per_hour"], EX["worker_brews_per_hour"], H)
    ns = session("1.2", "ppc-endpoints", f"""
hours = 8                       # EXAMPLE opening hours
robot = {sph} * hours, 20 * hours      # serves (recording), brews (EXAMPLE)
waiter = 40 * hours, 60 * hours        # EXAMPLE
robot, waiter
# the cafe with both: all serving, all brewing
robot[0] + waiter[0], robot[1] + waiter[1]
# point A: 300 serves and 300 brews. Can the waiter alone do it?
need = 300 / 40 + 300 / 60      # hours the waiter would need
need
""")
    fig, ax = plt.subplots()
    ax.plot([0, ws], [wb, 0], color=BLUE, label="waiter alone (EXAMPLE rates)")
    ax.plot([0, ws, ws + rs], [wb + rb, rb, 0], color=GREEN, label="waiter + robot: robot serves first")
    ax.plot([0, rs], [rb, 0], color=ORANGE, label="robot alone (serve time from the recording)")
    ax.plot(300, 300, "o", color=PURPLE, ms=16); ax.text(310, 310, "A (300, 300)", fontsize=22, color=PURPLE)
    ax.plot(150, 150, "o", color=GREY, ms=14); ax.text(20, 185, "B: inside = unused time", fontsize=22, color=GREY, va="center")
    ax.set_xlabel("cups served per day"); ax.set_ylabel("cups of tea brewed per day")
    ax.set_xlim(0, 640); ax.set_ylim(0, 700)
    ax.set_title("Production possibilities of the cafe in one 8-hour day")
    ax.set_ylim(0, 820); ax.legend(loc="upper right")
    ax.text(0.01, 0.98, "rates: EXAMPLE except robot serve time", transform=ax.transAxes, ha="left", va="top", fontsize=19, color=ORANGE,
            weight="bold", bbox=dict(fc="#ffffff", ec=ORANGE, boxstyle="round,pad=0.3"))
    figure("1.2", "ppc")
    measure(d1_2_robot_serves_day=rs, d1_2_robot_brews_day=rb, d1_2_waiter_serves_day=ws, d1_2_waiter_brews_day=wb,
            d1_2_both_serves_day=rs + ws, d1_2_both_brews_day=rb + wb, d1_2_point_a_hours_waiter=ns["need"])


def lesson_1_3():
    """Comparative advantage: opportunity costs and gains from specialising."""
    sph = round(serve_stats()["serves_per_hour"], 1)
    ns = session("1.3", "comparative-advantage", f"""
robot = dict(serve={sph}, brew=20)     # per hour; brew is EXAMPLE
waiter = dict(serve=40, brew=60)       # EXAMPLE
# opportunity cost of one serve, in brews given up
round(robot["brew"] / robot["serve"], 2), round(waiter["brew"] / waiter["serve"], 2)
# opportunity cost of one brew, in serves given up
round(robot["serve"] / robot["brew"], 2), round(waiter["serve"] / waiter["brew"], 2)
# 8 hours each. Plan 1: both split time half and half
s1 = 4 * robot["serve"] + 4 * waiter["serve"]
b1 = 4 * robot["brew"] + 4 * waiter["brew"]
round(s1), round(b1)
# Plan 2: robot only serves, waiter serves 1.6 hours and brews the rest
s2 = 8 * robot["serve"] + 1.6 * waiter["serve"]
b2 = 6.4 * waiter["brew"]
round(s2), round(b2)
""")
    s1, b1, s2, b2 = (ns[k] for k in ("s1", "b1", "s2", "b2"))
    fig, ax = plt.subplots()
    x = np.arange(2); w = 0.35
    ax.bar(x - w / 2, [s1, b1], w, color=GREY, label="Plan 1: both split their time")
    ax.bar(x + w / 2, [s2, b2], w, color=GREEN, label="Plan 2: each does its comparative advantage")
    for i, (a, b) in enumerate(((s1, s2), (b1, b2))):
        ax.text(i - w / 2, a + 6, f"{a:.0f}", ha="center", fontsize=24); ax.text(i + w / 2, b + 6, f"{b:.0f}", ha="center", fontsize=24, color=GREEN)
    ax.set_xticks(x, ["cups served per day", "cups brewed per day"]); ax.set_ylim(0, 480); ax.legend(loc="upper left")
    ax.set_title("Specialising by comparative advantage gives more of both")
    stamp(ax, "rates: EXAMPLE except robot serve time", ORANGE)
    figure("1.3", "gains-from-specialising")
    measure(d1_3_robot_oc_serve=EX["robot_brews_per_hour"] / sph, d1_3_waiter_oc_serve=EX["worker_brews_per_hour"] / EX["worker_serves_per_hour"],
            d1_3_robot_oc_brew=sph / EX["robot_brews_per_hour"], d1_3_waiter_oc_brew=EX["worker_serves_per_hour"] / EX["worker_brews_per_hour"],
            d1_3_plan1=[s1, b1], d1_3_plan2=[s2, b2])


def lesson_1_4():
    """Supply and demand: a robot lowers the cost of serving tea; supply shifts right."""
    ns = session("1.4", "equilibrium", """
import numpy as np
# EXAMPLE tea market of a small town, price in lira per cup, quantity in cups per day
demand = lambda p: 1000 - 40 * p             # EXAMPLE
supply = lambda p: -200 + 80 * p
p0 = np.roots([80 + 40, -(1000 + 200)])[0]   # 1000 - 40p = -200 + 80p
p0, demand(p0)
# robots make serving cheaper: sellers offer 120 more cups at every price
supply_new = lambda p: -80 + 80 * p
p1 = (1000 + 80) / (80 + 40)
p1, demand(p1)
supply_new(10) - demand(10)                  # surplus at the old price
""")
    p0, p1 = float(ns["p0"]), float(ns["p1"])
    q0, q1 = 1000 - 40 * p0, 1000 - 40 * p1
    Q = np.linspace(0, 1000, 50)
    fig, ax = plt.subplots()
    ax.plot(Q, (1000 - Q) / 40, color=BLUE, label="demand")
    ax.plot(Q, (Q + 200) / 80, color=ORANGE, label="supply before")
    ax.plot(Q, (Q + 80) / 80, color=GREEN, label="supply after the robots")
    ax.plot(q0, p0, "o", color=ORANGE, ms=16); ax.plot(q1, p1, "o", color=GREEN, ms=16)
    ax.text(q0 - 30, p0 + 0.6, f"before: {q0:.0f} cups at {p0:.0f} lira", fontsize=22, color=ORANGE, ha="right")
    ax.text(q1 + 25, p1 - 1.1, f"after: {q1:.0f} cups at {p1:.0f} lira", fontsize=22, color=GREEN)
    ax.set_xlabel("cups of tea per day"); ax.set_ylabel("price (lira per cup)"); ax.set_xlim(0, 1000); ax.set_ylim(0, 20)
    ax.set_title("A lower cost of serving shifts supply to the right")
    stamp(ax, "EXAMPLE market", ORANGE); ax.legend(loc="upper center")
    figure("1.4", "supply-shift")
    measure(d1_4_p0=p0, d1_4_q0=q0, d1_4_p1=p1, d1_4_q1=q1, d1_4_surplus_at_old_price=float(ns["supply_new"](10) - ns["demand"](10)))


if __name__ == "__main__":
    lesson_0_1(); lesson_1_1(); lesson_1_2(); lesson_1_3(); lesson_1_4()
