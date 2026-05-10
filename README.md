# learn-build123d

Hands-on lessons for learning [build123d](https://build123d.readthedocs.io/) — a parametric CAD library for Python.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Lessons

| # | Topic | File |
|---|-------|------|
| 1 | Hello World — your first part | `lessons/01_hello_world.py` |
| 2 | Basic shapes | `lessons/02_basic_shapes.py` |
| 3 | Boolean operations | `lessons/03_operations.py` |
| 4 | Workplanes & sketches | `lessons/04_workplanes.py` |
| 5 | Assemblies & constraints | `lessons/05_assemblies.py` |
| 6 | Export & fabrication | `lessons/06_export.py` |

Run a lesson:

```powershell
python lessons/01_hello_world.py
```
