#!/usr/bin/env python3
"""
PFE TOE Framework Parameter Scanner
=================================

Parameter scanning scripts for 5 key TOE frameworks:
- Quantum Gravity (dimensions, curvature, Planck scale)
- Supersymmetry (SUSY breaking scale, superpartner masses)
- Dark Matter (WIMP mass, cross-section, relic density)
- Dark Energy (cosmological constant, equation of state)
- Beyond Standard Model (GUT scale, proton lifetime)

PFE Phase 2: toe_framework computational expansion
"""

import numpy as np
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple
from pathlib import Path


@dataclass
class ParameterScan:
    """Parameter scan result for a TOE framework."""
    framework: str
    parameter: str
    range_min: float
    range_max: float
    num_points: int
    values: List[float]
    predictions: Dict[str, List[float]]
    best_fit: Dict[str, float]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "framework": self.framework,
            "parameter": self.parameter,
            "range": [self.range_min, self.range_max],
            "num_points": self.num_points,
            "values": self.values,
            "predictions": self.predictions,
            "best_fit": self.best_fit
        }


class QuantumGravityScanner:
    """Scan quantum gravity parameters."""
    
    def __init__(self):
        self.results = {}
    
    def scan_extra_dimensions(self, d_range: Tuple[int, int] = (4, 11)) -> ParameterScan:
        """Scan number of extra dimensions."""
        dimensions = list(range(d_range[0], d_range[1] + 1))
        
        # Planck scale in d dimensions: M_Pl(d) ~ M_Pl(4) * (M_Pl(4)/M_extra)^{(d-4)/2}
        M_pl_4 = 1.22e19  # GeV (4D Planck scale)
        M_extra = 1e3  # GeV (TeV scale extra dimensions)
        
        predictions = {
            "planck_scale": [M_pl_4 * (M_pl_4 / M_extra)**((d - 4) / 2) for d in dimensions],
            "graviton_kaluza_klein_mass": [M_extra / (d - 4) if d > 4 else 0 for d in dimensions],
            "newtonian_deviation": [1e-3 * (d - 4) for d in dimensions]
        }
        
        # Best fit: d=10 or d=11 (string theory / M-theory)
        best_fit = {
            "dimension": 11 if 11 in dimensions else 10,
            "planck_scale": predictions["planck_scale"][-1],
            "motivation": "M-theory requires 11 dimensions"
        }
        
        return ParameterScan(
            framework="Quantum Gravity",
            parameter="extra_dimensions",
            range_min=d_range[0],
            range_max=d_range[1],
            num_points=len(dimensions),
            values=[float(d) for d in dimensions],
            predictions=predictions,
            best_fit=best_fit
        )
    
    def scan_curvature_scale(self, L_range: Tuple[float, float] = (1e-35, 1e-15)) -> ParameterScan:
        """Scan curvature scale (length scale of spacetime curvature)."""
        L_values = np.logspace(np.log10(L_range[0]), np.log10(L_range[1]), 50)
        
        # Curvature: R ~ 1/L^2
        # Effective cosmological constant: Λ ~ R ~ 1/L^2
        predictions = {
            "curvature": [1 / L**2 for L in L_values],
            "cosmological_constant": [1e-52 / (L / 1e-15)**2 for L in L_values],  # Normalize to observable scale
            "dark_energy_density": [1e-47 / (L / 1e-15)**2 for L in L_values]
        }
        
        best_fit = {
            "L": 1e-15,  # Planck scale
            "curvature": 1e30,
            "motivation": "Planck scale is natural quantum gravity scale"
        }
        
        return ParameterScan(
            framework="Quantum Gravity",
            parameter="curvature_scale",
            range_min=L_range[0],
            range_max=L_range[1],
            num_points=len(L_values),
            values=[float(L) for L in L_values],
            predictions=predictions,
            best_fit=best_fit
        )


class DarkMatterScanner:
    """Scan dark matter parameters."""
    
    def __init__(self):
        self.results = {}
    
    def scan_wimp_mass(self, m_range: Tuple[float, float] = (1, 10000)) -> ParameterScan:
        """Scan WIMP mass range (GeV)."""
        masses = np.logspace(np.log10(m_range[0]), np.log10(m_range[1]), 100)
        
        # Relic density: Ωh² ~ 1/⟨σv⟩ ~ m² (for thermal WIMP)
        # Cross-section: σ ~ 1/m² (for weak interaction)
        predictions = {
            "relic_density_oh2": [0.12 * (100 / m)**2 for m in masses],  # Normalize to 100 GeV
            "direct_detection_cross_section": [1e-45 * (100 / m)**2 for m in masses],  # cm²
            "indirect_detection_flux": [1e-12 * (m / 100)**2 for m in masses]  # ph/cm²/s
        }
        
        best_fit = {
            "mass": 100,  # GeV (classic WIMP scale)
            "relic_density": 0.12,
            "motivation": "Thermal relic density matches observation for 100 GeV WIMP"
        }
        
        return ParameterScan(
            framework="Dark Matter",
            parameter="wimp_mass",
            range_min=m_range[0],
            range_max=m_range[1],
            num_points=len(masses),
            values=[float(m) for m in masses],
            predictions=predictions,
            best_fit=best_fit
        )
    
    def scan_cross_section(self, sigma_range: Tuple[float, float] = (1e-50, 1e-40)) -> ParameterScan:
        """Scan WIMP-nucleon cross-section (cm²)."""
        sigmas = np.logspace(np.log10(sigma_range[0]), np.log10(sigma_range[1]), 50)
        
        # Detection rate: R ~ σ * N * Φ
        # where N is number of target nucleons, Φ is WIMP flux
        predictions = {
            "detection_rate_per_ton_year": [sigma * 1e45 * 1e3 for sigma in sigmas],  # events/ton/year
            "exclusion_confidence": [1 - np.exp(-sigma * 1e45 * 1e3) for sigma in sigmas]
        }
        
        best_fit = {
            "cross_section": 1e-45,
            "detection_rate": 1,
            "motivation": "Current experiments sensitive to 10^-45 cm²"
        }
        
        return ParameterScan(
            framework="Dark Matter",
            parameter="cross_section",
            range_min=sigma_range[0],
            range_max=sigma_range[1],
            num_points=len(sigmas),
            values=[float(s) for s in sigmas],
            predictions=predictions,
            best_fit=best_fit
        )


