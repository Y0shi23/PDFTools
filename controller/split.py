import os
#import typing

from pdfrw import PdfReader, PdfWriter
from threading import Thread
from PyQt6 import QtCore as qtc

class PdfSplitter2:

  def __init__(self, input_directory, output_directory):
    self.input_directory : str = input_directory
    self.output_directory : str = output_directory
    self.log : str = ""

  def __split_pdf(self, input_pdf_path, output_directory, textbox):
    input_pdf : PdfReader = PdfReader(input_pdf_path)

    for page_number, page in enumerate(input_pdf.pages):
      pdf_writer : PdfWriter = PdfWriter()
      pdf_writer.addpage(page)

      output_filename = os.path.join(output_directory, f"split_page_{page_number + 1}.pdf")
      pdf_writer.write(output_filename)
      self.log : str = f"Created: {output_filename}"
      qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))

  def process_pdf(self, pdf_filename, textbox):
    input_pdf_path = os.path.join(self.input_directory, pdf_filename)
    current_output_directory = os.path.join(self.output_directory, os.path.splitext(pdf_filename)[0])
    os.makedirs(current_output_directory, exist_ok=True)
    self.__split_pdf(input_pdf_path, current_output_directory, textbox)

  def process_pdfs(self, textbox):
    pdf_files : list = [f for f in os.listdir(self.input_directory) if f.endswith('.pdf')]
    threads = []

    for pdf_filename in pdf_files:
      t : Thread = Thread(target=self.process_pdf, args=(pdf_filename, textbox))
      t.start()
      threads.append(t)

    for t in threads:
      t.join()
    
    self.log += "\n------------------------------------------\n"
    self.log += str(len(pdf_files)) + "個の処理が完了しました\n"
    self.log += "------------------------------------------\n"
    
    qtc.QMetaObject.invokeMethod(textbox, "append", qtc.Q_ARG(str, self.log))