"""Robots and the Economy — shared lab tools.
Data: veri/cay_servisi_kaydi.csv is the SIMULATION RECORDING of a humanoid robot that carries a cup in a cafe, 50 samples per second.
It is not a measurement of a real robot. Macro numbers come from official tables in veri/resmi/ (see kaynaklar.py).
Every number that comes neither from the recording nor from an official table is marked EXAMPLE.
(The CSV column names are Turkish; recording() gives them English names.)

  recording()                 : the recording as a dictionary with English keys (t, shoulder_pitch, elbow, cup_x ...)
  smooth(x, n)                : moving average over n samples (25 samples = half a second)
  at(t, seconds)              : index of the sample closest to a time
  session(lesson, name, code) : runs code like an interactive Python session and writes the output to ekran/<lesson>/<name>.txt
  figure(lesson, name)        : saves the open figure as ekran/<lesson>/<name>.png (1920 x 1080)
  measure(key=value)          : writes a measurement to OLCUMLER.json (every number in the lessons comes from this file)
The Turkish names kayit, yumusat, oturum, sekil and olc are aliases of the same functions.
"""
import ast, contextlib, io, json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LAB = pathlib.Path(__file__).resolve().parent
OLC = LAB / "OLCUMLER.json"
np.set_printoptions(precision=4, suppress=True, linewidth=88, legacy="1.25")
plt.rcParams.update({"font.size": 22, "axes.titlesize": 26, "axes.labelsize": 24, "legend.fontsize": 20,
                     "figure.figsize": (19.2, 10.8), "axes.grid": True, "grid.alpha": 0.35, "lines.linewidth": 3,
                     "font.family": "DejaVu Sans"})

# CSV column name -> English name used in the lessons
COLUMNS = {"zaman_s": "t", "omuz_pitch_rad": "shoulder_pitch", "omuz_roll_rad": "shoulder_roll", "dirsek_rad": "elbow",
           "bilek_pitch_rad": "wrist_pitch", "dirsek_hiz_rad_s": "elbow_velocity",
           "bardak_x_m": "cup_x", "bardak_y_m": "cup_y", "bardak_z_m": "cup_z"}


def recording():
    """The simulation recording as a dictionary of arrays: t (s), joint angles (rad), elbow_velocity (rad/s), cup_x, cup_y, cup_z (m)."""
    d = np.genfromtxt(LAB / "veri/cay_servisi_kaydi.csv", delimiter=",", names=True)
    return {COLUMNS[k]: d[k] for k in d.dtype.names}


def smooth(x, n=25):
    """Moving average over n samples (25 samples = half a second). Edges are padded by reflection."""
    x = np.asarray(x, float)
    k = np.ones(n) / n
    if x.ndim == 1:
        return np.convolve(np.pad(x, n, mode="reflect"), k, mode="same")[n:-n]
    return np.column_stack([smooth(x[:, i], n) for i in range(x.shape[1])])


def at(t, seconds):
    """Index of the sample closest to the given time in seconds."""
    return int(np.argmin(np.abs(np.asarray(t) - seconds)))


def _j(v):
    if isinstance(v, np.ndarray):
        return [_j(x) for x in v.tolist()]
    if isinstance(v, (list, tuple)):
        return [_j(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _j(x) for k, x in v.items()}
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (float, np.floating)):
        return round(float(v), 4)
    if isinstance(v, (np.integer,)):
        return int(v)
    return v


def measure(**kw):
    d = json.loads(OLC.read_text()) if OLC.exists() else {}
    d.update({k: _j(v) for k, v in kw.items()})
    OLC.write_text(json.dumps(d, ensure_ascii=False, indent=1))


def session(lesson, name, code, ns=None):
    """Runs the code like an interactive Python session: an expression's value is printed, an assignment is silent."""
    ns = {} if ns is None else ns
    ns.setdefault("__name__", "__session__")
    code = code.strip("\n")
    tree = ast.parse(code)
    lines = code.splitlines()
    out = []
    for st in tree.body:
        part = lines[st.lineno - 1: st.end_lineno]
        out.append(">>> " + part[0])
        out += ["... " + l for l in part[1:]]
        if len(part) > 1:
            out.append("...")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            if isinstance(st, ast.Expr):
                v = eval(compile(ast.Expression(st.value), "<session>", "eval"), ns)
                if v is not None:
                    print(repr(v))
            else:
                exec(compile(ast.Module([st], []), "<session>", "exec"), ns)
        out += buf.getvalue().rstrip("\n").splitlines() if buf.getvalue() else []
    path = LAB / "ekran" / lesson / f"{name}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return ns


def figure(lesson, name, fig=None):
    fig = fig or plt.gcf()
    path = LAB / "ekran" / lesson / f"{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)
    return path


kayit, yumusat, olc, oturum, sekil = recording, smooth, measure, session, figure
