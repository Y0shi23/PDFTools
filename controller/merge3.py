import os
import re
from PyPDF4 import PdfFileMerger
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw
from typing import Final

class MergePDFs:
  
  def __init__(self, input_directory: str, output_directory: str) -> None:
    # input dir
    self.input_directory: str = input_directory
    # output dir
    self.output_directory: str = output_directory
    # ディレクトリ配下にあるPDFファイルを全て取得する
    self.one_file_only: Final[str] = [os.path.join(self.input_directory, f) for f in os.listdir(self.input_directory) if f.endswith('.pdf')]
    # ログ出力用
    self.log = ""
    # 正規表現パターン
    self.pattern: str = "(a)?[0-9]{1,4}\-[0-9]{1,4}\-([^\x01-\x7E]|[A-Z]|[a-z]|[ ])+\-(2020)\-(雇入|基本|深夜|(健保指定)?ドッ(ク|グ)|不明)"

  def __merge_pdfs(self, input_dir: str, new_pdf_name: str, textbox: qtw.QTextEdit) -> None:
    pdf_merger: PdfFileMerger = PdfFileMerger()

    # 入力ディレクトリ内のPDFファイルを取得
    pdf_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.pdf')]
    # PDFファイルを結合
    try:
      for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as file:
          pdf_merger.append(file)
          pdf_file_name = os.path.basename(pdf_file)
          self.log = f"readed: {pdf_file_name}"
          qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))

      # 出力ファイルに結合したPDFを保存
      output_path: str = os.path.join(self.output_directory, new_pdf_name + ".pdf")

      with open(output_path, 'wb') as output:
        pdf_merger.write(output)
        self.log = f"merged: {output.name}" + "\n"
        qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))

      pdf_merger.close()

    except NotADirectoryError as e:
      self.log = str(e)
      print(e)
      qtc.QMetaObject.invokeMethod(textbox, "error", qtc.Q_ARG(str, self.log))

  def merge_all_pdfs(self, textbox: qtw.QTextEdit) -> None:
      
    if not os.path.exists(self.input_directory):
      return

    # ディレクトリでまとめて読み込む
    if os.path.isdir(self.input_directory):
      input_dirs = [os.path.join(self.input_directory, f) for f in os.listdir(self.input_directory) if os.path.isdir(os.path.join(self.input_directory, f))]
      for input_dir in input_dirs:
        self.__merge_pdfs(input_dir, os.path.basename(input_dir), textbox)
    
    # ディレクトリ配下にあるPDFファイルの存在確認
    if os.path.isfile(self.one_file_only[0]):
      input_file = os.path.abspath(self.input_directory)
      self.__merge_pdfs(input_file, os.path.splitext(os.path.basename(input_file))[0], textbox)

    else:
      self.log = "Invalid input directory or file"
      qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))