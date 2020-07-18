import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import csv

WIDTH = 800
HEIGHT = 800

class ec_polarization(QWidget):    
    angle_list = []
    resol = math.radians(15) #resolution degree
    def __init__(self, parent = None):
        super(ec_polarization, self).__init__(parent)
        self.initUI()
        self.setMouseTracking(True)
    
    def initUI(self):
        self.btn_generate()

        layout_top = QHBoxLayout()
        layout_top.addWidget(self.btn_open)
        layout_top.addWidget(self.btn_save)
        layout_top.addWidget(self.btn_close)

        self.label_img = image_board(self)
        layout_mid = QHBoxLayout()
        layout_mid.addStretch(1)
        layout_mid.addWidget(self.label_img)
        layout_mid.addStretch(1)

        layout_bot = QHBoxLayout()
        layout_bot.addStretch(1)
        layout_bot.addWidget(self.btn_add)
        layout_bot.addWidget(self.btn_del)
        layout_bot.addStretch(1)
        
        self.label_angle = QLabel(self)
        layout_l = QVBoxLayout()
        layout_l.addStretch(1)
        layout_l.addLayout(layout_top)
        layout_l.addLayout(layout_mid)
        layout_l.addLayout(layout_bot)
        layout_l.addWidget(self.label_angle)
        layout_l.addStretch(1)
        
        self.tree_list = QTreeWidget(self)
        self.tree_list.setFixedSize(400, 200)
        self.tree_list.setColumnWidth(0, 250)
        headers = ['(x1,y1) -> (x2,y2)', 'angle (degree)']
        self.tree_list.setColumnCount(len(headers))
        self.tree_list.setHeaderLabels(headers)
        
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFixedSize(400, 400)
        layout_r = QVBoxLayout()
        layout_r.addWidget(self.tree_list)        
        layout_r.addWidget(self.btn_angle)
        layout_r.addWidget(self.canvas)

        layout = QHBoxLayout()
        layout.addLayout(layout_l)
        layout.addLayout(layout_r)
        self.setLayout(layout)
        self.setGeometry(300,300, 1000,700)
        self.setWindowTitle("EC Polarization")


    def btn_generate (self):
        self.btn_open = QPushButton("Open Image")
        self.btn_open.clicked.connect(self.open_image)

        self.btn_save = QPushButton("Save Angles")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.save_angles)
        
        self.btn_close = QPushButton("Close Image")
        self.btn_close.setEnabled(False)
        self.btn_close.clicked.connect(self.close_image)

        self.btn_add = QPushButton("Add Vector")
        self.btn_add.setEnabled(False)
        self.btn_add.clicked.connect(self.add_vector)

        self.btn_del = QPushButton("Delete Vector")
        self.btn_del.setEnabled(False)
        self.btn_del.clicked.connect(self.del_vector)
        
        self.btn_angle = QPushButton("to Angle")
        self.btn_angle.clicked.connect(self.convert_to_angle)
		
    def open_image(self):
        self.label_img.fname = QFileDialog.getOpenFileName(self, 'Open file', './')[0]
        self.label_img.flag_draw = 1
        self.btn_save.setEnabled(True)
        self.btn_close.setEnabled(True)
        self.btn_add.setEnabled(True)
        self.btn_del.setEnabled(True)
        self.label_img.update()
        self.update()
        
    def save_angles(self):
        text, okPressed = QInputDialog.getText(self, "Get text","File Name to Save", QLineEdit.Normal, "")
        if okPressed and text != '':
            f = open(text, 'w', encoding='utf-8-sig')
            wr = csv.writer(f)
            for angle in self.angle_list:
                wr.writerow([math.degrees(angle)])
            f.close()

    def close_image(self):
        self.btn_save.setEnabled(False)
        self.btn_close.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.btn_del.setEnabled(False)
        self.label_img.close_image()
        self.label_img.vector_list.clear()
        self.tree_list.clear()
        self.update()

    def add_vector(self):
        data = [self.label_img.coord[2], self.label_img.coord[3], self.label_img.coord[4], self.label_img.coord[5]]
        angle = get_angle(self.label_img.coord)
        
        
        item = QTreeWidgetItem()
        item.setText(0, "(%d, %d) -> (%d, %d)"%tuple(data))
        item.setText(1, " %.1f degree" % math.degrees(angle))

        QTreeWidget.invisibleRootItem(self.tree_list).addChild(item)
        
        self.label_img.vector_list.append(self.label_img.coord)
        self.angle_list.append(angle)
        
        self.label_img.reset_xy()
        self.update()
        
    def del_vector(self):
        item = self.tree_list.selectedIndexes()[0]
        self.angle_list.pop(item.row())

        for item in self.tree_list.selectedItems():
            #print(self.label_img.vector_list.index(item))
            del self.label_img.vector_list[QTreeWidget.invisibleRootItem(self.tree_list).indexOfChild(item)]
            self.tree_list.invisibleRootItem().removeChild(item)

        self.update()

    def convert_to_angle(self):
        
        if len(self.angle_list):
            ax = self.fig.add_subplot(111, projection='polar')  # fig를 1행 1칸으로 나누어 1칸안에 넣어줍니다
            ax.clear()
            r = self.resol
            theta = np.linspace(0, 2 * np.pi, num=24, endpoint=False)
            angles = np.zeros(len(theta), dtype=int)
        
            for angle in self.angle_list:
                idx = 0
                if angle < 2*np.pi-r/2:
                    idx = round(angle /r)
                angles[idx] = angles[idx] + 1
            ax.bar(theta, angles, width=0.3, color='b', bottom=0.0, alpha=0.5)
            ax.set_theta_offset(np.pi/2.0)    # rotate
            ax.set_theta_direction(-1)         # clockwise
            ax.set_yticklabels([])              # ytick remove

            self.canvas.draw()


