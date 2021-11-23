# -*- coding: utf-8 -*-
# author:yangtao
# time: 2021/10/26

import traceback

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


def handle_error_dialog(func):
    '''
    弹出窗户口显示 traceback.format_exc() 的报错
    '''

    def handle(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print(traceback.format_exc())
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                  u"错误",
                                  traceback.format_exc()).exec_()

    return handle


class PathWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, mode="dir", default_path="", label_text="", dialog_label="",
                 file_filters="All Files (*.*)", selected_filter="All Files (*.*)"):
        super(PathWidget, self).__init__(parent)
        self.mode = mode
        self.default_path = default_path
        self.label_text = label_text
        self.dialog_label = dialog_label
        self.file_filters = file_filters
        self.selected_filter = selected_filter

        self._create_widgets()
        self._create_layouts()
        self._create_connections()

    @property
    def path(self):
        return self.line_edit.text()

    def _create_widgets(self):
        self.label = QtWidgets.QLabel(self.label_text)
        self.line_edit = QtWidgets.QLineEdit(self.default_path)
        self.browse_button = QtWidgets.QPushButton()
        self.browse_button.setIcon(QtGui.QIcon(":fileOpen.png"))

    def _create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.line_edit)
        self.main_layout.addWidget(self.browse_button)

    def _create_connections(self):
        self.browse_button.clicked.connect(self.browse_path)

    def browse_path(self):
        if self.mode == "dir":
            self._get_existing_dir()
        elif self.mode == "file":
            self._get_existing_file()
        elif self.mode == "save_file":
            self._get_save_file()

    def set_path(self, text):
        self.line_edit.setText(text)

    def _get_save_file(self):
        if not self.dialog_label:
            self.dialog_label = "Select save file"
        path, filters = QtWidgets.QFileDialog.getSaveFileName(None, self.dialog_label, self.line_edit.text(),
                                                              self.file_filters, self.selected_filter)
        if path:
            self.line_edit.setText(path)

    def _get_existing_file(self):
        if not self.dialog_label:
            self.dialog_label = "Select existing file"
        path, extra = QtWidgets.QFileDialog.getOpenFileName(None, self.dialog_label, self.line_edit.text(),
                                                            self.file_filters, self.selected_filter)
        if path:
            self.line_edit.setText(path)

    def _get_existing_dir(self):
        if not self.dialog_label:
            self.dialog_label = "Set directory"
        path = QtWidgets.QFileDialog.getExistingDirectory(None, self.dialog_label, self.line_edit.text())
        if path:
            self.line_edit.setText(path)

    def add_widget(self, widget):
        self.main_layout.addWidget(widget)


class SliderFieldWidget(QtWidgets.QWidget):
    def __init__(self,
                 data_type="int",
                 label_text="label",
                 min_value=0.0,
                 max_value=1.0,
                 default_value=1.0,
                 step=1.0,
                 slider_multiplier=1.0,
                 parent=None):
        super(SliderFieldWidget, self).__init__(parent)
        # Properties
        self.data_type = data_type
        self.setMinimumSize(100, 40)

        # Build components
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        # Set values
        self.slide_multiplier = slider_multiplier
        self.label_text = label_text
        self.min_value = min_value
        self.max_value = max_value
        self.step = step

        if data_type == "float":
            default_value = float(default_value)
        elif data_type == "int":
            default_value = int(default_value)
        self.spin_box.setValue(default_value)

    @property
    def label_text(self):
        return self._label_text

    @label_text.setter
    def label_text(self, text):
        self._label_text = text
        self.label.setText(text)

    @property
    def min_value(self):
        return self._min_value

    @min_value.setter
    def min_value(self, value):
        self._min_value = value
        self.spin_box.setMinimum(value)
        self.slider.setMinimum(value * self.slide_multiplier)

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        self._max_value = value
        self.spin_box.setMaximum(value)
        self.slider.setMaximum(value * self.slide_multiplier)

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value
        self.spin_box.setSingleStep(value)

    @property
    def value(self):
        return self.get_value()

    def set_value(self, value):
        self.spin_box.setValue(value)

    def get_value(self):
        return self.spin_box.value()

    def create_widgets(self):
        if self.data_type == "float":
            self.spin_box = QtWidgets.QDoubleSpinBox()
        elif self.data_type == "int":
            self.spin_box = QtWidgets.QSpinBox()
        self.spin_box.setMinimumWidth(40)
        self.label = QtWidgets.QLabel()
        self.spin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.addWidget(self.label, 0, 0)
        self.main_layout.addWidget(self.spin_box, 0, 1)
        self.main_layout.addWidget(self.slider, 0, 2)
        self.main_layout.setColumnMinimumWidth(0, 90)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.spin_box.valueChanged.connect(self._update_slider_value)
        self.slider.valueChanged.connect(self._update_field_value)

    @QtCore.Slot()
    def _update_field_value(self, value):
        self.spin_box.setValue(value / self.slide_multiplier)

    @QtCore.Slot()
    def _update_slider_value(self, value):
        self.slider.setValue(value * self.slide_multiplier)


