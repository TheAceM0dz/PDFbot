"""
idiomas.py - Textos da interface do PDFBOT em português e inglês
Criado por: TheAceModz
"""

TEXTOS = {
    "pt": {
        # Banner
        "banner_tagline": "Conversor de arquivos • Termux Edition",
        "banner_stats": "📊 {total} conversão(ões) realizada(s) até agora",

        # Menu principal
        "menu_titulo": "O que você quer fazer?",
        "menu_converter": "📄  Converter arquivo para PDF",
        "menu_de_pdf": "🔁  Converter PDF para outro formato",
        "menu_lote": "📦  Conversão em lote (pasta inteira)",
        "menu_ferramentas": "🛠️  Ferramentas de PDF",
        "menu_historico": "🕘  Ver histórico",
        "menu_idioma": "🌐  Idioma / Language",
        "menu_sair": "❌  Sair",

        # Submenu ferramentas
        "ferramentas_titulo": "Qual ferramenta de PDF?",
        "ferramentas_unir": "🧩  Unir vários PDFs em um só",
        "ferramentas_comprimir": "🗜️  Comprimir PDF (reduzir tamanho)",
        "ferramentas_extrair": "✂️  Extrair páginas específicas",
        "ferramentas_proteger": "🔒  Proteger com senha",
        "ferramentas_marca": "💧  Adicionar marca d'água",
        "ferramentas_ocr": "🔍  OCR (tornar PDF pesquisável)",
        "ferramentas_voltar": "↩️  Voltar",

        # Formato de destino (PDF -> outro)
        "formato_titulo": "Converter o PDF para qual formato?",
        "formato_png": "🖼️  PNG",
        "formato_jpeg": "🖼️  JPEG",
        "formato_docx": "📝  DOCX (Word)",
        "formato_txt": "📃  TXT (texto puro)",

        # Seleção de pasta/arquivo
        "pasta_pergunta": "Em qual pasta está o arquivo?",
        "pasta_ultimo": "🕘  Último local usado",
        "pasta_manual": "⌨️  Digitar caminho manualmente",
        "pasta_lote_manual_prompt": "Caminho completo da pasta:",
        "arquivo_manual_prompt": "Caminho completo do arquivo:",
        "arquivo_como_selecionar": "Como quer selecionar o arquivo?",
        "arquivo_usar_recente": "📌  Usar o mais recente ({nome})",
        "arquivo_digitar_nome": "⌨️  Escolher/digitar o nome",
        "arquivo_selecionar_tab": "Selecione o arquivo (Tab autocompleta):",

        # Saída
        "saida_pergunta_custom": "Deseja escolher outro nome/local pro PDF?",
        "saida_caminho": "Caminho de saída do PDF:",

        # Histórico
        "historico_titulo": "Histórico de Conversões",
        "historico_col_data": "Data/Hora",
        "historico_col_arquivo": "Arquivo",
        "historico_col_resultado": "Resultado",
        "historico_vazio": "Nenhuma conversão registrada ainda.",

        # Ferramentas - prompts específicos
        "unir_arquivo_n": "Arquivo #{n} (Tab autocompleta):",
        "unir_adicionado": "Adicionado: {caminho}",
        "unir_outro": "Adicionar outro PDF?",
        "compressao_titulo": "Qual nível de compressão?",
        "compressao_leve": "🔹  Leve (melhor qualidade, prepress)",
        "compressao_medio": "🔸  Médio (impressora, printer)",
        "compressao_forte": "🔻  Forte (ebook, bom equilíbrio)",
        "compressao_maxima": "⚡  Máxima (menor arquivo, tela/screen)",
        "paginas_pergunta": "Quais páginas? (ex: 1-3,5,8-10)",
        "senha_pergunta": "Digite a senha para proteger o PDF:",
        "marca_texto_pergunta": "Texto da marca d'água:",
        "ocr_idioma_pergunta": "Idioma do texto no PDF (pro OCR)?",
        "ocr_portugues": "🇧🇷  Português",
        "ocr_ingles": "🇺🇸  Inglês",

        # Escolha de idioma
        "idioma_pergunta": "Escolha o idioma / Choose the language:",
        "idioma_pt": "🇧🇷  Português",
        "idioma_en": "🇺🇸  English",
        "idioma_alterado": "Idioma alterado para Português.",

        # Spinners
        "status_convertendo": "Convertendo...",
        "status_unindo": "Unindo PDFs...",
        "status_comprimindo": "Comprimindo...",
        "status_extraindo": "Extraindo páginas...",
        "status_protegendo": "Protegendo PDF...",
        "status_marca": "Adicionando marca d'água...",
        "status_ocr": "Rodando OCR (pode demorar)...",
        "status_lote": "Convertendo",

        # Mensagens gerais (main.py)
        "msg_saida_padrao": "Saída padrão: {caminho}",
        "msg_nenhum_caminho": "Nenhum caminho informado.",
        "msg_arquivo_nao_existe": "Arquivo não existe.",
        "msg_arquivo_vazio": "Arquivo está vazio.",
        "msg_extensao_detectada": "Extensão detectada: {ext}",
        "msg_formato_incompativel": "Formato não compatível.",
        "msg_pasta_destino_inexistente": "A pasta de destino não existe.",
        "msg_pdf_sucesso": "PDF criado com sucesso: {caminho}",
        "msg_arquivo_sucesso": "Arquivo criado com sucesso: {caminho}",
        "msg_sem_permissao": "Sem permissão pra ler ou escrever o arquivo.",
        "msg_ferramenta_ausente_pandoc": "Alguma ferramenta necessária (ex: pandoc) não foi encontrada.",
        "msg_erro_converter": "Erro ao converter: {erro}",
        "msg_nao_e_pdf": "Esse arquivo não é um PDF.",
        "msg_nenhum_formato": "Nenhum formato de destino escolhido.",
        "msg_ferramenta_ausente_poppler": "Alguma ferramenta necessária não foi encontrada (instale com: pkg install poppler).",
        "msg_lib_ausente_docx": "Falta uma biblioteca pra essa conversão (instale com: pip install python-docx).",
        "msg_nenhum_arquivo_compativel": "Nenhum arquivo compatível encontrado nessa pasta.",
        "msg_lote_encontrados": "{n} arquivo(s) encontrado(s). Convertendo...",
        "msg_lote_sucesso": "{n} convertido(s) com sucesso.",
        "msg_lote_falhas": "{n} falharam (veja o histórico pra detalhes).",
        "msg_unir_minimo": "Selecione pelo menos 2 PDFs pra unir.",
        "msg_unir_sucesso": "PDFs unidos em: {caminho}",
        "msg_erro_unir": "Erro ao unir: {erro}",
        "msg_pdf_invalido": "Selecione um PDF válido.",
        "msg_comprimir_sucesso": "PDF comprimido: {caminho} ({reducao:.0f}% menor)",
        "msg_ghostscript_ausente": "Ghostscript não encontrado (instale com: pkg install ghostscript).",
        "msg_erro_comprimir": "Erro ao comprimir: {erro}",
        "msg_paginas_nao_informadas": "Nenhum intervalo de páginas informado.",
        "msg_extrair_sucesso": "Páginas extraídas em: {caminho}",
        "msg_erro_extrair": "Erro ao extrair páginas: {erro}",
        "msg_senha_nao_informada": "Nenhuma senha informada.",
        "msg_proteger_sucesso": "PDF protegido criado: {caminho}",
        "msg_erro_proteger": "Erro ao proteger: {erro}",
        "msg_marca_texto_nao_informado": "Nenhum texto informado.",
        "msg_marca_sucesso": "Marca d'água aplicada: {caminho}",
        "msg_erro_marca": "Erro ao aplicar marca d'água: {erro}",
        "msg_ocr_sucesso": "PDF pesquisável criado: {caminho}",
        "msg_tesseract_ausente": "Tesseract ou poppler não encontrados (instale com: pkg install poppler tesseract tesseract-data-por).",
        "msg_erro_ocr": "Erro no OCR: {erro}",
        "msg_pressione_continuar": "Pressione qualquer tecla para continuar...",
        "msg_pressione_voltar": "Pressione qualquer tecla para voltar ao menu...",
        "msg_ate_mais": "Até mais! 👋",

        # Diagnóstico de dependências (checagem inicial)
        "diag_pergunta_inicial": "Deseja verificar se todas as dependências estão instaladas?",
        "diag_titulo": "Diagnóstico de dependências",
        "diag_col_nome": "Componente",
        "diag_col_tipo": "Tipo",
        "diag_col_status": "Status",
        "diag_tipo_sistema": "Sistema (pkg)",
        "diag_tipo_python": "Python (pip)",
        "diag_tipo_dado": "Dado (idioma)",
        "diag_ok": "✔ instalado",
        "diag_faltando": "✘ faltando",
        "diag_tudo_ok": "Tudo certo! Todas as dependências estão instaladas.",
        "diag_faltam_n": "{n} dependência(s) faltando.",
        "diag_perguntar_instalar": "Deseja instalar automaticamente o que está faltando?",
        "diag_instalando": "Instalando {nome}...",
        "diag_instalado_sucesso": "{nome} instalado com sucesso.",
        "diag_instalado_falha": "Falha ao instalar {nome}: {erro}",
        "diag_resumo_final": "Instalação concluída: {sucesso} de {total} com sucesso.",
        "diag_pular_aviso": "Ok, seguindo sem instalar. Algumas funções podem falhar até você instalar manualmente.",

        # Breadcrumb (trilha de navegação)
        "trilha_menu": "Menu",
        "trilha_converter": "Converter para PDF",
        "trilha_de_pdf": "Converter PDF",
        "trilha_lote": "Lote",
        "trilha_ferramentas": "Ferramentas",
        "trilha_unir": "Unir",
        "trilha_comprimir": "Comprimir",
        "trilha_extrair": "Extrair páginas",
        "trilha_proteger": "Proteger",
        "trilha_marca": "Marca d'água",
        "trilha_ocr": "OCR",
        "trilha_historico": "Histórico",
        "trilha_idioma": "Idioma",

        # Preview do arquivo
        "preview_titulo": "Arquivo selecionado",
        "preview_nome": "Nome",
        "preview_tamanho": "Tamanho",
        "preview_paginas": "Páginas",
        "preview_tipo": "Tipo",

        # Resumo/confirmação antes de executar
        "resumo_titulo": "Confirme a operação",
        "resumo_confirmar": "Confirma?",
        "resumo_arquivo": "Arquivo",
        "resumo_arquivos": "Arquivos",
        "resumo_formato_saida": "Formato de saída",
        "resumo_destino": "Destino",
        "resumo_nivel": "Nível",
        "resumo_paginas": "Páginas",
        "resumo_idioma_ocr": "Idioma OCR",
        "resumo_texto_marca": "Texto",
        "resumo_pasta": "Pasta",
        "resumo_qtd_arquivos": "Arquivos encontrados",
        "operacao_cancelada": "Operação cancelada.",

        # Tela de despedida
        "despedida_titulo": "Até a próxima!",
        "despedida_sucessos": "✔ {n} operação(ões) concluída(s) com sucesso",
        "despedida_falhas": "✘ {n} operação(ões) com erro",
        "despedida_nenhuma": "Nenhuma operação realizada nessa sessão.",

        # ------------- Menu principal reorganizado em categorias -------------
        "menu_cat_converter": "📄  Converter",
        "menu_cat_ferramentas": "🛠️  Ferramentas de PDF",
        "menu_cat_extras": "🎧  Extras (EPUB, Áudio, Colagem)",
        "menu_cat_presets": "⭐  Presets",
        "menu_cat_estatisticas": "📊  Estatísticas",
        "menu_desfazer": "↩️  Desfazer última ação",
        "menu_voltar": "↩️  Voltar",

        # Submenu Converter
        "converter_sub_titulo": "O que converter?",
        "converter_sub_arquivo": "📄  Arquivo para PDF",
        "converter_sub_de_pdf": "🔁  PDF para outro formato",
        "converter_sub_lote": "📦  Em lote (pasta inteira)",
        "converter_sub_grade": "🖼️  Colagem de fotos em grade",

        # Submenu Ferramentas (itens novos, os antigos já existem acima)
        "ferramentas_dividir": "✂️  Dividir PDF",
        "ferramentas_rotacionar": "🔄  Rotacionar páginas",
        "ferramentas_numerar": "🔢  Numerar páginas",
        "ferramentas_metadados": "🏷️  Editar metadados",
        "ferramentas_remover_senha": "🔓  Remover senha",
        "ferramentas_censurar": "⬛  Censurar/redigir",
        "ferramentas_carimbo": "🖋️  Adicionar carimbo/assinatura",
        "ferramentas_comparar": "🔬  Comparar dois PDFs",
        "ferramentas_verificar": "🩺  Verificar integridade",

        # Submenu Extras
        "extras_titulo": "O que você quer fazer?",
        "extras_epub": "📚  PDF → EPUB",
        "extras_epub_para_pdf": "📚  EPUB → PDF",
        "extras_audio": "🔊  PDF → Áudio",

        # Presets
        "presets_titulo": "Presets",
        "presets_criar": "➕  Criar novo preset",
        "presets_usar": "▶️  Usar um preset",
        "presets_apagar": "🗑️  Apagar preset",
        "presets_nome_pergunta": "Nome do preset:",
        "presets_nenhum": "Nenhum preset salvo ainda.",
        "presets_criado": "Preset '{nome}' salvo!",
        "presets_apagado": "Preset '{nome}' apagado.",
        "presets_escolher": "Qual preset?",
        "presets_usar_pergunta": "Quer usar um preset salvo?",
        "presets_marca_texto": "Texto de marca d'água do preset (opcional):",
        "presets_autor": "Autor padrão do preset (opcional):",
        "presets_titulo_doc": "Título padrão do preset (opcional):",

        # Estatísticas
        "stats_titulo": "Estatísticas de uso",
        "stats_total": "Total de operações: {n}",
        "stats_sucesso": "✔ Sucessos: {n}",
        "stats_falhas": "✘ Falhas: {n}",
        "stats_por_tipo": "Por tipo de ação",
        "stats_vazio": "Ainda não há dados suficientes.",

        # Desfazer última ação
        "desfazer_nada": "Nada pra desfazer nessa sessão.",
        "desfazer_confirmar": "Apagar o arquivo gerado por último ({arquivo})?",
        "desfazer_sucesso": "Arquivo removido: {arquivo}",
        "desfazer_erro": "Não foi possível remover: {erro}",

        # Metadados
        "metadados_titulo_pergunta": "Título do documento (Enter p/ pular):",
        "metadados_autor_pergunta": "Autor (Enter p/ pular):",
        "metadados_assunto_pergunta": "Assunto (Enter p/ pular):",
        "msg_metadados_sucesso": "Metadados atualizados: {caminho}",
        "msg_erro_metadados": "Erro ao editar metadados: {erro}",

        # Rotacionar
        "rotacionar_graus_pergunta": "Girar quantos graus?",
        "rotacionar_90": "↻  90° (horário)",
        "rotacionar_180": "🔃  180°",
        "rotacionar_270": "↺  90° (anti-horário)",
        "rotacionar_paginas_pergunta": "Quais páginas? (Enter = todas)",
        "msg_rotacionar_sucesso": "Páginas rotacionadas: {caminho}",
        "msg_erro_rotacionar": "Erro ao rotacionar: {erro}",

        # Dividir
        "dividir_modo_pergunta": "Como dividir o PDF?",
        "dividir_por_pagina": "📄  Uma página por arquivo",
        "dividir_por_intervalo": "🔢  A cada N páginas",
        "dividir_n_pergunta": "A cada quantas páginas?",
        "msg_dividir_sucesso": "{n} arquivo(s) gerado(s) em: {pasta}",
        "msg_erro_dividir": "Erro ao dividir: {erro}",

        # Numerar páginas
        "numerar_formato_pergunta": "Formato do texto (use {atual} e {total}):",
        "msg_numerar_sucesso": "Páginas numeradas: {caminho}",
        "msg_erro_numerar": "Erro ao numerar páginas: {erro}",

        # Remover senha
        "remover_senha_pergunta": "Senha atual do PDF:",
        "msg_remover_senha_sucesso": "Senha removida: {caminho}",
        "msg_senha_incorreta": "Senha incorreta.",
        "msg_erro_remover_senha": "Erro ao remover senha: {erro}",

        # Censurar/redigir
        "censurar_regiao_pergunta": "Qual região censurar?",
        "censurar_topo": "⬆️  Topo da página",
        "censurar_meio": "➡️  Meio da página",
        "censurar_rodape": "⬇️  Rodapé da página",
        "msg_censurar_sucesso": "Área censurada em: {caminho}",
        "msg_erro_censurar": "Erro ao censurar: {erro}",

        # Comparar PDFs
        "comparar_segundo_arquivo": "Selecione o segundo PDF pra comparar:",
        "comparar_identico": "Os dois PDFs têm o mesmo texto.",
        "comparar_diferente": "Diferenças encontradas: +{add} linha(s) / -{rem} linha(s)",
        "msg_erro_comparar": "Erro ao comparar: {erro}",

        # Carimbo/assinatura
        "carimbo_imagem_pergunta": "Selecione a imagem do carimbo/assinatura:",
        "carimbo_posicao_pergunta": "Onde posicionar?",
        "carimbo_inferior_direito": "↘️  Inferior direito",
        "carimbo_inferior_esquerdo": "↙️  Inferior esquerdo",
        "carimbo_superior_direito": "↗️  Superior direito",
        "carimbo_superior_esquerdo": "↖️  Superior esquerdo",
        "msg_carimbo_sucesso": "Carimbo aplicado: {caminho}",
        "msg_erro_carimbo": "Erro ao aplicar carimbo: {erro}",

        # Verificar integridade
        "msg_verificar_ok": "✔ {arquivo}: {mensagem}",
        "msg_verificar_falha": "✘ {arquivo}: {mensagem}",

        # PDF -> EPUB / Áudio
        "epub_titulo_pergunta": "Título do e-book (opcional):",
        "epub_autor_pergunta": "Autor (opcional):",
        "msg_epub_sucesso": "EPUB criado: {caminho}",
        "msg_erro_epub": "Erro ao gerar EPUB: {erro}",
        "msg_epub_para_pdf_sucesso": "PDF criado a partir do EPUB: {caminho}",
        "msg_erro_epub_para_pdf": "Erro ao converter EPUB para PDF: {erro}",
        "audio_idioma_pergunta": "Idioma do texto (pra voz)?",
        "msg_audio_sucesso": "Áudio criado: {caminho}",
        "msg_erro_audio": "Erro ao gerar áudio: {erro}",
        "msg_espeak_ausente": "espeak não encontrado (instale com: pkg install espeak).",

        # Colagem de fotos em grade
        "grade_titulo": "Quantas fotos por página?",
        "grade_2x2": "▦  2x2 (4 fotos por página)",
        "grade_3x3": "▦  3x3 (9 fotos por página)",
        "grade_2x1": "▦  2x1 (2 fotos por página)",
        "grade_selecionar_fotos": "Selecione as fotos (uma por vez)",
        "msg_grade_sucesso": "PDF com colagem criado: {caminho}",
        "msg_erro_grade": "Erro ao montar colagem: {erro}",

        # Sumário automático (toc)
        "toc_pergunta": "Gerar sumário automático (baseado nos títulos)?",

        # Breadcrumb - itens novos
        "trilha_dividir": "Dividir",
        "trilha_rotacionar": "Rotacionar",
        "trilha_numerar": "Numerar páginas",
        "trilha_metadados": "Metadados",
        "trilha_remover_senha": "Remover senha",
        "trilha_censurar": "Censurar",
        "trilha_carimbo": "Carimbo/assinatura",
        "trilha_comparar": "Comparar PDFs",
        "trilha_verificar": "Verificar integridade",
        "trilha_extras": "Extras",
        "trilha_epub": "PDF → EPUB",
        "trilha_epub_para_pdf": "EPUB → PDF",
        "trilha_audio": "PDF → Áudio",
        "trilha_grade": "Colagem de fotos",
        "trilha_presets": "Presets",
        "trilha_estatisticas": "Estatísticas",
        "trilha_desfazer": "Desfazer",
    },

    "en": {
        # Banner
        "banner_tagline": "File converter • Termux Edition",
        "banner_stats": "📊 {total} conversion(s) done so far",

        # Main menu
        "menu_titulo": "What do you want to do?",
        "menu_converter": "📄  Convert file to PDF",
        "menu_de_pdf": "🔁  Convert PDF to another format",
        "menu_lote": "📦  Batch conversion (whole folder)",
        "menu_ferramentas": "🛠️  PDF tools",
        "menu_historico": "🕘  View history",
        "menu_idioma": "🌐  Language / Idioma",
        "menu_sair": "❌  Exit",

        # Tools submenu
        "ferramentas_titulo": "Which PDF tool?",
        "ferramentas_unir": "🧩  Merge several PDFs into one",
        "ferramentas_comprimir": "🗜️  Compress PDF (reduce size)",
        "ferramentas_extrair": "✂️  Extract specific pages",
        "ferramentas_proteger": "🔒  Protect with password",
        "ferramentas_marca": "💧  Add watermark",
        "ferramentas_ocr": "🔍  OCR (make PDF searchable)",
        "ferramentas_voltar": "↩️  Back",

        # Destination format (PDF -> other)
        "formato_titulo": "Convert the PDF to which format?",
        "formato_png": "🖼️  PNG",
        "formato_jpeg": "🖼️  JPEG",
        "formato_docx": "📝  DOCX (Word)",
        "formato_txt": "📃  TXT (plain text)",

        # Folder/file selection
        "pasta_pergunta": "Which folder is the file in?",
        "pasta_ultimo": "🕘  Last used location",
        "pasta_manual": "⌨️  Type the path manually",
        "pasta_lote_manual_prompt": "Full folder path:",
        "arquivo_manual_prompt": "Full file path:",
        "arquivo_como_selecionar": "How do you want to select the file?",
        "arquivo_usar_recente": "📌  Use the most recent ({nome})",
        "arquivo_digitar_nome": "⌨️  Choose/type the name",
        "arquivo_selecionar_tab": "Select the file (Tab autocompletes):",

        # Output
        "saida_pergunta_custom": "Want to choose another name/location for the PDF?",
        "saida_caminho": "PDF output path:",

        # History
        "historico_titulo": "Conversion History",
        "historico_col_data": "Date/Time",
        "historico_col_arquivo": "File",
        "historico_col_resultado": "Result",
        "historico_vazio": "No conversions recorded yet.",

        # Tool-specific prompts
        "unir_arquivo_n": "File #{n} (Tab autocompletes):",
        "unir_adicionado": "Added: {caminho}",
        "unir_outro": "Add another PDF?",
        "compressao_titulo": "Which compression level?",
        "compressao_leve": "🔹  Light (best quality, prepress)",
        "compressao_medio": "🔸  Medium (printer)",
        "compressao_forte": "🔻  Strong (ebook, good balance)",
        "compressao_maxima": "⚡  Maximum (smallest file, screen)",
        "paginas_pergunta": "Which pages? (e.g. 1-3,5,8-10)",
        "senha_pergunta": "Type the password to protect the PDF:",
        "marca_texto_pergunta": "Watermark text:",
        "ocr_idioma_pergunta": "Language of the text in the PDF (for OCR)?",
        "ocr_portugues": "🇧🇷  Portuguese",
        "ocr_ingles": "🇺🇸  English",

        # Language choice
        "idioma_pergunta": "Escolha o idioma / Choose the language:",
        "idioma_pt": "🇧🇷  Português",
        "idioma_en": "🇺🇸  English",
        "idioma_alterado": "Language switched to English.",

        # Spinners
        "status_convertendo": "Converting...",
        "status_unindo": "Merging PDFs...",
        "status_comprimindo": "Compressing...",
        "status_extraindo": "Extracting pages...",
        "status_protegendo": "Protecting PDF...",
        "status_marca": "Adding watermark...",
        "status_ocr": "Running OCR (this may take a while)...",
        "status_lote": "Converting",

        # General messages (main.py)
        "msg_saida_padrao": "Default output: {caminho}",
        "msg_nenhum_caminho": "No path provided.",
        "msg_arquivo_nao_existe": "File doesn't exist.",
        "msg_arquivo_vazio": "File is empty.",
        "msg_extensao_detectada": "Detected extension: {ext}",
        "msg_formato_incompativel": "Unsupported format.",
        "msg_pasta_destino_inexistente": "Destination folder doesn't exist.",
        "msg_pdf_sucesso": "PDF created successfully: {caminho}",
        "msg_arquivo_sucesso": "File created successfully: {caminho}",
        "msg_sem_permissao": "No permission to read or write the file.",
        "msg_ferramenta_ausente_pandoc": "A required tool (e.g. pandoc) was not found.",
        "msg_erro_converter": "Error converting: {erro}",
        "msg_nao_e_pdf": "That file is not a PDF.",
        "msg_nenhum_formato": "No destination format chosen.",
        "msg_ferramenta_ausente_poppler": "A required tool was not found (install with: pkg install poppler).",
        "msg_lib_ausente_docx": "Missing a library for this conversion (install with: pip install python-docx).",
        "msg_nenhum_arquivo_compativel": "No compatible files found in that folder.",
        "msg_lote_encontrados": "{n} file(s) found. Converting...",
        "msg_lote_sucesso": "{n} converted successfully.",
        "msg_lote_falhas": "{n} failed (check the history for details).",
        "msg_unir_minimo": "Select at least 2 PDFs to merge.",
        "msg_unir_sucesso": "PDFs merged into: {caminho}",
        "msg_erro_unir": "Error merging: {erro}",
        "msg_pdf_invalido": "Select a valid PDF.",
        "msg_comprimir_sucesso": "PDF compressed: {caminho} ({reducao:.0f}% smaller)",
        "msg_ghostscript_ausente": "Ghostscript not found (install with: pkg install ghostscript).",
        "msg_erro_comprimir": "Error compressing: {erro}",
        "msg_paginas_nao_informadas": "No page range provided.",
        "msg_extrair_sucesso": "Pages extracted into: {caminho}",
        "msg_erro_extrair": "Error extracting pages: {erro}",
        "msg_senha_nao_informada": "No password provided.",
        "msg_proteger_sucesso": "Protected PDF created: {caminho}",
        "msg_erro_proteger": "Error protecting: {erro}",
        "msg_marca_texto_nao_informado": "No text provided.",
        "msg_marca_sucesso": "Watermark applied: {caminho}",
        "msg_erro_marca": "Error applying watermark: {erro}",
        "msg_ocr_sucesso": "Searchable PDF created: {caminho}",
        "msg_tesseract_ausente": "Tesseract or poppler not found (install with: pkg install poppler tesseract tesseract-data-por).",
        "msg_erro_ocr": "OCR error: {erro}",
        "msg_pressione_continuar": "Press any key to continue...",
        "msg_pressione_voltar": "Press any key to go back to the menu...",
        "msg_ate_mais": "See you later! 👋",

        # Dependency diagnostics (startup check)
        "diag_pergunta_inicial": "Do you want to check if all dependencies are installed?",
        "diag_titulo": "Dependency diagnostics",
        "diag_col_nome": "Component",
        "diag_col_tipo": "Type",
        "diag_col_status": "Status",
        "diag_tipo_sistema": "System (pkg)",
        "diag_tipo_python": "Python (pip)",
        "diag_tipo_dado": "Data (language)",
        "diag_ok": "✔ installed",
        "diag_faltando": "✘ missing",
        "diag_tudo_ok": "All good! Every dependency is installed.",
        "diag_faltam_n": "{n} dependencie(s) missing.",
        "diag_perguntar_instalar": "Do you want to automatically install what's missing?",
        "diag_instalando": "Installing {nome}...",
        "diag_instalado_sucesso": "{nome} installed successfully.",
        "diag_instalado_falha": "Failed to install {nome}: {erro}",
        "diag_resumo_final": "Installation finished: {sucesso} of {total} succeeded.",
        "diag_pular_aviso": "Ok, continuing without installing. Some features may fail until you install manually.",

        # Breadcrumb
        "trilha_menu": "Menu",
        "trilha_converter": "Convert to PDF",
        "trilha_de_pdf": "Convert PDF",
        "trilha_lote": "Batch",
        "trilha_ferramentas": "Tools",
        "trilha_unir": "Merge",
        "trilha_comprimir": "Compress",
        "trilha_extrair": "Extract pages",
        "trilha_proteger": "Protect",
        "trilha_marca": "Watermark",
        "trilha_ocr": "OCR",
        "trilha_historico": "History",
        "trilha_idioma": "Language",

        # File preview
        "preview_titulo": "Selected file",
        "preview_nome": "Name",
        "preview_tamanho": "Size",
        "preview_paginas": "Pages",
        "preview_tipo": "Type",

        # Summary/confirmation before running
        "resumo_titulo": "Confirm the operation",
        "resumo_confirmar": "Confirm?",
        "resumo_arquivo": "File",
        "resumo_arquivos": "Files",
        "resumo_formato_saida": "Output format",
        "resumo_destino": "Destination",
        "resumo_nivel": "Level",
        "resumo_paginas": "Pages",
        "resumo_idioma_ocr": "OCR language",
        "resumo_texto_marca": "Text",
        "resumo_pasta": "Folder",
        "resumo_qtd_arquivos": "Files found",
        "operacao_cancelada": "Operation cancelled.",

        # Goodbye screen
        "despedida_titulo": "See you next time!",
        "despedida_sucessos": "✔ {n} operation(s) completed successfully",
        "despedida_falhas": "✘ {n} operation(s) with errors",
        "despedida_nenhuma": "No operations were performed this session.",

        # ------------- Main menu reorganized into categories -------------
        "menu_cat_converter": "📄  Convert",
        "menu_cat_ferramentas": "🛠️  PDF tools",
        "menu_cat_extras": "🎧  Extras (EPUB, Audio, Collage)",
        "menu_cat_presets": "⭐  Presets",
        "menu_cat_estatisticas": "📊  Statistics",
        "menu_desfazer": "↩️  Undo last action",
        "menu_voltar": "↩️  Back",

        # Convert submenu
        "converter_sub_titulo": "What do you want to convert?",
        "converter_sub_arquivo": "📄  File to PDF",
        "converter_sub_de_pdf": "🔁  PDF to another format",
        "converter_sub_lote": "📦  Batch (whole folder)",
        "converter_sub_grade": "🖼️  Photo grid collage",

        # Tools submenu - new items
        "ferramentas_dividir": "✂️  Split PDF",
        "ferramentas_rotacionar": "🔄  Rotate pages",
        "ferramentas_numerar": "🔢  Number pages",
        "ferramentas_metadados": "🏷️  Edit metadata",
        "ferramentas_remover_senha": "🔓  Remove password",
        "ferramentas_censurar": "⬛  Redact/censor",
        "ferramentas_carimbo": "🖋️  Add stamp/signature",
        "ferramentas_comparar": "🔬  Compare two PDFs",
        "ferramentas_verificar": "🩺  Check integrity",

        # Extras submenu
        "extras_titulo": "What do you want to do?",
        "extras_epub": "📚  PDF → EPUB",
        "extras_epub_para_pdf": "📚  EPUB → PDF",
        "extras_audio": "🔊  PDF → Audio",

        # Presets
        "presets_titulo": "Presets",
        "presets_criar": "➕  Create new preset",
        "presets_usar": "▶️  Use a preset",
        "presets_apagar": "🗑️  Delete preset",
        "presets_nome_pergunta": "Preset name:",
        "presets_nenhum": "No presets saved yet.",
        "presets_criado": "Preset '{nome}' saved!",
        "presets_apagado": "Preset '{nome}' deleted.",
        "presets_escolher": "Which preset?",
        "presets_usar_pergunta": "Want to use a saved preset?",
        "presets_marca_texto": "Preset's watermark text (optional):",
        "presets_autor": "Preset's default author (optional):",
        "presets_titulo_doc": "Preset's default title (optional):",

        # Statistics
        "stats_titulo": "Usage statistics",
        "stats_total": "Total operations: {n}",
        "stats_sucesso": "✔ Successes: {n}",
        "stats_falhas": "✘ Failures: {n}",
        "stats_por_tipo": "By action type",
        "stats_vazio": "Not enough data yet.",

        # Undo last action
        "desfazer_nada": "Nothing to undo this session.",
        "desfazer_confirmar": "Delete the last generated file ({arquivo})?",
        "desfazer_sucesso": "File removed: {arquivo}",
        "desfazer_erro": "Couldn't remove it: {erro}",

        # Metadata
        "metadados_titulo_pergunta": "Document title (Enter to skip):",
        "metadados_autor_pergunta": "Author (Enter to skip):",
        "metadados_assunto_pergunta": "Subject (Enter to skip):",
        "msg_metadados_sucesso": "Metadata updated: {caminho}",
        "msg_erro_metadados": "Error editing metadata: {erro}",

        # Rotate
        "rotacionar_graus_pergunta": "Rotate by how many degrees?",
        "rotacionar_90": "↻  90° (clockwise)",
        "rotacionar_180": "🔃  180°",
        "rotacionar_270": "↺  90° (counter-clockwise)",
        "rotacionar_paginas_pergunta": "Which pages? (Enter = all)",
        "msg_rotacionar_sucesso": "Pages rotated: {caminho}",
        "msg_erro_rotacionar": "Error rotating: {erro}",

        # Split
        "dividir_modo_pergunta": "How to split the PDF?",
        "dividir_por_pagina": "📄  One page per file",
        "dividir_por_intervalo": "🔢  Every N pages",
        "dividir_n_pergunta": "Every how many pages?",
        "msg_dividir_sucesso": "{n} file(s) created in: {pasta}",
        "msg_erro_dividir": "Error splitting: {erro}",

        # Page numbering
        "numerar_formato_pergunta": "Text format (use {atual} and {total}):",
        "msg_numerar_sucesso": "Pages numbered: {caminho}",
        "msg_erro_numerar": "Error numbering pages: {erro}",

        # Remove password
        "remover_senha_pergunta": "Current PDF password:",
        "msg_remover_senha_sucesso": "Password removed: {caminho}",
        "msg_senha_incorreta": "Incorrect password.",
        "msg_erro_remover_senha": "Error removing password: {erro}",

        # Redact/censor
        "censurar_regiao_pergunta": "Which region to redact?",
        "censurar_topo": "⬆️  Top of page",
        "censurar_meio": "➡️  Middle of page",
        "censurar_rodape": "⬇️  Bottom of page",
        "msg_censurar_sucesso": "Area redacted in: {caminho}",
        "msg_erro_censurar": "Error redacting: {erro}",

        # Compare PDFs
        "comparar_segundo_arquivo": "Select the second PDF to compare:",
        "comparar_identico": "Both PDFs have the same text.",
        "comparar_diferente": "Differences found: +{add} line(s) / -{rem} line(s)",
        "msg_erro_comparar": "Error comparing: {erro}",

        # Stamp/signature
        "carimbo_imagem_pergunta": "Select the stamp/signature image:",
        "carimbo_posicao_pergunta": "Where to place it?",
        "carimbo_inferior_direito": "↘️  Bottom right",
        "carimbo_inferior_esquerdo": "↙️  Bottom left",
        "carimbo_superior_direito": "↗️  Top right",
        "carimbo_superior_esquerdo": "↖️  Top left",
        "msg_carimbo_sucesso": "Stamp applied: {caminho}",
        "msg_erro_carimbo": "Error applying stamp: {erro}",

        # Integrity check
        "msg_verificar_ok": "✔ {arquivo}: {mensagem}",
        "msg_verificar_falha": "✘ {arquivo}: {mensagem}",

        # PDF -> EPUB / Audio
        "epub_titulo_pergunta": "E-book title (optional):",
        "epub_autor_pergunta": "Author (optional):",
        "msg_epub_sucesso": "EPUB created: {caminho}",
        "msg_erro_epub": "Error creating EPUB: {erro}",
        "msg_epub_para_pdf_sucesso": "PDF created from EPUB: {caminho}",
        "msg_erro_epub_para_pdf": "Error converting EPUB to PDF: {erro}",
        "audio_idioma_pergunta": "Text language (for the voice)?",
        "msg_audio_sucesso": "Audio created: {caminho}",
        "msg_erro_audio": "Error creating audio: {erro}",
        "msg_espeak_ausente": "espeak not found (install with: pkg install espeak).",

        # Photo grid collage
        "grade_titulo": "How many photos per page?",
        "grade_2x2": "▦  2x2 (4 photos per page)",
        "grade_3x3": "▦  3x3 (9 photos per page)",
        "grade_2x1": "▦  2x1 (2 photos per page)",
        "grade_selecionar_fotos": "Select the photos (one at a time)",
        "msg_grade_sucesso": "Collage PDF created: {caminho}",
        "msg_erro_grade": "Error building collage: {erro}",

        # Automatic table of contents (toc)
        "toc_pergunta": "Generate automatic table of contents (based on headings)?",

        # Breadcrumb - new items
        "trilha_dividir": "Split",
        "trilha_rotacionar": "Rotate",
        "trilha_numerar": "Number pages",
        "trilha_metadados": "Metadata",
        "trilha_remover_senha": "Remove password",
        "trilha_censurar": "Redact",
        "trilha_carimbo": "Stamp/signature",
        "trilha_comparar": "Compare PDFs",
        "trilha_verificar": "Check integrity",
        "trilha_extras": "Extras",
        "trilha_epub": "PDF → EPUB",
        "trilha_epub_para_pdf": "EPUB → PDF",
        "trilha_audio": "PDF → Audio",
        "trilha_grade": "Photo collage",
        "trilha_presets": "Presets",
        "trilha_estatisticas": "Statistics",
        "trilha_desfazer": "Undo",
    },
}
