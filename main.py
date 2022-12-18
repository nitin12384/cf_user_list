
from helper import load_data
from helper import config
import time
import json

#load_data.load_problemset()
#load_data.load_problemset_diff_count()

time.sleep(2)

load_data.load_user_submission('iamujj.15')
load_data.load_user_diff_submissions('iamujj.15')

# require everything loaded
def print_user_list(handle : str):
    load_data.load_user_submission(handle)
    user_diff_cnt = load_data.load_user_diff_submissions(handle)
    problemset_diff_cnt = json.load(open(config.cf_problemset_diff_cnt_path, 'r'))
    #print(user_diff_cnt)
    low, high, step = 800, 3500, 100 

    for rating_int in range(low, high+step, step):
        rating = str(rating_int)
        print("Rating : ", rating, " Total : ", problemset_diff_cnt[rating], " Solved by " +  handle + " : ", \
        user_diff_cnt[rating_int]["count"])


print_user_list('iamujj.15')
