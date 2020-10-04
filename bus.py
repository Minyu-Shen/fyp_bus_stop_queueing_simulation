from collections import defaultdict
import numpy as np
import torch


class Travel_Record(object):
    ### for recording system performance
    def __init__(self):
        self.queue_delay = 0.0
        self.berth_delay = 0.0

    def update_stats(self, type, value):
        if type == "queue_delay":
            self.queue_delay += value
        elif type == "berth_delay":
            self.berth_delay += value


class Bus(object):
    def __init__(self, ln_id, bus_id, mean_service_time, cv_service_time):
        self.ln_id = ln_id
        self.bus_id = bus_id
        self.mean_service_time = mean_service_time
        self.cv_service_time = cv_service_time

        self.rest_service_time_this_stop = self._generate_random_service_time()

        # for stats
        self.record = Travel_Record()

    def _generate_random_service_time(self):
        shape = 1 / (self.cv_service_time ** 2)
        scale = self.mean_service_time / shape
        serv_time = np.random.gamma(shape, scale, 1)
        return np.asscalar(serv_time)
