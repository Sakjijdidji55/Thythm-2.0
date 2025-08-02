import json

# import math
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

def load_from_json(file_name: str):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data # 从JSON文件中读取数据并返回
    
def deal_name(name: str):
    return name.replace(" ", "_")

def re_name(name: str):
    return name.replace("_", " ")
