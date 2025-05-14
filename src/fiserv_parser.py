import pandas as pd
from datetime import datetime

def convertir_a_decimal(cadena, total_digitos, decimales=2):
    cadena = cadena.strip().zfill(total_digitos)
    if len(cadena) <= decimales:
        return 0.0
    parte_entera = cadena[:-decimales]
    parte_decimal = cadena[-decimales:]
    return float(parte_entera + "." + parte_decimal)

# Mapeo de campos que requieren conversión: nombre del campo -> (total_digitos, decimales)
conversion_map = {
    "Importe Total": (11, 2), 
    "Importe Sin Dto.": (11, 2),
    "Importe Final": (11, 2),                
    "Porc. Descuento": (3, 2),
    "Importe Arancel": (7, 2),
    "I.V.A. Arancel": (7, 2), 
    "T.N.A": (3, 2),
    "Importe Costo Financiero": (7, 2),
    "I.V.A Costo Financiero": (7, 2),
    "Porcentaje Tasa Directa": (3, 2),
    "Importe Costo Tasa Dta.": (7, 2),
    "I.V.A Costo Tasa Dta.": (7, 2),
    "Alicuota-IVA-FO": (3, 2),
    "Total Importe Presentado": (11, 2),
    "Neto Liquid. original": (11, 2),
    "Descuento de Financiación": (11, 2),
    "Impuesto Ley 25063": (11, 2),
    "IVA Dto. Financiación": (11, 2),
    "Percep. IVA RG 3337":(11, 2),
    "Percepción Ing. Brutos": (11, 2),
    "Neto al Comercio_6": (11, 2),
    "Sellados Venta Liquid": (11, 2),
    "Total Importe":(11, 2),
    "Total Importe Sin Dto.":(11, 2),
    "Total Importe FinalNum":(11, 2),
    "Aranceles-Cto-Fin Num":(11, 2),
    "Retenciones Fiscales":(11, 2),
    "Otros Debitos":(11, 2),
    "Otros Creditos":(11, 2),
    "Neto al Comercio_7":(11, 2),
    "Monto Pend. de Cuotas":(11, 2),
    "I.V.A. Aranceles R.I.":(11, 2),
    "Impuesto Deb/CredNum":(11, 2),
    "I.V.A. Dto. Pago Anticipado":(11, 2),
    "Ret. I.V.A. Ventas":(11, 2),
    "Percepc I.V.A. RG 3337":(11, 2),
    "Ret. Imp. Ganancias":(11, 2),
    "Ret. Imp. IIBB":(11, 2),
    "I.V.A. Servicios":(11, 2),
    "Imp. S/Intereses Ley 25063":(7, 2),
    "Arancel":(9, 2),
    "Costo Financiero":(9, 2),
    "Retenciones AFAM":(7, 2),
    "Ingreso Brutos Cordoba":(9, 2),
    "Saldo Deudor":(9, 2),
    "Sellados":(9, 2),
    "Ingreso Brutos Tucuman":(9, 2),
    "Ingreso Brutos SIRTAC":(9, 2),
    "Total Gral Importe":(11, 2),
    "Total Gral Importe Sin Dto.":(11, 2),
    "Total Gral Importe Final":(11, 2),
    "Total Gral Aranc y C.Fin":(11, 2),
    "Total Gral Retenc Fiscal":(11, 2),
    "Total Gral Otros Debitos":(11, 2),
    "Total Gral Otros Creditos":(11, 2),
    "Total Gral Neto a Comercio":(11, 2),
    "Total Gral Monto P.Cuotas":(11, 2),
    "Total Gral Arancel":(11, 2),
    "Total Gral Costo Financiero":(11, 2),
}

