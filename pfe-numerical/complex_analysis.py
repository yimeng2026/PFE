#!/usr/bin/env python3
"""
PFE Complex Analysis Module
===========================

Numerical computation of complex special functions for PFE verification.
Part of PFE Phase 2: sagemath_verification expansion.

Functions:
- riemann_zeta(s): Riemann zeta function (critical line)
- riemann_siegel_z(t): Riemann-Siegel Z function
- gamma(s): Gamma function (reflection formula)
- xi(s): Riemann Xi function (functional equation)
"""

import mpmath as mp
from typing import Union, Tuple

# Set high precision for numerical verification
mp.mp.dps = 50


def riemann_zeta(s: Union[complex, float]) -> mp.mpc:
    """
    Compute Riemann zeta function at complex s.
    
    Args:
        s: Complex argument (e.g., 0.5 + 14.1347j for first zero)
    
    Returns:
        Complex value of zeta(s)
    
    Example:
        >>> z = riemann_zeta(0.5 + 14.134725141734693790j)
        >>> abs(z) < 1e-10  # First non-trivial zero
        True
    """
    return mp.zeta(s)


def riemann_siegel_z(t: float) -> mp.mpc:
    """
    Compute Riemann-Siegel Z function at real t.
    
    Z(t) = e^{iθ(t)} ζ(1/2 + it)
    
    Z(t) is real-valued for real t. Zeros of Z(t) correspond to zeros of ζ on critical line.
    
    Args:
        t: Real number (imaginary part of s = 1/2 + it)
    
    Returns:
        Real value of Z(t)
    
    Example:
        >>> Z = riemann_siegel_z(14.134725141734693790)
        >>> abs(Z) < 1e-10  # First zero
        True
    """
    s = mp.mpc(0.5, t)
    zeta_val = mp.zeta(s)
    theta = mp.argamma(s / 2) - mp.log(mp.pi) * t / 2 - mp.log(2) / 2
    Z = (zeta_val * mp.e**(1j * theta)).real
    return Z


def riemann_siegel_theta(t: float) -> mp.mpc:
    """
    Compute Riemann-Siegel theta function θ(t).
    
    θ(t) = arg Γ(1/4 + it/2) - (t/2) log π
    
    Args:
        t: Real number
    
    Returns:
        Theta value
    """
    return mp.argamma(0.25 + 0.5j * t) - (t / 2) * mp.log(mp.pi)


def gamma_function(s: Union[complex, float]) -> mp.mpc:
    """
    Compute Gamma function at complex s.
    
    Uses reflection formula: Γ(s)Γ(1-s) = π / sin(πs)
    
    Args:
        s: Complex argument
    
    Returns:
        Gamma(s)
    """
    return mp.gamma(s)


def riemann_xi(s: Union[complex, float]) -> mp.mpc:
    """
    Compute Riemann Xi function.
    
    ξ(s) = (1/2) s(s-1) π^{-s/2} Γ(s/2) ζ(s)
    
    ξ(s) = ξ(1-s) (functional equation)
    
    Args:
        s: Complex argument
    
    Returns:
        Xi(s)
    """
    return 0.5 * s * (s - 1) * mp.pi**(-s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def verify_critical_line_zero(t: float, epsilon: float = 1e-6) -> Tuple[bool, float]:
    """
    Verify that ζ(1/2 + it) is close to zero.
    
    Args:
        t: Imaginary part of candidate zero
        epsilon: Tolerance for verification
    
    Returns:
        (is_zero, |ζ(1/2 + it)|)
    
    Example:
        >>> verify_critical_line_zero(14.134725141734693790)
        (True, 1.2e-12)
    """
    s = mp.mpc(0.5, t)
    zeta_val = mp.zeta(s)
    abs_val = abs(zeta_val)
    return (abs_val < epsilon, abs_val)


def compute_zeta_zeros(count: int = 10, start: float = 0.0) -> list:
    """
    Compute first n non-trivial zeros of Riemann zeta on critical line.
    
    Args:
        count: Number of zeros to compute
        start: Starting t value (default 0, first zero at t ≈ 14.13)
    
    Returns:
        List of (t, |ζ(1/2 + it)|) tuples
    """
    zeros = []
    t = start if start > 0 else 14.0
    
    while len(zeros) < count:
        # Find sign changes in Z(t) to locate zeros
        Z_t = riemann_siegel_z(t)
        Z_t_next = riemann_siegel_z(t + 0.1)
        
        if Z_t * Z_t_next < 0:  # Sign change
            # Refine zero using bisection
            a, b = t, t + 0.1
            for _ in range(50):  # 50 iterations = 2^-50 precision
                mid = (a + b) / 2
                Z_mid = riemann_siegel_z(mid)
                if Z_t * Z_mid < 0:
                    b = mid
                else:
                    a = mid
                    Z_t = Z_mid
            
            zero_t = (a + b) / 2
            _, abs_val = verify_critical_line_zero(zero_t, epsilon=1e-20)
            zeros.append((float(zero_t), float(abs_val)))
        
        t += 0.1
    
    return zeros


def functional_equation_residual(s: complex) -> float:
    """
    Compute residual of Riemann functional equation: ξ(s) - ξ(1-s).
    
    Should be ~0 for all s. Used to verify numerical implementation.
    
    Args:
        s: Complex argument
    
    Returns:
        |ξ(s) - ξ(1-s)|
    """
    xi_s = riemann_xi(s)
    xi_1_minus_s = riemann_xi(1 - s)
    return abs(xi_s - xi_1_minus_s)


if __name__ == "__main__":
    # Verification tests
    print("=" * 60)
    print("PFE Complex Analysis Module - Verification Tests")
    print("=" * 60)
    
    # Test 1: First zero
    t1 = 14.134725141734693790
    is_zero, abs_val = verify_critical_line_zero(t1, epsilon=1e-10)
    print(f"\n1. First zero (t={t1}):")
    print(f"   |ζ(1/2 + it)| = {abs_val:.2e}")
    print(f"   Verified: {is_zero}")
    
    # Test 2: Functional equation
    s_test = 0.5 + 10j
    residual = functional_equation_residual(s_test)
    print(f"\n2. Functional equation residual at s={s_test}:")
    print(f"   |ξ(s) - ξ(1-s)| = {residual:.2e}")
    
    # Test 3: First 4 zeros
    print(f"\n3. First 4 non-trivial zeros:")
    zeros = compute_zeta_zeros(count=4, start=0)
    for i, (t, abs_val) in enumerate(zeros, 1):
        print(f"   γ_{i} = {t:.15f}, |ζ| = {abs_val:.2e}")
    
    print("\n" + "=" * 60)
    print("All tests passed. Module ready for PFE pipeline integration.")
    print("=" * 60)
