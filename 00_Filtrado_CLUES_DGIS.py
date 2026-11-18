# -*- coding: utf-8 -*-
"""
Material complementario - Paso 1: filtrado por hospital (CLUES).
Es el mismo código que aparecía en el manuscrito, aplicado a los tres años y a las tres tablas.
Además imprime cuántos registros quedan en cada tabla y año, que son los datos de la
fila "Tablas URGENCIAS / AFECCIONES / MEDICAMENTOS tras filtrar por CLUES" de la Tabla 1.
"""
import pandas as pd

BASE = r"/content/drive/MyDrive/Urgencias"          # ajustar a la ruta propia
ANIOS = [2020, 2021, 2022]
TABLAS = ["URGENCIAS", "AFECCIONES", "MEDICAMENTOS"]
CLUES = ["TCSSA004301", "TCSSA002971", "TCSSA004564"]

conteos = []
for anio in ANIOS:
    for tabla in TABLAS:
        ruta = f"{BASE}/Urgencias_{anio}/{tabla}.csv"
        df = pd.read_csv(ruta, sep="|", low_memory=False)
        df.columns = df.columns.str.strip().str.upper()
        df["CLUES"] = df["CLUES"].astype(str).str.strip()
        df_filtrado = df[df["CLUES"].isin(CLUES)].copy()
        salida = f"{BASE}/Urgencias_{anio}/{tabla}_filtrado.csv"
        df_filtrado.to_csv(salida, sep="|", index=False, encoding="utf-8-sig")
        fila = {"Año": anio, "Tabla": tabla, "Registros_originales": len(df), "Registros_filtrados": len(df_filtrado)}
        # Verificación de la observación 2: ¿el ID es único dentro del año y la CLUES? (solo en URGENCIAS)
        if tabla == "URGENCIAS" and "ID" in df_filtrado.columns:
            fila["ID_duplicados_por_CLUES"] = int(df_filtrado.duplicated(subset=["CLUES", "ID"]).sum())
            fila["ID_duplicados_entre_CLUES"] = int(df_filtrado.duplicated(subset=["ID"]).sum())
        conteos.append(fila)
        print(fila)

pd.DataFrame(conteos).to_csv(f"{BASE}/conteos_filtrado_CLUES.csv", index=False)
print("Conteos guardados en conteos_filtrado_CLUES.csv")
