import numpy as np
import math
import random


def get_dspt_times(sim_duration, schd_hdw, perturb_cv, distribution_type):
    if distribution_type == "Exponential":
        rate = 1 / schd_hdw
        assert perturb_cv == 1.0, "exponential distribution has only one parameter, which is the mean arrival interval (headway)"
        sts = []
        lasttime = 0
        while lasttime <= (sim_duration):
            next_st = -math.log(1.0 - random.random()) / rate
            lasttime += next_st
            sts.append(lasttime)
        sts.reverse()
        return sts

    elif distribution_type == "Gaussian":
        total_bus_no = math.ceil(sim_duration / schd_hdw) + 1
        perfect_times = [schd_hdw * (x + 1) for x in range(total_bus_no)]
        if perturb_cv > 0:
            perturb_std = perturb_cv * schd_hdw
            perturb_times = list(np.random.normal(size=total_bus_no) * perturb_std)
            dspt_times = [x + y for x, y in zip(perfect_times, perturb_times)]
            dspt_times.sort()
            dspt_times.reverse()
            return dspt_times
        else:
            perfect_times.reverse()
            return perfect_times


# if __name__ == "__main__":
#     print(type(gaussian_unit()))