signo_map = {
    "Importe Total": "Signo Total",
    "Importe Sin Dto.": "Signo Sin Dto.",
    "Importe Final": "Signo Final",
    "Importe Arancel": "Signo Arancel",
    "I.V.A. Arancel": "Signo I.V.A. Arancel",
    "Importe Costo Financiero": "Signo Costo Financiero",
    "I.V.A Costo Financiero": "Signo I.V.A Costo Financiero",
    "Importe Costo Tasa Dta.": "Signo Costo Tasa Dta.",
    "I.V.A Costo Tasa Dta.": "Signo I.V.A Costo Tasa Dta.",
    "Total Importe Presentado": "Signo Total",
    "Neto Liquid. original": "Signo Neto Liquid. original",
    "Descuento de Financiación": "Signo Descuento de Financiación",
    "Impuesto Ley 25063": "Signo Impuesto Ley",
    "IVA Dto. Financiación": "Signo IVA Dto Financiación",
    "Percep. IVA RG 3337": "Signo Percep IVA RG 3337",
    "Percepción Ing. Brutos": "Signo Percep IB",
    "Neto al Comercio_6": "Signo Neto al Comercio_6",
    "Sellados Venta Liquid": "Signo Sellados Venta Liquid",
    "Total Importe": "Signo Total",
    "Total Importe Sin Dto.": "Signo Total Importe Sin Dto",
    "Total Importe FinalNum": "Signo Total Importe FinalNum",
    "Aranceles-Cto-Fin Num": "Signo Aranceles-Cto-Fin Num",
    "Retenciones Fiscales": "Signo Retenciones Fiscales",
    "Otros Debitos": "Signo Otros Debitos",
    "Otros Creditos": "Signo Creditos",
    "Neto al Comercio_7": "Signo Neto al Comercio_7",
    "Monto Pend. de Cuotas": "Signo Monto Pend. de Cuotas",
    "I.V.A. Aranceles R.I.": "Signo I.V.A. Aranceles R.I.",
    "Impuesto Deb/CredNum": "Signo Impuesto Deb/CredNum",
    "I.V.A. Dto. Pago Anticipado": "Signo I.V.A. Dto. Pago Anticipado",
    "Ret. I.V.A. Ventas": "Signo Ret. I.V.A. Ventas",
    "Percepc I.V.A. RG 3337": "Signo Percepc I.V.A. RG 3337",
    "Ret. Imp. Ganancias": "Signo Ret. Imp. Ganancias",
    "Ret. Imp. IIBB": "Signo Ret. Imp. IIBB",
    "Percep. IIBB": "Signo Percep IIBB",
    "I.V.A. Servicios": "Signo I.V.A. Servicios",
    "Imp. S/Intereses Ley 25063": "Signo Imp. S/Intereses Ley 25063",
    "Arancel": "Signo Arancel",
    "Costo Financiero": "Signo Costo Financiero",
    "Retenciones AFAM": "Signo Retenciones AFAM",
    "Ingreso Brutos Cordoba": "Signo Ingreso Brutos Cordoba",
    "Saldo Deudor": "Signo Saldo Deudor",
    "Sellados": "Signo Sellados",
    "Ingreso Brutos Tucuman": "Signo Ingreso Brutos Tucuman",
    "Ingreso Brutos SIRTAC": "Signo Ingreso Brutos SIRTAC",
    "Total Gral Importe": "Signo Total Gral Importe",
    "Total Gral Importe Sin Dto.": "Signo Total Gral Importe Sin Dto.",
    "Total Gral Importe Final": "Signo Total Gral Importe Final",
    "Total Gral Aranc y C.Fin": "Signo Total Gral Aranc y C.Fin",
    "Total Gral Retenc Fiscal": "Signo Total Gral Retenc Fiscal",
    "Total Gral Otros Debitos": "Signo Total Gral Otros Debitos",
    "Total Gral Otros Creditos": "Signo Total Gral Otros Creditos",
    "Total Gral Neto a Comercio": "Signo Neto a Comercio",
    "Total Gral Monto P.Cuotas": "Signo Total Gral Monto P.Cuotas",
    "Total Gral Arancel": "Signo Total Gral Arancel",
    "Total Gral Costo Financiero": "Signo Total Gral Costo Financiero"
}

