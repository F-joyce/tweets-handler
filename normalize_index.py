''' Use this data to create an upper limit of retweets/followers ratio (and for likes too)
    on top of which normalise the other data, allowing some extra space if possible'''


retweets = {'@carterjwm':
                        {'rt_millions': 3.2,
                         'followers':28000},
            '@chadwickboseman':
                        {'rt_millions': 3.0,
                         'followers':2162885},
            '@TheEllenShow':
                        {'rt_millions': 2.9,
                         'followers':77725734},
            '@Louis_Tomlinson':
                        {'rt_millions': 2.8,
                         'followers':35977435},
            '@BTS_twt ':
                        {'rt_millions': 1.8,
                         'followers':42028157},
            '@BarackObama':
                        {'rt_millions': 1.5,
                         'followers':130392345}}

likes = {'@JoeBiden':
                        {'likes_millions': 4.0,
                         'followers':31856966},
            '@chadwickboseman':
                        {'likes_millions': 7.3,
                         'followers':2162885},
            '@andymilonakis':
                        {'likes_millions': 3.6,
                         'followers':600388},
            '@Twitter':
                        {'likes_millions': 3.3,
                         'followers':60522319},
            '@BTS_twt ':
                        {'likes_millions': 3.2,
                         'followers':42028157},
            '@BarackObama':
                        {'likes_millions': 4.2,
                         'followers':130392345}}


def calculate_ratio_rt():
    to_average = []

    for user in retweets:
        ratio = retweets[user]['rt_millions']*1000000/retweets[user]['followers']
        # print(f'The ratio retweets and followers is {ratio}')
        to_average.append(ratio)

    mean_ratio = sum(to_average)/6

    return print(f'Mean ratio for retweets is {mean_ratio}')

def calculate_ratio_l():
    to_average = []

    for user in likes:
        ratio = likes[user]['likes_millions']*1000000/likes[user]['followers']
        # print(f'The ratio likes and followers is {ratio}')
        to_average.append(ratio)

    mean_ratio = sum(to_average)/6

    return print(f'Mean ratio for likes is {mean_ratio}')

RATIO_RT = 19.307

RATIO_LK = 1.610


def Normalize_likes(likes, followers):
    ratio = 1.610
    ratio_instance = likes/followers
    return round(ratio_instance/ratio,5)

def Normalize_rtweets(rtweets, followers):
    ratio = 19.307
    ratio_instance = rtweets/followers
    return round(ratio_instance/ratio, 5)


def Normalize(followers,likes, rtweets):
    return (Normalize_likes(likes, followers)*2 + Normalize_rtweets(rtweets, followers)*8)


# Example to apply a multi parameter function to dataframe
# This is the function
# def v_index(nfollowers, nlikes, nretweets, nreplies):
# This how to apply it to a dataframe
# df['v_index'] = df.apply(lambda x: v_index(x['nFollowers'], x['nlikes'], x['nretweets'], x['nreplies']), axis=1)