class image_board(QWidget):
    fname = 'sample.tif'
    flag_draw = 0
    
    # For draw line [origin x, origin y, axis x, axis y, vector x, vector y]
    coord = [-1, -1, -1, -1, -1, -1]
    
    # real-time line drawing
    x = -1
    y = -1
    
    # for arrow [left x, left y, right x, right y]
    arrow = [-1, -1, -1, -1]    

    # For draw line history
    vector_list = []

    def __init__ (self, parent):
        QWidget.__init__(self, parent)
        self.setFixedSize(WIDTH,HEIGHT)
        self.setMouseTracking(True)

    # self.update()
    def paintEvent(self, event):        
        if self.flag_draw == 1:
            painter = QPainter()  #Painting the line
            self.image = QPixmap(self.fname)

            img_width = self.image.width()
            img_height = self.image.height()
          
            # Canvas Resizing
            if img_width < WIDTH and img_height < HEIGHT:   # If image is smaller than canvas (WIDTH, HEIGHT)
                self.setFixedSize(img_width, img_height)
            else:
                scale_w = img_width/WIDTH
                scale_h = img_height/HEIGHT
                scale = max(scale_w, scale_h)
                self.setFixedSize( int(img_width/scale), int(img_height/scale))

                
            painter.begin(self)
            painter.drawPixmap(self.rect(), self.image)
            
            for vec in self.vector_list:
                pen = QPen(Qt.yellow, 2)
                painter.setPen(pen)
                xl, yl, xr, yr = get_arrow(vec[0], vec[1], vec[4], vec[5])
                painter.drawLine(vec[0], vec[1], vec[4], vec[5])
                painter.drawLine(xl, yl, vec[4], vec[5])
                painter.drawLine(xr, yr, vec[4], vec[5])

            if self.coord[0] != -1 and self.coord[1] != -1 :
                if self.coord[2] != -1 and self.coord[3] != -1 :
                    pen = QPen(Qt.white, 2)
                    painter.setPen(pen)
                    xl, yl, xr, yr = get_arrow(self.coord[0], self.coord[1], self.coord[2], self.coord[3])
                    painter.drawLine(self.coord[0], self.coord[1], self.coord[2], self.coord[3])
                    painter.drawLine(xl, yl, self.coord[2], self.coord[3])
                    painter.drawLine(xr, yr, self.coord[2], self.coord[3])    
                
                pen = QPen(Qt.red, 2)
                painter.setPen(pen)
                xl, yl, xr, yr = get_arrow(self.coord[0], self.coord[1], self.x, self.y)
                painter.drawLine(self.coord[0], self.coord[1], self.x, self.y)
                painter.drawLine(xl, yl, self.x, self.y)
                painter.drawLine(xr, yr, self.x, self.y)
            
            painter.end()
            
    def mouseMoveEvent(self, event):
        if self.flag_draw and self.coord[0] != -1 and self.coord[1] != -1 and self.coord[4] == -1 and self.coord[5] == -1:
            self.x = event.x()
            self.y = event.y()
            if self.coord[2] != -1 and self.coord[3] != -1:
                angle = get_angle([self.coord[0], self.coord[1], self.coord[2], self.coord[3], self.x, self.y])
                txt_angle = "Angle: %.1f degree" % math.degrees(angle)
                
            self.update()

    def mousePressEvent(self, event):
        if self.flag_draw :
            if self.coord[4] != -1 and self.coord[5] != -1:
                self.reset_xy()

            if self.coord[0] == -1 and self.coord[1] == -1 :
                self.coord[0] = event.x()
                self.coord[1] = event.y()
            elif self.coord[2] == -1 and self.coord[3] == -1 :
                self.coord[2] = event.x()
                self.coord[3] = event.y()
                self.update()
            elif self.coord[4] == -1 and self.coord[5] == -1 :
                self.coord[4] = event.x()
                self.coord[5] = event.y()
                self.update()


    def close_image(self):
        self.flag_draw = 0
        self.flag_line = 0
        self.reset_xy()
        self.angle_list = []
        self.x = -1
        self.y = -1
        self.update()
    
    def reset_xy(self):
        self.coord = [-1, -1, -1, -1, -1, -1]

def get_angle(coord):
    axis_theta = math.atan2(coord[3] - coord[1], coord[2] - coord[0])
    vec_theta = math.atan2(coord[5] - coord[1], coord[4] - coord[0])
    angle = vec_theta-axis_theta  
    if angle < 0 :
        angle = 2*np.pi + angle
    return angle
    
def get_arrow(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    theta = math.atan2(dy, dx)
    length = math.sqrt( dx * dx + dy * dy)
    xl = int(x2 - 10 * math.sin(-theta - math.radians(-45)))
    yl = int(y2 - 10 * math.cos(-theta - math.radians(-45)))
    xr = int(x2 - 10 * math.cos(math.radians(-45) +theta ))
    yr = int(y2 - 10 * math.sin(math.radians(-45) +theta ))
    return xl, yl, xr, yr

def main():
    app = QApplication(sys.argv)
    ex = ec_polarization()
    ex.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()
