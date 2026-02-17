import numpy as np
import matplotlib.pyplot as plt
import random
import math

class NetworkConfig:
    def __init__(self):
        self.width, self.height = 100, 100
        self.n_nodes = 100
        self.advanced_ratio = 0.1 
        self.Eo, self.E_adv = 0.5, 1.0           
        self.E_elec = 50 * 1e-9
        self.E_fs, self.E_mp = 10 * 1e-12, 0.0013 * 1e-12
        self.E_da = 5 * 1e-9       
        self.packet_bits = 4000
        self.p = 0.1       
        self.rounds = 1500
        self.aggregation = 0.5 

class Node:
    def __init__(self, id, x, y, is_advanced, config):
        self.id, self.x, self.y = id, x, y
        self.is_advanced = is_advanced
        self.energy = config.E_adv if is_advanced else config.Eo
        self.initial_energy = self.energy
        self.alive = True

    def dist(self, tx, ty):
        return math.sqrt((self.x - tx)**2 + (self.y - ty)**2)

class WSN_Engine:
    def __init__(self, config, mode='standard'):
        self.cfg, self.mode = config, mode
        self.nodes, self.stats = [], {'alive': [], 'packets': []}
        self.total_packets = 0
        self._init_nodes()

    def _init_nodes(self):
        for i in range(self.cfg.n_nodes):
            x, y = random.uniform(0, self.cfg.width), random.uniform(0, self.cfg.height)
            is_adv = True if (self.mode == 'hybrid' and i < int(self.cfg.n_nodes*self.cfg.advanced_ratio)) else False
            self.nodes.append(Node(i, x, y, is_adv, self.cfg))

    def _energy_model(self, dist, bits):
        d0 = math.sqrt(self.cfg.E_fs / self.cfg.E_mp)
        return bits * (self.cfg.E_elec + (self.cfg.E_fs * dist**2 if dist < d0 else self.cfg.E_mp * dist**4))

    def run(self):
        for r in range(self.cfg.rounds):
            # Sink Position Logic
            sx, sy = (50 + 40*math.cos(r/50), 50 + 40*math.sin(r/50)) if self.mode in ['mobile', 'hybrid'] else (50, 50)
            alive = [n for n in self.nodes if n.alive]
            if not alive: break
            
            # CH Election
            heads = []
            for n in alive:
                p_eff = self.cfg.p * (n.energy / n.initial_energy) if self.mode == 'hybrid' else self.cfg.p
                T = p_eff / (1 - p_eff * (r % (1/p_eff))) if (r % (1/p_eff)) != 0 else 0
                if random.random() < T:
                    heads.append(n)

            if heads:
                for n in [nd for nd in alive if nd not in heads]:
                    ch = min(heads, key=lambda h: n.dist(h.x, h.y))
                    n.energy -= self._energy_model(n.dist(ch.x, ch.y), self.cfg.packet_bits)
                    ch.energy -= self.cfg.E_elec * self.cfg.packet_bits
                    if n.energy <= 0: n.alive = False
                for h in heads:
                    h.energy -= self.cfg.E_da * self.cfg.packet_bits
                    bits = self.cfg.packet_bits * self.cfg.aggregation if self.mode == 'hybrid' else self.cfg.packet_bits
                    h.energy -= self._energy_model(h.dist(sx, sy), bits)
                    if h.energy <= 0: h.alive = False
                    else: self.total_packets += 1
            
            self.stats['alive'].append(len([n for n in self.nodes if n.alive]))
            self.stats['packets'].append(self.total_packets)
        return self.stats

if __name__ == "__main__":
    conf = NetworkConfig()
    res_std = WSN_Engine(conf, mode='standard').run()
    res_mob = WSN_Engine(conf, mode='mobile').run()
    res_hyb = WSN_Engine(conf, mode='hybrid').run()

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(res_std['alive'], 'r--', label='1. Standard LEACH')
    plt.plot(res_mob['alive'], 'b:', label='2. Mobile Sink Only')
    plt.plot(res_hyb['alive'], 'g-', linewidth=2, label='3. Proposed H-LEACH (Final)')
    plt.title('Network Lifetime Comparison')
    plt.legend(); plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(res_std['packets'], 'r--', res_mob['packets'], 'b:', res_hyb['packets'], 'g-')
    plt.title('Throughput Analysis'); plt.grid(True, alpha=0.3)
    
    plt.savefig("results/Comparative_Analysis_Dashboard.png")
    plt.show()