# Mapeos de códigos a descripciones según la guía
PRODUCTO_MAP = {
    "C": "T.Crédito",
    "M": "Maestro",
    "S": "Argencard",
    "N": "Ticket Nación",
    "J": "Tarjeta MAS",
    "F": "Tarjeta CMR",
    "E": "Tarjeta Lider",
    "G": "Diners",
    "H": "Master Debit",
    "K": "Visa Crédito",
    "Y": "Visa Débito",
    "Q": "Amex"
}
MONEDA_MAP = {
    "032": "Pesos de Argentina",
    "840": "Dólares",
    "858": "Pesos de Uruguay",
    "999": "Moneda general"
}
TIPO_PLAZO_PAGO_MAP = {
    "C": "Días Corridos",
    "H": "Días Hábiles",
    "U": "Unificado"
}
MARCA_VENTA_MAP = {
    "S": "Se vende la liquidación",
    "N": "No se vende la liquidación"
}
MARCA_ACUERDO_MAP = {
    "I": "Venta minorista",
    "A": "Venta mayorista",
    "": "Otro"
}
SIGNO_MAP = {
    "1": "Positivo",
    "2": "Negativo"
}
TIPO_PLAN_CUOTAS_MAP = {
    "0": "Contado",
    "1": "Plan Cuotas Tradicional",
    "2": "Plan Cuotas Cobro Anticipado",
    "3": "Plan Cuotas Cobro Anticipado Financiado por Pagadora",
    "4": "Plan Cuotas Cobro Anticipado Financ. por Pagadora (Convertidos)",
    "5": "Plan Préstamos de Consumo",
    "6": "Plan Préstamos de Financiación",
    "7": "Pago Anticipado Contado",
    "8": "Plan Cuota Plazo Promedio Número de Tarjeta"
}
PROMO_CUOTAS_MAP = {
    "S": "Es promoción",
    "N": "No es promoción"
}

# Lista de campos de fecha AAAAMMDD extraídos del PDF
CAMPOS_FECHA_YYYYMMDD = [
    "Fecha de Presentación",
    "F.Vencimiento Clearing",
    "Fecha Operación",
    "Fecha de Presenta. Original",
    "F.Vencimiento Clearing (F. de Pago)",
    "F.Vencimiento\nClearing",
    "Fecha de\nPresentación",
    "Fecha de\nPresent. Original",
    # Agrega aquí otros nombres exactos según el PDF/tablas
]

