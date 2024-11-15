# -*- coding: utf-8 -*-

# 必要なモジュールをインポート
import os
from pyrevit import revit, DB, forms
from Autodesk.Revit.DB import Transaction, Line, XYZ, ImageExportOptions, ExportRange, ImageFileType, ImageResolution
from System.Collections.Generic import List

# ドキュメントとアクティブなビューを取得
uidoc = revit.uidoc
doc = revit.doc
view = doc.ActiveView

if not view:
    forms.alert("アクティブなビューが選択されていません。", exitscript=True)

# 四角形の座標を定義
pt1 = XYZ(-50, -50, 0)
pt2 = XYZ(250, -50, 0)
pt3 = XYZ(250, 250, 0)
pt4 = XYZ(-50, 250, 0)

# トランザクションの開始
t = Transaction(doc, "Draw Rectangle and Export View")
t.Start()

# ポイント間の線を作成
line1 = Line.CreateBound(pt1, pt2)
line2 = Line.CreateBound(pt2, pt3)
line3 = Line.CreateBound(pt3, pt4)
line4 = Line.CreateBound(pt4, pt1)

# アクティブなビューに詳細線を作成
doc.Create.NewDetailCurve(view, line1)
doc.Create.NewDetailCurve(view, line2)
doc.Create.NewDetailCurve(view, line3)
doc.Create.NewDetailCurve(view, line4)

# クロップボックスを四角形に合わせて設定
new_cropbox = DB.BoundingBoxXYZ()
new_cropbox.Min = XYZ(-50, -50, 0)
new_cropbox.Max = XYZ(250, 250, 0)
view.CropBox = new_cropbox
view.CropBoxActive = True
view.CropBoxVisible = False

# 必要に応じて、グリッド、文字、寸法、タグを非表示に設定
element_classes = [DB.Grid, DB.TextNote, DB.Dimension, DB.IndependentTag]

element_ids = List[DB.ElementId]()
for element_class in element_classes:
    elements = DB.FilteredElementCollector(doc, view.Id).OfClass(element_class).ToElements()
    for elem in elements:
        element_ids.Add(elem.Id)

# 要素を非表示に設定
# view.HideElements(element_ids)

# トランザクションのコミット
t.Commit()

# ビューをエクスポートする関数
def export_view_to_bmp(view, output_path):
    bmp_options = ImageExportOptions()
    bmp_options.ExportRange = ExportRange.SetOfViews
    bmp_options.HLRandWFViewsFileType = ImageFileType.BMP
    bmp_options.FilePath = output_path
    bmp_options.ViewName = view.Name

    # DPI を設定（必要に応じて調整）
    dpi = 1

    # ビューのバウンディングボックスを取得
    bounding_box = view.CropBox

    # フィートをインチに変換（1 フィート = 12 インチ）
    width_in_inches = abs(bounding_box.Max.X - bounding_box.Min.X) * 12
    height_in_inches = abs(bounding_box.Max.Y - bounding_box.Min.Y) * 12

    # ピクセルサイズを計算
    width_pixels = int(width_in_inches * dpi)
    height_pixels = int(height_in_inches * dpi)

    # ピクセルサイズが許容範囲内にあるか確認
    max_pixel_size = 10000  # 必要に応じて調整
    pixel_size = min(max(width_pixels, height_pixels), max_pixel_size)
    pixel_size = max(pixel_size, 256)  # 最小ピクセルサイズ

    bmp_options.PixelSize = pixel_size

    # ImageResolution を設定
    bmp_options.ImageResolution = ImageResolution.DPI_72

    # ビューのセットを作成
    view_set = List[DB.ElementId]()
    view_set.Add(view.Id)
    bmp_options.SetViewsAndSheets(view_set)

    # 画像をエクスポート
    doc.ExportImage(bmp_options)

# 保存先のディレクトリを指定
output_dir = "C:/yolov8/bim"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存先のファイルパスを指定
output_path = os.path.join(output_dir, "main.bmp")

# ビューをエクスポート
export_view_to_bmp(view, output_path)

forms.alert("ビューが BMP ファイルとしてエクスポートされました。\n保存先: {}".format(output_path))




