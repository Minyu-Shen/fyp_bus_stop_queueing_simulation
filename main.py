from config import Sim_Config
from simulator import Simulator

cv_service_times_to_simulated = [0.1, 0.3, 0.5, 0.7]
plot_result_dict = {cv: None for cv in cv_service_times_to_simulated}  # cv -> result

for cv_service_time in cv_service_times_to_simulated:
    # for each cv_service_time, we build the simulator, modify the sim_config, and simulate
    sim_config = Sim_Config()
    simulator = Simulator(sim_config)
    sim_config.ln_service_dict[0][
        "cv_service_time"
    ] = cv_service_time  # modify the configuration
    if sim_config.is_capacity_case is False:
        print("delay case of cv =", cv_service_time, " is being simulated")
    else:
        print("capacity case of cv =", cv_service_time, " is being simulated")

    round_num = 2  # you can run the simulation multiple rounds and take the mean. When doing so, please don't forget to reset the simulator at the end of each round.

    # for each cv_service_time, you run the simulation (with enough time) to get the converged results
    result_for_each_round_list = []
    for round in range(round_num):
        # for each round, the simulation lasts 1000 hours
        for _ in range(simulator.sim_config.sim_duration):
            simulator.move_one_step()

        # collect the statistics (e.g., bus delays) for all the buses and output the metric of interest
        if sim_config.is_capacity_case is False:  # delay case
            bus_count = 0
            total_delay = 0.0
            for ln, bus_dict_each_ln in simulator.ln_total_bus_dict.items():
                for bus in bus_dict_each_ln.values():
                    bus_count += 1
                    total_delay += bus.record.queue_delay + bus.record.berth_delay

            avg_bus_delay = total_delay / bus_count
            print("avg bus delay in round", str(round), "is:", avg_bus_delay)
            result_for_each_round_list.append(avg_bus_delay)
        else:
            the_num_of_buses_discharged = simulator.stop.num_of_buses_discharged
            capacity = the_num_of_buses_discharged / (sim_config.sim_duration / 3600)
            print("capacity in round", str(round), "is:", capacity)
            result_for_each_round_list.append(capacity)

        simulator.reset()

    result_for_all_rounds = 0.0
    if sim_config.is_capacity_case is False:
        # average the bus delay for each round
        result_for_all_rounds = sum(result_for_each_round_list) / len(
            result_for_each_round_list
        )
    else:
        result_for_all_rounds = sum(result_for_each_round_list) / len(
            result_for_each_round_list
        )

    # delay_result_dict[cv_service_time] = avg_delay_for_all_rounds
    plot_result_dict[cv_service_time] = result_for_all_rounds


# plot the things you want
print("the results to be plotted:", plot_result_dict)