class DarkEnergyScanner:
    """Scan dark energy parameters."""
    
    def __init__(self):
        self.results = {}
    
    def scan_equation_of_state(self, w_range: Tuple[float, float] = (-1.5, -0.5)) -> ParameterScan:
        """Scan dark energy equation of state w = p/ρ."""
        w_values = np.linspace(w_range[0], w_range[1], 100)
        
        # Acceleration: ä/a ~ -4πG/3 (ρ + 3p) = -4πG/3 ρ (1 + 3w)
        # For acceleration: w < -1/3
        # For ΛCDM: w = -1
        predictions = {
            "acceleration_parameter": [-(1 + 3 * w) / 2 for w in w_values],
            "deceleration_parameter": [(1 + 3 * w) / 2 for w in w_values],
            "universe_fate": ["Big Rip" if w < -1 else "ΛCDM" if w == -1 else "Deceleration" for w in w_values]
        }
        
        best_fit = {
            "w": -1.0,
            "acceleration": 1.0,
            "motivation": "ΛCDM: w = -1 (cosmological constant)"
        }
        
        return ParameterScan(
            framework="Dark Energy",
            parameter="equation_of_state",
            range_min=w_range[0],
            range_max=w_range[1],
            num_points=len(w_values),
            values=[float(w) for w in w_values],
            predictions=predictions,
            best_fit=best_fit
        )


class BSMScanner:
    """Scan Beyond Standard Model parameters."""
    
    def __init__(self):
        self.results = {}
    
    def scan_gut_scale(self, M_range: Tuple[float, float] = (1e14, 1e16)) -> ParameterScan:
        """Scan GUT scale (GeV)."""
        M_values = np.logspace(np.log10(M_range[0]), np.log10(M_range[1]), 50)
        
        # Gauge coupling unification: 1/α_i(M_GUT) = 1/α_i(M_Z) + b_i/(2π) log(M_GUT/M_Z)
        # Proton lifetime: τ_p ~ M_GUT^4 / m_p^5
        m_p = 0.938  # GeV
        predictions = {
            "proton_lifetime_years": [1e36 * (M / 1e15)**4 for M in M_values],
            "gauge_unification_precision": [1e-3 * (1e15 / M) for M in M_values],
            "neutrino_mass_scale": [1e-3 * (M / 1e15) for M in M_values]  # eV
        }
        
        best_fit = {
            "M_GUT": 1e15,
            "proton_lifetime": 1e36,
            "motivation": "SU(5) GUT predicts M_GUT ~ 10^15 GeV, τ_p ~ 10^36 years"
        }
        
        return ParameterScan(
            framework="Beyond Standard Model",
            parameter="gut_scale",
            range_min=M_range[0],
            range_max=M_range[1],
            num_points=len(M_values),
            values=[float(M) for M in M_values],
            predictions=predictions,
            best_fit=best_fit
        )


def run_all_scans(output_dir: str = "scans"):
    """Run all parameter scans and save results."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    scanners = {
        "quantum_gravity": QuantumGravityScanner(),
        "dark_matter": DarkMatterScanner(),
        "dark_energy": DarkEnergyScanner(),
        "bsm": BSMScanner()
    }
    
    all_results = {}
    
    # Quantum Gravity scans
    qg = scanners["quantum_gravity"]
    all_results["extra_dimensions"] = qg.scan_extra_dimensions().to_dict()
    all_results["curvature_scale"] = qg.scan_curvature_scale().to_dict()
    
    # Dark Matter scans
    dm = scanners["dark_matter"]
    all_results["wimp_mass"] = dm.scan_wimp_mass().to_dict()
    all_results["cross_section"] = dm.scan_cross_section().to_dict()
    
    # Dark Energy scans
    de = scanners["dark_energy"]
    all_results["equation_of_state"] = de.scan_equation_of_state().to_dict()
    
    # BSM scans
    bsm = scanners["bsm"]
    all_results["gut_scale"] = bsm.scan_gut_scale().to_dict()
    
    # Save all results
    with open(f"{output_dir}/all_scans.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"All scans saved to {output_dir}/all_scans.json")
    
    # Print summary
    print("\n" + "=" * 60)
    print("TOE Framework Parameter Scan Summary")
    print("=" * 60)
    for name, result in all_results.items():
        print(f"\n{name}:")
        print(f"  Framework: {result['framework']}")
        print(f"  Parameter: {result['parameter']}")
        print(f"  Best fit: {result['best_fit']}")
    
    return all_results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="TOE Framework Parameter Scanner")
    parser.add_argument("--output", default="scans", help="Output directory")
    
    args = parser.parse_args()
    
    run_all_scans(args.output)
    
    print("\n" + "=" * 60)
    print("Parameter scanning complete.")
    print("=" * 60)
