"""
display.py - Output formatting for SIR epidemic simulator
========================================================

Provides:
    - CLI banners and headers
    - Configuration display
    - Result formatting
    - Session report generation
"""


def format_header() -> str:
    """Return the CLI banner for this project.

    Returns:
        str: User-facing banner string.
    """
    return (
        "=" * 70
        + "\n"
        + "  SIR EPIDEMIC SIMULATOR - DISEASE SPREAD DYNAMICS + SCENARIOS\n"
        + "=" * 70
    )


def format_startup_guide(config: dict, param_ranges: dict) -> str:
    """Return startup guidance shown before simulation begins.

    Parameters:
        config (dict): Runtime configuration.
        param_ranges (dict): Available parameter ranges.

    Returns:
        str: Multi-line startup guide.
    """
    lines = [
        "",
        "Configuration:",
        f"  Simulation duration: {config['duration_days']} days",
        f"  Population: {config['population']}",
        f"  Initial infected: {config['initial_infected']}",
        f"  Transmission rate (beta): {config['beta']}",
        f"  Recovery rate (gamma): {config['gamma']}",
        f"  Show parameter sweep: {config.get('param_sweep', True)}",
        "",
        "Available parameters:",
    ]

    for param_name, param_info in param_ranges.items():
        min_val = param_info["min"]
        max_val = param_info["max"]
        description = param_info["description"]
        lines.append(
            f"  - {description} ({param_name}): {min_val} - {max_val}"
        )

    lines.extend(
        [
            "",
            "Session behavior:",
            "  1) Solve SIR compartmental model with initial parameters.",
            "  2) Generate epidemic curve showing S(t), I(t), R(t) over time.",
            "  3) Perform parameter sweep to inspect sensitivity.",
            "  4) Compare scenarios and compute epidemic metrics.",
        ]
    )
    return "\n".join(lines)


def _format_epidemic_metrics(metrics: dict) -> list[str]:
    """Return readable epidemic statistics.

    Parameters:
        metrics (dict): Computed epidemic metrics.

    Returns:
        list[str]: Formatted metric lines.
    """
    if not metrics:
        return ["  Metrics: no data"]

    lines = [
        f"  Peak infections: {metrics['peak_infected']:.0f} (day {metrics['peak_time']:.0f})",
        f"  Total infections: {metrics['total_infected']:.0f} ({metrics['attack_rate']:.1%} of population)",
        f"  Epidemic duration: {metrics['epidemic_duration']:.0f} days",
        f"  Effective R: {metrics['r_effective']:.2f}",
    ]
    return lines


def _format_sweep_summary(sweep_results: list[dict]) -> list[str]:
    """Return formatted summary of parameter sweep results.

    Parameters:
        sweep_results (list[dict]): Results from parameter sweep.

    Returns:
        list[str]: Summary lines for sweep.
    """
    if not sweep_results:
        return ["  Parameter sweep: not performed"]

    lines = [f"  Parameter sweep: {len(sweep_results)} variations tested"]
    
    peak_infections = [r["metrics"]["peak_infected"] for r in sweep_results]
    if peak_infections:
        lines.extend([
            f"    Min peak infections: {min(peak_infections):.0f}",
            f"    Max peak infections: {max(peak_infections):.0f}",
        ])
    
    return lines


def format_run_report(summary: dict) -> str:
    """Return formatted session report for display.

    Parameters:
        summary (dict): Complete session summary.

    Returns:
        str: Formatted multi-line report.
    """
    lines = ["", "Session summary:"]
    lines.append(f"  Status: {summary.get('status', 'unknown')}")
    
    config = summary.get("config", {})
    lines.append(f"  Simulation time: {config.get('duration_days', 0)} days")

    base_result = summary.get("base_result", {})
    metrics = base_result.get("metrics", {})
    lines.extend(_format_epidemic_metrics(metrics))

    sweep_results = summary.get("sweep_results", [])
    lines.extend(_format_sweep_summary(sweep_results))

    lines.extend([
        "  Saved plots: data/runs/epidemic_curve.png, data/runs/parameter_sweep.png",
        "Saved run artifact: data/runs/latest_sir_simulation.json",
        "",
    ])

    return "\n".join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string.
    
    Parameters:
        message (str): The message to format.
        
    Returns:
        str: Formatted message.
    """
    return f"[Project 16] {message}"
