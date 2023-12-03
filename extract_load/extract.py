import sys
# from dotenv import load_dotenv
import pandas as pd
import os
import pathlib
import praw

# script_path = pathlib.Path(__file__).parent.parent.resolve()
# load_dotenv(dotenv_path=f'{script_path}/.env')
# load_dotenv()

CLIENT_ID =os.getenv('CLIENT_ID')
SECRET_KEY=os.getenv('SECRET_KEY')
SUBREDDIT = os.getenv("SUBREDDIT")
TIME_FILTER = 'day'
LIMIT = None

POST_FIELDS = [
    'url',
    'author',
    'link_flair_text',
    'title',
    'score',
    'num_comments',
    'upvote_ratio',
    'created_utc'
]

def connect_to_api():
    try:
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=SECRET_KEY,
            user_agent="My User Agent",
        )
    except Exception as e:
        print(f"Couldn't connect to an api.Error: {e}")
        sys.exit(1)
    return reddit


def extract_posts(reddit):
    try:
        subreddit = reddit.subreddit(SUBREDDIT)
        dict = {}
        for s in subreddit.top(time_filter=TIME_FILTER,limit=LIMIT):
            data = {}
            s = vars(s)
            for i in POST_FIELDS:
                data[i]=s[i]
            dict[s['id']] = data
    except Exception as e:
        print(f'Couldn"t extract data from api.Error: {e}')
        sys.exit(1)
    return dict

def transform_to_dataframe(dict):
    try:
        df = pd.DataFrame(dict)
        df = df.transpose()
        df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")
        # df = df.astype({'edited':bool})
        df['id']=df.index
        df.reset_index(drop=True,inplace=True)
    except Exception as e:
        print(f"Couldn't transform data.Error: {e}")
        sys.exit(1)
    return df

def main():
    reddit = connect_to_api()
    raw_data = extract_posts(reddit)
    df = transform_to_dataframe(raw_data)
    # print(df[df['num_comments']=="-"])
    try:
        df.to_csv('/tmp/data.csv',index=False)
    except Exception as e:
        print(f"Couldn't save file.Error: {e}")
        sys.exit(1)

if __name__=="__main__":
    main()