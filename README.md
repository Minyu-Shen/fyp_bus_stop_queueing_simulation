# fyp_bus_stop_queueing_simulation

## Download

1. Click the green "Code" button and download the codes as zip file.
2. If you are familiar with the "git" tool, feel free to "git clone" it.

## Updates on Jan 26, 2021
1. This update added a boolean variable (“self.is_capacity_case") in the “config.py” to distinguish whether the simulation is for capacity or delay case. "True” means the capacity case while "False" means the delay one. If you are not interested in the capacity case, just set it to be False.
2. In the "main.py", this update gives an example showing how to get different metrics (average bus delay or capacity) for different parameters, e.g., the coefficent of variation in service time used in the code. Other parameters like berth number and arrival rate also apply.



## Introduction

This repository presents a discrete time-based simulation for emulating buses' queueing phenomenon at a single stop where the number of berths is limited. The entry of the program is located in the "main.py". (You can also start reading the code from there.)

Bus arrival process follows certain distributions, which is implemented in the "bus_generator.py" module. The arrived bus will first go to the entry queue of stop (in "stop.py" module). If the most-upstream berth is empty, it can then enter the stop for boarding and alighting passengers. The bus that is allowed to enter will advance until encountering either an occupied berth or the downstream-most berth. After service, it will eventually leave the stop only after any further downstream berths are all emptied. This is the so-called "First-In-First-Out" queueing rule.

Note that this repository can simulate multiple bus lines with different arrival and service distributions. Different parameters can be modified in the "config.py" module. The statistics of interest (e.g., average bus delay) are stored in each "bus" object. You can retrieve them after you finish one simulation round, whose duration can also be set in the "config.py".
