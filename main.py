import os
import re
import glob
import tkinter
from tkinter import filedialog
tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing


def main():
    folder_path = filedialog.askdirectory()
    folder_path_escaped = glob.escape(folder_path)
    srt_files = [os.path.basename(x) for x in glob.glob(folder_path_escaped + r"\*.srt")]
    mkv_files = remove_file_ext([os.path.basename(x) for x in glob.glob(folder_path_escaped + r"\*.mkv")])

    srt_files_map = map_season_episode_num(srt_files)
    mkv_files_map = map_season_episode_num(mkv_files)
    renaming_lst = calc_renaming(srt_files_map, mkv_files_map)
    change_srt_names(folder_path, renaming_lst)


def remove_file_ext(file_names):
    return [os.path.splitext(x)[0] for x in file_names]


def map_season_episode_num(file_names):
    srt_files_map = {}
    for fn in file_names:
        reg = re.search(r"[Ss](\d+)[Ee](\d+)", fn)
        season = int(reg.group(1))
        episode = int(reg.group(2))
        srt_files_map[(season, episode)] = fn

    return srt_files_map


def change_srt_names(root_path, renaming_list):
    for (old_fn,new_fn) in renaming_list:
        rename_file(root_path, old_fn, new_fn)


def rename_file(root_path, old_fn, new_fn):
    old_full_path = os.path.join(root_path, old_fn)
    new_full_path = os.path.join(root_path, new_fn)

    if not os.path.isfile(new_full_path):
        print("renaming " + old_full_path + " to " + new_full_path)
        os.rename(old_full_path, new_full_path)
    else:
        print("skipping " + old_full_path + " to " + new_full_path)


def calc_renaming(srt_map, mkv_map):
    renaming_lst = []
    for key in mkv_map:
        if key in srt_map:
            renaming_lst.append((srt_map[key], mkv_map[key] + ".srt"))

    return renaming_lst


if __name__ == '__main__':
    main()
