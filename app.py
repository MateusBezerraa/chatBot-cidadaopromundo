import chainlit as cl
import json
import unicodedata
from fuzzywuzzy import process, fuzz

# --- CONFIGURAÇÃO ---
# Ajustado para 70 para aceitar melhor frases naturais
THRESHOLD_CONFIANCA = 70  

def normalizar_texto(texto):
    """
    Remove acentos e deixa tudo minúsculo.
    Ex: "Horário" vira "horario"
    """
    if not texto:
        return ""
    # Normaliza para formulário NFD (separa letras de acentos)
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Filtra apenas caracteres que não são acentos e converte para minúsculo
    return "".join([c for c in texto_normalizado if unicodedata.category(c) != 'Mn']).lower()

def carregar_regras():
    try:
        with open('regras.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            # Normaliza as palavras-chave do banco assim que carrega
            for regra in dados:
                regra['palavras_chave'] = [normalizar_texto(p) for p in regra['palavras_chave']]
            return dados
    except Exception as e:
        print(f"Erro ao carregar: {e}")
        return []

base_de_conhecimento = carregar_regras()

def buscar_melhor_resposta(pergunta_usuario):
    # Normaliza a pergunta do usuário também
    pergunta_tratada = normalizar_texto(pergunta_usuario)
    
    todas_chaves = []
    mapa_chaves = {}

    for regra in base_de_conhecimento:
        for chave in regra['palavras_chave']:
            todas_chaves.append(chave)
            mapa_chaves[chave] = regra

    # Usa fuzz.partial_token_set_ratio que é mais permissivo com frases longas
    melhor_match, pontuacao = process.extractOne(
        pergunta_tratada, 
        todas_chaves, 
        scorer=fuzz.token_set_ratio
    )

    # Debug no terminal para você ajustar se precisar
    print(f"Entrada Original: '{pergunta_usuario}'")
    print(f"Entrada Tratada: '{pergunta_tratada}'")
    print(f"Match: '{melhor_match}' | Score: {pontuacao}")
    print("-" * 30)

    if pontuacao >= THRESHOLD_CONFIANCA:
        return mapa_chaves[melhor_match]['resposta']
    
    return None

@cl.on_chat_start
async def start():
    await cl.Message(content="👋 Olá! Sou o assistente da ONG.\nPergunte sobre **inscrições**, **aulas**, **certificados** ou **localização**.").send()

@cl.on_message
async def main(message: cl.Message):
    resposta = buscar_melhor_resposta(message.content)

    if resposta:
        await cl.Message(content=resposta).send()
    else:
        msg_fallback = (
            "Desculpe, não entendi. 😕\n"
            "Tente usar palavras-chave simples como: 'horários', 'preço', 'certificado' ou 'endereço'.\n\n"
            "Ou contate a secretaria: (11) 99999-9999"
        )
        await cl.Message(content=msg_fallback).send()