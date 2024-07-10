import geopandas as gpd
import matplotlib.pyplot as plt

from utils.save_read import read_to_df


class temp:
    def temp(self):
        df = read_to_df('data/clean_dataset.csv', 'csv')
        
        mapping = {
        'District': {
            'aalst': 21,
            'antwerp': 10,
            'arlon': 39,
            'ath': 41,
            'bastogne': 42,
            'brugge': 0,
            'brussels': 4,
            'charleroi': 17,
            'dendermonde': 28,
            'diksmuide': 27,
            'dinant': 32,
            'eeklo': 26,
            'gent': 25,
            'halle-vilvoorde': 7,
            'hasselt': 3,
            'huy': 30,
            'ieper': 11,
            'kortrijk': 24,
            'leuven': 16,
            'liège': 18,
            'maaseik': 19,
            'marche-en-famenne': 23,
            'mechelen': 6,
            'mons': 12,
            'mouscron': 34,
            'namur': 13,
            'neufchâteau': 33,
            'nivelles': 5,
            'oostend': 9,
            'oudenaarde': 31,
            'philippeville': 14,
            'roeselare': 36,
            'sint-niklaas': 8,
            'soignies': 15,
            'thuin': 38,
            'tielt': 35,
            'tongeren': 22,
            'tournai': 1,
            'turnhout': 37,
            'verviers': 20,
            'veurne': 2,
            'virton': 40,
            'waremme': 29,
        }
    }


        df = df.replace(mapping)
        print(df['District'])

