# -*- coding: utf-8 -*-
# author:yangtao
# time: 2021/10/26

"""
一个拍屏工具，首先调用 maya 自己的 playblast 拍出 avi 格式视频
然后通过 ffmpeg 将其转码为 mov（h.264）
ffmpeg 在 tools 文件夹中
"""

import os

import core
import ui


class Response(ui.MainUI):
    """
    连接UI和功能
    """
    INSTANCE = None

    def __init__(self):
        super(Response, self).__init__()
        # 设置连接
        self.__set_connections()

    def __set_connections(self):
        """
        设置连接
        Returns:

        """
        self.run_playblast_btn.clicked.connect(self.run_playblast)

    @ui.handle_error_dialog
    def run_playblast(self):
        """
        执行拍屏
        Returns:

        """
        # 获取输出路径
        output_path = self.out_file_path.path  # type: str
        if not os.path.isdir(os.path.dirname(output_path)):
            raise IOError("Invalid path: %s" % output_path)
            return

        # 拼接 avi 输出路径
        avi_path = os.path.splitext(output_path)[0] + ".avi"
        # 帧范围
        time_range = core.get_playback_range()
        # 拍屏
        core.playblast(f=avi_path,
                       cc=self.clear_cache_option.isChecked(),
                       orn=self.ornaments_option.isChecked(),
                       qlt=self.quality_field.value,
                       os=self.offscreen_option.isChecked(),
                       fp=self.padding_field.value,
                       p=self.scale_field.value * 100,
                       st=time_range[0],
                       et=time_range[1],
                       v=False,
                       fmt="avi",
                       fo=1)

        # 转为 mov
        core.convert_avi_to_mov(avi_path, output_path)

        # 打开视频
        if self.open_viewer_option.isChecked():
            os.startfile(output_path)

        # 移除临时视频
        if self.remove_temp_option.isChecked():
            os.remove(avi_path)


@ui.handle_error_dialog
def show_dialog():
    """
    只保留一个类实例
    """
    if not Response.INSTANCE:
        Response.INSTANCE = Response()
    Response.INSTANCE.show(dockable=True)  # 窗口可停靠

if __name__ == "__main__":
    show_dialog()