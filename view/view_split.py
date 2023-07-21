from controller.split import PdfSplitter2
from PyQt6 import QtWidgets as qtw
from threading import Thread
from typing import Final
from typing import overload


class ViewSplit(qtw.QWidget):
  
  def __init__(self)  -> None:
    super().__init__()
    
    # 説明文
    self.explanation : qtw.QLabel = qtw.QLabel("PDFを1つずつ分解", self)

    # input
    self.input_label : qtw.QLabel = qtw.QLabel("input dir", self)
    self.input_edit : qtw.QLineEdit = qtw.QLineEdit(self, placeholderText="入力してください。")
    self.input_button : qtw.QPushButton = qtw.QPushButton("ファイルを選択", self)

    # output
    self.output_label : qtw.QLabel = qtw.QLabel("output dir", self)
    self.output_edit : qtw.QLineEdit = qtw.QLineEdit(self, placeholderText="入力してください。")
    self.output_button : qtw.QPushButton = qtw.QPushButton("ファイルを選択", self)

    # submit button and output log
    self.submit : qtw.QPushButton = qtw.QPushButton("出 力", self)
    self.textbox : qtw.QTextEdit = qtw.QTextEdit(self)

  def getExplanation(self) -> qtw.QLabel:
    return self.explanation
  
  def getViewInfo(self) -> list:
    widgets : Final[tuple(list)] = [self.getInput_widgets, self.output_widgets]
    return widgets
  
  def getInput_widgets(self) -> list:
    input_widgets : Final[tuple(list)] = (self.input_label, self.input_edit, self.input_button)
    return input_widgets
  
  def output_widgets(self) -> list:
    output_widgets : Final[tuple(list)] = (self.output_label, self.output_edit, self.output_button)
    return output_widgets
  
  def submit_widgets(self) -> list:
    submit_widgets : Final[tuple(list)] = (self.submit, self.textbox)
    return submit_widgets
  
  # input
  def select_input_directory(self) -> None:
    directory : str = qtw.QFileDialog.getExistingDirectory(self, caption="Select Input Directory")
    self.input_edit.setText(directory)

  # output
  def select_output_directory(self) -> None:
    directory : str = qtw.QFileDialog.getExistingDirectory(self, caption="Select Output Directory")
    self.output_edit.setText(directory)
  
  # execute
  def start_pdf_splitting(self) -> None:
    input_directory : str = self.input_edit.text()
    output_directory : str = self.output_edit.text()

    if not input_directory or not output_directory:
      qtw.QMessageBox.warning(self, "Warning", "ファイルを選択してください.")
      return

    pdf_splitter : PdfSplitter2 = PdfSplitter2(input_directory, output_directory)
    thread : Thread = Thread(target=pdf_splitter.process_pdfs, args=(self.textbox,))
    thread.start()