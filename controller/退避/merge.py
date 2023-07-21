import os
import re

from PyPDF4 import PdfFileMerger
from PyQt6 import QtCore as qtc

class PDFMerge:

  def __init__(self, input_directory : str, output_directory : str) -> None:
    self.input_directory : str = input_directory
    self.output_directory : str = output_directory
    self.log : str = ""
    self.pdfFileName : str = ""
    # 入力ディレクトリ内のPDFファイルを取得
    #self.pdf_files : list = [f for f in os.listdir(self.input_directory) if f.endswith('.pdf')]
    self.pdf_files = [file for file in os.listdir(self.input_directory) if file.endswith('.pdf')]
    self.pattern : str = "^(a)?[0-9]{1,4}\-[0-9]{1,4}\-([^\x01-\x7E]|[A-Z]|[a-z]|[ ])+\-(2020)\-(雇入|基本|深夜|(健保指定)?ドッ(ク|グ)|不明)"
 
  def process_pdf(self, textbox):
    pdf_merger = PdfFileMerger()
    
    # 入力ディレクトリ内のPDFファイルを取得
    pdf_files = [f for f in os.listdir(self.input_directory) if f.endswith('.pdf')]
    # PDFファイルを結合
    for pdf_file in pdf_files:
      file_path = os.path.join(self.input_directory, pdf_file)
      pattern = re.match(self.pattern, pdf_file)

      if(pdf_file != pattern[0]):
        self.pdfFileName = os.path.join(self.output_directory, os.path.splitext(pattern[0])[0])
      
      self.log : str = f"readed: {pdf_file}"
      qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))

      with open(file_path, 'rb') as file:
        pdf_merger.append(file)

    # 出力ファイルに結合したPDFを保存
    with open(self.pdfFileName + ".pdf", 'wb') as output:
      pdf_merger.write(output)
      qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.pdfFileName + ".pdfを作成しました"))
