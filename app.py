import chainlit as cl
import json
import unicodedata
import os
from datetime import datetime
from fuzzywuzzy import process, fuzz

# --- CONFIGURAÇÃO ---
THRESHOLD_CONFIANCA = 70
ARQUIVO_HISTORICO = "historico.json"

def normalizar_texto(texto):
    if not texto: return ""
    texto_normalizado = unicodedata.normalize('NFD', texto)
    return "".join([c for c in texto_normalizado if unicodedata.category(c) != 'Mn']).lower()

def carregar_regras():
    try:
        with open('regras.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            for regra in dados:
                regra['palavras_chave'] = [normalizar_texto(p) for p in regra['palavras_chave']]
            return dados
    except Exception:
        return []

base_de_conhecimento = carregar_regras()

# --- NOVA FUNÇÃO DE LOG ---
def salvar_log(pergunta, resposta, intencao_detectada, pontuacao):
    """Salva a interação no arquivo JSON para o Dashboard ler depois."""
    novo_registro = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pergunta_usuario": pergunta,
        "resposta_bot": resposta,
        "intencao": intencao_detectada, # Ex: 'horarios', 'custo' ou 'nao_entendeu'
        "confianca": pontuacao
    }

    # Lê o arquivo existente ou cria uma lista vazia
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, 'r', encoding='utf-8') as f:
            try:
                historico = json.load(f)
            except:
                historico = []
    else:
        historico = []

    historico.append(novo_registro)

    # Salva de volta
    with open(ARQUIVO_HISTORICO, 'w', encoding='utf-8') as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

def buscar_melhor_resposta(pergunta_usuario):
    pergunta_tratada = normalizar_texto(pergunta_usuario)
    todas_chaves = []
    mapa_chaves = {}

    for regra in base_de_conhecimento:
        for chave in regra['palavras_chave']:
            todas_chaves.append(chave)
            mapa_chaves[chave] = regra

    melhor_match, pontuacao = process.extractOne(pergunta_tratada, todas_chaves, scorer=fuzz.token_set_ratio)

    if pontuacao >= THRESHOLD_CONFIANCA:
        regra = mapa_chaves[melhor_match]
        # Retorna a resposta E o ID da intenção (ex: 'horarios')
        return regra['resposta'], regra['id'], pontuacao
    
    return None, "nao_entendeu", pontuacao

@cl.on_chat_start
async def start():
    await cl.Message(content="👋 Olá! Sou o assistente da ONG.").send()

@cl.on_message
async def main(message: cl.Message):
    resposta_texto, intencao_id, score = buscar_melhor_resposta(message.content)

    if resposta_texto:
        msg_final = resposta_texto
    else:
        msg_final = "Desculpe, não entendi. Tente palavras mais simples ou contate a secretaria."
    
    # --- AQUI SALVAMOS O LOG ---
    salvar_log(message.content, msg_final, intencao_id, score)

    await cl.Message(content=msg_final).send()