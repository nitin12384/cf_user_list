from . import api_call, config
import json

# Todo  
# Error handling in json.dump(), json.load()

def generate_problemset_diff_cnt(problemset):
    problemset_diff_cnt = {}
    low, high, step = 800, 3500, 100
    for rating in range(low, high+step, step):
        problemset_diff_cnt[rating] = 0
    
    problem_list = problemset["result"]["problems"]
    problem_cnt = len(problem_list)
    rating_unavailable_cnt = 0

    for problem in problem_list:
        try:
            rating = problem["rating"]
            problemset_diff_cnt[rating] += 1
        except KeyError:
            rating_unavailable_cnt += 1
    
    problemset_diff_cnt["total"] = problem_cnt
    problemset_diff_cnt["count_rating_unavailable"] = rating_unavailable_cnt

    return problemset_diff_cnt

def load_problemset():
    problemset = api_call.Codeforces.get_problemset()

    problemset_file = open(config.cf_problemset_path, "w")
    json.dump(problemset, problemset_file)
    problemset_file.close()

def load_problemset_diff_count():
    problemset_file = open(config.cf_problemset_path, "r")
    problemset = json.load(problemset_file)


    problemset_diff_cnt = generate_problemset_diff_cnt(problemset)
    problemset_diff_count_file = open(config.cf_problemset_diff_cnt_path, "w")
    
    
    json.dump(problemset_diff_cnt, problemset_diff_count_file)
    problemset_file.close()