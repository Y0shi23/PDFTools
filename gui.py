import sys

from PyQt6 import QtWidgets as qtw
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QApplication, QHBoxLayout
from view.view_split import ViewSplit
from view.view_merge import ViewMerge
from view.view_rotate import ViewRotate
from typing import Final

sys.dont_write_bytecode = True

class MainWindow(qtw.QWidget):
  
  def __init__(self) ->None:
    super().__init__()
    # 画面タイトルの設定
    self.setWindowTitle("PDF編集ツール")
    # 画面サイズの設定
    # self.setFixedSize(720, 400)
    self.resize(720, 400)

    # メインレイアウトの設定
    self.main_layout : qtw.QVBoxLayout = qtw.QVBoxLayout()
    self.setLayout(self.main_layout)

    # ===== Tabウィジェットの用意
    self.tab_widget : qtw.QTabWidget = qtw.QTabWidget(
      movable=True,
      tabPosition=qtw.QTabWidget.TabPosition.North,
      tabShape=qtw.QTabWidget.TabShape.Rounded,
    )
    # メインレイアウトに追加
    self.main_layout.addWidget(self.tab_widget)
    #各Viewのインスタンスを生成
    self.tabinfo : Final[tuple[list]] = {
      "split" : ViewSplit(), 
      "merge" : ViewMerge(), 
      "rotate" : ViewRotate()
    }
    # 説明文
    self.explanationText : Final[tuple[list]] = {
      "split" : self.tabinfo["split"].getExplanation(),
      "merge" : self.tabinfo["merge"].getExplanation(),
      "rotate" : self.tabinfo["rotate"].getExplanation()
    }
    # widget情報取得(split)
    self.splitWidgets_list : Final[list] = [
      self.tabinfo["split"].getInput_widgets(),
      self.tabinfo["split"].output_widgets(),
      self.tabinfo["split"].submit_widgets()
    ]
    # 各buttonのclick event 情報(分割タブ)
    self.buttonClickEventInfo : Final[tuple[list]]= {      
      "input" : self.tabinfo["split"].select_input_directory,
      "output" : self.tabinfo["split"].select_output_directory,
      "execute" : self.tabinfo["split"].start_pdf_splitting
    }
    # widget情報取得(merge)
    self.mergeWidgets_list : Final[list] = [
      self.tabinfo["merge"].getInput_widgets(), 
      self.tabinfo["merge"].output_widgets(), 
      self.tabinfo["merge"].submit_widgets()
    ]
    # 各buttonのclick event 情報(結合タブ)
    self.merge_button_click_event_info : Final[tuple[list]]= {      
      "input" : self.tabinfo["merge"].select_input_directory,
      "output" : self.tabinfo["merge"].select_output_directory,
      "execute" : self.tabinfo["merge"].start_pdf_merging
    }
    #widget情報取得(rotate)_ラジオボタン
    self.rotateWWidgets_radio_button : Final[list] = [
      self.tabinfo["rotate"].getRadio_widgets()
    ]
    # widget情報取得(rotate)
    self.rotateWidgets_list : Final[tuple[list]] = [
      self.tabinfo["rotate"].getInput_widgets(), 
      self.tabinfo["rotate"].output_widgets(), 
      self.tabinfo["rotate"].submit_widgets()
    ]
    # 各buttonのclick event 情報(回転タブ)
    self.rotate_button_click_event_info : Final[tuple[list]] = {      
      "input" : self.tabinfo["rotate"].select_input_directory,
      "output" : self.tabinfo["rotate"].select_output_directory,
      "execute" : self.tabinfo["rotate"].start_pdf_rotating
    }
    # レイアウトをセット
    self.__setTab(self.explanationText["split"], self.splitWidgets_list, self.buttonClickEventInfo, "分割")
    self.__setTab(self.explanationText["merge"], self.mergeWidgets_list, self.merge_button_click_event_info, "結合")
    self.__setTab(self.explanationText["rotate"], self.rotateWidgets_list, self.rotate_button_click_event_info, "回転")
  
  def __setTab(self, explanationText : tuple[list], widgets_list : list, button_click_event_info : tuple[list], tabName : str):
    # ===== Tab1 の用意
    tab : qtw.QWidget = qtw.QWidget(self)
    
    for i, event in enumerate(button_click_event_info):
      if event != "execute":
        widgets_list[i][2].clicked.connect(button_click_event_info[event])
      else:
        widgets_list[i][0].clicked.connect(button_click_event_info[event])

    # タブ内のレイアウトの作成
    tab_layout : qtw.QVBoxLayout = qtw.QVBoxLayout()
    tab_hlayouts : Final[tuple[qtw.QHBoxLayout, qtw.QHBoxLayout, qtw.QVBoxLayout]] = (
      qtw.QHBoxLayout(), qtw.QHBoxLayout(), qtw.QVBoxLayout()
    )

    # 説明文
    tab_layout.addWidget(explanationText)

    # 回転のときだけ新たにウィジェットを追加
    if tabName == "回転":
      radio_button : qtw.QHBoxLayout = qtw.QHBoxLayout()
      tab_layout.addLayout(radio_button)

      for i, radios in enumerate(self.rotateWWidgets_radio_button):
        for widget in radios:
          radio_button.addWidget(widget)

    # レイアウトの配置
    for tab_hlayout in tab_hlayouts:
      tab_layout.addLayout(tab_hlayout)
    
    # ウィジェットを配置
    tab.setLayout(tab_layout)
    for i, widgets in enumerate(widgets_list):
      for widget in widgets:
        tab_hlayouts[i].addWidget(widget)

    tab_layout.addStretch()

    # タブにウィジェットを追加
    self.tab_widget.addTab(tab, tabName)

if __name__ == "__main__":
    app : qtw.QApplication = qtw.QApplication([])
    main_window : MainWindow = MainWindow()
    main_window.show()
    app.exec()
