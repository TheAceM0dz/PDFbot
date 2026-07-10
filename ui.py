"""
ui.py - Camada visual do PDFBOT
Criado por: TheAceModz

Responsável por: banner com gradiente RGB, menus interativos (questionary),
mensagens estilizadas (rich), persistência do último caminho usado e idioma.
"""

import os
import json
import colorsys
from datetime import datetime

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.rule import Rule
from rich import box
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

import questionary
from questionary import Style

import historico as _historico
from idiomas import TEXTOS

console = Console()

CONFIG_PATH = os.path.expanduser("~/.pdfbot_config.json")
RAIZ_STORAGE = "/data/data/com.termux/files/home/storage/"

ICONES_PASTA = {
    "dcim": "📷", "downloads": "⬇️", "download": "⬇️", "movies": "🎬",
    "music": "🎵", "pictures": "🖼️", "screenshots": "📱", "shared": "📂",
    "documents": "📄", "external-1": "💾", "external-sd": "💾",
}

# ------------------------------------------------------------------
# Configuração persistente (último caminho usado + idioma)
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


def nome_seguro(caminho_desejado):
    """Se já existe um arquivo com esse nome, gera outro nome com
    carimbo de data/hora em vez de sobrescrever sem avisar."""
    if not os.path.exists(caminho_desejado):
        return caminho_desejado
    pasta, nome = os.path.split(caminho_desejado)
    base, ext = os.path.splitext(nome)
    carimbo = datetime.now().strftime("%Y%m%d-%H%M%S")
    return os.path.join(pasta, f"{base}_{carimbo}{ext}")


def arquivo_mais_recente(pasta):
    """Retorna o caminho do arquivo modificado mais recentemente na pasta,
    ou None se a pasta estiver vazia/inacessível."""
    try:
        candidatos = [
            os.path.join(pasta, f) for f in os.listdir(pasta)
            if os.path.isfile(os.path.join(pasta, f))
        ]
    except OSError:
        return None
    if not candidatos:
        return None
    return max(candidatos, key=os.path.getmtime)


# ------------------------------------------------------------------
# Idioma
# ------------------------------------------------------------------

def idioma_atual():
    return carregar_config().get("idioma", "pt")

def definir_idioma(codigo):
    salvar_config({"idioma": codigo})

def t(chave, **kwargs):
    """Busca o texto traduzido no idioma atual. Aceita placeholders
    tipo t('msg_saida_padrao', caminho=algo)."""
    textos = TEXTOS.get(idioma_atual(), TEXTOS["pt"])
    bruto = textos.get(chave, TEXTOS["pt"].get(chave, chave))
    return bruto.format(**kwargs) if kwargs else bruto

def perguntar_idioma():
    escolha = questionary.select(
        t("idioma_pergunta"),
        choices=[
            questionary.Choice(t("idioma_pt"), value="pt"),
            questionary.Choice(t("idioma_en"), value="en"),
        ],
        style=ESTILO_MENU,
        qmark="🌐",
    ).ask()

    if escolha:
        definir_idioma(escolha)
        print_sucesso(t("idioma_alterado"))


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

_FONTE_BLOCO = {
    "P": ["█████", "█   █", "█████", "█    ", "█    ", "█    "],
    "D": ["████ ", "█   █", "█   █", "█   █", "█   █", "████ "],
    "F": ["█████", "█    ", "████ ", "█    ", "█    ", "█    "],
    "B": ["████ ", "█   █", "████ ", "█   █", "█   █", "████ "],
    "O": [" ███ ", "█   █", "█   █", "█   █", "█   █", " ███ "],
    "T": ["█████", "  █  ", "  █  ", "  █  ", "  █  ", "  █  "],
    " ": ["     ", "     ", "     ", "     ", "     ", "     "],
}

def _arte_titulo(texto="PDFBOT"):
    linhas = ["" for _ in range(6)]
    for letra in texto:
        padrao = _FONTE_BLOCO.get(letra.upper(), _FONTE_BLOCO[" "])
        for i in range(6):
            linhas[i] += padrao[i] + " "
    return linhas

