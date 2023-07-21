from controller.rotate import RoatePdfs
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from threading import Thread
from typing import Final
from typing import overload

class ViewRotate(qtw.QWidget):
  
  def __init__(self):
    super().__init__()
    # 説明文
    self.info_label : qtw.QLabel = qtw.QLabel("PDFデータを回転する", self)

    self.radio_button1 : qtw.QRadioButton = qtw.QRadioButton("左に90°回転", self)
    self.radio_button1.setChecked(True)
    #self.radio_button1.setGeometry(50, 50, 100, 30)
    self.radio_button2 : qtw.QRadioButton = qtw.QRadioButton("右に90°回転", self)
    self.radio_button3 : qtw.QRadioButton = qtw.QRadioButton("180°回転", self)
    #self.radio_button2.setGeometry(50, 100, 100, 30)

    self.pageinfo : qtw.QLabel = qtw.QLabel("回転させるページを選択:1,4-6など", self)
    self.pageedit  : qtw.QLineEdit = qtw.QLineEdit(self, placeholderText="入力してください。")
    
    #self.setGeometry(200, 200, 300, 200)

    # input
    self.input_label : qtw.QLabel = qtw.QLabel("input dir", self)
    self.input_edit  : qtw.QLineEdit = qtw.QLineEdit(self, placeholderText="入力してください。")
    self.input_button : qtw.QPushButton = qtw.QPushButton("ファイルを選択", self)

    # output
    self.output_label : qtw.QLabel = qtw.QLabel("output dir", self)
    self.output_edit : qtw.QLineEdit = qtw.QLineEdit(self, placeholderText="入力してください。")
    self.output_button : qtw.QPushButton = qtw.QPushButton("ファイルを選択", self)

    # checkbox = qtw.QCheckBox("チェック", self)
    self.submit : qtw.QPushButton = qtw.QPushButton("出 力", self)
    self.textbox : qtw.QTextEdit = qtw.QTextEdit(self)

  # 説明文
  def getExplanation(self) -> qtw.QLabel:
    return self.info_label
  
  # ラジオボタンと回転対象のページ
  def getRadio_widgets(self) -> list:
    input_widgets : Final[tuple(list)] = (self.radio_button1, self.radio_button2, self.radio_button3, self.pageinfo, self.pageedit)
    return input_widgets
  
  # 入力
  def getInput_widgets(self) -> list:
    input_widgets : Final[tuple(list)] = (self.input_label, self.input_edit, self.input_button)
    return input_widgets
  
  # 出力
  def output_widgets(self) -> list:
    output_widgets : Final[tuple(list)] = (self.output_label, self.output_edit, self.output_button)
    return output_widgets
  
  # 出力ボタンとログ出力用テキストボックス
  def submit_widgets(self) -> list:
    submit_widgets : Final[tuple(list)] = (self.submit, self.textbox)
    return submit_widgets
  
  # inputボタン
  def select_input_directory(self) -> None:
    directory : tuple[str, str] = qtw.QFileDialog.getOpenFileName(self, caption="Select Input Directory")
    self.input_edit.setText(directory[0])

  # outputボタン
  def select_output_directory(self) -> None:
    directory : str = qtw.QFileDialog.getExistingDirectory(self, caption="Select Output Directory")
    self.output_edit.setText(directory)
  
  # execute
  def start_pdf_rotating(self) -> None:
    input_directory : str = self.input_edit.text()
    output_directory : str = self.output_edit.text()
    # 入力ディレクトリ内のPDFファイルを取得
    pageedit : str = self.pageedit.text()

    if not input_directory or not output_directory:
      qtw.QMessageBox.warning(self, "Warning", "ファイルを選択してください.")
      return
    
    if pageedit == "":
      qtw.QMessageBox.warning(self, "Warning", "回転させるページを選択してください.")
      return
    
    if self.radio_button1.isChecked():
      mergePdfs : RoatePdfs = RoatePdfs(input_directory, output_directory, -90, pageedit)
      thread : Thread = Thread(target=mergePdfs.rotate_pdfs, args=(self.textbox,))
      thread.start()
    
    elif self.radio_button2.isChecked():
      mergePdfs : RoatePdfs = RoatePdfs(input_directory, output_directory, 90, pageedit)
      thread : Thread = Thread(target=mergePdfs.rotate_pdfs, args=(self.textbox,))
      thread.start()

    elif self.radio_button3.isChecked():
      mergePdfs : RoatePdfs = RoatePdfs(input_directory, output_directory, 180, pageedit)
      thread : Thread = Thread(target=mergePdfs.rotate_pdfs, args=(self.textbox,))
      thread.start()