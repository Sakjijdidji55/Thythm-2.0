import json
from pathlib import Path

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)


def load_from_json(file_name: str):
    return json.loads(Path(file_name).read_text("utf-8"))  # 从JSON文件中读取数据并返回


def deal_name(name: str):
    return name.replace(" ", "_")


def re_name(name: str):
    return name.replace("_", " ")
