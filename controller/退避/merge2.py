import os
import re

from PyPDF4 import PdfFileMerger
from PyQt6 import QtCore as qtc
from PyQt6 import QtWidgets as qtw
from typing import Tuple, Final

class MergePDFs:
  
  def __init__(self, input_directory : str, output_directory : str) -> None:
    self.input_directory : str = input_directory
    self.output_directory : str = output_directory
    self.pdfs : Final[Tuple] = list(os.listdir(self.input_directory))
    self.one_file_only = [os.path.join(self.input_directory, f) for f in os.listdir(self.input_directory) if f.endswith('.pdf')]
    
    # ログ出力用
    self.log = ""
    # 正規表現パターン
    self.pattern : str = "(a)?[0-9]{1,4}\-[0-9]{1,4}\-([^\x01-\x7E]|[A-Z]|[a-z]|[ ])+\-(2020)\-(雇入|基本|深夜|(健保指定)?ドッ(ク|グ)|不明)"

  def __merge_pdfs(self, input_dir: str, new_pdf_name: str, textbox : qtw.QTextEdit) -> None:
    pdf_merger : PdfFileMerger = PdfFileMerger()

    # 入力ディレクトリ内のPDFファイルを取得
    pdf_files: Final[Tuple] = list([os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.pdf')])
    
    # PDFファイルを結合
    for pdf_file in pdf_files:
      with open(pdf_file, 'rb') as file:
        pdf_merger.append(file)
        pdf_file_name = os.path.basename(pdf_file)
        self.log : str = f"readed: {pdf_file_name}"
        qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))
                   
    # 出力ファイルに結合したPDFを保存
    output_path : str = os.path.join(self.output_directory, new_pdf_name + ".pdf")

    with open(output_path, 'wb') as output:
      pdf_merger.write(output)
      self.log : str = f"merged: {output.name}" + "\n"
      qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))

    pdf_merger.close()

  def merge_all_pdfs(self, textbox : qtw.QTextEdit) -> None:
    for file_name in self.pdfs:
      # match : re.Match = re.match(self.pattern, file_name)
      pdf_dir : str = os.path.join(self.input_directory, file_name)
      # print(pdf_dir)
      self.__merge_pdfs(pdf_dir, file_name, textbox)
    
