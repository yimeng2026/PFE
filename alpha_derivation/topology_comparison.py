#!/usr/bin/env python3
"""
拓扑修正脚本：对比 S³、T³、ℝ³ 的连通性分布

核心假设：不同拓扑结构的因果网络具有不同的连通性分布
这会影响电荷的涌现值和精细结构常数 α

PFE Phase 2: alpha_derivation 工程化
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import json

# Add alpha_derivation to path for imports
sys.path.insert(0, str(Path(__file__).parent))


class TopologyComparison:
    """Compare causal networks on different topologies."""
    
    def __init__(self, num_nodes: int = 5000, dim: int = 4):
        self.num_nodes = num_nodes
        self.dim = dim
        self.results = {}
        
    def generate_flat_network(self) -> dict:
        """Generate causal network on flat ℝ³ topology."""
        # Random points in [0,1]^dim with time ordering
        nodes = np.random.rand(self.num_nodes, self.dim)
        # Sort by time coordinate (first coordinate)
        nodes = nodes[np.argsort(nodes[:, 0])]
        
        # Connect if causal (time-ordered and within light cone)
        edges = 0
        degrees = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                dt = nodes[j, 0] - nodes[i, 0]
                dx = np.linalg.norm(nodes[j, 1:] - nodes[i, 1:])
                if dx < dt:  # Causal: spatial separation < time separation
                    edges += 1
                    degrees[i] += 1
                    degrees[j] += 1
        
        return {
            "topology": "flat",
            "nodes": self.num_nodes,
            "edges": edges,
            "mean_degree": float(np.mean(degrees)),
            "std_degree": float(np.std(degrees)),
            "max_degree": int(np.max(degrees)),
            "degree_distribution": degrees.tolist()
        }
    
    def generate_torus_network(self) -> dict:
        """Generate causal network on T³ topology (periodic boundary)."""
        # Random points on torus [0,1]^dim with periodic boundaries
        nodes = np.random.rand(self.num_nodes, self.dim)
        nodes = nodes[np.argsort(nodes[:, 0])]
        
        edges = 0
        degrees = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                dt = nodes[j, 0] - nodes[i, 0]
                # Periodic spatial distance (minimum image convention)
                dx_spatial = np.abs(nodes[j, 1:] - nodes[i, 1:])
                dx_spatial = np.minimum(dx_spatial, 1 - dx_spatial)
                dx = np.linalg.norm(dx_spatial)
                if dx < dt:
                    edges += 1
                    degrees[i] += 1
                    degrees[j] += 1
        
        return {
            "topology": "torus",
            "nodes": self.num_nodes,
            "edges": edges,
            "mean_degree": float(np.mean(degrees)),
            "std_degree": float(np.std(degrees)),
            "max_degree": int(np.max(degrees)),
            "degree_distribution": degrees.tolist()
        }
    
    def generate_sphere_network(self) -> dict:
        """Generate causal network on S³ topology (3-sphere)."""
        # Random points on 3-sphere (embedded in ℝ⁴)
        # Generate 4D Gaussian points and normalize to unit sphere
        nodes_4d = np.random.randn(self.num_nodes, 4)
        nodes_4d = nodes_4d / np.linalg.norm(nodes_4d, axis=1)[:, np.newaxis]
        
        # Use one coordinate as "time" and sort
        time_coord = nodes_4d[:, 0]
        nodes_4d = nodes_4d[np.argsort(time_coord)]
        
        edges = 0
        degrees = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                # Geodesic distance on S³ (great circle distance)
                dot_product = np.clip(np.dot(nodes_4d[i], nodes_4d[j]), -1, 1)
                geodesic_dist = np.arccos(dot_product)
                
                # "Time" separation
                dt = nodes_4d[j, 0] - nodes_4d[i, 0]
                
                if geodesic_dist < dt and dt > 0:
                    edges += 1
                    degrees[i] += 1
                    degrees[j] += 1
        
        return {
            "topology": "sphere",
            "nodes": self.num_nodes,
            "edges": edges,
            "mean_degree": float(np.mean(degrees)),
            "std_degree": float(np.std(degrees)),
            "max_degree": int(np.max(degrees)),
            "degree_distribution": degrees.tolist()
        }
    
    def compare_topologies(self, trials: int = 5) -> dict:
        """Run comparison across all topologies."""
        print(f"Topology Comparison: {self.num_nodes} nodes, d={self.dim}, {trials} trials")
        print("=" * 60)
        
        topologies = {
            "flat": self.generate_flat_network,
            "torus": self.generate_torus_network,
            "sphere": self.generate_sphere_network
        }
        
        for topo_name, generator in topologies.items():
            print(f"\nTopology: {topo_name}")
            trials_results = []
            for t in range(trials):
                result = generator()
                trials_results.append(result)
                print(f"  Trial {t+1}: mean_degree = {result['mean_degree']:.2f}, edges = {result['edges']}")
            
            mean_degrees = [r['mean_degree'] for r in trials_results]
            self.results[topo_name] = {
                "mean_degree_mean": float(np.mean(mean_degrees)),
                "mean_degree_std": float(np.std(mean_degrees)),
                "edges_mean": float(np.mean([r['edges'] for r in trials_results])),
                "trials": trials_results
            }
            
            print(f"  Mean degree: {self.results[topo_name]['mean_degree_mean']:.2f} ± {self.results[topo_name]['mean_degree_std']:.2f}")
        
        return self.results
    
    def plot_comparison(self, save_path: str = "topology_comparison.png"):
        """Plot degree distribution comparison."""
        if not self.results:
            print("No results to plot. Run compare_topologies first.")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Degree distributions
        colors = {'flat': 'blue', 'torus': 'green', 'sphere': 'red'}
        for topo_name, result in self.results.items():
            # Use first trial for distribution plot
            degrees = result['trials'][0]['degree_distribution']
            ax1.hist(degrees, bins=50, alpha=0.5, label=topo_name, color=colors.get(topo_name, 'gray'))
        
        ax1.set_xlabel('Degree')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Degree Distribution by Topology')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Mean degree comparison
        topo_names = list(self.results.keys())
        mean_degrees = [self.results[t]['mean_degree_mean'] for t in topo_names]
        std_degrees = [self.results[t]['mean_degree_std'] for t in topo_names]
        
        ax2.bar(topo_names, mean_degrees, yerr=std_degrees, capsize=5, 
                color=[colors.get(t, 'gray') for t in topo_names], alpha=0.7)
        ax2.set_ylabel('Mean Degree')
        ax2.set_title('Mean Connectivity by Topology')
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved: {save_path}")
    
    def save_results(self, filename: str = "topology_comparison_results.json"):
        """Save results to JSON."""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved: {filename}")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Topology Comparison for Causal Networks")
    parser.add_argument("--nodes", type=int, default=5000, help="Number of nodes per network")
    parser.add_argument("--dim", type=int, default=4, help="Spacetime dimension")
    parser.add_argument("--trials", type=int, default=5, help="Trials per topology")
    parser.add_argument("--output", default="topology_comparison", help="Output prefix")
    
    args = parser.parse_args()
    
    comparator = TopologyComparison(num_nodes=args.nodes, dim=args.dim)
    comparator.compare_topologies(args.trials)
    comparator.plot_comparison(f"{args.output}.png")
    comparator.save_results(f"{args.output}_results.json")
    
    print("\n" + "=" * 60)
    print("Topology comparison complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
