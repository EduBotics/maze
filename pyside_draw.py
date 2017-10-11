#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PySide tutorial

In this example, we draw text in Russian azbuka.

author: Jan Bodnar
website: zetcode.com
last edited: August 2011
"""

import sys
import math
import random

from PySide import QtGui, QtCore
from PySide.QtGui import QPixmap, QImage, QColor, QPalette


class Robot(object):
    DIRECTIONS = ("RIGHT", "DOWN", "LEFT", "UP")
    ADJUSTMENTS = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def __init__(self, maze=None):
        self.maze = maze
        self.location = (1, 0)
        self.memory = []
        self.corridors = {}
        self.visits = {}

    def move(self):
        if self.location not in self.corridors:
            corridors = self.sense_corridors()
            self.corridors[self.location] = corridors
            self.visits[self.location] = 1
        else:
            if self.visits[self.location] > 1:
                while len(self.memory) and self.memory[-1] != self.location:
                    print "{}: {}".format(self.location, self.memory)
                    del(self.memory[-1])
            corridors = self.corridors[self.location]
            self.visits[self.location] += 1
        print self.location, corridors
        self.memory.append(self.location)

        if len(corridors):
            direction, adjustment = corridors[0]
            self.corridors[self.location] = corridors[1:]
            self.location = (self.location[0] + adjustment[0], self.location[1] + adjustment[1])
        else:
            print "Blocked!"
            exit()

    def sense_corridors(self):
        corridors = []
        for direction, adjustment in zip(self.DIRECTIONS, self.ADJUSTMENTS):
            test_loc = (self.location[0] + adjustment[0], self.location[1] + adjustment[1])
            dest_pix = self.maze.getpixel(*test_loc)
            if dest_pix == self.maze.white:
                corridors.append((direction, adjustment))
        return corridors


class Maze(QtGui.QWidget):

    def __init__(self, boxsize=40):
        super(Maze, self).__init__()
        self.speed = 500
        self.boxsize = boxsize
        self.screenheight = int(math.floor(self.contentsRect().height() / self.boxsize))
        self.screenwidth = int(math.floor(self.contentsRect().width() / self.boxsize))
        self.white = self.palette().color(QPalette.Active, QPalette.Window)
        self.search = True

        self.maze = []
        self.robot = Robot(self)

        # Initialise
        self.timer = QtCore.QBasicTimer()
        self.build_maze()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, self.contentsRect().width() + self.boxsize, self.contentsRect().height() + self.boxsize)
        self.setWindowTitle('Points')
        self.show()
        self.timer.start(self.speed, self)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_walls(qp)
        self.draw_maze(qp)
        self.draw_robot(qp)
        qp.end()

    def draw_walls(self, qp):
        # Draw Top
        for i in range(2, self.screenwidth + 1):
            self.drawSquare(qp, i, 0, 1)
        # Draw Right
        for j in range(0, self.screenheight + 1):
            self.drawSquare(qp, self.screenwidth, j, 1)
        # Draw Bottom
        for i in range(self.screenwidth - 2, -1, -1):
            self.drawSquare(qp, i, self.screenheight, 1)
        # Draw Left
        for j in range(self.screenheight, -1, -1):
            self.drawSquare(qp, 0, j, 1)

    def draw_maze(self, qp):
        for i, j in self.maze:
            self.drawSquare(qp, i, j, 2)

    def draw_robot(self, qp):
        self.drawSquare(qp, self.robot.location[0], self.robot.location[1], 3)

    def build_maze(self):
        random.seed()
        for i in range(1, self.screenwidth):
            for j in range(1, self.screenheight):
                if random.random() < 0.25:
                    if (i < 4 and j < 4):
                        continue
                    if (i > self.screenwidth - 4 and j > self.screenheight - 4):
                        continue
                    self.maze.append((i, j))

    def squareWidth(self):
        return self.boxsize

    def squareHeight(self):
        return self.boxsize

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QtGui.QColor(colorTable[shape])
        _x = x * self.boxsize
        _y = y * self.boxsize
        painter.fillRect(
            _x + 1, _y + 1,
            self.squareWidth() - 2, self.squareHeight() - 2,
            color
        )

        painter.setPen(color.lighter())
        painter.drawLine(_x, _y + self.squareHeight() - 1, _x, _y)
        painter.drawLine(_x, _y, _x + self.squareWidth() - 1, _y)

        painter.setPen(color.darker())
        painter.drawLine(
            _x + 1, _y + self.squareHeight() - 1,
            _x + self.squareWidth() - 1, _y + self.squareHeight() - 1
        )
        painter.drawLine(
            _x + self.squareWidth() - 1, _y + self.squareHeight() - 1,
            _x + self.squareWidth() - 1, _y + 1
        )

    def timerEvent(self, event):
        if self.search:
            if self.robot.location != (self.screenwidth - 1, self.screenheight):
                self.robot.move()
            else:
                # Exit found
                print "Complete"
                print "Rerun..."
                self.search = False
                self.memory_index = 0
        else:
            if self.memory_index == len(self.robot.memory):
                print "Completed"
                exit()
            else:
                self.robot.location = self.robot.memory[self.memory_index]
                print "MEM: {}: LOC: {}".format(self.memory_index, self.robot.location)
                self.memory_index += 1
        self.update()

    def getpixel(self, x, y):
        _x = int((x + 0.5) * self.boxsize)
        _y = int((y + 0.5) * self.boxsize)
        qpx = QPixmap.grabWidget(self)
        image = QImage(qpx.toImage())
        color = QColor(image.pixel(_x, _y))
        return color


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Maze(boxsize=int(sys.argv[1]))  # noqa
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
