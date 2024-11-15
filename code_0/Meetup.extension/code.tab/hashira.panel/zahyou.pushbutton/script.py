# -*- coding: utf-8 -*-

import os
from pyrevit import forms, script, revit, DB
import codecs
import csv
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Grid, ViewPlan
from Autodesk.Revit.UI import TaskDialog

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

def select_view(doc):
    views = DB.FilteredElementCollector(doc).OfClass(DB.View).ToElements()
    view_options = [view for view in views if not view.IsTemplate]

    options = [(view.Name, view.Id) for view in view_options]
    options_str = "\n".join(["{}. {}".format(i+1, name) for i, (name, _) in enumerate(options)])

    forms.alert("Select a view to export:\n\n" + options_str)
    selected_index = int(input("Enter the number of the view to export: ")) - 1

    if 0 <= selected_index < len(options):
        return doc.GetElement(options[selected_index][1])
    return None

def get_level_info(element):
    try:
        level_id = element.LevelId
        level = doc.GetElement(level_id)
        if level:
            return level.Name, level.Elevation
    except:
        pass
    
    return "N/A", "N/A"

def get_grid_coordinates(doc, view_id):
    grid_collector = FilteredElementCollector(doc, view_id).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType()
    grid_info = []
    for grid in grid_collector:
        grid_curve = grid.Curve
        start_point = grid_curve.GetEndPoint(0)
        end_point = grid_curve.GetEndPoint(1)
        # 中点を計算
        midpoint = DB.XYZ(
            (start_point.X + end_point.X) / 2.0,
            (start_point.Y + end_point.Y) / 2.0,
            (start_point.Z + end_point.Z) / 2.0
        )
        grid_info.append({
            'name': grid.Name,
            'start': (start_point.X, start_point.Y, start_point.Z),
            'end': (end_point.X, end_point.Y, end_point.Z),
            'midpoint': (midpoint.X, midpoint.Y, midpoint.Z)
        })
    return grid_info

selected_view = forms.select_views(title="Select a view", multiple=False, filterfunc=lambda x: isinstance(x, ViewPlan))

if not selected_view:
    TaskDialog.Show("Error", "No view was selected.")
    script.exit()

view_id = selected_view.Id

columns = FilteredElementCollector(doc, view_id).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
beams = FilteredElementCollector(doc, view_id).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()

columns_data = []
beams_data = []
grid_data = get_grid_coordinates(doc, view_id)

with revit.Transaction('Export Midpoints'):
    for element in columns:
        location = element.Location
        if isinstance(location, DB.LocationCurve):
            curve = location.Curve
            start_point = curve.GetEndPoint(0)
            end_point = curve.GetEndPoint(1)
            # 中点を計算
            midpoint = DB.XYZ(
                (start_point.X + end_point.X) / 2.0,
                (start_point.Y + end_point.Y) / 2.0,
                (start_point.Z + end_point.Z) / 2.0
            )
            level_name, level_elevation = get_level_info(element)
            columns_data.append((
                element.Id.IntegerValue,
                element.Name,
                midpoint.X,
                midpoint.Y,
                midpoint.Z,
                level_name,
                level_elevation
            ))

    for element in beams:
        location = element.Location
        if isinstance(location, DB.LocationCurve):
            curve = location.Curve
            start_point = curve.GetEndPoint(0)
            end_point = curve.GetEndPoint(1)
            # 中点を計算
            midpoint = DB.XYZ(
                (start_point.X + end_point.X) / 2.0,
                (start_point.Y + end_point.Y) / 2.0,
                (start_point.Z + end_point.Z) / 2.0
            )
            level_name, level_elevation = get_level_info(element)
            beams_data.append((
                element.Id.IntegerValue,
                element.Name,
                midpoint.X,
                midpoint.Y,
                midpoint.Z,
                level_name,
                level_elevation
            ))

columns_csv_file_path = "C:/yolov8/bim/columns_midpoints.csv"
beams_csv_file_path = "C:/yolov8/bim/beams_midpoints.csv"
grid_csv_file_path = "C:/yolov8/bim/grid_midpoints.csv"

