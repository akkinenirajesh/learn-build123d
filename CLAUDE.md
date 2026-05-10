# CLAUDE.md — learn-build123d

A hands-on, lesson-based project for mastering the **build123d** parametric CAD library.

## Environment

- Python 3.12+, dependencies in `pyproject.toml`
- Virtual env: `.venv/`
- Activate: `.venv\Scripts\activate` (Windows)
- Install: `pip install -e ".[dev]"`

## Project structure

```
lessons/          # Numbered, self-contained lesson scripts
  Nn_topic.py     # Run directly: python lessons/01_hello_world.py
output/           # Exported .step, .stl files (gitignored)
```

## Conventions

- Each lesson file is self-contained and runnable with `python lessons/Nn_topic.py`
- Lessons build on earlier ones; read comments in the file before running
- Use `from build123d import *` for the idiomatic "import everything" style
- Export files go to `output/` (created at runtime if missing)
- Use `ocp-vscode` for in-IDE preview when using VS Code

## build123d notes

- build123d uses a **builder pattern**: create a sketch on a workplane, then extrude/revolve
- `Box`, `Cylinder`, `Sphere` etc. are shape primitives (direct Part creation)
- `Pos(X=...)`, `Rot(X=...)` are location helpers
- Boolean ops: `+` (union), `-` (cut), `&` (intersect)
- Workplanes: `Plane.XY`, `Plane.YZ`, `Plane.XZ`, or faces of existing parts
- Build modes: `Mode.PRIVATE` (default, isolated), `Mode.ADD`, `Mode.SUBTRACT`, `Mode.INTERSECT`
- Export with `export_step(path)`, `export_stl(path)`

## When adding new lessons

- Follow the numbered naming pattern `Nn_topic.py`
- Keep each file ~30-60 lines, focused on one concept
- Add an intro comment block explaining what the lesson covers
- Update the table in README.md
