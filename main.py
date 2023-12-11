import time
from collections import namedtuple
from datetime import datetime

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
        for num in range(seed_start, seed_start+range_):
            yield num


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
    locations = set()
    # for seed in seeds():
    for seed in seeds_part2():
        key = int(seed)
        for ident in (seed_to_soil_map_identifier,
                      soil_to_fertilizer_map_identifier,
                      fertilizer_to_water_map_identifier,
                      water_to_light_map_identifier,
                      light_to_temperature_map_identifier,
                      temperature_to_humidity_map_identifier,
                      humidity_to_location_map_identifier):
            mapping_data = extract_data_mapping(ident)
            key = make_conversion(mapping_data, key)
        locations.add(key)

    print(min(locations))


if __name__ == '__main__':
    main()