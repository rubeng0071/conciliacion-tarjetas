import os
import pandas as pd
import openpyxl

def generate_excel(records, original_filepath, output_dir):
    filename = os.path.basename(original_filepath).replace('.TXT', '.xlsx')
    output_path = os.path.join(output_dir, filename)

    # Nombres descriptivos para las hojas
    sheet_names = {
        '1': "Header de Comercio Centralizador",
        '2': "Header de Liquidación a Comercio Participante",
        '3': "Detalle de Transacción",
        '6': "Trailer de Venta de Liquidación",
        '7': "Trailer de Liquidación a Comercio Participante",
        '8': "Trailer de Liquidación a Comercio Participante - Impuestos",
        '9': "Trailer de Comercio Centralizador",
        'unknown': "Registros Desconocidos"
    }

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for tipo, lines in records.items():
            if not lines:
                continue
            df = pd.DataFrame(lines)

            # Sobrescribir columnas originales con la descripción si existe
            sobrescribir = [
                ("Producto", "Producto Descripción"),
                ("Moneda", "Moneda Descripción"),
                ("Tipo de Plazo de Pago", "Tipo de Plazo de Pago Descripción"),
                ("Marca Venta", "Marca Venta Descripción"),
                ("Marca Acuerdo", "Marca Acuerdo Descripción"),
                ("Signo", "Signo Descripción"),
                ("Tipo Plan Cuotas", "Tipo Plan Cuotas Descripción"),
                ("Promoción Cuotas", "Promoción Cuotas Descripción"),
            ]
            for col, desc_col in sobrescribir:
                if desc_col in df.columns:
                    df[col] = df[desc_col]
                    df = df.drop(columns=[desc_col])

            # Usar nombre descriptivo para la hoja
            sheet_name = sheet_names.get(tipo, f"Tipo {tipo}")[:31]  # Excel limita a 31 caracteres
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Ajustar anchos de columna automáticamente
    wb = openpyxl.load_workbook(output_path)
    for ws in wb.worksheets:
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except Exception:
                    pass
            ws.column_dimensions[col_letter].width = max_length + 2
    wb.save(output_path)

    print(f"Excel generado: {output_path}")
    return output_path
