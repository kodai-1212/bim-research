# -*- coding: utf-8 -*-

# Import necessary modules from the Revit API and pyRevit
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Grid, ViewPlan
from Autodesk.Revit.UI import TaskDialog
from pyrevit import revit, DB, forms
import csv
import codecs

# Start a transaction to interact with the Revit document
doc = revit.doc
uidoc = revit.uidoc

# Prompt the user to select a view (plan)
selected_view = forms.select_views(title="Select a view", multiple=False, filterfunc=lambda x: isinstance(x, ViewPlan))

if selected_view:
    view_id = selected_view.Id

    # Collect all grid elements in the selected view
    grid_collector = FilteredElementCollector(doc, view_id).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType()

    # Initialize a list to store grid information
    grid_info = []

    # Iterate through each grid element and retrieve its coordinates
    for grid in grid_collector:
        grid_curve = grid.Curve
        start_point = grid_curve.GetEndPoint(0)
        end_point = grid_curve.GetEndPoint(1)
        grid_info.append({
            'name': grid.Name,
            'start': (start_point.X, start_point.Y, start_point.Z),
            'end': (end_point.X, end_point.Y, end_point.Z)
        })

    # Save the grid information to a CSV file
    csv_file_path = "C:/yolov8/bim/grid_coordinates.csv"

    with codecs.open(csv_file_path, mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Grid Name', 'Start X', 'Start Y', 'Start Z', 'End X', 'End Y', 'End Z'])
        for info in grid_info:
            writer.writerow([
                info['name'],
                info['start'][0], info['start'][1], info['start'][2],
                info['end'][0], info['end'][1], info['end'][2]
            ])

    # Build the output string using the format method
    output = "\n".join(["Grid {name}: Start - {start}, End - {end}".format(
        name=info['name'], 
        start=info['start'], 
        end=info['end']
    ) for info in grid_info])

    # Display the grid information in a TaskDialog
    TaskDialog.Show("Grid Coordinates", output)

    print("Grid data has been written to", csv_file_path)
else:
    TaskDialog.Show("Error", "No view was selected.")






       


"""# -*- coding: utf-8 -*-

import clr
import os
from pyrevit import forms
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ImageExportOptions, View, ElementId, XYZ, View3D, BuiltInParameter
from RevitServices.Persistence import DocumentManager
clr.AddReference('System.Drawing')
from System.Drawing import Bitmap, Graphics
from System import Drawing
from System.Collections.Generic import List

# Initialization
uidoc = __revit__.ActiveUIDocument  # Ensure `__revit__` is properly passed to the script environment when run in Revit
doc = uidoc.Document

# Function to find Site Boundaries
def find_site_boundaries(doc):
    boundaries = []
    # Assuming site boundary is a model line in OST_Lines category
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).WhereElementIsNotElementType()
    for element in collector:
        line_category = element.get_Parameter(BuiltInParameter.ELEM_CATEGORY_PARAM).AsValueString()
        if "Site" in line_category:  # Assuming any lines in 'Site' category
            boundaries.append(element)
    return boundaries

# Function to get the bounding box of boundaries
def get_bounding_box(boundaries):
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')
    for boundary in boundaries:
        bbox = boundary.get_BoundingBox(None)
        min_x = min(min_x, bbox.Min.X)
        min_y = min(min_y, bbox.Min.Y)
        min_z = min(min_z, bbox.Min.Z)
        max_x = max(max_x, bbox.Max.X)
        max_y = max(max_y, bbox.Max.Y)
        max_z = max(max_z, bbox.Max.Z)
    return (XYZ(min_x, min_y, min_z), XYZ(max_x, max_y, max_z))

# Function to export a view to BMP
def export_view_to_bmp(view, output_path):
    bmp_options = ImageExportOptions()
    bmp_options.ExportRange = ImageExportOptions.ExportRange.SetOfViews
    bmp_options.HLRandWFViewsFileType = ImageExportOptions.ImageFileType.BMP
    bmp_options.FilePath = output_path
    bmp_options.ViewName = view.Name

    # Set the pixel resolution
    bmp_options.PixelSize = 2000

    view_set = List[ElementId]()
    view_set.Add(view.Id)
    bmp_options.SetViewsAndSheets(view_set)

    doc.ExportImage(bmp_options)

# Function to adjust the origin in the BMP
def adjust_bmp_origin(bmp_path):
    with Bitmap(bmp_path) as bmp:
        width, height = bmp.Width, bmp.Height
        new_width, new_height = width + 20, height + 20

        with Bitmap(new_width, new_height) as new_bmp:
            g = Graphics.FromImage(new_bmp)
            g.Clear(Drawing.Color.White)
            g.DrawImage(bmp, 20, 20)
            
            # Save the new image with a temporary name to avoid access conflicts
            temp_path = bmp_path.replace(".bmp", "_temp.bmp")
            new_bmp.Save(temp_path)
            g.Dispose()

        # Replace the original file with the new one
        os.remove(bmp_path)
        os.rename(temp_path, bmp_path)

# Find site boundaries
boundaries = find_site_boundaries(doc)
if not boundaries:
    forms.alert("No site boundaries found", exitscript=True)

# Get bounding box
bbox_min, bbox_max = get_bounding_box(boundaries)

# Create a 3D view (or adjust an existing one) for the export
collector = FilteredElementCollector(doc).OfClass(View3D)
view = None
for v in collector:
    if v.Name == "SiteBoundaryExportView":  # Choose or create a view suitable for export
        view = v
        break

if not view:
    view = View3D.CreateIsometric(doc, doc.ActiveView.GetTypeId())
    view.Name = "SiteBoundaryExportView"

view.CropBoxActive = True
view.CropBoxVisible = False
view.CropBox.Min = bbox_min
view.CropBox.Max = bbox_max

# Define the directory to save BMP files
output_dir = "C:/yolov8/bim"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Export the view to BMP
output_path = os.path.join(output_dir, "site_boundary.bmp")
export_view_to_bmp(view, output_path)

# Adjust the BMP origin
adjust_bmp_origin(output_path)

print("Site boundary view exported to BMP:", output_path)"""