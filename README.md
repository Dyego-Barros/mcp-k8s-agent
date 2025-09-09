# 🖥️ MCP Kubernetes Agent

Um **agente inteligente** que se conecta a um servidor MCP para consultar recursos de um cluster Kubernetes em linguagem natural. O agente utiliza **LangChain**, **Groq LLM**, e **REACT Agent**, permitindo que você faça consultas como “listar pods no namespace kube-system” e receba respostas formatadas automaticamente. Ainda precisa de evoluções que virão nos proximos commits

---

## 🌟 Funcionalidades

* Consulta recursos do Kubernetes em linguagem natural:

  * Listar Pods em um namespace.
  * Listar Deployments em um namespace.
* Respostas simplificadas e diretas em **português brasileiro**.
* Suporte a múltiplas ferramentas MCP.
* Saída legível para terminal ou integração em scripts.
* Streaming de respostas em tempo real usando Groq.
* Mas ferramentas e recursos podem ser disponibilizados atraves do MCP

---

## ⚙️ Tecnologias Utilizadas

* **Python 3.13**
* [Kubernetes Python Client](https://github.com/kubernetes-client/python)
* [LangChain MCP Adapters](https://github.com/hwchase17/langchain)
* [LangGraph](https://github.com/hwchase17/langgraph)
* [Groq LLM API](https://www.groq.com/)
* MCP Client (Stdio e Streamable HTTP)
* `dotenv` para variáveis de ambiente

---

## 📦 Estrutura do Projeto

```
Client/
├─ Client.py           # Script principal do agente
Server/
├─ Server.py           # Servidor FastMCP 
├─ K8s_Client.py.      # Funções para interação com Kubernetes

```

---

## 🛠️ Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/mcp-k8s-agent.git
cd mcp-k8s-agent/Client
```

2. Crie e ative o ambiente virtual:

```bash
python3 -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o arquivo `.env`:

```env
API_GROQ=your_groq_api_key
```

5. Garanta que você tenha acesso ao Kubernetes (via `kubeconfig`):

```bash
export KUBECONFIG=/caminho/para/seu/kubeconfig
```

---

## 🚀 Uso

Execute o agente:

```bash
python3 Client.py
```

Digite suas consultas em linguagem natural, por exemplo:

```
Digite sua consulta: :
listar pods namespace kube-system
```

Saída esperada:

```
calico-kube-controllers-85b459fb9c-hg827 (Running)
coredns-5d784884df-sdwz6 (Running)
...
```

Para sair:

```
sair
```

---

## 🔧 Personalização

* **Prompt do agente**: altere o texto em `Client.py` para ajustar instruções ou idioma.
* **Ferramentas MCP**: adicione ou remova ferramentas no carregamento em `load_mcp_tools(session)`.
* **Formatos de saída**: altere as funções `listar_pods` ou `get_deployments` para customizar a exibição.

---

## 📸 Screenshots (Exemplo de Saída)

```
🤖 Resposta do agente:
calico-kube-controllers-85b459fb9c-hg827 (Running)
coredns-5d784884df-sdwz6 (Running)
...
```

---

## 📝 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