specs = {
    '1': [
        ("Tipo Registro", 0, 1),
        ("Nombre Archivo", 1, 7),
        ("Comercio Centralizador", 7, 15),
        ("Producto", 15, 16),
        ("Moneda", 16, 19),
        ("Grupo de Presentación", 19, 21),
        ("Plazo de Pago", 21, 23),
        ("Tipo de Plazo de Pago", 23, 24),
        ("Fecha de Presentación", 24, 32),
        ("F.Vencimiento Clearing", 32, 40),
        ("Relleno1", 40, 46),
        ("Leyenda", 46, 67),
        ("Relleno2", 67, 350)
    ],
    '2': [
        ("Tipo Registro", 0, 1),
        ("Nombre Archivo", 1, 7),
        ("Comercio Centralizador", 7, 15),
        ("Producto", 15, 16),
        ("Moneda", 16, 19),
        ("Grupo de Presentación", 19, 21),
        ("Plazo de Pago", 21, 23),
        ("Tipo de Plazo de Pago", 23, 24),
        ("Fecha de Presentación", 24, 32),
        ("F.Vencimiento Clearing", 32, 40),
        ("Comercio Participante", 40, 48),
        ("Entidad Pagadora", 48, 51),
        ("Sucursal Pagadora", 51, 54),
        ("Número Liquidación", 54, 61),
        ("Marca Venta", 61, 62),
        ("Marca Acuerdo", 62, 63),
        ("RUT comercio", 63, 76),
        ("Provincia Comercio", 76, 77),
        ("Provincia Ing. Brutos", 77, 78),
        ("CUIT/RUT", 78, 91),
        ("Relleno", 91, 350)
    ],
    '3': [  # Registro de Detalle de Liquidación a Comercio Participante
        ("Tipo Registro", 0, 1),                    # Pos 001, Long 001
        ("Nombre Archivo", 1, 7),                   # Pos 002, Long 006
        ("Comercio Centralizador", 7, 15),          # Pos 008, Long 008
        ("Producto", 15, 16),                       # Pos 016, Long 001
        ("Moneda", 16, 19),                         # Pos 017, Long 003
        ("Grupo de Presentación", 19, 21),          # Pos 020, Long 002
        ("Plazo de Pago", 21, 23),                  # Pos 022, Long 002
        ("Tipo de Plazo de Pago", 23, 24),          # Pos 024, Long 001
        ("Fecha de Presentación", 24, 32),          # Pos 025, Long 008
        ("F.Vencimiento Clearing", 32, 40),         # Pos 033, Long 008
        ("Comercio Participante", 40, 48),          # Pos 041, Long 008
        ("Entidad Pagadora", 48, 51),               # Pos 049, Long 003
        ("Sucursal Pagadora", 51, 54),              # Pos 052, Long 003
        ("Número Liquidación", 54, 61),             # Pos 055, Long 007
        ("Fecha Operación", 61, 69),                # Pos 062, Long 008
        ("Código Movimiento", 69, 72),              # Pos 070, Long 003
        ("Código de Origen", 72, 73),               # Pos 073, Long 001
        ("Caja/Nro. Cinta Posnet", 73, 82),         # Pos 074, Long 009
        ("Carátula/Terminal Posnet", 82, 91),       # Pos 083, Long 009
        ("Resumen/Lote Posnet", 91, 94),            # Pos 092, Long 003
        ("Cupón/Cupón Posnet", 94, 99),             # Pos 095, Long 005
        ("Cuotas plan", 99, 101),                   # Pos 100, Long 002
        ("Cuota Vigente", 101, 103),                # Pos 102, Long 002
        ("Importe Total", 103, 116),                # Pos 104, Long 013
        ("Signo Total", 116, 117),                  # Pos 117, Long 001
        ("Importe Sin Dto.", 117, 130),             # Pos 118, Long 013
        ("Signo Sin Dto.", 130, 131),               # Pos 131, Long 001
        ("Importe Final", 131, 144),                # Pos 132, Long 013
        ("Signo Final", 144, 145),                  # Pos 145, Long 001
        ("Porc. Descuento", 145, 150),              # Pos 146, Long 005
        ("Marca Error", 150, 151),                  # Pos 151, Long 001
        ("Tipo Plan Cuotas", 151, 152),             # Pos 152, Long 001
        ("Nro. de Tarjeta", 152,171),               # Pos 153, Long 019
        ("Motivo de Rechezo-1", 171, 174),          # Pos 172, Long 003
        ("Motivo de Rechezo-2", 174, 177),          # Pos 175, Long 003
        ("Motivo de Rechezo-3", 177, 180),          # Pos 178, Long 003
        ("Motivo de Rechezo-4", 180, 183),          # Pos 181, Long 003
        ("Fecha de Presenta. Original", 183, 191),  # Pos 184, Long 008 Formato AAAA-MM-DD
        ("Motivo Reversion", 191, 193),             # Pos 192, Long 002
        ("Tipo de Operacion", 193, 195),            # Pos 194, Long 002
        ("Marca Campania", 195, 196),               # Pos 196, Long 001
        ("Codigo de Cargo/Pago", 196, 199),         # Pos 197, Long 003
        ("Entidad Emisora", 199, 202),              # Pos 200, Long 003
        ("Importe Arancel", 202, 211),              # Pos 203, Long 009
        ("Signo Arancel", 211, 212),                # Pos 212, Long 001
        ("I.V.A. Arancel", 212, 221),             # Pos 213, Long 009
        ("Signo I.V.A. Arancel", 221, 222),       # Pos 222, Long 001
        ("Promocion Cuotas Alfa", 222, 223),        # Pos 223, Long 001
        ("T.N.A", 223, 228),                        # Pos 224, Long 005
        ("Importe Costo Financiero", 228, 237),     # Pos 229, Long 009
        ("Signo Costo Financiero", 237, 238),       # Pos 238, Long 001
        ("I.V.A Costo Financiero", 238, 247),       # Pos 239, Long 009
        ("Signo I.V.A Costo Financiero", 247, 248), # Pos 248, Long 001
        ("Porcentaje Tasa Directa", 248, 253),      # Pos 249, Long 005
        ("Importe Costo Tasa Dta.", 253, 262),      # Pos 250, Long 009
        ("Signo Costo Tasa Dta.", 262, 263),        # Pos 263, Long 001
        ("I.V.A Costo Tasa Dta.", 263, 272),        # Pos 264, Long 009
        ("Signo I.V.A Costo Tasa Dta.", 272, 273),  # Pos 273, Long 001
        ("Nro-Autorizacion", 273, 281),             # Pos 274, Long 008
        ("Alicuota-IVA-FO", 281, 286),              # Pos 282, Long 005
        ("Marca Cashback", 286, 287),               # Pos 287, Long 001
        ("Resumen/lote-Orig", 287, 290),            # Pos 288, Long 003
        ("Marca Cupón Riego", 290, 291),            # Pos 291, Long 001
        ("Tipo de Anticipacion", 291, 293),         # Pos 292, Long 001
        ("Relleno", 293, 350)                       # Relleno hasta 350
    ],
    '6': [
        ("Tipo Registro", 0, 1),
        ("Nombre Archivo", 1, 7),
        ("Comercio Centralizador", 7, 15),
        ("Producto", 15, 16),
        ("Moneda", 16, 19),
        ("Grupo de Presentación", 19, 21),
        ("Plazo de Pago", 21, 23),
        ("Tipo de Plazo de Pago", 23, 24),
        ("Fecha de Presentación", 24, 32),
        ("F.Vencimiento Clearing", 32, 40),
        ("Comercio Participante", 40, 48),
        ("Entidad Pagadora", 48, 51),
        ("Sucursal Pagadora", 51, 54),
        ("Número Liquidación", 54, 61),
        ("Importe Presentado", 61, 74),
        ("Signo Presentado", 74, 75),
        ("Neto Original", 75, 88),
        ("Signo Neto Original", 88, 89),
        ("Descuento Financiero", 89, 102),
        ("Signo Descuento Financiero", 102, 103),
        ("Impuesto Ley", 103, 116),
        ("Signo Impuesto Ley", 116, 117),
        ("IVA Descuento Financiero", 117, 130),
        ("Signo IVA Dto Fin", 130, 131),
        ("TNA", 131, 136),
        ("Importe Costo Financiero", 136, 145),
        ("Signo Costo Financiero", 145, 146),
        ("IVA Costo Financiero", 146, 155),
        ("Signo IVA Costo Financiero", 155, 156),
        ("Porcentaje Tasa Directa", 156, 161),
        ("Importe Tasa Directa", 161, 170),
        ("Signo Tasa Directa", 170, 171),
        ("IVA Tasa Directa", 171, 180),
        ("Signo IVA Tasa Directa", 180, 181),
        ("Relleno", 181, 350)
    ],
    '7': [  # Trailer de Liquidación a Comercio Participante
        ("Tipo Registro", 0, 1),                    # Pos 001, Long 001 (valor 7)
        ("Nombre Archivo", 1, 7),                   # Pos 002, Long 006
        ("Comercio Centralizador", 7, 15),          # Pos 008, Long 008
        ("Producto", 15, 16),                       # Pos 016, Long 001
        ("Moneda", 16, 19),                         # Pos 017, Long 003
        ("Grupo de Presentación", 19, 21),          # Pos 020, Long 002
        ("Plazo de Pago", 21, 23),                  # Pos 022, Long 002
        ("Tipo de Plazo de Pago", 23, 24),          # Pos 024, Long 001
        ("Fecha de Presentación", 24, 32),          # Pos 025, Long 008
        ("F.Vencimiento Clearing", 32, 40),         # Pos 033, Long 008
        ("Comercio Participante", 40, 48),          # Pos 041, Long 008
        ("Entidad Pagadora", 48, 51),               # Poske 049, Long 003
        ("Sucursal Pagadora", 51, 54),              # Pos 052, Long 003
        ("Número Liquidación", 54, 61),             # Pos 055, Long 007
        ("Total Importe", 61, 74),                  # Pos 062, Long 013
        ("Signo Total", 74, 75),                    # Pos 075, Long 001
        ("Total Importe Sin Dto", 75, 88),          # Pos 076, Long 013
        ("Signo Total Importe Sin Dto", 88, 89),    # Pos 089, Long 001
        ("Total Importe FinalNum", 89, 102),        # Pos 090, Long 013
        ("Signo Total Importe FinalNum", 102, 103), # Pos 103, Long 001
        ("Aranceles-Cto-Fin Num", 103, 116),        # Pos 104, Long 013
        ("Signo Aranceles-Cto-Fin Num", 116, 117),  # Pos 117, Long 001
        ("Retenciones Fiscales", 117, 130),         # Pos 118, Long 013
        ("Signo Retenciones Fiscales", 130, 131),   # Pos 131, Long 001
        ("Otros Debitos", 131, 144),                # Pos 132, Long 013
        ("Signo Otros Debitos", 144, 145),          # Pos 145, Long 001
        ("Otros Creditos", 145, 158),               # Pos 146, Long 013
        ("Signo Creditos", 158, 159),               # Pos 159, Long 001
        ("Neto al Comercio_7", 159, 172),             # Pos 160, Long 013
        ("Signo Neto al Comercio_7", 172, 173),       # Pos 173, Long 001
        ("Total Registros Detalle", 173, 180),      # Pos 174, Long 007
        ("Monto Pend. de Cuotas", 180, 193),        # Pos 181, Long 013
        ("Signo Monto Pend. de Cuotas", 193, 194),  # Pos 194, Long 001
        ("Relleno", 194, 350)                       # Relleno hasta 350
    ],
    '8': [  # Trailer de Liquidación a Comercio Participante - Impuestos -
        ("Tipo Registro", 0, 1),                    # Pos 001, Long 001 (valor 8)
        ("Nombre Archivo", 1, 7),                   # Pos 002, Long 006
        ("Comercio Centralizador", 7, 15),          # Pos 008, Long 008
        ("Producto", 15, 16),                       # Pos 016, Long 001
        ("Moneda", 16, 19),                         # Pos 017, Long 003
        ("Grupo de Presentación", 19, 21),          # Pos 020, Long 002
        ("Plazo de Pago", 21, 23),                  # Pos 022, Long 002
        ("Tipo de Plazo de Pago", 23, 24),          # Pos 024, Long 001
        ("Fecha de Presentación", 24, 32),          # Pos 025, Long 008
        ("F.Vencimiento Clearing", 32, 40),         # Pos 033, Long 008
        ("Comercio Participante", 40, 48),          # Pos 041, Long 008
        ("Entidad Pagadora", 48, 51),               # Pos 049, Long 003
        ("Sucursal Pagadora", 51, 54),              # Pos 052, Long 003
        ("Número Liquidación", 54, 61),             # Pos 055, Long 007
        ("Subtipo de Registro", 61, 63),            # Pos 062, Long 002
        ("I.V.A. Aranceles R.I.", 63, 76),          # Pos 064, Long 013
        ("Signo I.V.A. Aranceles R.I.", 76, 77),    # Pos 077, Long 001
        ("Impuesto Deb/CredNum", 77, 90),           # Pos 078, Long 013
        ("Signo Impuesto Deb/CredNum", 90, 91),                 # Pos 091, Long 001
        ("I.V.A. Dto. Pago Anticipado", 91, 104),   # Pos 092, Long 013
        ("Signo I.V.A. Dto. Pago Anticipado", 104, 105),  # Pos 105, Long 001
        ("Ret. I.V.A. Ventas", 105, 118),           # Pos 106, Long 013
        ("Signo Ret. I.V.A. Ventas", 118, 119),     # Pos 119, Long 001
        ("Percepc I.V.A. RG 3337", 119, 132),       # Pos 120, Long 013
        ("Signo Percepc I.V.A. RG 3337", 132, 133),             # Pos 133, Long 001
        ("Ret. Imp. Ganancias", 133, 146),          # Pos 134, Long 013
        ("Signo Ret. Imp. Ganancias", 146, 147),    # Pos 147, Long 001
        ("Ret. Imp. IIBB", 147, 160),               # Pos 148, Long 013
        ("Signo Ret. Imp. IIBB", 160, 161),         # Pos 161, Long 001
        ("Percep. IIBB", 161, 174),                 # Pos 162, Long 013
        ("Signo Percep IIBB", 174, 175),            # Pos 175, Long 001
        ("I.V.A. Servicios", 175, 188),             # Pos 176, Long 013
        ("Signo I.V.A. Servicios", 188, 189),       # Pos 189, Long 001
        ("Categoria I.V.A.", 189, 190),             # Pos 190, Long 001
        ("Imp. S/Intereses Ley 25063", 190, 199),   # Pos 191, Long 009
        ("Signo Imp. S/Intereses Ley 25063", 199, 200),  # Pos 200, Long 001
        ("Arancel", 200, 211),                      # Pos 201, Long 011
        ("Signo Arancel", 211, 212),                # Pos 212, Long 001
        ("Costo Financiero", 212, 223),             # Pos 213, Long 011
        ("Signo Costo Financiero", 223, 224),       # Pos 224, Long 001
        ("Retenciones AFAM", 224, 233),             # Pos 225, Long 009
        ("Signo Retenciones AFAM", 233, 234),       # Pos 234, Long 001
        ("Ingreso Brutos Cordoba", 234, 245),       # Pos 235, Long 011
        ("Signo Ingreso Brutos Cordoba", 245, 246), # Pos 246, Long 001
        ("Saldo Deudor", 246, 257),                 # Pos 247, Long 011
        ("Signo Saldo Deudor", 257, 258),           # Pos 258, Long 001
        ("Sellados", 258, 269),                     # Pos 259, Long 011
        ("Signo Sellados", 269, 270),               # Pos 270, Long 001
        ("Ingreso Brutos Tucuman", 270, 281),       # Pos 271, Long 011
        ("Signo Ingreso Brutos Tucuman", 281, 282), # Pos 282, Long 001
        ("Ingreso Brutos SIRTAC", 282, 293),        # Pos 283, Long 011
        ("Signo Ingreso Brutos SIRTAC", 293, 294),  # Pos 294, Long 001
        ("Relleno", 294, 350)                       # Relleno hasta 350  
    ],
    '9': [  # Trailer de Comercio Centralizador
        ("Tipo Registro", 0, 1),                    # Pos 001, Long 001 (valor 9)
        ("Nombre Archivo", 1, 7),                   # Pos 002, Long 006
        ("Comercio Centralizador", 7, 15),          # Pos 008, Long 008
        ("Producto", 15, 16),                       # Pos 016, Long 001
        ("Moneda", 16, 19),                         # Pos 017, Long 003
        ("Grupo de Presentación", 19, 21),          # Pos 020, Long 002
        ("Plazo de Pago", 21, 23),                  # Pos 022, Long 002
        ("Tipo de Plazo de Pago", 23, 24),          # Pos 024, Long 001
        ("Fecha de Presentación", 24, 32),          # Pos 025, Long 008
        ("F.Vencimiento Clearing", 32, 40),         # Pos 033, Long 008
        ("Total Gral Importe", 40, 53),             # Pos 041, Long 013
        ("Signo Total Gral Importe", 53, 54),       # Pos 054, Long 001
        ("Total Gral Importe Sin Dto.", 54, 67),    # Pos 055, Long 013
        ("Signo Total Gral Importe Sin Dto.", 67, 68),    # Pos 068, Long 001
        ("Total Gral Importe Final", 68, 81),       # Pos 069, Long 013
        ("Signo Total Gral Importe Final", 81, 82), # Pos 082, Long 001
        ("Total Gral Aranc y C.Fin", 82, 95),       # Pos 083, Long 013
        ("Signo Total Gral Aranc y C.Fin", 95, 96), # Pos 096, Long 001
        ("Total Gral Retenc Fiscal", 96, 109),      # Pos 097, Long 013
        ("Signo Total Gral Retenc Fiscal", 109, 110),   # Pos 110, Long 001
        ("Total Gral Otros Debitos", 110, 123),     # Pos 111, Long 013
        ("Signo Total Gral Otros Debitos", 123, 124),    # Pos 124, Long 001
        ("Total Gral Otros Creditos", 124, 137),    # Pos 125, Long 013
        ("Signo Total Gral Otros Creditos", 137, 138),  # Pos 138, Long 001
        ("Total Gral Neto a Comercio", 138, 151),   # Pos 139, Long 013
        ("Signo Neto a Comercio", 151, 152),        # Pos 152, Long 001
        ("Total Gral Reg Detalles", 152, 159),      # Pos 153, Long 007
        ("Total Gral Reg Trailer", 159, 166),       # Pos 160, Long 007
        ("Total Gral Monto P.Cuotas", 166, 179),    # Pos 167, Long 013
        ("Signo Total Gral Monto P.Cuotas", 179, 180),  # Pos 180, Long 001
        ("Total Gral Arancel", 180, 193),           # Pos 181, Long 013
        ("Signo Total Gral Arancel", 193, 194),     # Pos 194, Long 001
        ("Total Gral Costo Financiero", 194, 207),  # Pos 195, Long 013
        ("Signo Total Gral Costo Financiero", 207, 208),# Pos 208, Long 001
        ("RellenoFinal", 208, 350)                  # Pos 209, Long 0142
    ]
}

