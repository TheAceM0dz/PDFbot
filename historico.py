import json
import os
from datetime import datetime

CAMINHO_LOG = "logs/log.json"

def carregar_historico():
    if not os.path.exists(CAMINHO_LOG):
        return []
    try:
        with open(CAMINHO_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

def salvar_historico(arquivo, resultado):
    historico = carregar_historico()
    historico.append({
        "arquivo": arquivo,
        "resultado": resultado,
        "hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    with open(CAMINHO_LOG, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

def mostrar_historico():
    historico = carregar_historico()
    if not historico:
        print("Nenhuma conversão registrada ainda.")
        return
    print("\n--- Histórico de conversões ---")
    for item in historico:
        print(f"{item['hora']} | {item['arquivo']} -> {item['resultado']}")
    print("-------------------------------\n")