"""# -*- coding: utf-8 -*-

import os
from pyrevit import forms, revit, DB
from System.Collections.Generic import List
#通常実行すると画像出力及び範囲指定できる
uidoc = revit.uidoc
doc = revit.doc

def set_cropbox_for_view(view):
    #ビューの CropBox を原点から x が 0 から 90、y が 0 から 90 の範囲に設定する関数
    # 新しい CropBox を作成
    new_cropbox = DB.BoundingBoxXYZ()
    new_cropbox.Min = DB.XYZ(-50, -50, 0)    # 最小座標（X, Y, Z）
    new_cropbox.Max = DB.XYZ(80, 80, 0)  # 最大座標（X, Y, Z）

    # CropBox を設定
    view.CropBox = new_cropbox
    view.CropBoxActive = True   # CropBox をアクティブにする
    view.CropBoxVisible = False  # CropBox の表示をオフ

def hide_elements_in_view(view):
    #ビュー内のグリッド、文字、寸法、タグを非表示にする関数
    # 非表示にする要素のクラスリスト
    element_classes = [DB.Grid, DB.TextNote, DB.Dimension, DB.IndependentTag]

    element_ids = List[DB.ElementId]()
    for element_class in element_classes:
        elements = DB.FilteredElementCollector(doc, view.Id).OfClass(element_class).ToElements()
        for elem in elements:
            element_ids.Add(elem.Id)
    # 要素を非表示に設定
    view.HideElements(element_ids)

def export_view_to_bmp(view, output_path):
    bmp_options = DB.ImageExportOptions()
    bmp_options.ExportRange = DB.ExportRange.SetOfViews
    bmp_options.HLRandWFViewsFileType = DB.ImageFileType.BMP
    bmp_options.FilePath = output_path
    bmp_options.ViewName = view.Name

    # DPI を 1 に設定（1 インチ＝1 ピクセル）
    dpi = 1

    # ビューのバウンディングボックスを取得
    # チェックprint文で行う
    bounding_box = view.CropBox
    print("a")


    # フィートをインチに変換（1 フィート = 12 インチ）
    width_in_inches = abs(bounding_box.Max.X - bounding_box.Min.X) * 12
    height_in_inches = abs(bounding_box.Max.Y - bounding_box.Min.Y) * 12

    # ピクセルサイズを計算（1 インチ = 1 ピクセル）
    width_pixels = int(width_in_inches * dpi)
    height_pixels = int(height_in_inches * dpi)

    # ピクセルサイズが 0 の場合は 1 に設定
    width_pixels = max(width_pixels, 1)
    height_pixels = max(height_pixels, 1)

    # PixelSize は画像の最大寸法（幅または高さ）をピクセル単位で指定
    bmp_options.PixelSize = max(width_pixels, height_pixels)

    # ImageResolution を設定（1 インチ 1 ピクセル）
    bmp_options.ImageResolution = DB.ImageResolution.DPI_72  # 最小の DPI を使用

    # ビューのセットを作成
    view_set = List[DB.ElementId]()
    view_set.Add(view.Id)
    bmp_options.SetViewsAndSheets(view_set)

    # 画像をエクスポート
    doc.ExportImage(bmp_options)

#start

# 現在のアクティブなビューを取得
selected_view = uidoc.ActiveView

if not selected_view:
    forms.alert("アクティブなビューが選択されていません。", exitscript=True)

# トランザクションを開始
with revit.Transaction('Set up View for Export'):
    # CropBox を設定
    set_cropbox_for_view(selected_view)

    # グリッド、文字、寸法、タグを非表示に設定
    #hide_elements_in_view(selected_view)

# 保存先のディレクトリを指定
output_dir = "C:/yolov8/bim"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存先のファイルパスを指定
output_path = os.path.join(output_dir, "main.bmp")

# ビューをエクスポート
with revit.Transaction('Export Active View to BMP'):
    export_view_to_bmp(selected_view, output_path)

forms.alert("ビューが BMP ファイルとしてエクスポートされました（グリッド、文字、寸法、タグは非表示）。\n保存先: {}".format(output_path))"""