def banner():
    """Mostra o título PDFBOT com moldura e gradiente estilo RGB
    (a cor muda a cada retorno ao menu, não a cada tecla)."""
    hue = _proximo_hue()
    linhas = _arte_titulo()
    texto_titulo = _gradiente(linhas, hue, span=0.9, sat=0.9)

    r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 1.0)
    cor_moldura = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    conteudo = Align.center(texto_titulo)

    console.clear()
    console.print(
        Panel(
            conteudo,
            border_style=cor_moldura,
            box=box.DOUBLE,
            padding=(0, 2),
        )
    )
    console.print(Align.center(Text(t("banner_tagline"), style="dim italic")))
    console.print(Align.center(Text("by TheAceModz", style=f"bold {cor_moldura}")))

    total = len(_historico.carregar_historico())
    console.print(Rule(style=f"dim {cor_moldura}"))
    console.print(Align.center(Text(t("banner_stats", total=total), style="dim")))
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
    console.print(Panel(f"✔ {msg}", border_style="green", expand=False))

def print_erro(msg):
    console.print(Panel(f"✘ {msg}", border_style="red", expand=False))

def print_info(msg):
    console.print(Panel(f"ℹ {msg}", border_style="cyan", expand=False))

def print_painel(titulo, conteudo, cor="magenta"):
    console.print(Panel(conteudo, title=titulo, border_style=cor, expand=False))


# ------------------------------------------------------------------
# Breadcrumb (trilha de navegação)
# ------------------------------------------------------------------

def trilha(*partes):
    caminho = " › ".join(partes)
    console.print(f"[dim]{caminho}[/dim]")


# ------------------------------------------------------------------
# Preview do arquivo antes de processar
# ------------------------------------------------------------------

def formatar_tamanho(num_bytes):
    tamanho = float(num_bytes)
    for unidade in ["B", "KB", "MB", "GB"]:
        if tamanho < 1024:
            return f"{tamanho:.0f} {unidade}" if unidade == "B" else f"{tamanho:.1f} {unidade}"
        tamanho /= 1024
    return f"{tamanho:.1f} TB"

def preview_arquivo(caminho):
    try:
        tamanho = os.path.getsize(caminho)
    except OSError:
        tamanho = 0
    extensao = os.path.splitext(caminho)[1].lower()

    linhas = [
        f"[bold]{t('preview_nome')}:[/bold] {os.path.basename(caminho)}",
        f"[bold]{t('preview_tamanho')}:[/bold] {formatar_tamanho(tamanho)}",
        f"[bold]{t('preview_tipo')}:[/bold] {extensao or '?'}",
    ]

    if extensao == ".pdf":
        try:
            from pypdf import PdfReader
            paginas = len(PdfReader(caminho).pages)
            linhas.append(f"[bold]{t('preview_paginas')}:[/bold] {paginas}")
        except Exception:
            pass

    console.print(
        Panel("\n".join(linhas), title=f"📄 {t('preview_titulo')}", border_style="cyan", expand=False)
    )


# ------------------------------------------------------------------
# Resumo/confirmação antes de executar a operação
# ------------------------------------------------------------------

def painel_resumo(itens, titulo=None):
    if titulo is None:
        titulo = t("resumo_titulo")
    linhas = [f"[bold]{chave}:[/bold] {valor}" for chave, valor in itens.items()]
    console.print(Panel("\n".join(linhas), title=f"📋 {titulo}", border_style="yellow", expand=False))

def confirmar_resumo(itens, titulo=None):
    painel_resumo(itens, titulo)
    resposta = questionary.confirm(
        t("resumo_confirmar"), default=True, style=ESTILO_MENU
    ).ask()
    return bool(resposta)


# ------------------------------------------------------------------
# Tela de despedida com resumo da sessão
# ------------------------------------------------------------------

