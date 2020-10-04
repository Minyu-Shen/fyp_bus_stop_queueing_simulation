from config import Sim_Config
from simulator import Simulator

sim_config = Sim_Config()
simulator = Simulator(sim_config)
round = 2  # you can run the simulation multiple rounds and take the mean. When doing so, please don't forget to reset the simulator at the end of each round.

for _ in range(round):

    for _ in range(simulator.sim_config.sim_duration):
        simulator.move_one_step()

    # collect the statistics (e.g., bus delays) for all the buses and output the metric of interest
    bus_count = 0
    total_delay = 0.0
    for ln, bus_dict_each_ln in simulator.ln_total_bus_dict.items():
        for bus in bus_dict_each_ln.values():
            bus_count += 1
            total_delay += bus.record.queue_delay + bus.record.berth_delay

    print(total_delay / bus_count)

    simulator.reset()
