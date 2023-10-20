

class Cook(object):

    def __init__(self, cook_mode):
        self.cooking_mode = cook_mode
        self.valids_cooking_modes = [
            'UNKNOWN_COOKING_MODE',
            'BAKE',
            'BEAT',
            'BLEND',
            'BOIL',
            'BREW',
            'BROIL',
            'CONVECTION_BAKE',
            'COOK',
            'DEFROST',
            'DEHYDRATE',
            'FERMENT',
            'FRY',
            'GRILL',
            'KNEAD',
            'MICROWAVE',
            'MIX',
            'PRESSURE_COOK',
            'PUREE',
            'ROAST',
            'SAUTE',
            'SLOW_COOK',
            'SOUS_VIDE',
            'STEAM',
            'STEW',
            'STIR',
            'WARM',
            'WHIP'
        ]
