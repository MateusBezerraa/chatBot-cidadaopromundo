# Chatbot - Cidadão Pró-Mundo

> ⚠️ **AVISO: VERSÃO DRAFT / MVP**
>
> Este projeto é um protótipo funcional desenvolvido para validar a solução de atendimento automatizado da ONG. A arquitetura atual foca em simplicidade e execução local. **Muitas funcionalidades, tecnologias e estruturas de dados estão sujeitas a alterações drásticas em versões futuras visando produção e escalabilidade.**

## Objetivo do Projeto

Este projeto visa auxiliar uma ONG de ensino de inglês a otimizar o atendimento aos alunos e comunidade externa. O Chatbot atua como uma primeira camada de suporte, respondendo automaticamente a dúvidas frequentes (FAQ) para reduzir a sobrecarga da equipe da secretaria.

**Funcionalidades Atuais:**
* 🤖 **Chatbot Baseado em Regras:** Responde dúvidas sobre matrículas, horários, valores e certificados.
* 🧠 **Lógica Fuzzy:** Compreende variações de digitação e erros ortográficos leves.
* 📊 **Dashboard Analítico:** Painel administrativo para visualizar métricas de atendimento e perguntas mais frequentes.
* 🔄 **Transbordo Humano:** Encaminha o usuário para contato real caso não entenda a dúvida.

## Como Executar

Instale as dependencias

```
pip install -r requirements.txt
```

Para executar o chat utilize o seguinte comando:

```
chainlit run app.py -w
```

Para executar o dashboard utilize o comando:

```
streamlit run dashboard.py
```

## 🛠️ Stack Tecnológica

A solução foi construída priorizando **Python** e simplicidade de implementação:

* **Interface de Chat:** [Chainlit](https://docs.chainlit.io)
* **Dashboard:** [Streamlit](https://streamlit.io)
* **Processamento de Texto:** FuzzyWuzzy + Python-Levenshtein (Matching de String)
* **Persistência de Dados:** Arquivos JSON (Local Storage para o MVP)

## 📂 Estrutura do Projeto

```bash
bot-ong/
├── app.py              # Código principal do Chatbot (Chainlit)
├── dashboard.py        # Código do Painel Administrativo (Streamlit)
├── regras.json         # "Cérebro" do bot: Banco de perguntas e respostas
├── historico.json      # Log automático das conversas (Gerado automaticamente)
└── requirements.txt    # Dependências do projeto