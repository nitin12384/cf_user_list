import requests
import time 

from . import logger

# Todo
# API call check for status == OK

class CodeforcesAPI:
    last_time_ns = 0
    ns_conversion_const = 10**9

    @staticmethod
    def perform_api_call(api_url : str):
        cur_time_ns = time.time_ns()
        diff_s =  (cur_time_ns - CodeforcesAPI.last_time_ns) / CodeforcesAPI.ns_conversion_const 

        if diff_s <= 2:
            logger.error("Can only perform 1 request every 2 seconds.")
            return None
        else:
            CodeforcesAPI.last_time_ns = cur_time_ns
            response = requests.get(api_url)
            return response.json() 

class Codeforces:
    @staticmethod
    def get_problemset():
        return CodeforcesAPI.perform_api_call("https://codeforces.com/api/problemset.problems")

    @staticmethod
    def get_user_submissions(handle: str):
        return CodeforcesAPI.perform_api_call("https://codeforces.com/api/user.status?handle=" + handle)
