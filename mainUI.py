# coding:utf-8
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import qtawesome
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox,QSlider
import cv2
import os
import paddlehub as hub


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 加载移动端预训练模型
        self.flag = "None"
        self.cap = None
        self.imgList = []
        self.ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
        self.setFixedSize(960, 700)

        self.init_button()
        self.init_label()
        self.init_lineedit()
        self.init_toolBar()
        self.init_widget()

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0) # 去缝

    def init_button(self):
        self.left_close = QtWidgets.QPushButton("×")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("一")  # 最小化按钮

        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小

        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.film', color='white'), "一段视频")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.file-image-o', color='white'), "一张图片")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.picture-o', color='white'), "图片目录")
        self.left_button_3.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_9.setObjectName('left_button')
        self.left_xxx = QtWidgets.QPushButton(" ")

        # 槽函数
        self.left_button_2.clicked.connect(self.readImage)
        self.left_button_1.clicked.connect(self.readVedio)
        self.left_button_3.clicked.connect(self.readPictures)
        self.left_close.clicked.connect(self.close)
        self.left_mini.clicked.connect(self.showMinimized)

    def init_label(self):
        self.left_label_1 = QtWidgets.QPushButton("识别种类")
        self.left_label_1.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        self.sourceImage_label = QtWidgets.QLabel()
        self.sourceImage_label.setObjectName('sourceImageLabel')
        self.sourceImage_label.setFixedSize(400,400)
        self.sourceImage_label.setStyleSheet("border:1px solid black")

    def init_lineedit(self):
        self.resultTxt_lineedit = QtWidgets.QTextEdit()
        self.resultTxt_lineedit.setObjectName("resultTxtLineedit")
        self.resultTxt_lineedit.setFixedSize(400,400)
        self.resultTxt_lineedit.setStyleSheet("border:1px solid black")

    def init_widget(self):
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.left_layout.addWidget(self.left_mini, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)
        self.right_layout.addWidget(self.sourceImage_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.resultTxt_lineedit, 1, 10, 1, 9)
        self.right_layout.addWidget(self.sld, 2, 0, 1, 9)

        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#left_widget{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

    def init_toolBar(self):
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(30, 40, 100, 30)
        self.sld.sliderReleased.connect(self.changeValue)



    def changeValue(self):
        if self.flag in "vedio":
            if not self.cap:
                return
            frameNums = self.cap.get(7) - 2 # 不能大于等于总帧数减一！
            print(frameNums)
            pos = float(frameNums * self.sld.sliderPosition()/self.sld.maximum())

            print(pos)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
            if self.cap.isOpened():  # 判断是否正常打开
                _,img = self.cap.read()
                predictList = [img]
                res = self.img_resize(img, self.sourceImage_label)
                img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
                _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                                      QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
                jpg_out = QtGui.QPixmap(_image)  # 转换成QPixmap
                self.sourceImage_label.setPixmap(jpg_out)  # 设置图片显示
                results = self.ocr.recognize_text(
                    images=predictList,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
                    use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
                    output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
                    visualization=True,  # 是否将识别结果保存为图片文件；
                    box_thresh=0.5,  # 检测文本框置信度的阈值；
                    text_thresh=0.5)  # 识别中文文本置信度的阈值；

                for result in results:
                    data = result['data']
                    str = ""
                    for information in data:
                        str += information["text"] + "\n"
                    self.resultTxt_lineedit.setText(str)
        elif self.flag in "pictures":
            nums = len(self.imgList) - 1
            pos = int(nums * self.sld.sliderPosition() / self.sld.maximum())
            print(pos)
            img = self.imgList[pos]
            predictList = [img]
            res = self.img_resize(img, self.sourceImage_label)
            img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
            _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
            jpg_out = QtGui.QPixmap(_image)  # 转换成QPixmap
            self.sourceImage_label.setPixmap(jpg_out)  # 设置图片显示
            results = self.ocr.recognize_text(
                images=predictList,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
                use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
                output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
                visualization=True,  # 是否将识别结果保存为图片文件；
                box_thresh=0.5,  # 检测文本框置信度的阈值；
                text_thresh=0.5)  # 识别中文文本置信度的阈值；

            for result in results:
                data = result['data']
                str = ""
                for information in data:
                    str += information["text"] + "\n"
                self.resultTxt_lineedit.setText(str)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def readImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', 'open file', 'Image files(*)')
        if len(fname) != 0:
            if self.is_chinese(fname):
                print("有中文")
                QMessageBox.warning(self, '警告', '暂不支持含有中文的路径')
                self.flag = "none"
                return
            else:
                print("无中文")
                self.flag = "one_picture"
                img = cv2.imread(fname)  # opencv读取图片
                predictList = [img]
                res = self.img_resize(img, self.sourceImage_label)
                img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
                _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                                      QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
                jpg_out = QtGui.QPixmap(_image)  # 转换成QPixmap
                self.sourceImage_label.setPixmap(jpg_out)  # 设置图片显示
                self.sourceImage_label.setAlignment(Qt.AlignCenter)
                results = self.ocr.recognize_text(
                    images=predictList,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
                    use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
                    output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
                    visualization=True,  # 是否将识别结果保存为图片文件；
                    box_thresh=0.5,  # 检测文本框置信度的阈值；
                    text_thresh=0.5)  # 识别中文文本置信度的阈值；

                for result in results:
                    data = result['data']
                    str = ""
                    for information in data:
                        str += information["text"] + "\n"
                    self.resultTxt_lineedit.setText(str)


    def readVedio(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择视屏', 'open file', 'Image files(*.mp4 *.mkv *.avi)')
        if len(fname) != 0:
            if self.is_chinese(fname):
                print("有中文")
                QMessageBox.warning(self, '警告', '暂不支持含有中文的路径')
                self.flag = "none"
                return
            else:
                self.flag = "vedio"
                print("无中文")
                self.cap = cv2.VideoCapture(fname)
                if not self.cap.isOpened():
                    QMessageBox.warning(self, '警告', '视频打开失败！')
                    return
                _,img = self.cap.read()
                predictList = [img]
                res = self.img_resize(img, self.sourceImage_label)
                img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
                _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                                      QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
                jpg_out = QtGui.QPixmap(_image)  # 转换成QPixmap
                self.sourceImage_label.setPixmap(jpg_out)  # 设置图片显示
                self.sourceImage_label.setAlignment(Qt.AlignCenter)
                results = self.ocr.recognize_text(
                    images=predictList,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
                    use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
                    output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
                    visualization=True,  # 是否将识别结果保存为图片文件；
                    box_thresh=0.5,  # 检测文本框置信度的阈值；
                    text_thresh=0.5)  # 识别中文文本置信度的阈值；

                for result in results:
                    data = result['data']
                    str = ""
                    for information in data:
                        str += information["text"] + "\n"
                    self.resultTxt_lineedit.setText(str)
                    # for infomation in data:
                    #     self.resultTxt_lineedit.append('text: ', infomation['text'], '\nconfidence: ', infomation['confidence'],
                    #           '\ntext_box_position: ', infomation['text_box_position'])
                    #     print('text: ', infomation['text'], '\nconfidence: ', infomation['confidence'],
                    #           '\ntext_box_position: ', infomation['text_box_position'])


    def readPictures(self):
        _dir = QFileDialog.getExistingDirectory(self,"选取文件夹","./")
        if len(_dir) != 0:
            if self.is_chinese(_dir):
                print("有中文")
                QMessageBox.warning(self, '警告', '暂不支持含有中文的路径')
                self.flag = "none"
                return
            else:
                self.flag = "pictures"
                print("无中文")
                imgdirList = os.listdir(_dir)
                for i,img in enumerate(imgdirList):
                    if img.split(".")[-1] not in ["jpg","png","jpeg"]:
                        del imgdirList[i]
                self.imgList.clear()
                self.imgList = [cv2.imread(_dir + "\\" + _d) for _d in imgdirList]
                # print(self.imgList)
                img = self.imgList[0]
                predictList = [img]
                res = self.img_resize(img, self.sourceImage_label)
                img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
                _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                                      QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
                jpg_out = QtGui.QPixmap(_image)  # 转换成QPixmap
                self.sourceImage_label.setPixmap(jpg_out)  # 设置图片显示
                self.sourceImage_label.setAlignment(Qt.AlignCenter)
                results = self.ocr.recognize_text(
                    images=predictList,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
                    use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
                    output_dir='ocr_result',  # 图片的保存路径，默认设为 ocr_result；
                    visualization=True,  # 是否将识别结果保存为图片文件；
                    box_thresh=0.5,  # 检测文本框置信度的阈值；
                    text_thresh=0.5)  # 识别中文文本置信度的阈值；

                for result in results:
                    data = result['data']
                    str = ""
                    for information in data:
                        str += information["text"] + "\n"
                    self.resultTxt_lineedit.setText(str)


    def img_resize(self,image,label):
        height, width = image.shape[0], image.shape[1]
        # 设置新的图片分辨率框架
        width_new = label.width()
        height_new = label.height()
        # 判断图片的长宽比率
        if width / height >= width_new / height_new:
            img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
        else:
            img_new = cv2.resize(image, (int(width * height_new / height), height_new))
        return img_new

    def is_chinese(self,string):
        """
        检查整个字符串是否包含中文
        :param string: 需要检查的字符串
        :return: bool
        """
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True

        return False


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()