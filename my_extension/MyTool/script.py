from pyrevit import forms
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

doc = __revit__.ActiveUIDocument.Document

# Collect all walls in the document
walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

# Show a message box with the number of walls
forms.alert("There are {} walls in the document.".format(len(walls)), exitscript=True)