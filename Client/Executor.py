import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.resources import load_mcp_resources
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_groq import ChatGroq
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from Planejador import Planejador
import json

# Carrega variáveis de ambiente
load_dotenv()
# Caminho absoluto para o servidor MCP
path = os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__))))
# Configurações do LLM Groq
llm = ChatGroq(
    api_key=os.environ.get("API_GROQ"),
    model="llama-3.1-8b-instant",
    temperature=0.5,
    max_retries=3,
    streaming=True,
)
#Instância do planejador
planejador = Planejador(modelo=llm)

# Parâmetros do servidor MCP
url="http://127.0.0.1:8000/mcp"

async def run_agent(pergunta):
    try:
        async with streamablehttp_client(url) as (read, write, _):
            async with ClientSession(read, write) as session:
                # Inicializa a sessão MCP
                await session.initialize()
                
                # Carrega ferramentas MCP
                tools = await load_mcp_tools(session)
                #Planejador
                output_planner = await planejador.Planejar(tools=tools, pergunta=pergunta)
                
                try:
                    planner_data = json.loads(output_planner)
                except Exception as e:
                    return f"Erro ao interpretar saída do planejador: {e}\nSaída bruta: {output_planner}"
                
                #Apenas debug
                agent = create_react_agent(model=llm, tools=tools)                
                #agente_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
                
                resposta = await agent.ainvoke({"messages":{"role":"user","content":f"Execute a ferramenta {planner_data ['tool']} com os seguintes parâmetros {planner_data['params']}"}} )
                
                return resposta
    except Exception as e:
        return f"Erro ao executar o agente: {e}"

async def formata_resposta(resposta_bruta):
    try:
        # Define o prompt corretamente
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "Você é um assistente especialista em Kubernetes. "
            "Você irá receber uma resposta em forma bruta de uma ferramenta de um servidor MCP. "            
            "Analise  {resposta} e formate de maneira legivel, clara e organizada para o usuário final. "
            "Retire mensagens de boas vindas, evite mensagens desnecessárias. "
            "Forneca uma concluso curta e objetiva. "
            "Sempre que possível, use formatações como tabela. OU outro tipo de formatacao que facilite a leitura. "
            "Use pipes `|` para separar colunas caso escolha usar tabelas."
            "Os pipes precisam ficar alinhados horizontalmente e verticalmente."
            "Alinhe as colunas com espaços iguais."
            "Alinhe as linhas da tabela com espaços iguais ao das colunas."
            "Sempre coloque os nomes das colunas em negrito."
            "Preencha espaços para que todas as colunas fiquem alinhadas verticalmente."            
            "Evite jargões técnicos e explique termos complexos de forma simples. "
            "Se a resposta indicar que não há recursos, informe isso de maneira amigável. "
            "Se a resposta indicar um erro, informe isso de maneira amigável. "
            "Se a resposta indicar que o namespace não existe, informe isso de maneira amigável. "
            "Se a resposta estiver vazia, informe que não há dados disponíveis. "            
            "Se a resposta não estiver relacionada a Kubernetes, informe que só pode responder perguntas relacionadas a Kubernetes."
            )
        
        ])

        # Formata o prompt passando a variável
        messages = prompt.format_prompt(resposta=str(resposta_bruta)).to_messages()

        # Chama o LLM
        resultado = await llm.ainvoke(messages)
        return resultado.content
    except Exception as e:
         # Formata o prompt passando a variável
        messages = prompt.format_prompt(resposta=str(e)).to_messages()

        # Chama o LLM
        resultado = await llm.ainvoke(messages)
        return resultado.content
        
    
def create_agent(pergunta):
    # Loop de interação com usuário    
    return asyncio.run(run_agent(pergunta=pergunta))
            

if __name__ == "__main__":
    while True:
        pergunta_usuario = input("Digite sua consulta: :\n")
        if pergunta_usuario.lower() in ["sair", "exit", "quit"]:
            print("Encerrando...")
            break

        if pergunta_usuario:            
            resposta = create_agent(pergunta=pergunta_usuario)
            # Executa o agente    
            
            resposta_formatada = asyncio.run(formata_resposta(resposta_bruta=resposta))        
            print("\n🤖 Resposta do agente:\n", resposta_formatada)
    