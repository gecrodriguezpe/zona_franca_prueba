from typing import List, Dict, Tuple
from pathlib import Path 

import itertools
from accounting_templates import plantillas_contables_1
from utils import cargar_plantillas_cuentas
import classes as cl

# TODO: Usar pathlib para manejar todas las rutas


PATH = str((Path(__file__).resolve()).parent)

# Ruta de la plantilla contable
ruta = r"/home/germankux/Documents/MIT/RA/GSF/FTZ_Model"

# Cargar la plantilla contable
plantilla_1 = cargar_plantillas_cuentas(ruta)


### Diccionario precios:
dict_precios_2 = {
    # Combinaciones de "MKT" como vendedor
    ("MKT", "ZF", "materia_prima"): 1,
    ("MKT", "NCT", "materia_prima"): 1,
    # Combinaciones de "MKT" como comprador
    ("NCT", "MKT", "bien_final"): 7,
    ("ZF", "MKT", "bien_final"): 7,
    # Combinaciones de "NCT" como vendedor
    ("NCT", "ZF", "materia_prima"): 3,
    ("NCT", "ZF", "bien_intermedio"): 5,
    ("NCT", "ZF", "bien_final"): 6,
    # Combinaciones de "ZF" como vendedor
    ("ZF", "NCT", "materia_prima"): 2,
    ("ZF", "NCT", "bien_intermedio"): 4,
    ("ZF", "NCT", "bien_final"): 6,
}

### Instanciar Agentes de NCT y ZF
planta_NCT = cl.NCT("NCT", plantilla_1, plantillas_contables_1)
planta_ZF = cl.ZF("ZF", plantilla_1, plantillas_contables_1PATH = str((Path(__file__).resolve()).parent))


lista_planes = list(itertools.product([0, 1], repeat=3))

for plan in lista_planes:
    planta_NCT.reiniciar_estado_contable()
    planta_ZF.reiniciar_estado_contable()
    print("---------------------------------------------")
    print("Los resultados para el plan", " ", plan)
    ejecutor = cl.EjecutorPlan(plan, planta_NCT, planta_ZF, dict_precios_2)
    ejecutor.ejecutar()

    u1 = planta_NCT.generar_estado_resultados()

    u2 = planta_ZF.generar_estado_resultados()

    W = (
        planta_NCT.calcular_utilidad_operacional()
        + planta_ZF.calcular_utilidad_operacional()
    )

    print(u1, u2, "Utilidad Agregada", "|", W)
    print("---------------------------------------------")
