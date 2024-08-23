# -*- coding: utf-8 -*-

# IMPORTS
from Autodesk.Revit.DB import *

# VARIABLES

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

# FUNCTIONS

def get_selected_elements(uidoc):
    return [vidoc.Document.GetElement(elem_id) for elem_id in vidoc.Selection.GetElementIds()]