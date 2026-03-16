"""
operations.py - SIR simulation engine and analysis workflows
===========================================================

Implements:
    - SIR differential equations solver
    - Time-series trajectory generation
    - Epidemic metrics computation
    - Parameter sensitivity analysis
    - Scenario comparison workflows
"""

from __future__ import annotations

import random
import numpy as np
from scipy.integrate import odeint

from models import (
    create_epidemic_metrics,
    create_project_config,
    create_simulation_result,
    create_sir_state,
)
from storage import save_latest_session


def load_parameter_ranges() -> dict:
    """Return parameter ranges for sensitivity analysis.

    Returns:
        dict: Min and max values for each tunable parameter.
    """
    return {
        "beta": {"min": 0.1, "max": 1.0, "description": "Transmission rate"},
        "gamma": {"min": 0.05, "max": 0.25, "description": "Recovery rate"},
        "initial_infected": {
            "min": 1,
            "max": 100,
            "description": "Starting infected count",
        },
    }


def _sir_derivatives(state: list[float], time: float, beta: float, gamma: float, N: int) -> list[float]:
    """Compute SIR differential equations.

    dS/dt = -beta * S * I / N
    dI/dt = beta * S * I / N - gamma * I
    dR/dt = gamma * I

    Parameters:
        state (list[float]): [S, I, R] at current time.
        time (float): Current time (used for integration interface).
        beta (float): Transmission rate.
        gamma (float): Recovery rate.
        N (int): Total population.

    Returns:
        list[float]: [dS/dt, dI/dt, dR/dt]
    """
    S, I, R = state
    N = S + I + R
    if N == 0:
        return [0, 0, 0]

    dS_dt = -beta * S * I / N
    dI_dt = beta * S * I / N - gamma * I
    dR_dt = gamma * I

    return [dS_dt, dI_dt, dR_dt]


def simulate_sir(config: dict) -> dict:
    """Run a single SIR simulation with given parameters.

    Parameters:
        config (dict): Simulation configuration with beta, gamma, duration, etc.

    Returns:
        dict: Complete simulation result with trajectory and metrics.
    """
    # Extract parameters
    population = config["population"]
    initial_infected = config["initial_infected"]
    duration_days = config["duration_days"]
    beta = config["beta"]
    gamma = config["gamma"]

    # Initialize compartments
    initial_susceptible = population - initial_infected
    initial_state = [initial_susceptible, initial_infected, 0]

    # Create time array
    times = np.linspace(0, duration_days, min(duration_days, 365))

    # Solve ODE
    trajectory = odeint(
        _sir_derivatives,
        initial_state,
        times,
        args=(beta, gamma, population),
    )

    # Extract compartments
    S = trajectory[:, 0]
    I = trajectory[:, 1]
    R = trajectory[:, 2]

    # Build state records
    states = []
    for i, t in enumerate(times):
        state = create_sir_state(
            time=float(t),
            susceptible=float(S[i]),
            infected=float(I[i]),
            recovered=float(R[i]),
        )
        states.append(state)

    # Compute metrics
    peak_infected = float(np.max(I))
    peak_time = float(times[np.argmax(I)])
    total_infected = float(R[-1])
    attack_rate = total_infected / population
    
    # Epidemic duration: from first infection to near-zero new infections
    active_threshold = population * 0.001
    active_days = times[I > active_threshold]
    epidemic_duration = float(active_days[-1] - active_days[0]) if len(active_days) > 0 else 0
    
    # Basic reproduction number from beta/gamma
    r_effective = beta / gamma if gamma > 0 else 0

    metrics = create_epidemic_metrics(
        peak_infected=peak_infected,
        peak_time=peak_time,
        total_infected=total_infected,
        attack_rate=attack_rate,
        epidemic_duration=epidemic_duration,
        r_effective=r_effective,
    )

    result = create_simulation_result(
        config=config,
        times=times.tolist(),
        states=states,
        metrics=metrics,
    )

    return result


def run_parameter_sweep(config: dict, param_name: str, num_points: int = 5) -> list[dict]:
    """Run multiple simulations varying one parameter.

    Parameters:
        config (dict): Base configuration.
        param_name (str): Name of parameter to sweep (beta, gamma, etc).
        num_points (int): Number of parameter values to sample.

    Returns:
        list[dict]: Results for each parameter value.
    """
    ranges = load_parameter_ranges()
    if param_name not in ranges:
        return []

    param_range = ranges[param_name]
    param_values = np.linspace(param_range["min"], param_range["max"], num_points)
    
    results = []
    for value in param_values:
        sweep_config = config.copy()
        sweep_config[param_name] = float(value)
        result = simulate_sir(sweep_config)
        results.append(result)

    return results


def create_scenario_comparison(scenarios: list[dict]) -> dict:
    """Create a comparison report across multiple scenarios.

    Parameters:
        scenarios (list[dict]): List of simulation results.

    Returns:
        dict: Comparison summary with all metrics side-by-side.
    """
    if not scenarios:
        return {}

    comparison = {
        "num_scenarios": len(scenarios),
        "scenarios": [],
    }

    for i, scenario in enumerate(scenarios):
        scenario_summary = {
            "index": i,
            "config": scenario.get("config", {}),
            "metrics": scenario.get("metrics", {}),
        }
        comparison["scenarios"].append(scenario_summary)

    return comparison


def run_core_flow(config: dict | None = None) -> dict:
    """Execute the main SIR simulation workflow.

    Parameters:
        config (dict | None): Override default configuration. If None, uses default.

    Returns:
        dict: Session summary with results and metadata.
    """
    if config is None:
        config = create_project_config()

    # Run base simulation
    base_result = simulate_sir(config)

    # Run parameter sweep if requested
    sweep_results = []
    if config.get("param_sweep", True):
        sweep_results = run_parameter_sweep(config, param_name="beta", num_points=5)

    # Create scenario comparison
    all_scenarios = [base_result] + sweep_results
    comparison = create_scenario_comparison(all_scenarios)

    # Create session summary
    session_summary = {
        "status": "completed",
        "config": config,
        "base_result": base_result,
        "sweep_results": sweep_results,
        "comparison": comparison,
    }

    # Save to disk
    save_latest_session(session_summary)

    return session_summary