class MainUI(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    """
    主 UI
    """
    OBJECT_NAME = u"hz_playbast"
    SETTING = QtCore.QSettings(u"maya_soft", OBJECT_NAME)
    WINDOW_TITLE = u"拍屏工具[mov h264]"

    def __init__(self):
        super(MainUI, self).__init__()

        # 手动设置 object name，再开始时删除它, 防止窗口打开多个窗口
        try:
            cmds.deleteUI(u"{0}WorkspaceControl".format(self.OBJECT_NAME))
        except:
            pass
        self.setObjectName(self.OBJECT_NAME)

        # 添加控件
        self.__setup_UI()
        # 设置默认值
        self.load_setting()

    def __setup_UI(self):
        """
        生成 UI 部分
        Returns:

        """
        # 标题
        self.setWindowTitle(self.WINDOW_TITLE)

        # region 视频质量
        # 质量
        self.quality_field = SliderFieldWidget(data_type="int",
                                               label_text=u"质量(Quality):",
                                               min_value=0,
                                               max_value=100,
                                               default_value=100)
        # 缩放
        self.scale_field = SliderFieldWidget(data_type="float",
                                             label_text=u"缩放(Scale):",
                                             min_value=0.1,
                                             max_value=1.0,
                                             default_value=1.0,
                                             step=0.1,
                                             slider_multiplier=100.0)
        # 帧填充
        self.padding_field = SliderFieldWidget(data_type="int",
                                               label_text=u"帧填充(Frame padding):",
                                               min_value=0,
                                               max_value=4,
                                               default_value=4)
        # 视频设置布局
        self.image_layout = QtWidgets.QVBoxLayout()
        self.image_layout.addWidget(self.quality_field)
        self.image_layout.addWidget(self.scale_field)
        self.image_layout.addWidget(self.padding_field)
        self.image_layout.addStretch()

        self.image_grp = QtWidgets.QGroupBox(u"视频设置")
        self.image_grp.setLayout(self.image_layout)
        # endregion

        # region 输出设置
        self.out_file_path = PathWidget(mode="save_file",
                                        label_text=u"输出路径:",
                                        dialog_label=u"设置文件输出路径",
                                        file_filters="MOV video (*.mov)",
                                        selected_filter="MOV video (*.MOV)")
        self.open_viewer_option = QtWidgets.QCheckBox(u"预览视频(Open viewer)")
        self.ornaments_option = QtWidgets.QCheckBox(u"显示装饰(Show Ornaments)")
        self.remove_temp_option = QtWidgets.QCheckBox(u"移除临时文件(Remove temporary files)")
        self.offscreen_option = QtWidgets.QCheckBox(u"渲染屏幕外(Render offscreen)")
        self.clear_cache_option = QtWidgets.QCheckBox(u"清理缓存(Clear cache)")

        # 输出设置布局
        self.output_layout = QtWidgets.QGroupBox()
        self.output_layout = QtWidgets.QVBoxLayout()
        self.output_layout.addWidget(self.out_file_path)
        self.output_layout.addWidget(self.open_viewer_option)
        self.output_layout.addWidget(self.ornaments_option)
        self.output_layout.addWidget(self.remove_temp_option)
        self.output_layout.addWidget(self.offscreen_option)
        self.output_layout.addWidget(self.clear_cache_option)
        self.output_layout.addStretch()

        self.output_grp = QtWidgets.QGroupBox(u"输出设置")
        self.output_grp.setLayout(self.output_layout)
        # endregion

        # 执行拍屏
        self.run_playblast_btn = QtWidgets.QPushButton(u"执行拍屏")

        # 主布局
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.image_grp)
        self.main_layout.addWidget(self.output_grp)
        self.main_layout.addWidget(self.run_playblast_btn)

    def save_setting(self):
        self.SETTING.setValue(u"quality", self.quality_field.value)
        self.SETTING.setValue(u"scale", self.scale_field.value)
        self.SETTING.setValue(u"fpadding", self.padding_field.value)
        self.SETTING.setValue(u"out_file_path", self.out_file_path.path)
        self.SETTING.setValue(u"open_viewer", int(self.open_viewer_option.isChecked()))
        self.SETTING.setValue(u"ornaments", int(self.ornaments_option.isChecked()))
        self.SETTING.setValue(u"remove_temp", int(self.remove_temp_option.isChecked()))
        self.SETTING.setValue(u"offscreen", int(self.offscreen_option.isChecked()))
        self.SETTING.setValue(u"clear_cache", int(self.clear_cache_option.isChecked()))

    def load_setting(self):
        self.quality_field.set_value(int(self.SETTING.value(u"quality", 100)))
        self.scale_field.set_value(float(self.SETTING.value(u"scale", 1.0)))
        self.padding_field.set_value(int(self.SETTING.value(u"fpadding", 4)))
        self.out_file_path.set_path(self.SETTING.value(u"out_file_path", u""))
        self.open_viewer_option.setChecked(bool(self.SETTING.value(u"open_viewer", True)))
        self.ornaments_option.setChecked(bool(self.SETTING.value(u"ornaments", True)))
        self.remove_temp_option.setChecked(bool(self.SETTING.value(u"remove_temp", True)))
        self.offscreen_option.setChecked(bool(self.SETTING.value(u"offscreen", False)))
        self.clear_cache_option.setChecked(bool(self.SETTING.value(u"clear_cache", True)))

    def hideEvent(self, event):
        self.save_setting()