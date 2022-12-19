from . import config, logger
import json
import atexit
# Todo : replace file open check with file exists check.
# Todo : check for directory availability - ./data/codeforces/, ./data/codeforces/user_submissions/ .....

class ToolConfig:

    def load_tool_config(tool_config_path):
        config_file = None
        config_obj = None
        try:
            config_file = open(tool_config_path, "r")
            config_obj = json.load(config_file)
        except FileNotFoundError:

            config_file = open(tool_config_path, "w")
            config_obj = {
                "last_load_time" : {
                    "problemset" : 0,
                    "user_submissions" : {}
                }
            }
            json.dump(config_obj, config_file)

        config_file.close()
        return config_obj 

    def __init__(self, tool_config_path : str):
        self.tool_config = ToolConfig.load_tool_config(tool_config_path)
        self.tool_config_path = tool_config_path
        atexit.register(self.on_exit)
    
    def get_last_load_pset(self):
        return self.tool_config["last_load_time"]["problemset"]

    def set_last_load_pset(self, load_time_ns:int):
        self.tool_config["last_load_time"]["problemset"] = load_time_ns

    def get_last_load_sub(self, handle:str):
        result = 0
        try:
            result = self.tool_config["last_load_time"]["user_submissions"][handle]
        except KeyError:
            self.tool_config["last_load_time"]["user_submissions"][handle] = 0

        return result

    def set_last_load_sub(self, handle:str, load_time_ns:int):
        self.tool_config["last_load_time"]["user_submissions"][handle] = load_time_ns

    def on_exit(self):
        json.dump(self.tool_config, open(self.tool_config_path, "w"))
        logger.log("Saved new tool config values.")



cf_tool_config = ToolConfig(config.cf_tool_config_path)
