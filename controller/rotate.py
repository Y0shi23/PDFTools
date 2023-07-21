import os
import re

from PyPDF4 import PdfFileReader, PdfFileWriter
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw

class RoatePdfs:
    
  def __init__(self, input_directory : str, output_directory :str, rotateAngle, page_ranges : str):
    # input dir
    self.input_directory: str = input_directory
    # output dir
    self.output_directory: str = output_directory
    # 回転させる方角[-90:左に90°, 90:右に90°]
    self.rotateAngle : int = rotateAngle
    self.page_ranges = page_ranges
    self.log : str = ""
    self.new_file_name = os.path.basename(self.input_directory)
    print(self.new_file_name)

  def __parse_page_range(self, page_range : str):
    page_range = page_range.strip()
    if '-' not in page_range:
        return [int(page_range)]

    start, end = map(int, page_range.split('-'))
    return list(range(start, end + 1))

  def __parse_pages_to_rotate(self, page_ranges):
    pages_to_rotate = []
    for page_range in page_ranges.split(','):
        pages_to_rotate.extend(self.__parse_page_range(page_range))
    return pages_to_rotate

  def __rotate_pages(self, rotation_angle : int, pages_to_rotate : list, textbox : qtw.QTextEdit):
    with open(self.input_directory, 'rb') as file:
      print(file)
      pdf_reader = PdfFileReader(file)
      pdf_writer = PdfFileWriter()

      for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        if page_num + 1 in pages_to_rotate:
          page.rotateClockwise(rotation_angle)

        pdf_writer.addPage(page)

      with open(self.output_directory + "/" + self.new_file_name, 'wb') as output_file:
          pdf_writer.write(output_file)
          self.log : str = f"created:" +  self.output_directory + "/" + self.new_file_name
          qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))

  def rotate_pdfs(self, textbox):
    self.log : str = f"reading:" + self.input_directory
    qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))
    pages_to_rotate = self.__parse_pages_to_rotate(self.page_ranges)
    self.__rotate_pages(self.rotateAngle, pages_to_rotate, textbox)