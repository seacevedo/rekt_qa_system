import pandas as pd
from typing import List


def import_documents(path: str) -> List[dict]:
    try:
        df_rekt = pd.read_csv(path, index_col=0)
        df_rekt = df_rekt.dropna()
        df_rekt = df_rekt[['Hack' in i for i  in  df_rekt.tags]]
        df_rekt = df_rekt.reset_index()
        df_rekt = df_rekt.drop(columns=['index'])
        df_rekt['id'] = df_rekt.index
        return df_rekt.to_dict(orient='records')
    except FileNotFoundError:
        print("No such file exists: ", path)


