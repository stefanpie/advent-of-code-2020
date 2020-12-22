from sympy.ntheory.modular import crt

if __name__ == "__main__":
    with open("input.txt") as f:
        raw_data = [line.rstrip() for line in f]
        earliest_time = int(raw_data[0])
        busses = raw_data[1].split(",")

    busses_with_ids = [b for b in busses if b != "x"]
    busses_with_ids = list(map(int, busses_with_ids))
    max_time = earliest_time + max(busses_with_ids) + 1
    possible_times = list(range(earliest_time, max_time))
    bus_table = []
    for b in busses_with_ids:
        bus_data = {}
        bus_data["id"] = b
        bus_data["departing"] = [t % b == 0 for t in possible_times]
        bus_data["departing_time_index"] = bus_data["departing"].index(True)
        bus_data["departing_time"] = possible_times[bus_data["departing_time_index"]]
        bus_table.append(bus_data)

    bus_table.sort(key=lambda b: b["departing_time"])
    next_bus_id = bus_table[0]["id"]
    waiting_time = bus_table[0]["departing_time"] - earliest_time
    bus_waiting_number = next_bus_id * waiting_time
    print(f"Part 1: {bus_waiting_number}")

    busses_with_index = list(enumerate(busses))
    busses_with_index_valid = list(filter(lambda x: x[1] != "x", busses_with_index))
    busses_with_index_valid = [tuple(map(int, i)) for i in busses_with_index_valid]
    time_dividers = [i[1] for i in busses_with_index_valid]
    time_remainders = [(i[1] - i[0]) % i[1] for i in busses_with_index_valid]
    sequence_starting_time = crt(time_dividers, time_remainders)[0]
    print(f"Part 1: {sequence_starting_time}")
