# Beginner Project 16: SIR Epidemic Simulator With Visualization

**Time:** 3-5 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** disease compartment modeling, parameter sensitivity analysis, scenario comparison, and epidemic behavior visualization

---

## Why This Project?

Understanding infectious disease dynamics helps public health decision-making and builds intuition about epidemic behavior.
This project gives you a practical beginner workflow where you can:

- simulate compartmental disease models with configurable parameters,
- analyze how changes in transmission and recovery rates affect epidemic curves,
- run parameter sweep studies to identify critical intervention thresholds,
- compare multiple epidemic scenarios side-by-side with uncertainty bands,
- and save simulation results for reproducible analysis.

---

## More Projects

You can access this project and more in this separate repository:

[student-interview-prep](https://github.com/ShamShamsw/student-interview-prep.git)

---

## What You Will Build

You will build a command-line SIR (Susceptible-Infected-Recovered) epidemic simulator that:

1. Implements the core SIR compartmental model using ordinary differential equations.
2. Solves the model numerically across time with configurable initial conditions and parameters.
3. Generates time-series prevalence curves showing susceptible, infected, and recovered populations.
4. Performs parameter sweep studies to visualize model sensitivity (e.g., transmission rate impact).
5. Compares multiple epidemic scenarios with overlaid curves and summary statistics.
6. Computes epidemic metrics (peak infection time, peak size, total infections) for each run.
7. Saves simulation results and plots to JSON and PNG for review and reproducibility.

---

## Requirements

- Python 3.11+
- `numpy`
- `scipy`
- `matplotlib`
- `seaborn`

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
  SIR EPIDEMIC SIMULATOR - DISEASE SPREAD DYNAMICS + SCENARIOS
======================================================================

Configuration:
  Simulation duration: 365 days
  Population: 10000
  Initial infected: 10
  Transmission rate (beta): 0.5
  Recovery rate (gamma): 0.1
  Show parameter sweep: True

Available parameters:
  - Transmission rate (beta): How quickly infection spreads (0.1 - 1.0)
  - Recovery rate (gamma): How quickly people recover (0.05 - 0.25)
  - Initial infected: Starting number of infected individuals (1 - 100)

Session behavior:
  1) Solve SIR compartmental model with initial parameters.
  2) Generate epidemic curve showing S(t), I(t), R(t) over time.
  3) Perform parameter sweep to inspect sensitivity.
  4) Compare scenarios and compute epidemic metrics.

Session summary:
  Status: completed
  Simulation time: 365 days
  Peak infections: 2847 (day 58)
  Total infections: 9651 (96.5% of population)
  Epidemic duration: 287 days
  Saved plots: data/runs/epidemic_curve.png, data/runs/parameter_sweep.png
Saved run artifact: data/runs/latest_sir_simulation.json
```

---

## Build Order

Follow this order for clean architecture:

1. `storage.py`
2. `models.py`
3. `operations.py`
4. `display.py`
5. `main.py`

---
