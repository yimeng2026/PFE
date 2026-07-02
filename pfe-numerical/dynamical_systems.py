#!/usr/bin/env python3
"""
PFE Dynamical Systems Module
===========================

Numerical integration and chaos detection for PFE verification.
Part of PFE Phase 2: sagemath_verification expansion.

Functions:
- ode_integrate: Numerical ODE integration (Runge-Kutta, adaptive)
- lyapunov_exponent: Lyapunov exponent computation (chaos detection)
- phase_space_analysis: Phase space trajectory analysis
- poincare_section: Poincare section for periodic orbit detection
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
from typing import Callable, Tuple, List, Optional
from dataclasses import dataclass


@dataclass
class IntegrationResult:
    """Result of ODE integration."""
    t: np.ndarray
    y: np.ndarray
    success: bool
    message: str
    nfev: int
    njev: int


def ode_integrate(f: Callable, y0: np.ndarray, t_span: Tuple[float, float],
                 method: str = "RK45", rtol: float = 1e-6, atol: float = 1e-9,
                 max_step: Optional[float] = None, dense_output: bool = True) -> IntegrationResult:
    """
    Integrate ODE system dy/dt = f(t, y).
    
    Args:
        f: Right-hand side function f(t, y) -> dy/dt
        y0: Initial condition
        t_span: (t_start, t_end)
        method: Integration method (RK45, RK23, DOP853, Radau, BDF, LSODA)
        rtol: Relative tolerance
        atol: Absolute tolerance
        max_step: Maximum step size
        dense_output: Whether to return dense output
    
    Returns:
        IntegrationResult with time points, solution, and metadata
    
    Example:
        >>> def lorenz(t, y, sigma=10, rho=28, beta=8/3):
        ...     return [sigma*(y[1]-y[0]), y[0]*(rho-y[2])-y[1], y[0]*y[1]-beta*y[2]]
        >>> result = ode_integrate(lorenz, [1, 1, 1], (0, 50))
        >>> result.success
        True
    """
    sol = solve_ivp(f, t_span, y0, method=method, rtol=rtol, atol=atol,
                    max_step=max_step, dense_output=dense_output)
    
    return IntegrationResult(
        t=sol.t,
        y=sol.y,
        success=sol.success,
        message=sol.message,
        nfev=sol.nfev,
        njev=sol.njev if hasattr(sol, 'njev') else 0
    )


def lyapunov_exponent(f: Callable, y0: np.ndarray, t_span: Tuple[float, float],
                     perturbation: float = 1e-10, n_steps: int = 1000) -> float:
    """
    Compute largest Lyapunov exponent using finite differences.
    
    λ > 0 indicates chaos (exponential divergence of nearby trajectories).
    λ ≈ 0 indicates periodic/quasi-periodic behavior.
    λ < 0 indicates stable fixed point.
    
    Args:
        f: Right-hand side function
        y0: Initial condition
        t_span: (t_start, t_end)
        perturbation: Initial perturbation magnitude
        n_steps: Number of integration steps
    
    Returns:
        Largest Lyapunov exponent estimate
    
    Example:
        >>> def lorenz(t, y): ...
        >>> lyap = lyapunov_exponent(lorenz, [1, 1, 1], (0, 100))
        >>> lyap > 0  # Lorenz system is chaotic
        True
    """
    t_eval = np.linspace(t_span[0], t_span[1], n_steps)
    dt = (t_span[1] - t_span[0]) / n_steps
    
    # Integrate reference trajectory
    sol_ref = solve_ivp(f, t_span, y0, t_eval=t_eval, method="RK45")
    y_ref = sol_ref.y
    
    # Integrate perturbed trajectory
    y0_perturbed = y0 + perturbation * np.random.randn(len(y0))
    sol_pert = solve_ivp(f, t_span, y0_perturbed, t_eval=t_eval, method="RK45")
    y_pert = sol_pert.y
    
    # Compute divergence
    divergence = np.linalg.norm(y_pert - y_ref, axis=0)
    
    # Fit exponential growth: divergence ~ exp(λ t)
    # Use linear regression on log(divergence) vs t
    valid_idx = divergence > 0
    if np.sum(valid_idx) < 10:
        return 0.0
    
    log_div = np.log(divergence[valid_idx])
    t_valid = t_eval[valid_idx]
    
    # Linear regression: log_div = λ * t + c
    A = np.vstack([t_valid, np.ones(len(t_valid))]).T
    lambda_est, _ = np.linalg.lstsq(A, log_div, rcond=None)[0]
    
    return lambda_est


def phase_space_analysis(y: np.ndarray, dimension: int = 3,
                        delay: Optional[int] = None) -> np.ndarray:
    """
    Reconstruct phase space from time series using delay embedding (Takens' theorem).
    
    Args:
        y: Time series data (1D array)
        dimension: Embedding dimension
        delay: Time delay (default: auto-estimated)
    
    Returns:
        Phase space trajectory (dimension × n_points)
    
    Example:
        >>> x = np.sin(np.linspace(0, 20*np.pi, 1000))
        >>> ps = phase_space_analysis(x, dimension=3, delay=25)
        >>> ps.shape
        (3, 975)
    """
    if delay is None:
        # Auto-estimate delay using first minimum of mutual information
        # Simplified: use 1/4 of dominant period
        delay = max(1, len(y) // 100)
    
    n_points = len(y) - (dimension - 1) * delay
    phase_space = np.zeros((dimension, n_points))
    
    for i in range(dimension):
        phase_space[i, :] = y[i * delay : i * delay + n_points]
    
    return phase_space


def poincare_section(y: np.ndarray, section_func: Callable,
                    direction: str = "both") -> np.ndarray:
    """
    Compute Poincare section of trajectory.
    
    Args:
        y: Trajectory data (n_dim × n_points)
        section_func: Function defining section (e.g., lambda x: x[0] - 1)
        direction: "both", "positive", or "negative" crossing
    
    Returns:
        Points on Poincare section
    
    Example:
        >>> y = np.array([[np.sin(t) for t in np.linspace(0, 10*np.pi, 1000)]])
        >>> ps = poincare_section(y, lambda x: x[0])
        >>> ps.shape[1] > 0  # Should have crossings
        True
    """
    n_dim, n_points = y.shape
    section_values = np.array([section_func(y[:, i]) for i in range(n_points)])
    
    # Find crossings
    crossings = []
    for i in range(n_points - 1):
        if section_values[i] * section_values[i + 1] < 0:  # Sign change
            if direction == "both" or \
               (direction == "positive" and section_values[i] < 0) or \
               (direction == "negative" and section_values[i] > 0):
                # Linear interpolation for exact crossing
                alpha = abs(section_values[i]) / (abs(section_values[i]) + abs(section_values[i + 1]))
                crossing_point = y[:, i] + alpha * (y[:, i + 1] - y[:, i])
                crossings.append(crossing_point)
    
    return np.array(crossings).T if crossings else np.zeros((n_dim, 0))


def detect_chaos(f: Callable, y0: np.ndarray, t_span: Tuple[float, float],
                threshold: float = 0.001) -> Tuple[bool, float, str]:
    """
    Detect chaos in dynamical system using Lyapunov exponent.
    
    Args:
        f: Right-hand side function
        y0: Initial condition
        t_span: (t_start, t_end)
        threshold: Lyapunov exponent threshold for chaos detection
    
    Returns:
        (is_chaotic, lyapunov_exponent, interpretation)
    
    Example:
        >>> def lorenz(t, y): ...
        >>> chaotic, lyap, interp = detect_chaos(lorenz, [1, 1, 1], (0, 100))
        >>> chaotic
        True
    """
    lyap = lyapunov_exponent(f, y0, t_span)
    
    if lyap > threshold:
        return True, lyap, f"Chaotic (λ = {lyap:.4f} > {threshold})"
    elif lyap < -threshold:
        return False, lyap, f"Stable (λ = {lyap:.4f} < -{threshold})"
    else:
        return False, lyap, f"Periodic/Quasi-periodic (|λ| = {abs(lyap):.4f} < {threshold})"


if __name__ == "__main__":
    # Demo: Lorenz system
    print("=" * 60)
    print("PFE Dynamical Systems Module - Demo")
    print("=" * 60)
    
    def lorenz(t, y, sigma=10, rho=28, beta=8/3):
        return [sigma*(y[1]-y[0]), y[0]*(rho-y[2])-y[1], y[0]*y[1]-beta*y[2]]
    
    # Integrate Lorenz system
    result = ode_integrate(lorenz, [1, 1, 1], (0, 50), method="RK45")
    print(f"\n1. Lorenz System Integration:")
    print(f"   Success: {result.success}")
    print(f"   Time points: {len(result.t)}")
    print(f"   Function evaluations: {result.nfev}")
    
    # Detect chaos
    chaotic, lyap, interp = detect_chaos(lorenz, [1, 1, 1], (0, 100))
    print(f"\n2. Chaos Detection:")
    print(f"   Lyapunov Exponent: {lyap:.4f}")
    print(f"   Interpretation: {interp}")
    
    # Phase space reconstruction
    x_data = result.y[0, :]
    ps = phase_space_analysis(x_data, dimension=3, delay=10)
    print(f"\n3. Phase Space Reconstruction:")
    print(f"   Embedding dimension: 3")
    print(f"   Delay: 10")
    print(f"   Phase space shape: {ps.shape}")
    
    print("\n" + "=" * 60)
    print("Module ready for PFE pipeline integration.")
    print("=" * 60)
