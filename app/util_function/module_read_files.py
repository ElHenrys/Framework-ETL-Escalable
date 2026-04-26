import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import win32security  # pip install pywin32N

from util_function.module_config import ConfigJson


def get_ntfs_owner(filepath: str) -> str:
    sd = win32security.GetFileSecurity(
        filepath,
        win32security.OWNER_SECURITY_INFORMATION,
    )
    owner_sid = sd.GetSecurityDescriptorOwner()
    name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
    return f"{domain}\\{name}"


def read_file_auto(
    id_path_files: int,
    name_file: str,
    read_kwargs: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Lee un archivo automaticamente segun su extension.

    Extensiones soportadas:
    - .csv -> pd.read_csv
    - .xlsx -> pd.read_excel
    - .parquet -> pd.read_parquet
    - .html -> pd.read_html (retorna la primera tabla)

    ### CSV con separador ; y encoding latin-1
    df = read_file_auto(0, "ventas.csv", read_kwargs={"sep": ";", "encoding": "latin-1"})

    ### Excel leyendo una hoja específica
    df = read_file_auto(0, "reporte.xlsx", read_kwargs={"sheet_name": "Data"})

    ### HTML con header en otra fila
    df = read_file_auto(0, "tabla.html", read_kwargs={"header": 1})

    """
    read_kwargs = read_kwargs or {}

    files = ConfigJson().get_content_json_date(file_json="path_files")["files"][
        id_path_files
    ]
    path_origin = files["PATH_ORIGIN"]
    full_path = os.path.join(path_origin, name_file)
    ext = Path(name_file).suffix.lower()

    print("\n### Reading file")
    print(name_file + "\n")

    readers = {
        ".csv": pd.read_csv,
        ".xlsx": pd.read_excel,
        ".parquet": pd.read_parquet,
        ".html": pd.read_html,
    }

    if ext not in readers:
        raise ValueError(
            f"Extension no soportada: {ext}. Soportadas: {', '.join(readers.keys())}"
        )

    if ext == ".html":
        tables = readers[ext](full_path, **read_kwargs)
        data = tables[0] if tables else pd.DataFrame()
    else:
        data = readers[ext](full_path, **read_kwargs)

    # De-fragmentar el DataFrame para evitar PerformanceWarning en archivos con muchas columnas
    data = data.copy()
    data["Load_date"] = datetime.now()
    data["Filename"] = name_file
    data["cargado_por"] = get_ntfs_owner(full_path)

    if len(data.index) > 0:
        return data

    print("INFO: Archivo sin datos")
    return pd.DataFrame()
