"""Robots and the Economy — sources outside the recording (kayıt dışı kaynaklar).
Every macro number in the lessons comes from one of the official sources below; the files were downloaded on 2026-10-08 and are kept in
veri/resmi/ so that the lab gives the same numbers again. Official series are revised from time to time: a later download can differ.
No source was used that could not be opened and read. Robot and cafe numbers come from the simulation recording or are marked EXAMPLE.
  SYLLABUS : the course document the lessons are mapped to
  DATA     : official data series  ·  PAPERS : research cited for the two views on automation and jobs
  IFR_2025 : figures read from the IFR press release (no data file; numbers copied as printed)
Each entry: yazar (author), yil (year), baslik (title), yer (where), dogrulama (how it was verified)."""

SYLLABUS = dict(
    ap_macro_ced=dict(
        yazar="College Board", yil=2026,
        baslik="AP Macroeconomics Course and Exam Description, Effective Fall 2026",
        yer="https://apcentral.collegeboard.org/media/pdf/ap-macroeconomics-course-and-exam-description.pdf",
        dogrulama="PDF downloaded 2026-10-08 and converted to text; cover reads 'Effective Fall 2026', '© 2026 College Board'. Unit titles "
                  "read: 1 Basic Economic Concepts, 2 Economic Indicators and the Business Cycle, 3 National Income and Price "
                  "Determination, 4 Financial Sector, 5 Long-Run Consequences of Stabilization Policies, 6 Open Economy—International "
                  "Trade and Finance. Topic titles 1.1 to 6.6 read from the unit guides (e.g. 1.2 Opportunity Cost and the Production "
                  "Possibilities Curve (PPC), 3.2 Multipliers, 4.7 The Loanable Funds Market, 5.6 Economic Growth). Exam: Section I 60 "
                  "multiple-choice questions in 70 minutes, Section II 3 free-response questions in 60 minutes."),
)

DATA = dict(
    fred=dict(
        yazar="Federal Reserve Bank of St. Louis, FRED (series from BLS, BEA and the Board of Governors of the Federal Reserve System)",
        yil=2026, baslik="FRED series GDP, GDPC1, GDPDEF, UNRATE, CPIAUCSL, FEDFUNDS, OPHNFB",
        yer="https://fred.stlouisfed.org/graph/fredgraph.csv?id=<series>",
        dogrulama="CSV files downloaded 2026-10-08 into veri/resmi/fred_<series>.csv. Last observations in the files: GDP and GDPC1 "
                  "2026-04-01, UNRATE 2026-09-01, CPIAUCSL 2026-08-01, FEDFUNDS 2026-09-01, OPHNFB 2026-04-01. Original sources as "
                  "listed by FRED: GDP, GDPC1, GDPDEF from BEA; UNRATE, CPIAUCSL, OPHNFB from BLS; FEDFUNDS from the Federal Reserve."),
    worldbank_tur=dict(
        yazar="World Bank, World Development Indicators", yil=2026,
        baslik="Türkiye: FP.CPI.TOTL.ZG Inflation, consumer prices (annual %); SL.UEM.TOTL.ZS Unemployment, total (% of total labor force) "
               "(modeled ILO estimate); NY.GDP.MKTP.KD.ZG GDP growth (annual %)",
        yer="https://api.worldbank.org/v2/country/TUR/indicator/<code>?format=json",
        dogrulama="JSON downloaded 2026-10-08 (API 'lastupdated' 2026-10-08 for inflation and growth, 2026-07-13 for unemployment), "
                  "saved as veri/resmi/worldbank_TUR_<code>.csv for 2019-2025. TÜİK's own tables were not downloaded; the World Bank "
                  "inflation series for Türkiye is based on national consumer prices."),
)

IFR_2025 = dict(
    yazar="International Federation of Robotics (IFR)", yil=2025,
    baslik="Global Robot Demand in Factories Doubles Over 10 Years (press release on World Robotics 2025, Frankfurt, Sep 25, 2025)",
    yer="https://ifr.org/ifr-press-releases/news/global-robot-demand-in-factories-doubles-over-10-years",
    dogrulama="Web page opened and read 2026-10-08. Sentences read: '542,000 robots installed in 2024', 'The total number of industrial "
              "robots in operational use worldwide was 4,664,000 units in 2024 – an increase of 9%', China 'representing 54% of global "
              "deployments ... 295,000 industrial robots have been installed'. Industrial robots in factories only, not service robots.",
    installations_2024=542_000, operational_stock_2024=4_664_000, stock_growth_pct=9,
    china_installations_2024=295_000, china_share_pct=54,
)

PAPERS = dict(
    acemoglu_restrepo=dict(
        yazar="Acemoglu, D. and Restrepo, P.", yil=2020, baslik="Robots and Jobs: Evidence from US Labor Markets",
        yer="Journal of Political Economy 128(6), doi:10.1086/705716",
        dogrulama="Title, authors, journal, volume, issue and year checked in the Crossref record of the DOI on 2026-10-08. Used only for "
                  "the view that industrial robots reduced employment and wages in the local labor markets most exposed to them; "
                  "no number from the paper is used."),
    autor=dict(
        yazar="Autor, D. H.", yil=2015,
        baslik="Why Are There Still So Many Jobs? The History and Future of Workplace Automation",
        yer="Journal of Economic Perspectives 29(3), doi:10.1257/jep.29.3.3",
        dogrulama="Title, author, journal, volume, issue and year checked in the Crossref record of the DOI on 2026-10-08. Used only for "
                  "the view that automation also complements workers and raises demand for other tasks; no number from the paper is used."),
)

TABLES = dict(
    recording=dict(dosya="veri/cay_servisi_kaydi.csv",
                   aciklama="simulation recording of one serve: time, four joint angles of the right arm (rad), elbow velocity (rad/s), "
                            "cup position x, y, z (m); 5666 samples at 50 samples per second; not a measurement of a real robot. "
                            "The course uses only time and cup position."),
)
