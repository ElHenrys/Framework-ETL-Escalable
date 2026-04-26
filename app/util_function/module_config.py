import json
from root_dir import get_root_dir



class ConfigJson(object):
    __root_dir = get_root_dir()

    def get_content_json_date(self, file_json: str):
        dir_json = self.__root_dir + f'\\config\\{file_json}.json'
        with open(dir_json, 'r') as json_file:
            j = json_file.read()
        str_to_dict = json.loads(j)
        return str_to_dict
