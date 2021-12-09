from typing import NoReturn
import pandas as pd
from normalize_index import Normalize

df = pd.read_pickle("./df_followers.pkl")


def main():

    df['v_index'] = df.apply(lambda x: Normalize(x['nFollowers'], x['nlikes'], x['nretweets']), axis=1)

    df.to_pickle('./df_norm.pkl')

if __name__ == "__main__":
    main()

