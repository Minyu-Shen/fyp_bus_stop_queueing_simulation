class Stop(object):
    def __init__(self, berth_num):
        self._berth_num = berth_num

        self._entry_queue = []
        self._buses_in_berth = [None] * self._berth_num

    def reset(self):
        self._entry_queue = []
        self._buses_in_berth = [None] * self._berth_num

    def enter_bus(self, bus):
        self._entry_queue.append(bus)

    def operation(self, delta_t, curr_time):
        self._queueing(curr_time, delta_t)
        self._boarding(delta_t)
        self._finishing(curr_time, delta_t)

    def _boarding(self, delta_t):
        for berth, bus in enumerate(self._buses_in_berth):
            if bus is None:
                continue
            bus.rest_service_time_this_stop -= delta_t

    def _finishing(self, curr_time, delta_t):
        # holding is (maybe) applied only after the boarding process finishes
        for berth, bus in enumerate(self._buses_in_berth):
            if bus is None:
                continue  # no bus in this berth
            # 1. check if the generated random service time is finished or not
            if bus.rest_service_time_this_stop > 0.0:  # not finished
                continue
            if self._check_out(berth) is False:  # the bus is blocked
                bus.record.update_stats("berth_delay", delta_t)
            else:  # the bus can leave
                self._leaving_operations_for_bus(bus, berth)

    def _leaving_operations_for_bus(self, bus, berth):
        self._buses_in_berth[berth] = None

    def _queueing(self, curr_time, delta_t):
        if len(self._entry_queue) == 0:
            return
        bus = self._entry_queue[0]
        target_berth = self._check_in()
        if target_berth >= 0:  # has available berth, enter
            self._buses_in_berth[target_berth] = bus
            self._entry_queue.pop(0)

        for _, bus in enumerate(self._entry_queue):
            bus.record.update_stats("queue_delay", delta_t)

    def _check_in(self):
        target_berth = -1  # negative means no berth is available
        for b in range(len(self._buses_in_berth) - 1, -1, -1):
            if self._buses_in_berth[b] == None:
                target_berth = b
            else:
                break
        return target_berth

    def _check_out(self, which_berth):
        if which_berth == 0:  # most downstream berth, directly leave
            return True
        for b in range(which_berth - 1, -1, -1):
            if self._buses_in_berth[b] != None:
                break
            else:
                if b == 0:  # all the most downstream berths are clear
                    return True
        return False

    def reset(self):
        self._entry_queue = []
        self._buses_in_berth = [None] * self._berth_num
