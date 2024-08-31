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
    sel = revit.get_selection()
    if len(sel.element_ids) == 1: ref_object = sel.elements[0]
    else: ref_object = revit.pick_element(message="Seleccione un elemento")
    return ref_object

def set_workset_from_object(ref_object):
    """ Pide al usuario que seleccione un objeto y hace activo su subproyecto. """
    try:
        ro_workset_id = ref_object.WorksetId
        wstable = Document.GetWorksetTable(doc)
        wstable.SetActiveWorksetId(ro_workset_id)

    except:
        print("No fue posible establecer como activo el subproyecto de este objeto")

if __name__ == '__main__':
    ref_object = get_one_element()
    set_workset_from_object(ref_object)