def parse_line(line, spec_list):
    parsed = {}
    for field, start, end in spec_list:
        valor = line[start:end]
        if field in conversion_map:
            total, dec = conversion_map[field]
            decimal_value = convertir_a_decimal(valor, total, dec)
            # Aplicar signo si corresponde
            signo_campo = signo_map.get(field)
            signo_valor = None
            if signo_campo:
                for s_name, s_start, s_end in spec_list:
                    if s_name == signo_campo:
                        signo_valor = line[s_start:s_end].strip()
                        break
                if signo_valor and signo_valor == "-":
                    decimal_value *= -1
            parsed[field] = decimal_value
        else:
            parsed[field] = valor.strip()

    # Enriquecimiento de campos codificados con descripción legible
    if "Producto" in parsed:
        parsed["Producto"] = PRODUCTO_MAP.get(parsed["Producto"], parsed["Producto"])
    if "Moneda" in parsed:
        parsed["Moneda"] = MONEDA_MAP.get(parsed["Moneda"], parsed["Moneda"])
    if "Tipo de Plazo de Pago" in parsed:
        parsed["Tipo de Plazo de Pago"] = TIPO_PLAZO_PAGO_MAP.get(parsed["Tipo de Plazo de Pago"], parsed["Tipo de Plazo de Pago"])
    if "Marca Venta de Liquid." in parsed:
        parsed["Marca Venta de Liquid."] = MARCA_VENTA_MAP.get(parsed["Marca Venta de Liquid."], parsed["Marca Venta de Liquid."])
    if "Marca Acuerdo Minor/May" in parsed:
        parsed["Marca Acuerdo Minor/May"] = MARCA_ACUERDO_MAP.get(parsed["Marca Acuerdo Minor/May"], parsed["Marca Acuerdo Minor/May"])
    if "Signo" in parsed:
        parsed["Signo"] = SIGNO_MAP.get(parsed["Signo"], parsed["Signo"])
    if "Tipo Plan Cuotas" in parsed:
        parsed["Tipo Plan Cuotas"] = TIPO_PLAN_CUOTAS_MAP.get(parsed["Tipo Plan Cuotas"], parsed["Tipo Plan Cuotas"])
    if "Promoción Cuotas" in parsed:
        parsed["Promoción Cuotas"] = PROMO_CUOTAS_MAP.get(parsed["Promoción Cuotas"], parsed["Promoción Cuotas"])

    # Sobrescribir campos de fecha AAAAMMDD con formato legible
    for k in CAMPOS_FECHA_YYYYMMDD:
        if k in parsed and isinstance(parsed[k], str) and len(parsed[k]) == 8 and parsed[k].isdigit():
            try:
                dt = datetime.strptime(parsed[k], "%Y%m%d")
                parsed[k] = dt.strftime("%d-%m-%Y")
            except Exception:
                pass

    return parsed

def parse_txt(filepath):
    records = {k: [] for k in ['1', '2', '3', '6', '7', '8', '9', 'unknown']}
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip():
                continue
            tipo = line[0]
            spec = specs.get(tipo, specs.get('unknown'))
            parsed = parse_line(line, spec)
            records[tipo if tipo in records else 'unknown'].append(parsed)
    return records
