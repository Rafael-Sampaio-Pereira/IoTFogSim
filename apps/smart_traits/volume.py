



class Volume(object):

    def __init__(self, volume):
        self.current_volume=volume
        self.is_muted=False
        self.volume_max_level=11
        self.volume_can_mute_and_unmute=True
        self.level_step_size=1