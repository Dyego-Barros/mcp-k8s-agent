from kubernetes import client, config

# Carrega kubeconfig
config.load_kube_config()

v1 = client.CoreV1Api()

apps_v1 = client.AppsV1Api()

# Função para listar pods em um namespace específico
async def listar_pods(namespace: str):
    try:
        pods = v1.list_namespaced_pod(namespace) 
        # Formata a saída como string
        
        #Verifica se tem pods rodando no namespace
        if pods.items == []:
            return f"Nenhum pod encontrado no namespace '{namespace}'."        
        pods_str = "\n".join([f"{pod.metadata.name}  ({pod.status.phase}) ({pod.metadata.namespace}) ({pod.spec.node_name})" for pod in pods.items])        
        return pods_str
    except client.exceptions.ApiException as e:
        return f"Erro ao listar pods no namespace '{namespace}': {e}"

#Função para listar deployments em um namespace específico
async def get_deployments(namespace: str):
    try:
        deployments = apps_v1.list_namespaced_deployment(namespace)
        # Formata a saída como string
        
        #Verifica se tem deployments no namespace
        if deployments.items == []:
            return f"Nenhum deployment encontrado no namespace '{namespace}'."
        
        deployments_str = "\n".join([f"{dep.metadata.name} {dep.metadata.namespace} Replicas: {dep.status.replicas} Ready: {dep.status.ready_replicas}" for dep in deployments.items])        
        return deployments_str
    except client.exceptions.ApiException as e:
        return f"Erro ao listar deployments no namespace '{namespace}': {e}"
    

async def get_services(namespace: str):
    try:
        services = v1.list_namespaced_service(namespace)

        # Verifica se há serviços no namespace
        if services.items == []:
            return f"Nenhum serviço encontrado no namespace '{namespace}'."
        # Formatar como string legível
        services_str = "\n".join(
            [f"{svc.metadata.name} {svc.metadata.namespace}  {svc.spec.type} {svc.spec.cluster_ip}" for svc in services.items]
        )
        
        return services_str
        
    except client.exceptions.ApiException as e:
        return f"Erro: Namespace '{namespace}' não encontrado. Detalhes: {e}"   
    


if __name__ == "__main__":
    import asyncio
    namespace = "metallb-system"  # Exemplo de namespace
    print("Pods:")
    print(asyncio.run(listar_pods(namespace)))
    print("\nDeployments:")
    print(asyncio.run(get_deployments(namespace)))
    print("\nServices:")
    print(asyncio.run(get_services(namespace)))