"""Robots and the Economy — shared numbers and drawing helpers.

Two kinds of numbers are used in the lessons:
  1. From the SIMULATION RECORDING (veri/cay_servisi_kaydi.csv): how long one serve takes, how far the cup moves.
     serve_stats() computes them. The recording is not a measurement of a real robot.
  2. From OFFICIAL SOURCES (veri/resmi/*.csv, downloaded 2026-10-08, see kaynaklar.py): FRED series (US data from BLS and BEA,
     Federal Reserve) and World Bank series for Türkiye. official() and worldbank() read them.
Every other number (prices, wages, the cafe's sales, model curves) is an EXAMPLE value and is defined in EX below."""
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from ortak import LAB, recording, smooth

ORANGE, BLUE, GREEN, PURPLE, GREY, INK, RED = "#C2410C", "#1D4ED8", "#0F766E", "#7E22CE", "#6B7280", "#111111", "#B91C1C"
SIM = "simulation recording"
MOVING_SPEED = 0.05        # m/s: smoothed horizontal cup speed above this = the cup is moving

# EXAMPLE values (not from the recording, not from an official table)
EX = dict(
    hours_per_day=8,               # opening hours used in the PPC
    worker_serves_per_hour=40,     # a waiter
    worker_brews_per_hour=60,      # a waiter brewing tea
    robot_brews_per_hour=20,       # the robot brewing tea
    wage_per_hour=10.0,            # dollars
    robot_price=60000.0,           # dollars
    robot_upkeep=3000.0,           # dollars per year
    robot_life_years=5,
    serves_needed_per_day=200,
    days_per_year=360,
    mpc=0.8,
)


def serve_stats(rec=None):
    """Numbers of one serve in the recording: duration (s), serves per hour if every serve took this long,
    share of time the cup moves, time the cup moves (s), straight-line distance from start to end (m)."""
    rec = rec or recording()
    t = rec["t"]
    p = smooth(np.column_stack([rec["cup_x"], rec["cup_y"]]))
    v = np.gradient(p, t, axis=0)
    moving = np.hypot(v[:, 0], v[:, 1]) > MOVING_SPEED
    dt = float(t[1] - t[0])
    duration = float(t[-1])
    return dict(duration_s=duration, serves_per_hour=3600.0 / duration, moving_share=float(moving.mean()),
                moving_s=float(moving.sum() * dt), distance_m=float(np.hypot(rec["cup_x"][-1] - rec["cup_x"][0],
                                                                              rec["cup_y"][-1] - rec["cup_y"][0])),
                speed=np.hypot(v[:, 0], v[:, 1]), moving=moving)


def official(series):
    """A FRED series as (dates as numpy datetime64[D], values). File: veri/resmi/fred_<series>.csv"""
    d, v = [], []
    with open(LAB / f"veri/resmi/fred_{series}.csv") as fh:
        for row in csv.DictReader(fh):
            if row[series] not in ("", "."):
                d.append(row["observation_date"]); v.append(float(row[series]))
    return np.array(d, dtype="datetime64[D]"), np.array(v)


def worldbank(code):
    """A World Bank series for Türkiye as (years, values). File: veri/resmi/worldbank_TUR_<code>.csv"""
    y, v = [], []
    with open(LAB / f"veri/resmi/worldbank_TUR_{code}.csv") as fh:
        for row in csv.DictReader(fh):
            y.append(int(row["year"])); v.append(float(row["value"]))
    return np.array(y), np.array(v)


def value_at(dates, values, day):
    """Value of a series on a given date (exact match)."""
    i = np.where(dates == np.datetime64(day))[0]
    assert len(i) == 1, day
    return float(values[i[0]])


def box(ax, x, y, w, h, text, color, size=24, ink="#ffffff"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03", fc=color, ec="none"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=ink, fontsize=size, linespacing=1.4)


def arrow(ax, p, q, color=INK, lw=4, label=None, off=(0, 0), size=22):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=30, shrinkA=0, shrinkB=0))
    if label:
        ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], label, color=color, fontsize=size, weight="bold",
                ha="center", va="center")


def blank(title):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_title(title)
    return fig, ax


def stamp(ax, text, color=ORANGE):
    """Small label in the top-right corner, for 'EXAMPLE' or the source of a series."""
    ax.text(0.99, 0.98, text, transform=ax.transAxes, ha="right", va="top", fontsize=19, color=color, weight="bold",
            bbox=dict(fc="#ffffff", ec=color, boxstyle="round,pad=0.3"))
