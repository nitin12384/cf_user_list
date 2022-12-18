from . import api_call, config, logger, tool_config
import json
import time

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


# load problemset into file, and return problemset object and problemset_diff_cnt object
def load_problemset(force_reload = False, return_problemset = False):
    last_load = tool_config.cf_tool_config.get_last_load_pset()
    cur_time = time.time_ns()

    problemset, problemset_diff_cnt = None, None

    if cur_time - last_load < config.cf_problemset_reload_lim_ns and not force_reload :
        logger.log("Not reloading problemset, because last load was recent.")

        if return_problemset:
            with open(config.cf_problemset_path, "r") as problemset_file :
                problemset = json.load(problemset_file)
            
        with open(config.cf_problemset_diff_cnt_path, "r") as problemset_diff_cnt_file :
            problemset_diff_cnt = json.load(problemset_diff_cnt_file)
        

    else:        
        logger.log("Reloading Problemset")
        problemset_response = api_call.Codeforces.get_problemset()
        problemset = problemset_response["result"]["problems"]
        problemset_diff_cnt = generate_problemset_diff_cnt(problemset)
        tool_config.cf_tool_config.set_last_load_pset(time.time_ns())

        with open(config.cf_problemset_path, "w") as problemset_file :
            json.dump(problemset, problemset_file)

        with open(config.cf_problemset_diff_cnt_path, "w") as problemset_diff_cnt_file :
            json.dump(problemset_diff_cnt, problemset_diff_cnt_file)
    

    if return_problemset :
        return problemset_diff_cnt, problemset
    else :
        return problemset_diff_cnt

# Only return the difficulty wise submissions
def load_user_submission(handle : str, force_reload = False):
    last_load = tool_config.cf_tool_config.get_last_load_sub(handle)
    cur_time = time.time_ns()
    
    user_diff_sub = None
    user_diff_sub_file_path = config.cf_user_submission_diff_base_path + "/" + handle + ".json"
    
    # No need to reload
    if cur_time - last_load < config.cf_user_submission_reload_lim_ns and (not force_reload):
        with open(user_diff_sub_file_path, "r") as f :
            user_diff_sub = json.load(f)
    else:
        submissions_file_path = config.cf_user_submission_base_path + '/' + handle + ".json"
        
        submissions_resp = api_call.Codeforces.get_user_submissions(handle)
        submissions = submissions_resp["result"]
        user_diff_submissions = generate_user_diff_submissions(submissions)    

        with open(submissions_file_path, "w") as submissions_file :
            json.dump(submissions, submissions_file)
        
        with open(user_diff_sub_file_path, "w") as user_diff_sub_file:
            json.dump(user_diff_submissions, user_diff_sub_file)
        
    return user_diff_sub


