import json

print("Start Loading Json files in", __file__)

contents: dict = {}
with open("Content.json") as contents_file:
    contents = json.load(contents_file)

topics: dict = {}
with open("Topics.json") as topics_file:
    topics = json.load(topics_file)
    
submissions: dict = {}
with open("Submissions.json") as submissions_file:
    submissions = json.load(submissions_file)
    
comments: dict = {}
with open("Comments.json") as comments_file:
    comments = json.load(comments_file)
    
comments_meta: dict = {}
with open("Meta_Data_Comments.json") as comments_meta_file:
    comments_meta = json.load(comments_meta_file)
    
print("Done Loading Json files in", __file__)

def get_id_text_map(input_dict: dict, lookup: str) -> dict:
    result: dict = {}
    for sub_reddit in contents.keys():
        for main_topic in contents[sub_reddit].keys():
            for input in input_dict[sub_reddit][main_topic]:
                if lookup in input.keys():
                    text = input[lookup]
                else:
                    text = ""
                result[input['id']] = text
    return result

id_submission: dict = get_id_text_map(submissions, "selftext")
id_comment: dict = get_id_text_map(comments, "body")

for sub_reddit in contents.keys():
        for main_topic in contents[sub_reddit].keys():
            for idx in range(0, comments_meta[sub_reddit][main_topic]):
                parent_id = comments[sub_reddit][main_topic][idx]['parent_id'].split('_')[1]
                parent_body = ""
                if parent_id in id_submission.keys():
                    parent_body = id_submission[parent_id]
                elif parent_id in id_comment.keys():
                    parent_body = id_comment[parent_id]
                else:
                    parent_body = ""
                comments[sub_reddit][main_topic][idx]['parent_body'] = parent_body

with open("Submissions_id_map.json", "w+") as submissions_id_file:
    json.dump(id_submission, submissions_id_file, indent=2, sort_keys=True)

with open("Comments_id_map.json", "w+") as comments_id_file:
    json.dump(id_comment, comments_id_file, indent=2, sort_keys=True)
    
with open("Comments.json", "w+") as comments_file:
    json.dump(comments, comments_file, indent=2, sort_keys=True)
