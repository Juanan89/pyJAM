# -*- coding: utf-8 -*-


from Autodesk.Revit.DB import(
    Document
)

from pyrevit import revit

__title__   = "Copiar subproyectos"
__author__  = "Juanan Martínez"
__doc__     = """Establece como actual el subproyecto seleccionado"""

doc = revit.doc
uidoc = revit.uidoc

def get_one_element():
    """Devuelve el objeto seleccionado. Si no hay un único objeto seleccionado, pide al usuario que seleccione uno.

    Returns:
    ref_object (Autodesk.Revit.DB.Element): Objeto seleccionado

   """
    sel = revit.get_selection()
    if len(sel.element_ids) == 1:
        ref_object = sel.elements[0]
    else:
        ref_object = revit.pick_element(message="Seleccione un elemento")
    return ref_object

def set_workset_from_object(ref_object):
    """Establece como subproyecto activo el subproyecto del objeto de referencia

    Parameters:
    ref_object (Autodesk.Revit.DB.Element): Objeto de referencia

   """
    ro_workset_id = ref_object.WorksetId
    wstable = Document.GetWorksetTable(doc)
    wstable.SetActiveWorksetId(ro_workset_id)

if __name__ == '__main__':
    ref_object = get_one_element()
    set_workset_from_object(ref_object)