def tela_despedida(sucessos=0, falhas=0):
    linhas = []
    if sucessos == 0 and falhas == 0:
        linhas.append(t("despedida_nenhuma"))
    else:
        if sucessos:
            linhas.append(f"[green]{t('despedida_sucessos', n=sucessos)}[/green]")
        if falhas:
            linhas.append(f"[red]{t('despedida_falhas', n=falhas)}[/red]")

    console.print(
        Panel(
            "\n".join(linhas),
            title=f"👋 {t('despedida_titulo')}",
            border_style="magenta",
            expand=False,
        )
    )


# ------------------------------------------------------------------
# Seleção de pasta/arquivo
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
        escolhas.append(questionary.Choice(t("pasta_ultimo"), value=ultimo))
    for p in pastas:
        icone = ICONES_PASTA.get(p.lower(), "📁")
        escolhas.append(questionary.Choice(f"{icone}  {p}", value=os.path.join(RAIZ_STORAGE, p)))
    escolhas.append(questionary.Choice(t("pasta_manual"), value="__manual__"))

    escolha = questionary.select(
        t("pasta_pergunta"),
        choices=escolhas,
        style=ESTILO_MENU,
        qmark="📂",
    ).ask()

    return escolha if escolha else RAIZ_STORAGE


def escolher_pasta_para_lote():
    """Como escolher_pasta_base, mas o resultado final tem que ser
    sempre uma pasta (não um arquivo)."""
    pasta = escolher_pasta_base()
    if pasta != "__manual__":
        return pasta

    caminho = questionary.path(
        t("pasta_lote_manual_prompt"),
        default=RAIZ_STORAGE,
        only_directories=True,
        style=ESTILO_MENU,
    ).ask()
    return caminho.strip() if caminho else RAIZ_STORAGE


def perguntar_caminho_arquivo():
    pasta = escolher_pasta_base()

    if pasta == "__manual__":
        caminho = questionary.path(
            t("arquivo_manual_prompt"),
            default=RAIZ_STORAGE,
            style=ESTILO_MENU,
        ).ask()
        return caminho.strip() if caminho else ""

    recente = arquivo_mais_recente(pasta)
    if recente:
        modo = questionary.select(
            t("arquivo_como_selecionar"),
            choices=[
                questionary.Choice(
                    t("arquivo_usar_recente", nome=os.path.basename(recente)),
                    value="recente"
                ),
                questionary.Choice(t("arquivo_digitar_nome"), value="digitar"),
            ],
            style=ESTILO_MENU,
            qmark="📄",
        ).ask()
        if modo == "recente":
            return recente

    caminho = questionary.path(
        t("arquivo_selecionar_tab"),
        default=pasta.rstrip("/") + "/",
        style=ESTILO_MENU,
    ).ask()
    return caminho.strip() if caminho else ""


def perguntar_caminho_saida(padrao_sugerido):
    quer_custom = questionary.confirm(
        t("saida_pergunta_custom"),
        default=False,
        style=ESTILO_MENU,
    ).ask()

    if not quer_custom:
        return padrao_sugerido

    caminho = questionary.path(
        t("saida_caminho"),
        default=padrao_sugerido,
        style=ESTILO_MENU,
    ).ask()

    if not caminho:
        return padrao_sugerido
    caminho = caminho.strip()
    if not caminho.endswith(".pdf"):
        caminho += ".pdf"
    return caminho


# ------------------------------------------------------------------
# Menus
# ------------------------------------------------------------------

def menu_principal():
    return questionary.select(
        t("menu_titulo"),
        choices=[
            questionary.Choice(t("menu_converter"), value="converter"),
            questionary.Choice(t("menu_de_pdf"), value="de_pdf"),
            questionary.Choice(t("menu_lote"), value="lote"),
            questionary.Choice(t("menu_ferramentas"), value="ferramentas"),
            questionary.Choice(t("menu_historico"), value="historico"),
            questionary.Choice(t("menu_idioma"), value="idioma"),
            questionary.Choice(t("menu_sair"), value="sair"),
        ],
        style=ESTILO_MENU,
        qmark="➤",
    ).ask()


