from kubernetes import client, config

# Carrega kubeconfig
config.load_kube_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

# Função para listar pods em um namespace específico
async def listar_pods(namespace: str):
    pods = v1.list_namespaced_pod(namespace)
    
    # Formata a saída como string
    pods_str = "\n".join([f"{pod.metadata.name} ({pod.status.phase})" for pod in pods.items])
    
    return pods_str

#Função para listar deployments em um namespace específico
async def get_deployments(namespace: str):
    deployments = apps_v1.list_namespaced_deployment(namespace)
    
    # Formatar como string legível
    deployments_str = "\n".join(
        [f"{dep.metadata.name} (replicas: {dep.status.replicas})" for dep in deployments.items]
    )
    
    return deployments_str