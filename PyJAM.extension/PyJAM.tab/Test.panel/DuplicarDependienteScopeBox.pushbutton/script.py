#! python3
# -*- coding: utf-8 -*-

from typing import List

from Autodesk.Revit import Exceptions

from Autodesk.Revit.DB import(
    BuiltInCategory,
    Document,
    Element,
    View,
    ViewDuplicateOption,
    Transaction,
    ForgeTypeId
)

from Autodesk.Revit.UI import(
    UIDocument,
)

from pyrevit import revit

__title__   = "Duplicar como dependiente desde caja de referencia"
__author__  = "Juanan Martínez"
__doc__     = """Duplica la vista actual como dependiente y le asigna la caja de referencia seleccionada. Permite crear múltiples vistas."""
__highlight__ = "new"

doc: Document = revit.doc
uidoc: UIDocument = revit.uidoc
vista_activa: View = doc.ActiveView
param_vista_nombre: ForgeTypeId = ForgeTypeId('autodesk.revit.parameter:viewName-1.0.0')
param_vista_caja: ForgeTypeId = ForgeTypeId('autodesk.revit.parameter:viewerVolumeOfInterestCrop-1.0.0')

preseleccion: List[Element] = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]

def filtrar_elementos_por_categoria(elementos: List[Element], categoria: BuiltInCategory):
    '''Dada una lista de elementos, devuelve sólo los de la categoría dada

    Parameters:
    elementos (list[Autodesk.Revit.DB.Element]): la lista de elementos a comprobar
    categoria (Autodesk.Revit.DB.BuiltInCategory): la categoría a comprobar

    Returns:
    elementos_filtrados (list[Autodesk.Revit.DB.Element]): la lista de elementos que pertenecen a la categoría
    
    '''
    elementos_filtrados: List[Element] = []
    for elemento in elementos:
        if elemento.Category.BuiltInCategory == BuiltInCategory.OST_VolumeOfInterest:
            elementos_filtrados.append(elemento)
    
    return elementos_filtrados

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
    vista_nueva.GetParameter(param_vista_nombre).Set(vista_nueva_nombre)
    vista_nueva.GetParameter(param_vista_caja).Set(caja.Id)

    return vista_nueva

seleccion: List[Element] = filtrar_elementos_por_categoria(preseleccion,BuiltInCategory.OST_VolumeOfInterest)

if len(seleccion) == 0:
    try:
        preseleccion = revit.pick_elements(message='Seleccione una o varias cajas de referencia')
        seleccion = filtrar_elementos_por_categoria(preseleccion,BuiltInCategory.OST_VolumeOfInterest)

    except Exceptions.OperationCanceledException:
        import sys

        sys.exit()

if len(seleccion) != 0:
    t: Transaction = Transaction(doc,'Crear vista dependiente')
    t.Start()
    for caja_referencia in seleccion:
        DuplicarConCaja(vista_activa, caja_referencia)

    t.Commit()
