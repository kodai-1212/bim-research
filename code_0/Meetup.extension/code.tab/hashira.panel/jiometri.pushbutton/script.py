# -*- coding: utf-8 -*-

import clr
import System
from System import Guid
from System.Collections.Generic import List
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.ApplicationServices import Application

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# ドキュメントの取得
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# 通り芯の非表示設定
def hide_grids(view):
    collector = FilteredElementCollector(doc, view.Id)
    grids = collector.OfClass(Grid).ToElements()
    grid_ids = List[ElementId]([grid.Id for grid in grids])
    view.HideElements(grid_ids)

# 画像のエクスポート
def export_view_to_image(view, filepath, format='BMP'):
    options = ImageExportOptions()
    options.ExportRange = ExportRange.CurrentView
    options.FilePath = filepath
    options.HLRandWFViewsFileType = ImageFileType.BMP if format.upper() == 'BMP' else ImageFileType.PNG
    options.ImageResolution = ImageResolution.DPI_150

    doc.ExportImage(options)

# メイン処理
def main():
    # 対象のビューを取得（ここではアクティブビューを使用）
    view = doc.ActiveView

    # 通り芯を非表示にする
    TransactionManager.Instance.EnsureInTransaction(doc)
    hide_grids(view)
    TransactionManager.Instance.TransactionTaskDone()

    # 画像をエクスポート
    filepath = 'C:/yolov8/bim/output_image.bmp'  # 保存先のパスを設定
    export_view_to_image(view, filepath, format='BMP')

# スクリプトの実行
main()
