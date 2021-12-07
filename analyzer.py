from typing import NoReturn
import pandas as pd

df = pd.read_pickle("./df_followers.pkl")

def v_index(nfollowers, nlikes, nretweets, nreplies):
    nf = nfollowers
    nl = nlikes
    nrts = nretweets
    nrps = nreplies

    if nf == 0:
        return 0
    else:
        v_index = (nrts*0.8 + nl*0.05 + nrps*0.15)/nfollowers

        return v_index

def analyze(tweet):
    if tweet.count('and') > 1:
        return 'Connected'
    else:
        return 'Disconnected'


def main():

    df['v_index'] = df.apply(lambda x: v_index(x['nFollowers'], x['nlikes'], x['nretweets'], x['nreplies']), axis=1)

    df['connection'] = df['tweet'].apply(analyze)

    df.to_pickle('./df_connect.pkl')

if __name__ == "__main__":
    main()