class CategoricalNumDict : 
    def __init__(self) -> None:
        self.dictionaries = {
            "Kitchen" : {
                'not_installed': 0,
                'usa_uninstalled': 1,
                'semi_equipped': 2,
                'usa_semi_equipped': 3,
                'installed': 4,
                'usa_installed': 5,
                'hyper_equipped': 6,
                'usa_hyper_equipped': 7
            } ,
            "PEB" : {
                'F': 0, 
                'F/D': 1, 
                'F/C': 2, 
                'F/E': 3, 
                'E': 4, 
                'E/D': 5, 
                'E/C': 6, 
                'D': 7, 
                'C': 8, 
                'B/A': 9, 
                'B': 10, 
                'A': 11, 
                'A+': 12, 
                'A++': 13
                }, 
            "FloodingZone" :  {
                'recognized_n_circumscribed_flood_zone': 0,
                'recognized_flood_zone': 1,
                'recognized_n_circumscribed_waterside_flood_zone': 2,
                'circumscribed_flood_zone': 3,
                'circumscribed_waterside_zone': 4,
                'possible_n_circumscribed_flood_zone': 5,
                'possible_flood_zone': 6,
                'possible_n_circumscribed_waterside_zone': 7,
                'non_flood_zone': 8
            }
        }
    
    def get_dict(self, key):
        return self.dictionaries.get(key)
        