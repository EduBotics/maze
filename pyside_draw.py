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
from collections import namedtuple


class Location(object):
    LOCATION = namedtuple("Location", ["x", "y"])
    CACHE = {}

    def __new__(cls, *args):
        x, y = args
        location = cls.LOCATION(x, y)
        if location in cls.CACHE:
            return cls.CACHE[location]
        else:
            return super(Location, cls).__new__(cls, *args)

    def __init__(self, x, y):
        location = self.LOCATION(x, y)
        self._location = location
        self.CACHE[location] = self

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    @property
    def x(self):
        return self._location.x

    @property
    def y(self):
        return self._location.y

    def __call__(self):
        return self._location

    def __add__(self, adjustment):
        try:
            return Location(
                self.x + adjustment.x,
                self.y + adjustment.y
            )
        except AttributeError:
            try:
                return Location(
                    self.x + adjustment[0],
                    self.y + adjustment[1]
                )
            except IndexError:
                raise


class LinkedList(object):
    class LinkedListItem(object):
        def __init__(self, value=None, next=None, prev=None):
            self._next = next
            self._prev = prev
            self._value = value

        @property
        def next(self):
            return self._next

        @next.setter
        def next(self, item):
            self._next = item

        @property
        def prev(self):
            return self._prev

        @prev.setter
        def prev(self, item):
            self._prev = item

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, val):
            self._value = val

    def __init__(self, root=None):
        self._root = self.LinkedListItem(value=root)
        self._head = None

    def __str__(self):
        out = ""
        item = self.root
        out += item.value
        while item.next:
            item = item.next
            out += ";{}".format(item.value)
        return out

    @property
    def root(self):
        return self._root

    @property
    def head(self):
        if self._head is None:
            item = self.root
            while item.next:
                item = item.next
            self._head = item
        return self._head

    @head.setter
    def head(self, item):
        self._head = item

    def append(self, value):
        item = self.head
        item.next = self.LinkedListItem(value=value, prev=item)
        self._head = item.next


class Robot(object):
    DIRECTIONS = ("RIGHT", "DOWN", "LEFT", "UP")
    ADJUSTMENTS = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def __init__(self, maze=None):
        self.maze = maze
        self.location = Location(1, 0)
        self.memory = LinkedList(root=self.location)
        self.corridors = {}
        self.visits = {}

    def move(self):
        self.memory.append(self.location)
        if self.location not in self.corridors:
            corridors = self.sense_corridors()
            self.corridors[self.location] = corridors
            self.visits[self.location] = 1
        else:
            if self.visits[self.location] > 1:
                print "Backtracking..."
                item = self.memory.head.prev
                print "Checking {}".format(item.value)
                while item.value != self.location:
                    item = item.prev
                    print "Checking {}".format(item.value)
                self.memory.head = item.prev
                print "Set head to {}".format(self.memory.head.value)

            corridors = self.corridors[self.location]
            self.visits[self.location] += 1

        if len(corridors):
            direction, adjustment = corridors[0]
            self.corridors[self.location] = corridors[1:]
            self.location += adjustment
        else:
            print "Blocked!"
            exit()

    def sense_corridors(self):
        corridors = []
        for direction, adjustment in zip(self.DIRECTIONS, self.ADJUSTMENTS):
            test_loc = self.location + adjustment
            dest_pix = self.maze.getpixel(test_loc.x, test_loc.y)
            if dest_pix == self.maze.white:
                corridors.append((direction, adjustment))
        return corridors


class Maze(QtGui.QWidget):

    def __init__(self, boxsize=40):
        super(Maze, self).__init__()
        self.speed = 500
        self.boxsize = boxsize
        self.screenheight = int(
            math.floor(self.contentsRect().height() / self.boxsize)
        )
        self.screenwidth = int(
            math.floor(self.contentsRect().width() / self.boxsize)
        )
        self.white = self.palette().color(QPalette.Active, QPalette.Window)
        self.search = True

        self.maze = []
        self.robot = Robot(self)
        self.end_location = Location(self.screenwidth - 1, self.screenheight)

        # Initialise
        self.timer = QtCore.QBasicTimer()
        self.build_maze()
        self.initUI()

    def initUI(self):
        self.setGeometry(
            300, 300,
            self.contentsRect().width() + self.boxsize,
            self.contentsRect().height() + self.boxsize
        )
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
        self.drawSquare(qp, self.robot.location.x, self.robot.location.y, 3)

    def build_maze(self):
        random.seed()
        for i in range(1, self.screenwidth):
            for j in range(1, self.screenheight):
                if random.random() < 0.25:
                    if (i < 4 and j < 4):
                        continue
                    if (i > self.screenwidth - 4 and j > self.screenheight - 4):  # noqa
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
            if (self.robot.location != self.end_location):
                self.robot.move()
            else:
                # Exit found
                print "Complete"
                print "Rerun..."
                self.search = False
                self.memory_index = self.robot.memory.root
        else:
            self.robot.location = self.memory_index.value
            print "MEM: {}".format(self.memory_index.value)
            if self.memory_index.next:
                self.memory_index = self.memory_index.next
            else:
                print "Completed"
                exit()
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
