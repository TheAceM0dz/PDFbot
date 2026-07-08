"""
lote.py - Conversão em lote (pasta inteira de uma vez)
Criado por: TheAceModz
"""

import os
import glob


def listar_arquivos_compativeis(pasta, extensoes):
    """Lista todos os arquivos da pasta cuja extensão está em `extensoes`
    (não entra em subpastas)."""
    arquivos = []
    for ext in extensoes:
        arquivos.extend(glob.glob(os.path.join(pasta, f"*{ext}")))
        arquivos.extend(glob.glob(os.path.join(pasta, f"*{ext.upper()}")))
    return sorted(set(arquivos))
