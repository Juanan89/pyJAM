#! python3
# -*- coding: utf-8 -*-


from Autodesk.Revit.DB import(
    BuiltInCategory,
    Document,
    Element,
    View,
    ViewDuplicateOption,
    Transaction,
)

from Autodesk.Revit.UI import(
    UIDocument,
)

from pyrevit import revit

__title__   = "Duplicar como dependiente desde caja de referencia"
__author__  = "Juanan Martínez"
__doc__     = """Duplica la vista actual como dependiente y le asigna la caja de referencia seleccionada"""

doc: Document = revit.doc
uidoc: UIDocument = revit.uidoc
vista_activa: View = doc.ActiveView

caja_referencia: Element = revit.pick_element(message='Seleccione una caja de referencia')

def DuplicarConCaja(vista: View, caja: Element):
    '''Duplica una vista como dependiente, le asigna la caja de referencia y añade el nombre de la caja de referencia a la vista dependiente.

    Parameters:
    vista (Autodesk.Revit.DB.View): la vista que se va a duplicar
    caja (Autodesk.Revit.DB.Element): la caja de referencia que se va a aplicar a la nueva vista dependiente

    Returns:
    vista_nueva (Autodesk.Revit.DB.View): la nueva vista dependiente
    
    '''
    vista_nueva_id: int = vista.Duplicate(ViewDuplicateOption.AsDependent)
    vista_nueva: View = doc.GetElement(vista_nueva_id)

    vista_nueva_nombre: str = vista.Name + " - " + caja.Name
    vista_nueva.LookupParameter('Nombre de vista').Set(vista_nueva_nombre)
    vista_nueva.LookupParameter('Caja de referencia').Set(caja.Id)

    return vista_nueva

t: Transaction = Transaction(doc,'Crear vista dependiente')
t.Start()
if caja_referencia.Category.BuiltInCategory == BuiltInCategory.OST_VolumeOfInterest:
    DuplicarConCaja(vista_activa, caja_referencia)
else:
    print("El objeto seleccionado no era una caja de referencia")
t.Commit()