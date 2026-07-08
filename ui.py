"""
ui.py - Camada visual do PDFBOT
Criado por: TheAceModz

Responsável por: banner com gradiente RGB, menus interativos (questionary),
mensagens estilizadas (rich) e persistência do último caminho usado.
"""

import os
import json
import colorsys

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

import questionary
from questionary import Style

try:
    from pyfiglet import Figlet
    _TEM_FIGLET = True
except ImportError:
    _TEM_FIGLET = False

console = Console()

CONFIG_PATH = os.path.expanduser("~/.pdfbot_config.json")
RAIZ_STORAGE = "/data/data/com.termux/files/home/storage/"

ICONES_PASTA = {
    "dcim": "📷", "downloads": "⬇️", "download": "⬇️", "movies": "🎬",
    "music": "🎵", "pictures": "🖼️", "screenshots": "📱", "shared": "📂",
    "documents": "📄", "external-1": "💾", "external-sd": "💾",
}

# ------------------------------------------------------------------
# Configuração persistente (último caminho usado)
# ------------------------------------------------------------------

def carregar_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

def salvar_config(dados):
    atual = carregar_config()
    atual.update(dados)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(atual, f, indent=2, ensure_ascii=False)

def ultimo_diretorio():
    return carregar_config().get("ultimo_diretorio", RAIZ_STORAGE)

def salvar_ultimo_diretorio(caminho):
    pasta = os.path.dirname(caminho) or caminho
    salvar_config({"ultimo_diretorio": pasta})


# ------------------------------------------------------------------
# Estilo visual (RGB "sutil" - muda a cada retorno ao menu, não a cada tecla)
# ------------------------------------------------------------------

_hue_state = {"valor": 0.0}

def _proximo_hue():
    _hue_state["valor"] = (_hue_state["valor"] + 0.09) % 1.0
    return _hue_state["valor"]

def _gradiente(linhas, hue_inicial, span=0.75, sat=0.85):
    largura_max = max((len(linha) for linha in linhas), default=1) or 1
    texto = Text()
    for linha in linhas:
        for j, ch in enumerate(linha):
            if ch == " ":
                texto.append(" ")
                continue
            hue = (hue_inicial + (j / largura_max) * span) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, sat, 1.0)
            cor = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            texto.append(ch, style=f"bold {cor}")
        texto.append("\n")
    return texto

def _arte_titulo():
    if _TEM_FIGLET:
        try:
            fig = Figlet(font="slant")
            return fig.renderText("PDFBOT").rstrip("\n").split("\n")
        except Exception:
            pass
    # fallback simples, caso pyfiglet não esteja instalado
    return [
        " ____  ____  _____ ____   ___ _____ ",
        "|  _ \\|  _ \\|  ___| __ ) / _ \\_   _|",
        "| |_) | | | | |_  |  _ \\| | | || |  ",
        "|  __/| |_| |  _| | |_) | |_| || |  ",
        "|_|   |____/|_|   |____/ \\___/ |_|  ",
    ]

def banner():
    """Mostra o título PDFBOT com gradiente estilo RGB (muda a cada exibição)."""
    hue = _proximo_hue()
    linhas = _arte_titulo()
    texto_titulo = _gradiente(linhas, hue)

    console.clear()
    console.print(Align.center(texto_titulo))
    console.print(Align.center(Text("by TheAceModz", style="dim italic")))
    console.print()


# ------------------------------------------------------------------
# Estilo do questionary (combina com o tema RGB/roxo-ciano)
# ------------------------------------------------------------------

ESTILO_MENU = Style([
    ("qmark", "fg:#ff5fd7 bold"),
    ("question", "bold"),
    ("answer", "fg:#5fffd7 bold"),
    ("pointer", "fg:#ff5fd7 bold"),
    ("highlighted", "fg:#5fd7ff bold"),
    ("selected", "fg:#5fffaf bold"),
    ("separator", "fg:#6c6c6c"),
    ("instruction", "fg:#8a8a8a italic"),
])


# ------------------------------------------------------------------
# Mensagens padronizadas
# ------------------------------------------------------------------

def print_sucesso(msg):
    console.print(f"[bold green]✔ {msg}[/bold green]")

def print_erro(msg):
    console.print(f"[bold red]✘ {msg}[/bold red]")

