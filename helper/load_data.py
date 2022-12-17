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

    return problemset_diff_cnt

def load_user_submission(handle : str):
    submissions_resp = api_call.Codeforces.get_user_submissions(handle)
    if submissions_resp is not None :
        submissions_file_path = config.cf_user_submission_base_path + '/' + handle + ".json"
        submissions_file = open(submissions_file_path, "w")
        json.dump(submissions_resp["result"], submissions_file)
        submissions_file.close()

def generate_user_diff_submissions(submissions):
    user_diff_submissions = {}
    low, high, step = 800, 3500, 100
    for rating in range(low, high+step, step):
        user_diff_submissions[rating] = { "count" : 0, "problems" : set()}
    
    num_solved = 0
    solved_rating_unavailable = set()
    

    for submission in submissions:
        if submission["verdict"] == "OK":
            problem_id = str(submission["problem"]["contestId"]) + "-" + submission["problem"]["index"] 
            
            try:
                rating = submission["problem"]["rating"]
                user_diff_submissions[rating]["problems"].add(problem_id)
            except KeyError:
                solved_rating_unavailable.add(problem_id)
                pass

    
    for rating in range(low, high+step, step):
        user_diff_submissions[rating]["problems"] = list(user_diff_submissions[rating]["problems"])
        user_diff_submissions[rating]["count"] = len(user_diff_submissions[rating]["problems"])
        num_solved += user_diff_submissions[rating]["count"]
    
    num_solved += len(solved_rating_unavailable)

    user_diff_submissions["total_count"] = num_solved

    return user_diff_submissions

# requires user submissions to be loaded
def load_user_diff_submissions(handle : str):
    submissions_file_path = config.cf_user_submission_base_path + "/" + handle + ".json"
    submissions_file = open(submissions_file_path, "r")
    submissions = json.load(submissions_file)
    
    user_diff_submissions = generate_user_diff_submissions(submissions)
    user_diff_submissions_file_path = config.cf_user_submission_diff_base_path + "/" + handle + ".json"
    user_diff_submissions_file = open(user_diff_submissions_file_path, "w")

    json.dump(user_diff_submissions, user_diff_submissions_file)

    user_diff_submissions_file.close()
    submissions_file.close()

    return user_diff_submissions

    

