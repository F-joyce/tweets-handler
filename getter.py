import twint
import datetime

        # For customizing, these are all the columns of the twint original dataframe
        # ['id', 'conversation_id', 'created_at', 'date', 'timezone', 'place',
        # 'tweet', 'language', 'hashtags', 'cashtags', 'user_id', 'user_id_str',
        # 'username', 'name', 'day', 'hour', 'link', 'urls', 'photos', 'video',
        # 'thumbnail', 'retweet', 'nlikes', 'nreplies', 'nretweets', 'quote_url',
        # 'search', 'near', 'geo', 'source', 'user_rt_id', 'user_rt',
        # 'retweet_id', 'reply_to', 'retweet_date', 'translate', 'trans_src',
        # 'trans_dest']



# TODO
# Substitute Limit with Data, last 10 minutes, as parameter given in main.py


now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

_ago = (datetime.datetime.utcnow() - datetime.timedelta(minutes = 22)).strftime('%Y-%m-%d %H:%M:%S')

_toago = (datetime.datetime.utcnow() - datetime.timedelta(minutes = 20)).strftime('%Y-%m-%d %H:%M:%S')

def search(since = None, until = None):
    c = twint.Config()
    c.Pandas = True
    c.Search = 'covid'
    c.Since = since
    c.Until = until
   

    twint.run.Search(c)
    
    Tweets_df = twint.storage.panda.Tweets_df

    df_clean = Tweets_df[Tweets_df['language']=='en'].copy()
    
    df_clean = df_clean[['id', 'tweet', 'date', 'nlikes', 'nreplies', 'nretweets', 'hour', 'geo', 'day']].copy()

    df_clean.rename(columns={'id':'_id'}, inplace=True)

    df_clean.to_pickle("./df_clean.pkl")
    

if __name__ == "__main__":
    search(_ago, _toago)

    