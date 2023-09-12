


class OccupancySensing(object):

    def __init__(self, delay=10):
        self.occupancy = 'UNOCCUPIED' # OCCUPIED / UNKNOWN_OCCUPANCY_STATE
        self.occupancy_sensor_type = 'PIR',
        self.occupied_to_unoccupied_delay_sec = delay,
        self.unoccupied_to_occupied_delay_sec = delay