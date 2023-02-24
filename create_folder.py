import os
import shutil
from datetime import datetime

from test_settings import *

# test_number = "9999"
# env = "L2"
path_to_created_folder = "c:/AWR/"


def create_new_folder(test_number, env, path_to_created_folder):
    new_dir_name = "".join([test_number, env])
    absolute_path_to_new_dir = "".join([path_to_created_folder, new_dir_name])

    # print(f"new_dir_name: {new_dir_name}, absolute_path_to_new_dir: {absolute_path_to_new_dir}")

    if os.path.exists(absolute_path_to_new_dir):
        timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        absolute_path_to_new_dir_with_timestamp = "_".join([absolute_path_to_new_dir, timestamp])
        os.mkdir(absolute_path_to_new_dir_with_timestamp)
        print(f"Директория {new_dir_name} уже существует, создана дир. {absolute_path_to_new_dir_with_timestamp}") 
    
    else:
        os.mkdir(absolute_path_to_new_dir)
        print(f"Создана дир. {absolute_path_to_new_dir}") 


def copy_and_rename_file_txt(test_number, env, path_to_created_folder):
    dirs_list = sorted(os.listdir(path_to_created_folder))
    dir_for_copy_txt = str

    for dir in dirs_list[::-1]:
        if dir.endswith(env) and not dir.startswith(test_number):
            dir_for_copy_txt = dir
            break

    source_dir_for_copy = "".join([path_to_created_folder, dir_for_copy_txt, "/", dir_for_copy_txt, ".txt"])
    target_dir_for_copy = "".join([path_to_created_folder, test_number, env, "/", dir_for_copy_txt, ".txt"])

    shutil.copy2(source_dir_for_copy, target_dir_for_copy)
    os.rename(target_dir_for_copy, "".join([path_to_created_folder, test_number, env, "/", test_number, env, ".txt"]))


create_new_folder(test_number, env, path_to_created_folder)
copy_and_rename_file_txt(test_number, env, path_to_created_folder)
