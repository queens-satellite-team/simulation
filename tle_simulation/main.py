from skyfield.api import EarthSatellite, load, wgs84
from spacetrack import SpaceTrackClient
import argparse


def ground_station_visibility(latitude, longitude, min_elevation, satellite, ts):
    kingston = wgs84.latlon(latitude, longitude)
    SIMULATION_TIME = 3  # days
    sim_start = ts.now()
    sim_end = ts.tt_jd(sim_start.tt + SIMULATION_TIME)
    times, events = satellite.find_events(
        kingston, sim_start, sim_end, min_elevation)
    pass_start_times = [time.utc_datetime() for time in times[::3]]
    pass_end_times = [time.utc_datetime() for time in times[2::3]]
    pass_lengths = [
        end - start for (end, start) in zip(pass_end_times, pass_start_times)]
    pass_intervals = []
    for idx, start_time in enumerate(pass_start_times[1:]):
        pass_intervals.append(start_time - pass_end_times[idx])

    print(
        f'Ground Station Pass Lenghts with {min_elevation} minumum elevation:')
    for length in pass_lengths:
        print(f'    {length}')

    print('Time between consectutive passes:')
    for interval in pass_intervals:
        print(f'    {interval}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', required=True)
    # Default ground station in Kingston
    parser.add_argument('--latitude', default=44.2334, type=int)
    parser.add_argument('--longitude', default=76.4930, type=int)
    parser.add_argument('-m', '--min_elevation', default=10,
                        type=int, help='Minimum elevation of pass')
    args = parser.parse_args()

    ts = load.timescale()
    # Make a free SpaceTrack account at https://www.space-track.org/auth/createAccount
    st = SpaceTrackClient(identity='',
                          password='')

    sat_tles = st.tle_latest(norad_cat_id=args.id, format='tle')
    tle = sat_tles.split('\n')[:2]

    satellite = EarthSatellite(tle[0], tle[1], ts=ts)

    ground_station_visibility(
        args.latitude, args.longitude, args.min_elevation, satellite, ts)


if __name__ == '__main__':
    main()
