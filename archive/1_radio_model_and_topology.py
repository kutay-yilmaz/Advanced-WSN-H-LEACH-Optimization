import numpy as np
import matplotlib.pyplot as plt
import random

class NetworkConfig:
    def __init__(self):
        self.width = 100
        self.height = 100
        self.sink_x = 50
        self.sink_y = 50
        self.n = 100
        self.e_init = 0.5
        # mit standart radyo parametreleri
        self.e_elec = 50 * 1e-9
        self.e_fs = 10 * 1e-12
        self.e_mp = 0.0013 * 1e-12
        self.bits = 4000

def calculate_energy_cost(dist, config):
    # d0: esik mesafesi hesabi
    d0 = np.sqrt(config.e_fs / config.e_mp)
    if dist < d0:
        return (config.e_elec * config.bits) + (config.e_fs * config.bits * (dist**2))
    else:
        return (config.e_elec * config.bits) + (config.e_mp * config.bits * (dist**4))

config = NetworkConfig()
x = np.linspace(0, 100, 100)
y = np.linspace(0, 100, 100)
x_mesh, y_mesh = np.meshgrid(x, y)
distances = np.sqrt((x_mesh - config.sink_x)**2 + (y_mesh - config.sink_y)**2)

# her nokta icin enerji maliyeti hesabi
costs = np.vectorize(calculate_energy_cost)(distances, config)

plt.figure(figsize=(10, 8))
cp = plt.contourf(x_mesh, y_mesh, costs, cmap='YlOrRd', levels=50)
plt.colorbar(cp).set_label('energy consumption per packet (joules)')
plt.scatter(config.sink_x, config.sink_y, color='blue', marker='X', s=200, label='base station')
plt.title('radio energy model: energy cost vs. spatial distribution')
plt.xlabel('x (meters)')
plt.ylabel('y (meters)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()