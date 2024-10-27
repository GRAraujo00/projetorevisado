from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI()

# Habilitar CORS para permitir acesso via navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Configurar a API do Gemini
API_KEY = "AIzaSyCVkItx4781WnhJWFkIk6YFelhxMTLVWpk"
genai.configure(api_key=API_KEY)

# Lista de tipos de bolo possíveis
tipos_de_bolo = [
    "chocolate", "cenoura", "milho", "fubá", "laranja", "limao", "maracujá", "coco", 
    "baunilha", "morango", "abacaxi", "banana", "maçã", "canela", "nozes", "castanha", 
    "pistache", "amêndoas", "queijo", "creme", "brigadeiro", "cobertura de chocolate",
    "frutas vermelhas", "doce de leite", "marmore", "aipim", "mandioca", "pé de moleque", 
    "fofo", "pão de ló", "formigueiro","jilo","jiló"
]

@app.get("/receitas/{query}")
async def get_receita(query: str):
    # Verifica se a consulta contém a palavra "bolo"
    if "bolo" not in query.lower():
        raise HTTPException(status_code=400, detail="Somente receitas de bolo são aceitas.")
    
    # Extrai o tipo de bolo da consulta
    tipo_bolo = query.lower().replace("bolo de ", "").strip()
    
    # Verifica se o tipo de bolo está na lista de tipos de bolo
    if tipo_bolo not in tipos_de_bolo:
        raise HTTPException(status_code=400, detail=f"O tipo de bolo '{tipo_bolo}' não é reconhecido. Tente um dos seguintes: {', '.join(tipos_de_bolo)}.")
    
    try:
        # Utilizando o modelo do Gemini para gerar conteúdo
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"receita de {query}")
        
        # Dividindo a resposta em seções para melhor legibilidade
        receita = response.text
        
        # Processamento básico para organizar a receita
        # Separar seções "Ingredientes" e "Instruções" ou outras relevantes
        ingredientes = ""
        instrucoes = ""
        
        if "Ingredientes:" in receita and "Instruções:" in receita:
            partes = receita.split("Instruções:")
            ingredientes = partes[0].strip()
            instrucoes = "Instruções:" + partes[1].strip()
        else:
            # Caso não tenha as seções bem definidas, retornamos tudo junto
            ingredientes = receita
        
        # Retorna a receita organizada em seções distintas
        return {
            "ingredientes": ingredientes,
            "instrucoes": instrucoes
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao processar a solicitação.")
