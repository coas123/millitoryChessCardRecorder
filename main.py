import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QMainWindow, QButtonGroup, QRadioButton, QWidget, QDialog

num = 0

def buttonClick(which):
    global num
    num = which
    subWidget.setHidden(False)

def handleComb():
    chosenText = comb.checkedButton().text()
    btNow = btList[num]
    btNow.setText(chosenText)
    comb.setExclusive(False)
    for button in buttonList:
        button.setChecked(False)
    comb.setExclusive(True)
    subWidget.setHidden(True)

def clearAll():
    for bt in btList:
        bt.setText("")

app = QApplication(sys.argv)
widget = QWidget()

btClear = QPushButton("清除", widget)
btClear.move(20, 300)
btClear.clicked.connect(clearAll)

def getChase(id,x,y):
    button = QPushButton("", widget)
    button.setFixedWidth(40)
    button.setFixedHeight(40)
    button.move(x, y)
    button.clicked.connect(lambda: buttonClick(id))
    return button

# 上家的棋
bt0 = getChase(0,20,40)
bt1 = getChase(1,60,40)
bt2 = getChase(2,100,40)
bt3 = getChase(3,140,40)
bt4 = getChase(4,180,40)
bt5 = getChase(5,220,40)

bt6 = getChase(6,20,80)
bt7 = getChase(7,60,80)
bt8 = getChase(8,140,80)
bt9 = getChase(9,220,80)

bt10 = getChase(10,20,120)
bt11 = getChase(11,60,120)
bt12 = getChase(12,100,120)
bt13 = getChase(13,180,120)
bt14 = getChase(14,220,120)

bt15 = getChase(15,20,160)
bt16 = getChase(16,60,160)
bt17 = getChase(17,140,160)
bt18 = getChase(18,220,160)

bt19 = getChase(19,20,200)
bt20 = getChase(20,60,200)
bt21 = getChase(21,100,200)
bt22 = getChase(22,140,200)
bt23 = getChase(23,180,200)
bt24 = getChase(24,220,200)

# 下家的棋
bt25 = getChase(25,300,40)
bt26 = getChase(26,340,40)
bt27 = getChase(27,380,40)
bt28 = getChase(28,420,40)
bt29 = getChase(29,460,40)
bt30 = getChase(30,500,40)

bt31 = getChase(31,300,80)
bt32 = getChase(32,380,80)
bt33 = getChase(33,460,80)
bt34 = getChase(34,500,80)

bt35 = getChase(35,300,120)
bt36 = getChase(36,340,120)
bt37 = getChase(37,420,120)
bt38 = getChase(38,460,120)
bt39 = getChase(39,500,120)

bt40 = getChase(40,300,160)
bt41 = getChase(41,380,160)
bt42 = getChase(42,460,160)
bt43 = getChase(43,500,160)

bt44 = getChase(44,300,200)
bt45 = getChase(45,340,200)
bt46 = getChase(46,380,200)
bt47 = getChase(47,420,200)
bt48 = getChase(48,460,200)
bt49 = getChase(49,500,200)

btList = [bt0, bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9, bt10, bt11, bt12, bt13, bt14, bt15, bt16, bt17, bt18, bt19, bt20, bt21, bt22, bt23, bt24, bt25, bt26, bt27, bt28, bt29, bt30, bt31, bt32, bt33, bt34, bt35, bt36, bt37, bt38, bt39, bt40, bt41, bt42, bt43, bt44, bt45, bt46, bt47, bt48, bt49]

btNow = bt0

subWidget = QWidget(widget)
subWidget.setFixedWidth(200)
subWidget.setFixedHeight(200)
subWidget.move(180,230)
subWidget.setHidden(True)

comb = QButtonGroup(subWidget)

button1 = QRadioButton("司", subWidget)
button1.move(10,20)
button2 = QRadioButton("军", subWidget)
button2.move(50,20)
button3 = QRadioButton("师", subWidget)
button3.move(90,20)
button4 = QRadioButton("旅", subWidget)
button4.move(130,20)
button5 = QRadioButton("团", subWidget)
button5.move(10,50)
button6 = QRadioButton("营", subWidget)
button6.move(50,50)
button7 = QRadioButton("连", subWidget)
button7.move(90,50)
button8 = QRadioButton("排", subWidget)
button8.move(130,50)
button9 = QRadioButton("兵", subWidget)
button9.move(10,80)
button10 = QRadioButton("炸", subWidget)
button10.move(50,80)
button11 = QRadioButton("雷", subWidget)
button11.move(90,80)
button12 = QRadioButton("旗", subWidget)
button12.move(130,80)
button13 = QRadioButton("大", subWidget)
button13.move(10,110)
button14 = QRadioButton("中", subWidget)
button14.move(50,110)
button15 = QRadioButton("小", subWidget)
button15.move(90,110)
button16 = QRadioButton("!", subWidget)
button16.move(10,140)
button17 = QRadioButton("?", subWidget)
button17.move(50,140)
button18 = QRadioButton("*", subWidget)
button18.move(90,140)
button19 = QRadioButton("", subWidget)
button19.move(130,140)

buttonList = [button1,button2,button3,button4,button5,button6,button7,button8,button9,button10,button11,button12,button13,button14,button15,button16,button17,button18,button19]

comb.addButton(button1)
comb.addButton(button2)
comb.addButton(button3)
comb.addButton(button4)
comb.addButton(button5)
comb.addButton(button6)
comb.addButton(button7)
comb.addButton(button8)
comb.addButton(button9)
comb.addButton(button10)
comb.addButton(button11)
comb.addButton(button12)
comb.addButton(button13)
comb.addButton(button14)
comb.addButton(button15)
comb.addButton(button16)
comb.addButton(button17)
comb.addButton(button18)
comb.addButton(button19)

comb.buttonClicked.connect(handleComb)

comb.setParent(widget)




widget.resize(600, 400)
widget.setWindowTitle("军旗记牌器")
widget.show()
sys.exit(app.exec())




