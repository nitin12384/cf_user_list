from . import api_call, config
import json

# Todo  
# Error handling in json.dump(), json.load()
# What if user handle containg characters that cannot be used in file naming, like obscure UTF characters

def generate_problemset_diff_cnt(problemset):
    problemset_diff_cnt = {}
    low, high, step = 800, 3500, 100
    for rating in range(low, high+step, step):
        problemset_diff_cnt[rating] = 0
    
    problem_cnt = len(problemset)
    rating_unavailable_cnt = 0

    for problem in problemset:
        try:
            rating = problem["rating"]
            problemset_diff_cnt[rating] += 1
        except KeyError:
            rating_unavailable_cnt += 1
    
    problemset_diff_cnt["total"] = problem_cnt
    problemset_diff_cnt["count_rating_unavailable"] = rating_unavailable_cnt

    return problemset_diff_cnt

def load_problemset():
    problemset_response = api_call.Codeforces.get_problemset()

    problemset_file = open(config.cf_problemset_path, "w")
    json.dump(problemset_response["result"]["problems"], problemset_file)
    problemset_file.close()

def load_problemset_diff_count():
    problemset_file = open(config.cf_problemset_path, "r")
    problemset = json.load(problemset_file)


    problemset_diff_cnt = generate_problemset_diff_cnt(problemset)
    problemset_diff_count_file = open(config.cf_problemset_diff_cnt_path, "w")
    
    
    json.dump(problemset_diff_cnt, problemset_diff_count_file)
    problemset_file.close()
    problemset_diff_count_file.close()

def load_user_submission(handle : str):
    submissions_resp = api_call.Codeforces.get_user_submissions(handle)
    if submissions_resp is not None :
        submissions_file_path = config.cf_user_submission_base_path + '/' + handle + ".json"
        submissions_file = open(submissions_file_path, "w")
        json.dump(submissions_resp["result"], submissions_file)
        submissions_file.close()
    

    

