# -*- coding: utf-8 -*-
"""
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, FamilyInstance
from Autodesk.Revit.UI import TaskDialog

# Get the current document
doc = __revit__.ActiveUIDocument.Document

# Collect all structural columns in the project
columns = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()

# Prepare a list to store column coordinates
column_coordinates = []

# Iterate over each column and get its location point
for column in columns:
    location = column.Location
    if isinstance(location, Autodesk.Revit.DB.LocationPoint):
        point = location.Point
        column_coordinates.append((point.X, point.Y, point.Z))

# Display the coordinates
message = "\n".join([f"Column at X: {coord[0]}, Y: {coord[1]}, Z: {coord[2]}" for coord in column_coordinates])
TaskDialog.Show("Column Coordinates", message)
"""


# Revitの現在のドキュメントを取得
doc = __revit__.ActiveUIDocument.Document
print(len(doc))



