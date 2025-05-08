import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QPushButton, QMainWindow, QButtonGroup, 
                            QRadioButton, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, 
                            QLabel, QGroupBox, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QIcon

# 添加兼容层处理旧版Windows系统
def get_safe_path(path):
    """安全处理路径，避免使用现代Windows API"""
    try:
        # 使用基本os.path功能替代新API
        return os.path.normpath(path)
    except:
        return path

class ChessButton(QPushButton):
    def __init__(self, id, parent=None):
        super().__init__("", parent)
        self.id = id
        self.setFixedSize(40, 40)
        # 使用更通用的字体
        try:
            self.setFont(QFont("SimHei", 12, QFont.Bold))
        except:
            # 后备字体方案
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.setFont(font)
        
class ChessSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)
        self.setFixedWidth(300)
        
        layout = QVBoxLayout()
        
        # 添加标题
        title = QLabel("选择棋子类型")
        title.setAlignment(Qt.AlignCenter)
        try:
            title.setFont(QFont("SimHei", 10, QFont.Bold))
        except:
            font = QFont()
            font.setPointSize(10)
            font.setBold(True)
            title.setFont(font)
        layout.addWidget(title)
        
        # 创建棋子选择网格
        grid = QGridLayout()
        
        self.buttonGroup = QButtonGroup(self)
        self.buttonList = []
        
        # 棋子类型
        pieces = [
            "司", "军", "师", "旅", "团", "营", "连", "排", "兵", 
            "炸", "雷", "旗", "大", "中", "小", "!", "?", "*", ""
        ]
        
        # 创建单选按钮并添加到网格中
        row, col = 0, 0
        for i, piece in enumerate(pieces):
            button = QRadioButton(piece)
            try:
                button.setFont(QFont("SimHei", 12))
            except:
                font = QFont()
                font.setPointSize(12)
                button.setFont(font)
            self.buttonGroup.addButton(button)
            self.buttonList.append(button)
            grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        layout.addLayout(grid)
        self.setLayout(layout)
        
class MilitaryChessRecorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currentButton = None
        self.chessButtons = []
        self.initUI()
        
    def initUI(self):
        # 主窗口设置
        self.setWindowTitle("军旗记牌器")
        self.setFixedSize(640, 350)
        
        # 设置窗口始终显示在最上面
        try:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        except:
            # 如果设置窗口标志失败，忽略错误
            pass
        
        # 创建中央窗口部件
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        
        # 主布局
        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        
        # 创建两个棋盘区域
        boardsLayout = QHBoxLayout()
        
        # 上家棋盘
        topGroupBox = QGroupBox("上家")
        try:
            topGroupBox.setFont(QFont("SimHei", 12))
        except:
            font = QFont()
            font.setPointSize(12)
            topGroupBox.setFont(font)
        topLayout = QGridLayout()
        self.createChessBoard(topLayout, 0, 5, 5)
        topGroupBox.setLayout(topLayout)
        
        # 下家棋盘
        bottomGroupBox = QGroupBox("下家")
        try:
            bottomGroupBox.setFont(QFont("SimHei", 12))
        except:
            font = QFont()
            font.setPointSize(12)
            bottomGroupBox.setFont(font)
        bottomLayout = QGridLayout()
        self.createChessBoard(bottomLayout, 25, 5, 5, flip=True)
        bottomGroupBox.setLayout(bottomLayout)
        
        boardsLayout.addWidget(topGroupBox)
        boardsLayout.addWidget(bottomGroupBox)
        mainLayout.addLayout(boardsLayout)
        
        # 底部按钮区域
        buttonLayout = QHBoxLayout()
        
        self.clearButton = QPushButton("清除所有")
        try:
            self.clearButton.setFont(QFont("SimHei", 10))
        except:
            font = QFont()
            font.setPointSize(10)
            self.clearButton.setFont(font)
        self.clearButton.clicked.connect(self.clearAll)
        
        self.saveButton = QPushButton("保存")
        try:
            self.saveButton.setFont(QFont("SimHei", 10))
        except:
            font = QFont()
            font.setPointSize(10)
            self.saveButton.setFont(font)
        self.saveButton.clicked.connect(self.saveState)
        
        self.loadButton = QPushButton("加载")
        try:
            self.loadButton.setFont(QFont("SimHei", 10))
        except:
            font = QFont()
            font.setPointSize(10)
            self.loadButton.setFont(font)
        self.loadButton.clicked.connect(self.loadState)
        
        self.topMostButton = QPushButton("取消置顶")
        try:
            self.topMostButton.setFont(QFont("SimHei", 10))
        except:
            font = QFont()
            font.setPointSize(10)
            self.topMostButton.setFont(font)
        self.topMostButton.clicked.connect(self.toggleTopMost)
        
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.loadButton)
        buttonLayout.addWidget(self.topMostButton)
        
        mainLayout.addLayout(buttonLayout)
        
        # 创建棋子选择器
        self.chessSelector = ChessSelector(self)
        self.chessSelector.buttonGroup.buttonClicked.connect(self.handleSelection)
        self.chessSelector.hide()
        
        # 设置样式
        self.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QPushButton {
            background-color: #e0e0e0;
            border: 1px solid #b0b0b0;
            border-radius: 4px;
            padding: 4px;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        QGroupBox {
            border: 2px solid #c0c0c0;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
        }
        ChessButton {
            background-color: #f0f0f0;
            border: 2px solid #a0a0a0;
        }
        ChessButton:hover {
            background-color: #e5e5e5;
            border: 2px solid #808080;
        }
        """)
        
    def createChessBoard(self, layout, startId, cols, rows, flip=False):
        """创建棋盘网格
        
        参数:
            layout: 布局管理器
            startId: 起始按钮ID
            cols: 列数
            rows: 行数
            flip: 是否镜像列布局
        """
        # 创建棋盘的特定布局 (基于军旗游戏)
        chessPositions = [
            # 第一行
            [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5)],
            # 第二行
            [(1,0), (1,1), None, (1,3), None, (1,5)],
            # 第三行
            [(2,0), (2,1), (2,2), None, (2,4), (2,5)],
            # 第四行
            [(3,0), (3,1), None, (3,3), None, (3,5)],
            # 第五行
            [(4,0), (4,1), (4,2), (4,3), (4,4), (4,5)]
        ]
        
        # 如果需要镜像列布局
        if flip:
            # 只镜像列顺序，不颠倒行
            flipped_positions = []
            # 总列数减1（0-based索引）
            total_cols = 5
            
            for row_index, row_positions in enumerate(chessPositions):
                new_row = []
                for pos in row_positions:
                    if pos is not None:
                        # 只镜像列索引: (total_cols - pos[1])，保持行索引不变
                        new_row.append((pos[0], total_cols - pos[1]))
                    else:
                        new_row.append(None)
                flipped_positions.append(new_row)
            chessPositions = flipped_positions
            
        buttonId = startId
        
        for row, positions in enumerate(chessPositions):
            for col, pos in enumerate(positions):
                if pos is not None:
                    button = ChessButton(buttonId, self)
                    button.clicked.connect(lambda checked, btn=button: self.buttonClick(btn))
                    layout.addWidget(button, pos[0], pos[1])
                    self.chessButtons.append(button)
                    buttonId += 1
        
    def buttonClick(self, button):
        try:
            self.currentButton = button
            
            # 显示选择器在按钮附近
            buttonPos = button.mapToGlobal(QPoint(0, 0))
            self.chessSelector.move(buttonPos + QPoint(button.width(), 0))
            self.chessSelector.show()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"点击处理出错: {str(e)}")
        
    def handleSelection(self, radioButton):
        try:
            if self.currentButton:
                self.currentButton.setText(radioButton.text())
                
                # 根据选项设置不同的样式
                text = radioButton.text()
                if text in ["司", "军", "师"]:
                    self.currentButton.setStyleSheet("background-color: #ffe6e6;")
                elif text in ["旅", "团", "营", "连", "排", "兵"]:
                    self.currentButton.setStyleSheet("background-color: #e6f2ff;")
                elif text in ["炸", "雷", "旗"]:
                    self.currentButton.setStyleSheet("background-color: #ffffcc;")
                elif text in ["大", "中", "小"]:
                    self.currentButton.setStyleSheet("background-color: #e6ffe6;")
                elif text in ["!", "?", "*"]:
                    self.currentButton.setStyleSheet("background-color: #f2e6ff;")
                else:
                    self.currentButton.setStyleSheet("")
                    
            self.chessSelector.hide()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"选择处理出错: {str(e)}")
        
    def clearAll(self):
        try:
            for button in self.chessButtons:
                button.setText("")
                button.setStyleSheet("")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"清除出错: {str(e)}")
            
    def saveState(self):
        """保存当前标记状态到文件"""
        try:
            fileName, _ = QFileDialog.getSaveFileName(self, "保存记录", "", 
                                                   "军旗记录文件 (*.jq);;所有文件 (*)")
            if fileName:
                # 确保文件名有正确的扩展名
                if not fileName.lower().endswith('.jq'):
                    fileName += '.jq'
                
                # 使用安全路径处理
                fileName = get_safe_path(fileName)
                
                data = []
                for button in self.chessButtons:
                    data.append({
                        'id': button.id,
                        'text': button.text(),
                        'style': button.styleSheet()
                    })
                    
                with open(fileName, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                QMessageBox.information(self, "保存成功", "记录已成功保存！")
        except Exception as e:
            QMessageBox.warning(self, "保存失败", f"保存记录时出错: {str(e)}")
                
    def loadState(self):
        """从文件加载标记状态"""
        try:
            fileName, _ = QFileDialog.getOpenFileName(self, "加载记录", "", 
                                                   "军旗记录文件 (*.jq);;所有文件 (*)")
            if fileName:
                # 使用安全路径处理
                fileName = get_safe_path(fileName)
                
                with open(fileName, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                button_dict = {btn.id: btn for btn in self.chessButtons}
                
                for item in data:
                    if item['id'] in button_dict:
                        button = button_dict[item['id']]
                        button.setText(item['text'])
                        button.setStyleSheet(item['style'])
                        
                QMessageBox.information(self, "加载成功", "记录已成功加载！")
        except UnicodeError:
            # 尝试不同的编码
            try:
                with open(fileName, 'r', encoding='gbk') as f:
                    data = json.load(f)
                # 处理数据...
                QMessageBox.information(self, "加载成功", "记录已成功加载！")
            except Exception as e:
                QMessageBox.warning(self, "加载失败", f"加载记录时出错: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "加载失败", f"加载记录时出错: {str(e)}")

    def toggleTopMost(self):
        try:
            flags = self.windowFlags()
            if flags & Qt.WindowStaysOnTopHint:
                # 取消置顶
                self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
                self.topMostButton.setText("置顶窗口")
            else:
                # 设置置顶
                self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
                self.topMostButton.setText("取消置顶")
            self.show()  # 必须重新显示窗口才能应用标志更改
        except Exception as e:
            QMessageBox.warning(self, "错误", f"切换置顶状态出错: {str(e)}")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MilitaryChessRecorder()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        # 捕获主程序异常
        QMessageBox.critical(None, "程序错误", f"程序启动失败: {str(e)}")
        sys.exit(1)




