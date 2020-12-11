import numpy as np
from numpy.lib.utils import info


class Sim_Config(object):
    def __init__(self):
        self.delta_t = 1.0 # second
        self.sim_duration = int(3600 * 150) # 150 hours
        self.berth_num = 2
        self.ln_arrival_dict, self.ln_service_dict = self._generate_line_info()

    def _generate_line_info(self):
        # key is line_no, value is the line arrival information
        # arrival time interval follows a distribution, with the first being bus arrival flow (buses/hr), the second the coefficient of variation
        ln_arrival_dict = {
            0: {
                "mean_arrival_hdw": 3600
                / 200,  # the interval between two consecutively-arrived buses (seconds)
                "cv_arrival_hdw": 1.0,
                "hdw_distribution_type": "Exponential",
            }
        }

        # key is line_no, value is line service information
        # service time follows a distribution, with the first being mean service time (seconds), the second the coefficient of variation
        ln_service_dict = {0: {"mean_service_time": 25, "cv_service_time": 0.5}}

        return ln_arrival_dict, ln_service_dict
