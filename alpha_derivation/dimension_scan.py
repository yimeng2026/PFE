#!/usr/bin/env python3
"""
维度扫描脚本：验证精细结构常数 α 随因果网络维度变化

核心假设：α(d) = C(d) / (4π) 其中 C(d) 是 d 维因果网络的平均连通性

PFE Phase 2: alpha_derivation 工程化
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import json

# Add alpha_derivation to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from _causal_network_simulation import CausalNetwork, analyze_connectivity, charge_from_connectivity
    HAS_SIMULATION = True
except ImportError:
    HAS_SIMULATION = False
    print("Warning: causal_network_simulation not available, using simplified model")


class DimensionScanner:
    """Scan alpha across dimensions d=2,3,4,5,6."""
    
    def __init__(self, num_nodes: int = 10000, trials: int = 10):
        self.num_nodes = num_nodes
        self.trials = trials
        self.results = {}
        
    def run_single_trial(self, dim: int, topology: str = "flat") -> dict:
        """Run single trial for given dimension."""
        if HAS_SIMULATION:
            network = CausalNetwork(dim=dim, num_nodes=self.num_nodes)
            network.generate_nodes()
            network.connect_causal_edges()
            stats = analyze_connectivity(network)
            charge = charge_from_connectivity(stats["mean_degree"])
            alpha = charge**2 / (4 * np.pi)
        else:
            # Simplified model: alpha ~ 1/d
            mean_degree = 2 * dim  # Simplified
            charge = np.sqrt(mean_degree / 10)  # Simplified
            alpha = charge**2 / (4 * np.pi)
        
        return {
            "dim": dim,
            "topology": topology,
            "mean_degree": mean_degree if HAS_SIMULATION else 2 * dim,
            "charge": float(charge),
            "alpha": float(alpha),
            "alpha_inv": float(1/alpha) if alpha > 0 else float('inf')
        }
    
    def scan_dimensions(self, dimensions: list = [2, 3, 4, 5, 6]) -> dict:
        """Run full dimension scan."""
        print(f"Dimension Scan: {self.num_nodes} nodes, {self.trials} trials per dimension")
        print("=" * 60)
        
        for dim in dimensions:
            print(f"\nDimension d={dim}:")
            trials = []
            for t in range(self.trials):
                result = self.run_single_trial(dim)
                trials.append(result)
                print(f"  Trial {t+1}: α = {result['alpha']:.6f}, 1/α = {result['alpha_inv']:.2f}")
            
            alphas = [r['alpha'] for r in trials]
            self.results[dim] = {
                "alpha_mean": float(np.mean(alphas)),
                "alpha_std": float(np.std(alphas)),
                "alpha_inv_mean": float(np.mean([1/a for a in alphas])),
                "alpha_inv_std": float(np.std([1/a for a in alphas])),
                "trials": trials
            }
            
            print(f"  Mean α = {self.results[dim]['alpha_mean']:.6f} ± {self.results[dim]['alpha_std']:.6f}")
            print(f"  Mean 1/α = {self.results[dim]['alpha_inv_mean']:.2f} ± {self.results[dim]['alpha_inv_std']:.2f}")
        
        return self.results
    
    def plot_results(self, save_path: str = "dimension_scan_alpha.png"):
        """Plot alpha vs dimension."""
        if not self.results:
            print("No results to plot. Run scan_dimensions first.")
            return
        
        dims = sorted(self.results.keys())
        alpha_means = [self.results[d]['alpha_mean'] for d in dims]
        alpha_stds = [self.results[d]['alpha_std'] for d in dims]
        alpha_inv_means = [self.results[d]['alpha_inv_mean'] for d in dims]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Alpha plot
        ax1.errorbar(dims, alpha_means, yerr=alpha_stds, marker='o', capsize=5, linewidth=2)
        ax1.axhline(y=1/137.036, color='r', linestyle='--', label='Experimental α (1/137.036)')
        ax1.set_xlabel('Dimension d')
        ax1.set_ylabel('α = e²/4π')
        ax1.set_title('Fine-Structure Constant vs Dimension')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 1/Alpha plot
        ax2.errorbar(dims, alpha_inv_means, yerr=[self.results[d]['alpha_inv_std'] for d in dims],
                     marker='o', capsize=5, linewidth=2, color='green')
        ax2.axhline(y=137.036, color='r', linestyle='--', label='Experimental 1/α = 137.036')
        ax2.set_xlabel('Dimension d')
        ax2.set_ylabel('1/α')
        ax2.set_title('Inverse Fine-Structure Constant vs Dimension')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved: {save_path}")
    
    def save_results(self, filename: str = "dimension_scan_results.json"):
        """Save results to JSON."""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved: {filename}")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dimension Scan for Alpha")
    parser.add_argument("--nodes", type=int, default=10000, help="Number of nodes per network")
    parser.add_argument("--trials", type=int, default=10, help="Trials per dimension")
    parser.add_argument("--dims", type=int, nargs='+', default=[2, 3, 4, 5, 6], help="Dimensions to scan")
    parser.add_argument("--output", default="dimension_scan", help="Output prefix")
    
    args = parser.parse_args()
    
    scanner = DimensionScanner(num_nodes=args.nodes, trials=args.trials)
    scanner.scan_dimensions(args.dims)
    scanner.plot_results(f"{args.output}_alpha.png")
    scanner.save_results(f"{args.output}_results.json")
    
    print("\n" + "=" * 60)
    print("Dimension scan complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
