from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QWidget, QPushButton, QFileDialog
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QDesktopWidget


# 设置
def showSettingsContent(self):
    # 清空当前内容
    for i in reversed(range(self.layout.count())):
        self.layout.itemAt(i).widget().deleteLater()

    # 加载自定义字体
    font_path = os.path.join(os.path.dirname(__file__), 'font\\HarmonyOS_Sans_Medium.ttf')  # 相对路径
    font_id = QFontDatabase.addApplicationFont(font_path)
    
    # 检查字体是否加载成功
    if font_id != -1:
        self.custom_font = QFont(QFontDatabase.applicationFontFamilies(font_id)[0])
    else:
        self.custom_font = QFont("黑体")  # 默认字体

    # 设置字体
    self.setFont(self.custom_font)

    # 获取屏幕尺寸
    screen = QDesktopWidget().availableGeometry()
    screenWidth = screen.width()
    screenHeight = screen.height()

    # 定义缩放因子
    font_scale_factor = 0.014

    # 计算字体大小
    self.fontPointSize = int(min(screenWidth, screenHeight) * font_scale_factor)
    self.custom_font.setPointSize(self.fontPointSize)

    # 创建一个QWidget作为容器
    container = QWidget()

    # 创建一个垂直布局
    v_layout = QVBoxLayout(container)

    # 设置布局的对齐标志，使所有控件在布局中垂直居中
    v_layout.setAlignment(Qt.AlignCenter)

    # 设置布局的间距
    v_layout.setSpacing(10)

    # 添加按钮,用于修改下载目录
    change_download_dir_button = QPushButton('设置/修改下载目录', self)
    change_download_dir_button.clicked.connect(lambda: change_download_dir(self))
    # 设置按钮的样式和文本对齐
    change_download_dir_button.setStyleSheet(f""" 
        QPushButton {{
            font-family: "{self.custom_font.family()}";
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: {self.fontPointSize + 2}px;
        }}
        QPushButton:hover {{
            background-color: #1976D2; /* 鼠标悬停颜色 */
        }}
        QPushButton:pressed {{
            background-color: #1976D2; /* 点击时颜色 */
        }}
    """)

    
    def change_download_dir(self):
        # 打开下载目录选择对话框
        download_dir = QFileDialog.getExistingDirectory(
            self, '选择下载目录', os.path.expanduser('Downloads')
        )

        # 如果用户选择了下载目录，则保存到配置文件
        if download_dir:
            setDownloadPath(download_dir)

    def setDownloadPath(selected_path):
        # 这里可以根据需要实现设置默认下载路径的逻辑
        # 例如，使用QSettings类保存设置
        config_dir = os.path.join(os.getcwd(), 'config', 'download_file_path')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(os.path.join(config_dir, 'default_path.ini'), 'w') as f:
            f.write(selected_path)
            self.show_custom_message(self, "设置成功", f"下载目录已设置为: {selected_path}", QMessageBox.Information)

            
    # 将按钮添加到布局中
    v_layout.addWidget(change_download_dir_button)

    # 设置容器的布局
    container.setLayout(v_layout)

    # 将容器添加到主窗口的布局中
    self.layout.addWidget(container)
    self.layout.setStretchFactor(container, 1)  # 确保容器在主窗口中垂直居中

    # 设置窗口标题和状态栏消息
    self.setWindowTitle('SectionIstool - 设置')

    # 返回container，以便可以在initUI中使用
    return container
