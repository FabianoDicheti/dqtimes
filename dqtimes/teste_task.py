from tasks import previsao_task

resultado = previsao_task.delay("Série1", "RefA", 5)
print("Aguardando resultado...")
resposta = resultado.get(timeout=30)
print(resposta)