def print_info(msg):
    console.print(f"[bold cyan]ℹ {msg}[/bold cyan]")

def print_painel(titulo, conteudo, cor="magenta"):
    console.print(Panel(conteudo, title=titulo, border_style=cor, expand=False))


# ------------------------------------------------------------------
# Prompts reaproveitáveis
# ------------------------------------------------------------------

def listar_pastas_storage():
    try:
        itens = sorted(os.listdir(RAIZ_STORAGE))
    except OSError:
        return []
    return [i for i in itens if os.path.isdir(os.path.join(RAIZ_STORAGE, i))]


def escolher_pasta_base():
    """Deixa o usuário escolher em qual pasta de armazenamento navegar,
    em vez de sempre cair direto em Downloads."""
    pastas = listar_pastas_storage()
    ultimo = carregar_config().get("ultimo_diretorio")

    escolhas = []
    if ultimo:
        escolhas.append(questionary.Choice(f"🕘  Último local usado", value=ultimo))
    for p in pastas:
        icone = ICONES_PASTA.get(p.lower(), "📁")
        escolhas.append(questionary.Choice(f"{icone}  {p}", value=os.path.join(RAIZ_STORAGE, p)))
    escolhas.append(questionary.Choice("⌨️  Digitar caminho manualmente", value="__manual__"))

    escolha = questionary.select(
        "Em qual pasta está o arquivo?",
        choices=escolhas,
        style=ESTILO_MENU,
        qmark="📂",
    ).ask()

    return escolha if escolha else RAIZ_STORAGE


def perguntar_caminho_arquivo():
    pasta = escolher_pasta_base()

    if pasta == "__manual__":
        caminho = questionary.path(
            "Caminho completo do arquivo:",
            default=RAIZ_STORAGE,
            style=ESTILO_MENU,
        ).ask()
    else:
        caminho = questionary.path(
            "Selecione o arquivo (Tab autocompleta):",
            default=pasta.rstrip("/") + "/",
            style=ESTILO_MENU,
        ).ask()

    return caminho.strip() if caminho else ""

def perguntar_caminho_saida(padrao_sugerido):
    quer_custom = questionary.confirm(
        "Deseja escolher outro nome/local pro PDF?",
        default=False,
        style=ESTILO_MENU,
    ).ask()

    if not quer_custom:
        return padrao_sugerido

    caminho = questionary.path(
        "Caminho de saída do PDF:",
        default=padrao_sugerido,
        style=ESTILO_MENU,
    ).ask()

    if not caminho:
        return padrao_sugerido
    caminho = caminho.strip()
    if not caminho.endswith(".pdf"):
        caminho += ".pdf"
    return caminho

def menu_principal():
    return questionary.select(
        "O que você quer fazer?",
        choices=[
            questionary.Choice("📄  Converter arquivo para PDF", value="converter"),
            questionary.Choice("🔁  Converter PDF para outro formato", value="de_pdf"),
            questionary.Choice("🕘  Ver histórico", value="historico"),
            questionary.Choice("❌  Sair", value="sair"),
        ],
        style=ESTILO_MENU,
        qmark="➤",
    ).ask()


def perguntar_formato_destino():
    """Usado no modo PDF -> outro formato."""
    return questionary.select(
        "Converter o PDF para qual formato?",
        choices=[
            questionary.Choice("🖼️  PNG", value=".png"),
            questionary.Choice("🖼️  JPEG", value=".jpg"),
            questionary.Choice("📝  DOCX (Word)", value=".docx"),
            questionary.Choice("📃  TXT (texto puro)", value=".txt"),
        ],
        style=ESTILO_MENU,
        qmark="🔁",
    ).ask()


def tabela_historico(itens):
    tabela = Table(title="Histórico de Conversões", border_style="magenta", expand=False)
    tabela.add_column("Data/Hora", style="cyan", no_wrap=True)
    tabela.add_column("Arquivo", style="white")
    tabela.add_column("Resultado", style="bold")

    for item in itens:
        resultado = item["resultado"]
        estilo = "green" if resultado == "Sucesso" else "red"
        tabela.add_row(item["hora"], item["arquivo"], f"[{estilo}]{resultado}[/{estilo}]")

    return tabela
