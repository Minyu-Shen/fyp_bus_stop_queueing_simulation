from arena import get_dspt_times
from math import ceil
from bus import Bus
from collections import defaultdict


class Generator(object):
    def __init__(self, ln_arrival_info, ln_service_info, sim_duration):
        self._ln_no = len(ln_arrival_info)
        self._ln_arrival_info_dict = ln_arrival_info
        self._ln_service_info_dict = ln_service_info
        self._sim_duration = sim_duration

        self._ln_dspted_num_dict = {ln: 0 for ln in range(self._ln_no)}
        self._ln_arrive_times = {}  # ln -> dspt moments
        self._generate_bus_arrival_time()

    def _generate_bus_arrival_time(self):
        for ln in range(self._ln_no):
            line_info_dict = self._ln_arrival_info_dict[ln]
            schd_hdw, perturb_cv, distribution_type = (
                line_info_dict["mean_arrival_hdw"],
                line_info_dict["cv_arrival_hdw"],
                line_info_dict["hdw_distribution_type"],
            )
            self._ln_arrive_times[ln] = get_dspt_times(
                self._sim_duration, schd_hdw, perturb_cv, distribution_type
            )

    def dispatch(self, curr_time):
        """ At each time step, check if any line arrives, if yes, dispatch to the stop"""
        arrived_buses = []
        for ln in range(self._ln_no):
            arrive_times = self._ln_arrive_times[ln]
            # if len(dspt_times) == 0: return dspt_buses
            if arrive_times[-1] <= curr_time:
                # dspt_buses.append(bus)
                mean_time, cv_time = (
                    self._ln_service_info_dict[ln]["mean_service_time"],
                    self._ln_service_info_dict[ln]["cv_service_time"],
                )
                bus = Bus(ln, self._ln_dspted_num_dict[ln], mean_time, cv_time)
                self._ln_dspted_num_dict[ln] += 1
                arrived_buses.append(bus)
                arrive_times.pop()
        return arrived_buses

    def reset(self):
        self._ln_dspted_num_dict = {ln: 0 for ln in range(self._ln_no)}
        self._generate_bus_arrival_time()


if __name__ == "__main__":
    pass
