import pandas as pd
import user_fll

df = pd.read_pickle("./df_clean.pkl")


def analyze(tweet):
    if tweet.count('and') > 1:
        return 'Connected'
    else:
        return 'Disconnected'


def main():
    df['n_followers'] = df['username'].apply(user_fll.get_number_followers)

    df['connection'] = df['tweet'].apply(analyze)

    df.to_pickle('./df_connect.pkl')

if __name__ == "__main__":
    main()