import json
import time
from psaw import PushshiftAPI
api = PushshiftAPI()

contents: dict = {}
with open("Content.json") as contents_file:
    contents = json.load(contents_file)

topics: dict = {}
with open("Topics.json") as topics_file:
    topics = json.load(topics_file)

for sub_reddit in contents.keys():
    for main_topic in topics.keys():
        content: list = []
        for topic in topics[main_topic]:
            time.sleep(5)
            print("For sub_reddit:", sub_reddit, "with topic:", topic)
            gen = api.search_submissions(q=topic, before="1y",
                               subreddit=[sub_reddit],
                               num_comments=">10",
                               limit = 500
                              )
            for item in gen:
                # if item.selftext != "[deleted]" and item.selftext != "[removed]":
                content.append(item.d_)
            
        contents[sub_reddit][main_topic] = content
    
print("Shards: ", api.metadata_.get('shards'))

with open("Submissions.json", "w+") as submissions_file:
    json.dump(contents, submissions_file, indent=2, sort_keys=True)