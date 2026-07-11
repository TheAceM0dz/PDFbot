"""
diagnostico.py - Verifica e instala automaticamente as dependências do PDFBOT
Criado por: TheAceModz
"""

import os
import shutil
import subprocess
import importlib.util

# Pacotes de sistema (instalados via `pkg install` no Termux)
_PACOTES_SISTEMA = [
    {"nome": "pandoc", "comando": "pandoc", "pkg": "pandoc"},
    {"nome": "tectonic", "comando": "tectonic", "pkg": "tectonic"},
    {"nome": "ghostscript", "comando": "gs", "pkg": "ghostscript"},
    {"nome": "poppler (pdftoppm/pdftotext)", "comando": "pdftoppm", "pkg": "poppler"},
    {"nome": "tesseract", "comando": "tesseract", "pkg": "tesseract"},
    {"nome": "espeak", "comando": "espeak", "pkg": "espeak"},
]

# Bibliotecas Python (instaladas via `pip install`)
_PACOTES_PYTHON = [
    {"nome": "rich", "modulo": "rich", "pip": "rich"},
    {"nome": "questionary", "modulo": "questionary", "pip": "questionary"},
    {"nome": "pypdf", "modulo": "pypdf", "pip": "pypdf"},
    {"nome": "reportlab", "modulo": "reportlab", "pip": "reportlab"},
    {"nome": "python-docx", "modulo": "docx", "pip": "python-docx"},
    {"nome": "Pillow", "modulo": "PIL", "pip": "Pillow"},
]

_URL_TESSDATA_POR = "https://github.com/tesseract-ocr/tessdata_fast/raw/main/por.traineddata"


def _caminho_tessdata_por():
    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    return os.path.join(prefix, "share", "tessdata", "por.traineddata")


def verificar_tudo():
    """Retorna uma lista de dicts: nome, tipo (sistema/python/dado), instalado (bool)."""
    resultados = []

    for pacote in _PACOTES_SISTEMA:
        instalado = shutil.which(pacote["comando"]) is not None
        resultados.append({
            "nome": pacote["nome"],
            "tipo": "sistema",
            "instalado": instalado,
            "alvo": pacote["pkg"],
        })

    for pacote in _PACOTES_PYTHON:
        instalado = importlib.util.find_spec(pacote["modulo"]) is not None
        resultados.append({
            "nome": pacote["nome"],
            "tipo": "python",
            "instalado": instalado,
            "alvo": pacote["pip"],
        })

    resultados.append({
        "nome": "Tesseract - idioma Português",
        "tipo": "dado",
        "instalado": os.path.exists(_caminho_tessdata_por()),
        "alvo": "por.traineddata",
    })

    return resultados


def instalar_item(item):
    """Tenta instalar o item faltante. Retorna (sucesso: bool, erro: str|None)."""
    try:
        if item["tipo"] == "sistema":
            subprocess.run(
                ["pkg", "install", "-y", item["alvo"]],
                check=True,
                capture_output=True,
            )
        elif item["tipo"] == "python":
            subprocess.run(
                ["pip", "install", "--break-system-packages", item["alvo"]],
                check=True,
                capture_output=True,
            )
        elif item["tipo"] == "dado":
            pasta = os.path.dirname(_caminho_tessdata_por())
            os.makedirs(pasta, exist_ok=True)
            subprocess.run(
                ["curl", "-fsSL", "-o", _caminho_tessdata_por(), _URL_TESSDATA_POR],
                check=True,
                capture_output=True,
            )
        return True, None
    except subprocess.CalledProcessError as e:
        detalhe = e.stderr.decode(errors="ignore")[-300:] if e.stderr else str(e)
        return False, detalhe
    except Exception as e:
        return False, str(e)
