import asyncio

class Planejador:
    def __init__(self, modelo):
        self.modelo= modelo
        
    async def Planejar(self, tools, pergunta):
        try:
            descricao_tools = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
            prompt = f""" 
            Voce é um planejador de tarefas para um agene MCP de kubernetes.
            O usuario fara pergunta em linguagem natural.
            Seu trabalho é:
            
            1. Identificar qual ferramenta (tool) deve ser usada.
            2. Identificar quais parâmetros devem ser passados para a ferramenta.
            3. Retornar a resposta no seguinte formato JSON:
            {{
                "tool": "nome_da_ferramenta",
                "params": {{"parametro1": "valor1", "parametro2": "valor2"}}        
            }}
            Sempre responda no formato JSON, sem explicações adicionais.
            Tools disponíveis:
            {descricao_tools}
            
            Pergunta do usuário: {pergunta}
            """
            resultado = await self.modelo.ainvoke([{"role": "user", "content": prompt}])
            return resultado.content
        except Exception as e:
            return f"Erro ao planejar: {e}"
    