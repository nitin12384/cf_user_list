# cf_user_list

## What it can do 
Find the count and the list of problems solved by a handle on codeforces, grouped according to problem difficulty rating

## Requirements
Python version - 3.10.6

## Steps to run 
(Steps are given for a linux system. For windows system steps are similiar)
1. Clone this repository
    - $ `git clone https://www.github.com/nitin12384/cf_user_list` 
2. Change directory to the repository's main direcotory
    - $ `cd cf_user_list`
3. Install python packages
    - $ `pip install - r requirements.txt`
4. Edit main.py file. Write the handles of whosoever's data you want to load.
    - load_data.load_user_submission("`<your_handle>`")
5. Run the main.py file.
    - $ `python3 main.py`
6. A file will be generated containing submission details of handle difficulty wise in `data/codeforces/diff_submissions/<your_handle>.json`
