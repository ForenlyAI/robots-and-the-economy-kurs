# Robots and the Economy — course files

These are the lab files of the **Robots and the Economy** course on Forenly AI Academy. Every Python session, graph and number you see on the screen in the lessons was produced by these scripts.

You do not need to write a program to follow the course. The files are for students who want to repeat the calculations on their own computer and try other numbers.

## What you need

- **Python 3.10 or newer**, `numpy` (2.0 or newer) and `matplotlib`. All of them are free.
- Install: `python -m pip install -r requirements.txt`
- If you do not want to install anything, upload this folder to a notebook that runs in the browser (for example Google Colab) and run the same scripts there.

## How to run

1. Download this repository (Code → Download ZIP) and open a terminal in the folder.
2. Run the weeks in order: `python hafta1.py`, `python hafta2.py`, `python hafta3.py`, `python hafta4.py`. (`hafta` means "week".)
3. The scripts write figures (`.png`) and Python session records (`.txt`) to `ekran/<lesson>/`, and the measured numbers to `OLCUMLER.json`. (`ekran` means "screen", `OLCUMLER` means "measurements".)
4. Optional: `python komut_ciz.py` draws the session records as images, as in the lessons (needs Pillow).

## Compare your results

`beklenen/OLCUMLER.json` holds the numbers our team measured in the run of 2026-10-08. `beklenen/ekran/` holds the figures and session records of the same run. (`beklenen` means "expected".) If your numbers match these, your setup works. On another computer a figure can differ by a few pixels and an unrounded number can differ in its last digits; that is normal.

## Files

| File | Content |
|---|---|
| `ortak.py` | Shared tools: load the recording, save sessions, figures and measurements |
| `arac.py` | Serve statistics from the recording, readers for the official series, drawing helpers |
| `kaynaklar.py` | The course document (AP Macroeconomics CED), the official data series, the IFR figures and the two research papers, with how each was checked |
| `hafta1.py` | Week 1 · Basic Economic Concepts: opportunity cost, production possibilities, comparative advantage, supply and demand |
| `hafta2.py` | Week 2 · Measuring the Economy: GDP, unemployment, price indices and inflation, real and nominal |
| `hafta3.py` | Week 3 · National Income and Policy: AD–AS, the spending multiplier, fiscal policy, an automation shock |
| `hafta4.py` | Week 4 · Money, Growth and Trade: interest rates, net present value, productivity growth, exchange rates |
| `komut_ciz.py` | Draws session records as images (optional) |
| `veri/cay_servisi_kaydi.csv` | The simulation recording of one serve: time, arm joint angles, elbow velocity, cup position × 5666 samples (50 per second); the course uses only time and cup position |
| `veri/resmi/` | Official series downloaded on 2026-10-08: FRED (GDP, real GDP, GDP deflator, unemployment rate, CPI, federal funds rate, labour productivity) and World Bank (Türkiye inflation, GDP growth, unemployment) |

## About the data

The robot data is a **simulation recording**. It is **not** a measurement of a real robot. It comes from one run of Forenly AI's [cafe project](https://forenly.ai/work/cafe), in which a humanoid robot carries a cup of tea from a counter to a table in simulation.

Country figures come from the official files in `veri/resmi/`. Official series are revised from time to time, so a new download can give slightly different numbers. Numbers that come neither from the recording nor from an official source (the waiter's rates, market lines, the MPC, the robot price, exchange-rate and interest-rate scenarios) are **EXAMPLE** values.

On robots and jobs the course shows two published views and does not take a side. The course is not an official programme of the College Board; the AP topic titles are listed in `kaynaklar.py` only to show where each lesson fits.

## Final project

Write a one-page robot investment analysis for a cafe: the robot's price in lira at two exchange rates, the yearly saving, the net present value at two interest rates and the break-even rate, the effect on productivity, and your recommendation with reasons.
