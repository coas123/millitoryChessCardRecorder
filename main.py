import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QPushButton, QMainWindow, QButtonGroup, 
                            QRadioButton, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, 
                            QLabel, QGroupBox, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QIcon

class ChessButton(QPushButton):
    def __init__(self, id, parent=None):
        super().__init__("", parent)
        self.id = id
        self.setFixedSize(40, 40)
        self.setFont(QFont("SimHei", 12, QFont.Bold))
        
class ChessSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)
        self.setFixedWidth(240)
        
        layout = QVBoxLayout()
        
        # 添加标题
        title = QLabel("选择棋子类型")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("SimHei", 10, QFont.Bold))
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
            button.setFont(QFont("SimHei", 12))
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
        topGroupBox.setFont(QFont("SimHei", 12))
        topLayout = QGridLayout()
        self.createChessBoard(topLayout, 0, 5, 5)
        topGroupBox.setLayout(topLayout)
        
        # 下家棋盘
        bottomGroupBox = QGroupBox("下家")
        bottomGroupBox.setFont(QFont("SimHei", 12))
        bottomLayout = QGridLayout()
        self.createChessBoard(bottomLayout, 25, 5, 5)
        bottomGroupBox.setLayout(bottomLayout)
        
        boardsLayout.addWidget(topGroupBox)
        boardsLayout.addWidget(bottomGroupBox)
        mainLayout.addLayout(boardsLayout)
        
        # 底部按钮区域
        buttonLayout = QHBoxLayout()
        
        self.clearButton = QPushButton("清除所有")
        self.clearButton.setFont(QFont("SimHei", 10))
        self.clearButton.clicked.connect(self.clearAll)
        
        self.saveButton = QPushButton("保存")
        self.saveButton.setFont(QFont("SimHei", 10))
        self.saveButton.clicked.connect(self.saveState)
        
        self.loadButton = QPushButton("加载")
        self.loadButton.setFont(QFont("SimHei", 10))
        self.loadButton.clicked.connect(self.loadState)
        
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.loadButton)
        
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
        
    def createChessBoard(self, layout, startId, cols, rows):
        """创建棋盘网格"""
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
        self.currentButton = button
        
        # 显示选择器在按钮附近
        buttonPos = button.mapToGlobal(QPoint(0, 0))
        self.chessSelector.move(buttonPos + QPoint(button.width(), 0))
        self.chessSelector.show()
        
    def handleSelection(self, radioButton):
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
        
    def clearAll(self):
        for button in self.chessButtons:
            button.setText("")
            button.setStyleSheet("")
            
    def saveState(self):
        """保存当前标记状态到文件"""
        fileName, _ = QFileDialog.getSaveFileName(self, "保存记录", "", 
                                                 "军旗记录文件 (*.jq);;所有文件 (*)")
        if fileName:
            data = []
            for button in self.chessButtons:
                data.append({
                    'id': button.id,
                    'text': button.text(),
                    'style': button.styleSheet()
                })
                
            try:
                with open(fileName, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                QMessageBox.information(self, "保存成功", "记录已成功保存！")
            except Exception as e:
                QMessageBox.warning(self, "保存失败", f"保存记录时出错: {str(e)}")
                
    def loadState(self):
        """从文件加载标记状态"""
        fileName, _ = QFileDialog.getOpenFileName(self, "加载记录", "", 
                                                 "军旗记录文件 (*.jq);;所有文件 (*)")
        if fileName:
            try:
                with open(fileName, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                button_dict = {btn.id: btn for btn in self.chessButtons}
                
                for item in data:
                    if item['id'] in button_dict:
                        button = button_dict[item['id']]
                        button.setText(item['text'])
                        button.setStyleSheet(item['style'])
                        
                QMessageBox.information(self, "加载成功", "记录已成功加载！")
            except Exception as e:
                QMessageBox.warning(self, "加载失败", f"加载记录时出错: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MilitaryChessRecorder()
    window.show()
    sys.exit(app.exec_())




