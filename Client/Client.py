import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroqf
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain.prompts import ChatPromptTemplate

# Carrega variáveis de ambiente
load_dotenv()

# Caminho absoluto para o servidor MCP
path = os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__))))


# Prompt do Agente

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um assistente conectado a um servidor MCP que consulta Kubernetes. "
     "Suas resposta sempre devem estar em português brasileiro."
     "Sua função é: interpretar o pedido do usuário em linguagem natural e "
     "transformá-lo em uma chamada de ferramenta MCP, extraindo ACTION, NAMESPACE e, se houver, FILTERS."
     "Sua resposta deve ser simples e direta, sem explicações adicionais."
    ),
    ("human", "{pergunta}")
])
# Configurações do LLM Groq
llm = ChatGroq(
    api_key=os.environ.get("API_GROQ"),
    model="llama-3.1-8b-instant",
    temperature=0.5,
    max_retries=3,
    streaming=True,
)

# Parâmetros do servidor MCP
url="http://127.0.0.1:8000/mcp"

async def run_agent(pergunta):
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            # Inicializa a sessão MCP
            await session.initialize()
            
            # Carrega ferramentas MCP
            tools = await load_mcp_tools(session)
            #Apenas debug
            #print(f"Ferramentas carregadas: {[tool.name for tool in tools]}")
            agent = create_react_agent(llm, tools)
            
            resposta = await agent.ainvoke({"messages": [{"role": "user", "content": pergunta}]})
            #Somente para debug do agente 
            for message in resposta["messages"]:
                 print(message.pretty_print())
            # Cria agente REACT usando Groq
            return resposta["messages"][-1].content
            
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
            print("\n🤖 Resposta do agente:\n", resposta)
    