def menu_ferramentas():
    return questionary.select(
        t("ferramentas_titulo"),
        choices=[
            questionary.Choice(t("ferramentas_unir"), value="unir"),
            questionary.Choice(t("ferramentas_comprimir"), value="comprimir"),
            questionary.Choice(t("ferramentas_extrair"), value="extrair"),
            questionary.Choice(t("ferramentas_proteger"), value="proteger"),
            questionary.Choice(t("ferramentas_marca"), value="marca_dagua"),
            questionary.Choice(t("ferramentas_ocr"), value="ocr"),
            questionary.Choice(t("ferramentas_voltar"), value="voltar"),
        ],
        style=ESTILO_MENU,
        qmark="🛠️",
    ).ask()


def perguntar_formato_destino():
    """Usado no modo PDF -> outro formato."""
    return questionary.select(
        t("formato_titulo"),
        choices=[
            questionary.Choice(t("formato_png"), value=".png"),
            questionary.Choice(t("formato_jpeg"), value=".jpg"),
            questionary.Choice(t("formato_docx"), value=".docx"),
            questionary.Choice(t("formato_txt"), value=".txt"),
        ],
        style=ESTILO_MENU,
        qmark="🔁",
    ).ask()


def tabela_historico(itens):
    tabela = Table(title=t("historico_titulo"), border_style="magenta", expand=False)
    tabela.add_column(t("historico_col_data"), style="cyan", no_wrap=True)
    tabela.add_column(t("historico_col_arquivo"), style="white")
    tabela.add_column(t("historico_col_resultado"), style="bold")

    for item in itens:
        resultado = item["resultado"]
        estilo = "green" if resultado == "Sucesso" else "red"
        tabela.add_row(item["hora"], item["arquivo"], f"[{estilo}]{resultado}[/{estilo}]")

    return tabela


# ------------------------------------------------------------------
# Prompts das ferramentas de PDF
# ------------------------------------------------------------------

def perguntar_lista_pdfs_para_unir():
    """Pergunta arquivos um por um até o usuário dizer 'não tenho mais'."""
    caminhos = []
    while True:
        pasta = escolher_pasta_base()
        default = "" if pasta == "__manual__" else pasta.rstrip("/") + "/"
        caminho = questionary.path(
            t("unir_arquivo_n", n=len(caminhos) + 1),
            default=default,
            style=ESTILO_MENU,
        ).ask()
        if caminho:
            caminhos.append(caminho.strip())
            print_sucesso(t("unir_adicionado", caminho=caminho.strip()))
        continuar = questionary.confirm(
            t("unir_outro"), default=len(caminhos) < 2, style=ESTILO_MENU
        ).ask()
        if not continuar:
            break
    return caminhos


def perguntar_nivel_compressao():
    return questionary.select(
        t("compressao_titulo"),
        choices=[
            questionary.Choice(t("compressao_leve"), value="prepress"),
            questionary.Choice(t("compressao_medio"), value="printer"),
            questionary.Choice(t("compressao_forte"), value="ebook"),
            questionary.Choice(t("compressao_maxima"), value="screen"),
        ],
        style=ESTILO_MENU,
        qmark="🗜️",
    ).ask()


def perguntar_intervalo_paginas():
    return questionary.text(
        t("paginas_pergunta"),
        style=ESTILO_MENU,
    ).ask()


def perguntar_senha():
    return questionary.password(
        t("senha_pergunta"),
        style=ESTILO_MENU,
    ).ask()


def perguntar_texto_marca_dagua():
    return questionary.text(
        t("marca_texto_pergunta"),
        default="CONFIDENCIAL",
        style=ESTILO_MENU,
    ).ask()


def perguntar_idioma_ocr():
    return questionary.select(
        t("ocr_idioma_pergunta"),
        choices=[
            questionary.Choice(t("ocr_portugues"), value="por"),
            questionary.Choice(t("ocr_ingles"), value="eng"),
        ],
        style=ESTILO_MENU,
        qmark="🔍",
    ).ask()


def barra_progresso(total, descricao=None):
    """Retorna um contexto de progress bar do rich pronto pra usar em loop."""
    if descricao is None:
        descricao = t("status_lote")
    return Progress(
        TextColumn("[bold cyan]" + descricao + "[/bold cyan]"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeRemainingColumn(),
        console=console,
    )
