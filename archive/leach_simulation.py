import numpy as np
import matplotlib.pyplot as plt
import random

class NetworkSettings:
    def __init__(self):
        self.width = 100
        self.height = 100
        self.sink_x = 50
        self.sink_y = 50
        self.n = 100
        self.e_init = 0.5 
        self.e_elec = 50 * 1e-9     
        self.e_fs = 10 * 1e-12      
        self.e_mp = 0.0013 * 1e-12  
        self.e_da = 5 * 1e-9        
        self.p = 0.1                
        self.packet_bits = 4000     
        self.max_rounds = 1500 

class SensorNode:
    def __init__(self, node_id, config):
        self.id = node_id
        self.x = random.uniform(0, config.width)
        self.y = random.uniform(0, config.height)
        self.energy = config.e_init
        self.is_alive = True
        self.role = "member"
        self.d_sink = np.sqrt((self.x - config.sink_x)**2 + (self.y - config.sink_y)**2)
        self.ch_timer = 0 
        
    def update_energy(self):
        if self.energy <= 0:
            self.energy = 0
            self.is_alive = False

    def decide_leadership(self, r, config, network_avg_dist):
        if not self.is_alive or self.ch_timer > 0:
            self.role = "member"
            if self.ch_timer > 0: self.ch_timer -= 1
            return False
        
        t_base = config.p / (1 - config.p * (r % int(1/config.p)))
        f_energy = self.energy / config.e_init
        f_dist = network_avg_dist / (self.d_sink + 1e-9)
        threshold = t_base * f_energy * f_dist
        
        if random.random() < threshold:
            self.role = "head"
            self.ch_timer = int(1/config.p) - 1
            return True
        self.role = "member"
        return False

    def consume_tx(self, dist, bits, config):
        d0 = np.sqrt(config.e_fs / config.e_mp)
        if dist < d0:
            e_tx = (config.e_elec * bits) + (config.e_fs * bits * (dist**2))
        else:
            e_tx = (config.e_elec * bits) + (config.e_mp * bits * (dist**4))
        self.energy -= e_tx
        self.update_energy()

class SimulationEngine:
    def __init__(self):
        self.config = NetworkSettings()
        self.nodes = [SensorNode(i, self.config) for i in range(self.config.n)]
        self.stats = {'alive': [], 'energy': [], 'packets': []}
        self.total_packets = 0

    def run(self):
        print("Akilli LEACH+ (Energy & Distance Aware) baslatildi...")
        for r in range(self.config.max_rounds):
            alive_nodes = [n for n in self.nodes if n.is_alive]
            if not alive_nodes:
                print(f"Ag {r}. turda tamamen coktu.")
                break
            
            avg_dist = np.mean([n.d_sink for n in alive_nodes])
            heads = []
            members = []
            
            for n in alive_nodes:
                if n.decide_leadership(r, self.config, avg_dist):
                    heads.append(n)
                else:
                    members.append(n)
            
            for m in members:
                if heads:
                    dists = [np.sqrt((m.x - h.x)**2 + (m.y - h.y)**2) for h in heads]
                    idx = np.argmin(dists)
                    m.consume_tx(dists[idx], self.config.packet_bits, self.config)
                    heads[idx].energy -= (self.config.e_elec + self.config.e_da) * self.config.packet_bits
                else:
                    m.consume_tx(m.d_sink, self.config.packet_bits, self.config)
                    self.total_packets += 1

            for h in heads:
                h.consume_tx(h.d_sink, self.config.packet_bits, self.config)
                self.total_packets += 1

            self.stats['alive'].append(len(alive_nodes))
            self.stats['energy'].append(sum(n.energy for n in alive_nodes))
            self.stats['packets'].append(self.total_packets)
            
            if r % 100 == 0:
                print(f"Islem devam ediyor... Tur: {r}")

        self.visualize(heads)

    def visualize(self, current_heads):
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Network Lifetime
        axes[0,0].plot(self.stats['alive'], color='green')
        axes[0,0].set_title("Network Lifetime (Alive Nodes)")
        axes[0,0].grid(True)

        # 2. Total Energy
        axes[0,1].plot(self.stats['energy'], color='blue')
        axes[0,1].set_title("Total Residual Energy (J)")
        axes[0,1].grid(True)

        # 3. Throughput
        axes[1,0].plot(self.stats['packets'], color='red')
        axes[1,0].set_title("Throughput (Total Packets)")
        axes[1,0].grid(True)

        # 4. Final Topology (Show)
        axes[1,1].scatter(self.config.sink_x, self.config.sink_y, color='red', marker='X', s=200, label='Sink')
        for n in self.nodes:
            if n.is_alive:
                if n.role == "head":
                    axes[1,1].scatter(n.x, n.y, color='orange', marker='*', s=150, edgecolors='black')
                    axes[1,1].plot([n.x, self.config.sink_x], [n.y, self.config.sink_y], 'r--', alpha=0.2)
                else:
                    axes[1,1].scatter(n.x, n.y, color='blue', s=20, alpha=0.4)
                    if current_heads:
                        dists = [np.sqrt((n.x - h.x)**2 + (n.y - h.y)**2) for h in current_heads]
                        nearest_ch = current_heads[np.argmin(dists)]
                        axes[1,1].plot([n.x, nearest_ch.x], [n.y, nearest_ch.y], 'k-', alpha=0.05)
        
        axes[1,1].set_title("Final Round Clustering Topology")
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    sim = SimulationEngine()
    sim.run()