with codecs.open(columns_csv_file_path, mode='w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Element ID", "Name", "Midpoint X", "Midpoint Y", "Midpoint Z", "Level Name", "Level Elevation"])
    for data in columns_data:
        writer.writerow(data)

with codecs.open(beams_csv_file_path, mode='w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Element ID", "Name", "Midpoint X", "Midpoint Y", "Midpoint Z", "Level Name", "Level Elevation"])
    for data in beams_data:
        writer.writerow(data)

with codecs.open(grid_csv_file_path, mode='w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Grid Name', 'Start X', 'Start Y', 'Start Z', 'End X', 'End Y', 'End Z', 'Midpoint X', 'Midpoint Y', 'Midpoint Z'])
    for info in grid_data:
        writer.writerow([
            info['name'],
            info['start'][0], info['start'][1], info['start'][2],
            info['end'][0], info['end'][1], info['end'][2],
            info['midpoint'][0], info['midpoint'][1], info['midpoint'][2]
        ])

print("Columns, beams, and grid midpoints have been written to", columns_csv_file_path, beams_csv_file_path, "and", grid_csv_file_path)


"""# -*- coding: utf-8 -*-

import os
from pyrevit import forms, script
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, FamilyInstance, BuiltInParameter, View, Element
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

def select_view(doc):
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    view_options = [view for view in views if not view.IsTemplate]

    options = [(view.Name, view.Id) for view in view_options]
    options_str = "\n".join(["{}. {}".format(i+1, name) for i, (name, _) in enumerate(options)])

    dialog = TaskDialog("Select View")
    dialog.MainInstruction = "Select a view to export"
    dialog.MainContent = options_str
    dialog.CommonButtons = TaskDialogCommonButtons.Close
    dialog.DefaultButton = TaskDialogResult.Close
    dialog_result = dialog.Show()

    if dialog_result == TaskDialogResult.Close:
        selected_index = int(input("Enter the number of the view to export: ")) - 1
        if 0 <= selected_index < len(options):
            return doc.GetElement(options[selected_index][1])
    return None

# 選択したビューを取得
selected_view = select_view(doc)

# ビューが選択されていない場合、スクリプトを終了
if not selected_view:
    forms.alert("ビューが選択されていません", exitscript=True)

# 選択されたビュー内のすべての要素を取得
elements = FilteredElementCollector(doc, selected_view.Id).WhereElementIsNotElementType().ToElements()

# ビュー内に要素がない場合、警告を表示してスクリプトを終了
if not elements:
    forms.alert("選択されたビュー内に要素がありません", exitscript=True)

# CSVファイルのパスを指定 (ユーザーのデスクトップに保存)
#desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
#csv_file_path = os.path.join(desktop_path, "ElementCoordinates.csv")
csv_file_path = ("C:/yolov8/bim/main_zahyou.csv")

# CSVデータの作成
csv_rows = [["Element ID", "Name", "X", "Y", "Z"]]

for element in elements:
    element_id = element.Id.IntegerValue
    name = element.Name
    location = element.Location
    
    if hasattr(location, 'Point'):
        point = location.Point
        csv_rows.append([element_id, name, (point.X * 13.97 +330) / 2000, (1533 - point.Y * 13.97 - 360) / 1533, point.Z])
        print("Element ID: {}, Name: {}, Coordinates: X: {}, Y: {}, Z: {}".format(element_id, name, point.X, point.Y, point.Z))
    elif hasattr(location, 'Curve'):
        curve = location.Curve
        start_point = curve.GetEndPoint(0)
        end_point = curve.GetEndPoint(1)
        csv_rows.append([element_id, name, (start_point.X * 13.97 +330) / 2000, (1533 - start_point.Y * 13.97 - 360) / 1533, start_point.Z])
        print("Element ID: {}, Name: {}, Start Coordinates: X: {}, Y: {}, Z: {}".format(element_id, name, start_point.X, start_point.Y, start_point.Z))
        csv_rows.append([element_id, floa, name, (end_point.X * 13.97 +330) / 2000, (1533 - end_point.Y * 13.97 - 360) / 1533, end_point.Z])
        print("Element ID: {}, Name: {}, End Coordinates: X: {}, Y: {}, Z: {}".format(element_id, name, end_point.X, end_point.Y, end_point.Z))
    else:
        print("Element ID: {} has no point or curve location.".format(element_id))
        continue  # この行を追加して、メッセージが出力された要素を飛ばします

# CSVファイルに書き込む
script.dump_csv(csv_rows, csv_file_path)

# 完了メッセージを表示
print("終わり")
"""