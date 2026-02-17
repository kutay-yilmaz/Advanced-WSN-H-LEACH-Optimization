# Advanced Hybrid-LEACH (H-LEACH) Protocol Optimization

This repository presents a comprehensive optimization of the **Low-Energy Adaptive Clustering Hierarchy (LEACH)** protocol for Wireless Sensor Networks (WSNs). The proposed **H-LEACH** model addresses critical challenges such as the "Energy Hole" problem, unbalanced load distribution, and rapid node depletion through a multi-layered optimization strategy.

## 🔬 Project Methodology

The simulation transitions from a standard homogeneous network to a sophisticated hybrid environment. It incorporates mathematical energy modeling based on the **First Order Radio Model**, accounting for both Free Space and Multipath fading channels.

### Optimization Layers

| Optimization | Description | Impact on Network |
| :--- | :--- | :--- |
| **Network Heterogeneity** | Integration of 10% "Advanced Nodes" with 2.0x higher initial energy (1.0J vs 0.5J). | Enhances overall network resilience and prolongs the stability period. |
| **Sink Mobility** | The Base Station (Sink) follows a dynamic circular trajectory instead of remaining static. | Eliminates the "Energy Hole" problem by reducing the average communication distance. |
| **Energy-Aware Threshold** | CH election probability is dynamically weighted by the node's residual energy. | Prevents low-energy nodes from assuming power-intensive leadership roles. |
| **Data Aggregation** | Cluster Heads implement a 50% data compression ratio before long-range transmission. | Reduces the transmission overhead and conserves energy for the entire cluster. |

---

## 📊 Performance Analysis

The repository includes a comparative analysis across three distinct developmental stages to validate the performance of the proposed algorithm.

1. **Baseline (Standard LEACH):** Homogeneous nodes with a static central Sink.
2. **Intermediate (Mobile Sink):** Implementation of Sink mobility in a homogeneous environment.
3. **Proposed (H-LEACH):** Full integration of mobility, heterogeneity, and energy-aware threshold logic.

### Comparative Metrics

| Metric | Standard LEACH | Proposed H-LEACH | Improvement Status |
| :--- | :--- | :--- | :--- |
| **First Node Dead (FND)** | ~1150 Rounds | ~1300 Rounds | **+13% Extension** |
| **Stability Period** | Moderate | High | **Superior** |
| **Energy Balance** | Stochastic / Random | Optimized / Weighted | **Excellent** |
| **Data Throughput** | 1.0x (Raw Data) | 2.0x (Compressed) | **High Efficiency** |

![Comparative Analysis Results](results/Comparative_Analysis_Dashboard.png)

---

## 📂 Repository Structure

* **src/**: Contains the primary simulation engine (`H_LEACH_Simulation.py`).
* **results/**: Stores the `Comparative_Analysis_Dashboard.png` and other performance metrics.
* **archive/**: Legacy scripts and initial radio model analysis for theoretical verification.

---

## 🚀 Execution Guide

1. **Environment Setup:** Ensure Python 3.x is installed.
2. **Install Dependencies:**
```bash
pip install numpy matplotlib
Run Simulation:

Bash

python src/H_LEACH_Simulation.py
👨‍💻 Author
Ismail Kutay Yilmaz Electrical & Electronics Engineering Project specialized in Energy-Efficient Wireless Communication and Network Optimization.
