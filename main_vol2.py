import time
from collections import namedtuple
from datetime import datetime
from multiprocessing import Process, Queue

from inputs import data

seeds_identifier = "seeds:"
seed_to_soil_map_identifier = 'seed-to-soil map:'
soil_to_fertilizer_map_identifier = 'soil-to-fertilizer map:'
fertilizer_to_water_map_identifier = 'fertilizer-to-water map:'
water_to_light_map_identifier = 'water-to-light map:'
light_to_temperature_map_identifier = 'light-to-temperature map:'
temperature_to_humidity_map_identifier = 'temperature-to-humidity map:'
humidity_to_location_map_identifier = 'humidity-to-location map:'


def seeds(input_data: str = data):
    for line in input_data.splitlines():
        if line.startswith(seeds_identifier):
            _, s = line.split(seeds_identifier)
            for seed_ in s.strip().split():
                yield int(seed_)


def seeds_part2(input_data: str = data):
    seed_numbers = list(seeds(input_data))
    for seed_start, range_ in zip(seed_numbers[:-1:2], seed_numbers[1::2]):
        print(datetime.now(), seed_start, range_)
        num = seed_start
        while num < seed_start + range_:
            yield num
            num += 1


def seeds_part2_multiprocessing(input_data: str = data):
    seed_numbers = list(seeds(input_data))
    for seed_start, range_ in zip(seed_numbers[:-1:2], seed_numbers[1::2]):
        yield seed_start, seed_start + range_


RangeData = namedtuple("RangeDesc", "d_start, s_start, len")


def extract_data_mapping(identifier: str, input_data: str = data):
    found = False
    for line in input_data.splitlines():
        if found and line:
            d = [int(item) for item in line.split()]
            yield RangeData(*d)

        if found and not line:
            break

        if line.startswith(identifier):
            found = True


def make_conversion(range_descriptions, number):
    for rd in range_descriptions:
        if not (rd.s_start <= number < rd.s_start + rd.len):
            continue
        number - rd.s_start
        return rd.d_start + number - rd.s_start
    return number


def main():
    # for seed in seeds():
    min_location = None
    mapping = {
        seed_to_soil_map_identifier: list(extract_data_mapping(seed_to_soil_map_identifier)),
        soil_to_fertilizer_map_identifier: list(extract_data_mapping(soil_to_fertilizer_map_identifier)),
        fertilizer_to_water_map_identifier: list(extract_data_mapping(fertilizer_to_water_map_identifier)),
        water_to_light_map_identifier: list(extract_data_mapping(water_to_light_map_identifier)),
        light_to_temperature_map_identifier: list(extract_data_mapping(light_to_temperature_map_identifier)),
        temperature_to_humidity_map_identifier: list(extract_data_mapping(temperature_to_humidity_map_identifier)),
        humidity_to_location_map_identifier: list(extract_data_mapping(humidity_to_location_map_identifier)),
    }

    for seed in seeds_part2():
        key = seed
        for ident in (seed_to_soil_map_identifier,
                      soil_to_fertilizer_map_identifier,
                      fertilizer_to_water_map_identifier,
                      water_to_light_map_identifier,
                      light_to_temperature_map_identifier,
                      temperature_to_humidity_map_identifier,
                      humidity_to_location_map_identifier):
            key = make_conversion(mapping[ident], key)

        if min_location is None or key < min_location:
            min_location = key

    print(min_location)


def main_multi(seed_start, seed_stop, storage: Queue):
    min_location = None
    mapping = {
        seed_to_soil_map_identifier: list(extract_data_mapping(seed_to_soil_map_identifier)),
        soil_to_fertilizer_map_identifier: list(extract_data_mapping(soil_to_fertilizer_map_identifier)),
        fertilizer_to_water_map_identifier: list(extract_data_mapping(fertilizer_to_water_map_identifier)),
        water_to_light_map_identifier: list(extract_data_mapping(water_to_light_map_identifier)),
        light_to_temperature_map_identifier: list(extract_data_mapping(light_to_temperature_map_identifier)),
        temperature_to_humidity_map_identifier: list(extract_data_mapping(temperature_to_humidity_map_identifier)),
        humidity_to_location_map_identifier: list(extract_data_mapping(humidity_to_location_map_identifier)),
    }

    seed = seed_start

    while seed < seed_stop:
        key = seed
        for ident in (seed_to_soil_map_identifier,
                      soil_to_fertilizer_map_identifier,
                      fertilizer_to_water_map_identifier,
                      water_to_light_map_identifier,
                      light_to_temperature_map_identifier,
                      temperature_to_humidity_map_identifier,
                      humidity_to_location_map_identifier):
            key = make_conversion(mapping[ident], key)

        if min_location is None or key < min_location:
            min_location = key

        seed += 1
    print(min_location)
    storage.put(min_location)
    return min_location


if __name__ == '__main__':
    start = time.time()

    min_locations = Queue()
    processes = []
    for s, e in seeds_part2_multiprocessing():
        p = Process(target=main_multi, args=(s, e, min_locations))
        processes.append(p)
        p.start()

    print("processes: ", len(processes))

    # completing process
    for p in processes:
        p.join()

    # print the output
    while not min_locations.empty():
        print(min_locations.get())

    print(f'duration: {time.time() - start}')
