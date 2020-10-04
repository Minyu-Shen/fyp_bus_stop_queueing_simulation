from bus_generator import Generator
from collections import defaultdict
from stop import Stop


class Simulator(object):
    def __init__(self, sim_config):
        self.delta_t = sim_config.delta_t
        self.sim_config = sim_config
        # init bus generator (for scheduling arrivals)
        self.generator = Generator(
            sim_config.ln_arrival_dict,
            sim_config.ln_service_dict,
            self.sim_config.sim_duration,
        )

        ### init the stop
        self.stop = Stop(sim_config.berth_num)

        # running properties
        self._curr_time = 0
        self.ln_total_bus_dict = defaultdict(dict)

    def reset(self):
        self.generator.reset()
        self.stop.reset()
        self._curr_time = 0
        self.ln_total_bus_dict = defaultdict(dict)

    def move_one_step(self):
        dspt_buses = self.generator.dispatch(self._curr_time)

        # doing nothing ...
        for dspt_bus in dspt_buses:
            self.stop.enter_bus(dspt_bus)
            self.ln_total_bus_dict[dspt_bus.ln_id][dspt_bus.bus_id] = dspt_bus

        self.stop.operation(self.delta_t, self._curr_time)
        self._curr_time += self.delta_t
