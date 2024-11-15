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

def get_element_geometry(element):
    options = DB.Options()
    geometry_element = element.get_Geometry(options)
    return geometry_element

def transform_point(point, transform):
    transformed_point = transform.OfPoint(point)
    return transformed_point

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
        grid_info.append({
            'name': grid.Name,
            'start': (start_point.X, start_point.Y, start_point.Z),
            'end': (end_point.X, end_point.Y, end_point.Z)
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


with revit.Transaction('Export Selected View Geometry'):
    for element in columns:
        geometry = get_element_geometry(element)
        if geometry:
            for geom in geometry:
                if isinstance(geom, DB.Solid):
                    for face in geom.Faces:
                        for edge_loop in face.EdgeLoops:
                            for edge in edge_loop:
                                tessellated_shape = edge.Tessellate()
                                for point in tessellated_shape:
                                    transformed_point = transform_point(point, selected_view.CropBox.Transform)
                                    level_name, level_elevation = get_level_info(element)
                                    columns_data.append((
                                        element.Id.IntegerValue,
                                        element.Name,
                                        transformed_point.X,
                                        transformed_point.Y,
                                        transformed_point.Z,
                                        level_name,
                                        level_elevation
                                    ))
    
    for element in beams:
        geometry = get_element_geometry(element)
        if geometry:
            for geom in geometry:
                if isinstance(geom, DB.Solid):
                    for face in geom.Faces:
                        for edge_loop in face.EdgeLoops:
                            for edge in edge_loop:
                                tessellated_shape = edge.Tessellate()
                                for point in tessellated_shape:
                                    transformed_point = transform_point(point, selected_view.CropBox.Transform)
                                    level_name, level_elevation = get_level_info(element)
                                    beams_data.append((
                                        element.Id.IntegerValue,
                                        element.Name,
                                        transformed_point.X,
                                        transformed_point.Y,
                                        transformed_point.Z,
                                        level_name,
                                        level_elevation
                                    ))


columns_csv_file_path = "C:/yolov8/bim/columns_geometry.csv"
beams_csv_file_path = "C:/yolov8/bim/beams_geometry.csv"
grid_csv_file_path = "C:/yolov8/bim/grid_coordinates.csv"


with codecs.open(columns_csv_file_path, mode='w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Element ID", "Name", "X", "Y", "Z", "Level Name", "Level Elevation"])
    for vertex in columns_data:
        writer.writerow(vertex)

with codecs.open(beams_csv_file_path, mode='w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Element ID", "Name", "X", "Y", "Z", "Level Name", "Level Elevation"])
    for vertex in beams_data:
        writer.writerow(vertex)

with codecs.open(grid_csv_file_path, mode='w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Grid Name', 'Start X', 'Start Y', 'Start Z', 'End X', 'End Y', 'End Z'])
    for info in grid_data:
        writer.writerow([
            info['name'],
            info['start'][0], info['start'][1], info['start'][2],
            info['end'][0], info['end'][1], info['end'][2]
        ])

print("Columns, beams, and grid data have been written to", columns_csv_file_path, beams_csv_file_path, "and", grid_csv_file_path)




