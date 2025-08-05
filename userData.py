import json
import shutil
import tkinter as tk
from collections import defaultdict
from pathlib import Path
from tkinter import filedialog

from PIL import Image, ImageTk

user_inform_keys = ["name", "icon_path", "description"]
user_inform = defaultdict(str)
# 选择头像文件按钮
shift = False  # 用来判断是否需要改变头像

user_inform_path = "./UserData/userInform.json"

music_inform_path = "./UserData/musicInform.json"

music_notes_path = "./UserData/musicNotes.json"


def get_info(username_entry, description_text, file_path_label):
    global shift
    username = username_entry.get()
    user_inform["name"] = username  # 获取用户名
    description = description_text.get(
        "1.0", tk.END
    ).strip()  # 获取描述,strip()函数用于去除字符串两端的空白字符，get("1.0", tk.END) 用于获取文本框中的所有文本
    user_inform["description"] = description  # 赋值描述
    file_path = file_path_label.cget("text").replace(
        "选择的头像文件路径: ", ""
    )  # 获取文件路径
    if file_path:
        if file_path != user_inform["icon_path"]:
            shift = True
        user_inform["icon_path"] = file_path
    print(f"用户名: {username}")
    print(f"描述: {description}")
    print(f"头像文件路径: {file_path}")


def get_info_window():
    """定义一个函数，用于获取信息"""

    def choose_file():
        file_path = filedialog.askopenfilename(
            title="选择头像图片", filetypes=[("Image files", "*.png *.jpg")]
        )
        if file_path:
            image = Image.open(file_path).resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            if hasattr(root, "photo"):
                root.photo = None
                Image_label.config(image=None)
            Image_label.config(image=photo)
            root.photo = photo

            file_path_label.config(text=f"选择的头像文件路径: {file_path}")

    def sure_submit():
        get_info(username_entry, description_text, file_path_label)
        root.destroy()

    root = tk.Tk()
    root.title("欢迎来到THYTHM")
    root.geometry("400x300")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.iconbitmap("./image/icon.ico")  # 设置窗口图标

    default_image = Image.open("./image/icon.png").resize((100, 100))
    if user_inform["icon_path"]:
        default_image = Image.open(user_inform["icon_path"]).resize((100, 100))
    else:
        user_inform["icon_path"] = "./image/icon.png"
    default_photo = ImageTk.PhotoImage(default_image)
    root.photo = default_photo  # 赋值给root.photo

    # 创建一个标签，用于显示用户名
    name_label = tk.Label(root, text="昵称：", font=("楷体", 12))
    name_label.pack()
    username_entry = tk.Entry(root, font=("楷体", 14))
    username_entry.pack()
    description_label = tk.Label(root, text="简介：", font=("楷体", 12))
    description_label.pack()

    # 简介
    if user_inform["description"]:
        default_description = user_inform["description"]
    else:
        default_description = "默认简介"
    description_text = tk.Text(root, height=1, width=30, font=("楷体", 14))
    description_text.insert(tk.END, default_description)
    description_text.pack()

    choose_file_button = tk.Button(root, text="选择头像文件", command=choose_file)
    choose_file_button.pack()
    # 显示头像文件路径的标签
    file_path_label = tk.Label(root, text="选择的头像文件路径: ")
    file_path_label.pack()

    Image_label = tk.Label(root, image=default_photo)
    Image_label.pack()

    get_info_button = tk.Button(root, text="提交", command=sure_submit)
    get_info_button.pack()
    root.mainloop()


def set_user_inform(user_inform_path):
    global shift
    get_info_window()
    if user_inform["icon_path"] and shift:
        # 指定保存图片的目标目录
        shift = False
        target_folder = "UserInform"
        target_folder_path = Path(target_folder)
        target_folder_path.mkdir(parents=True, exist_ok=True)
        # 将头像文件移动到目标目录
        source_file = user_inform["icon_path"]
        destination_file = target_folder_path / Path(source_file).name
        shutil.copy2(source_file, destination_file)
        user_inform["icon_path"] = str(destination_file)
        print(f"头像文件已成功移动至{destination_file}")
    if user_inform["name"] == "":
        user_inform["name"] = "未命名"
    if user_inform["description"] == "":
        user_inform["description"] = "暂无简介"
    save_user_inform(
        user_inform_path, user_inform
    )  # 保存用户信息，将用户的头像路径放入自己数据库


def get_user_inform(user_inform_path):
    path = Path(user_inform_path)
    if not path.exists():
        set_user_inform(user_inform_path)

    return json.loads(path.read_text())  # 读取用户信息


def save_user_inform(user_inform_path, user_inform):
    path = Path(user_inform_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(user_inform))  # 保存用户信息


def save_music_inform(music_inform_path, music_inform):
    path = Path(music_inform_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(music_inform))  # 保存音乐信息


def get_music_inform(music_inform, music_inform_path=music_inform_path):
    path = Path(music_inform_path)
    if not path.exists():
        save_music_inform(music_inform_path, music_inform)
    return json.loads(path.read_text())  # 读取音乐信息


user_inform = get_user_inform(user_inform_path)
