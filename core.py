# -*- coding: utf-8 -*-
# author:yangtao
# time: 2021/10/26
import subprocess
import os

import pymel.core as pm

FFMPEG_PATH = os.path.join(os.path.dirname(__file__), u"tools", u"ffmpeg.exe")

def get_playback_range():
    time_range = (int(pm.playbackOptions(min=1, q=1)), int(pm.playbackOptions(max=1, q=1)))
    return time_range


def convert_avi_to_mov(input_path, output_path):
    cmd_args = [FFMPEG_PATH]
    cmd_args += ["-i", input_path]
    cmd_args += ["-vcodec", "libx264"]
    cmd_args += [output_path, "-y"]
    ffmpeg_process = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for std_out_line in iter(ffmpeg_process.stdout.readline, ""):
        print(std_out_line.strip())
    ffmpeg_process.stdout.close()
    return_code = ffmpeg_process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd_args)


def playblast(**kwargs):
    return pm.playblast(**kwargs)


if __name__ == "__main__":
    input_path = r"D:\output\ddddd.avi"
    output_path = r"D:\output\ddddd.mov"
    convert_avi_to_mov(input_path, output_path)