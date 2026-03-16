"""
models.py - Data models for SIR epidemic simulator
==================================================

Defines:
    - SIR model parameters and configurations
    - Simulation results and intermediate states
    - Epidemic metrics and summary statistics
"""

from datetime import datetime


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp.

    Returns:
        str: Timestamp string with trailing Z.
    """
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_project_config(
    duration_days: int = 365,
    population: int = 10000,
    initial_infected: int = 10,
    beta: float = 0.5,
    gamma: float = 0.1,
    param_sweep: bool = True,
) -> dict:
    """Create the default runtime configuration for SIR simulation.

    Parameters:
        duration_days (int): Length of simulation in days.
        population (int): Total population size.
        initial_infected (int): Starting number of infected individuals.
        beta (float): Transmission rate (contacts per day * infection probability).
        gamma (float): Recovery rate (1/infectious period).
        param_sweep (bool): Whether to perform parameter sweep study.

    Returns:
        dict: Configuration dictionary.
    """
    return {
        "duration_days": duration_days,
        "population": population,
        "initial_infected": initial_infected,
        "beta": beta,
        "gamma": gamma,
        "param_sweep": param_sweep,
        "created_at": _utc_timestamp(),
    }


def create_sir_state(
    time: float,
    susceptible: float,
    infected: float,
    recovered: float,
) -> dict:
    """Create a snapshot of SIR compartment values at a specific time point.

    Parameters:
        time (float): Time in days.
        susceptible (float): Number of susceptible individuals.
        infected (float): Number of infected individuals.
        recovered (float): Number of recovered individuals.

    Returns:
        dict: SIR state snapshot.
    """
    return {
        "time": time,
        "susceptible": susceptible,
        "infected": infected,
        "recovered": recovered,
    }


def create_simulation_result(
    config: dict,
    times: list[float],
    states: list[dict],
    metrics: dict,
) -> dict:
    """Create a complete simulation result with trajectory and metrics.

    Parameters:
        config (dict): Original simulation configuration.
        times (list[float]): Time points (in days).
        states (list[dict]): SIR states at each time point.
        metrics (dict): Computed epidemic metrics.

    Returns:
        dict: Complete simulation result.
    """
    return {
        "config": config,
        "trajectory": {
            "times": times,
            "states": states,
        },
        "metrics": metrics,
        "completed_at": _utc_timestamp(),
    }


def create_epidemic_metrics(
    peak_infected: float,
    peak_time: float,
    total_infected: float,
    attack_rate: float,
    epidemic_duration: float,
    r_effective: float,
) -> dict:
    """Create computed epidemic statistics from a simulation.

    Parameters:
        peak_infected (float): Maximum number of infected at any time.
        peak_time (float): Time when peak infection occurs (days).
        total_infected (float): Total number who became infected.
        attack_rate (float): Proportion of population that got infected (0-1).
        epidemic_duration (float): Days from first to last infection.
        r_effective (float): Effective reproduction number.

    Returns:
        dict: Epidemic metrics.
    """
    return {
        "peak_infected": peak_infected,
        "peak_time": peak_time,
        "total_infected": total_infected,
        "attack_rate": attack_rate,
        "epidemic_duration": epidemic_duration,
        "r_effective": r_effective,
    }
