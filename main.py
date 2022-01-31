import tkinter as tk
from tkinter import filedialog
import os.path
import csv
import xml.etree.ElementTree as ET

from abc import ABC, abstractmethod


# Here used Composite pattern


# Abstract class


class Template(ABC):

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def change(self):
        pass

    @abstractmethod
    def writeCSV(self):
        pass

    @abstractmethod
    def writeXML(self):
        pass


class TemplateClass(Template):
    # All variables for program
    file_path = ""
    extension = ""
    date = []
    time = []
    speed = []
    distance = []
    description = []

    convert_date = []
    convert_time = []
    convert_speed = []
    convert_distance = []

    def read(self):
        # Function to read file and add data to lists
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()
        extension = os.path.splitext(file_path)[1]

        with open(file_path) as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                self.date.append(row[0])
                self.time.append(row[1])
                self.speed.append(row[2])
                self.distance.append(row[3])
                self.description.append(row[4])
                print(row)

    def change(self):
        # Function to change data in every list for format that we need
        for i in range(len(self.date)):
            year = self.date[i].split('/')[0]
            day = self.date[i].split('/')[1]
            month = self.date[i].split('/')[2]
            self.convert_date.append(day + '.' + month + '.' + year)

        for i in range(len(self.time)):
            part = self.time[i].split(' ')[1]
            hour = self.time[i].split(' ')[0].split(':')[0]
            minute = self.time[i].split(' ')[0].split(':')[1]
            second = self.time[i].split(' ')[0].split(':')[2]

            if part.lower() == "am":
                self.convert_time.append(hour + ':' + minute + ':' + second)
            else:
                hour = int(hour) + 12
                self.convert_time.append(str(hour) + ':' + minute + ':' + second)

        for i in range(len(self.speed)):
            self.convert_speed.append(int(self.speed[i]) * 1.94384449)

        for i in range(len(self.distance)):
            self.convert_distance.append(int(self.distance[i]) * 0.539956803)

    def writeCSV(self):
        # Write changed data to csv
        with open('result.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for i in range(len(self.date)):
                writer.writerow(
                    [self.convert_date[i], self.convert_time[i], self.convert_speed[i], self.convert_distance[i],
                     self.description[i]])

    def writeXML(self):
        # Write changed data to XML
        points = ET.Element("points")
        points = ET.SubElement(points, "points")

        for i in range(len(self.date)):
            point = ET.SubElement(points, "point")
            usr = ET.SubElement(point, "date")
            usr.text = str(self.convert_date[i])
            usr = ET.SubElement(point, "time")
            usr.text = str(self.convert_time[i])
            usr = ET.SubElement(point, "speed")
            usr.text = str(self.convert_speed[i])
            usr = ET.SubElement(point, "distance")
            usr.text = str(self.convert_distance[i])
            usr = ET.SubElement(point, "description")
            usr.text = str(self.description[i])
        tree = ET.ElementTree(points)
        tree.write("result.xml", encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    program = TemplateClass()
    program.read()
    program.change()
    program.writeCSV()
    program.writeXML()
