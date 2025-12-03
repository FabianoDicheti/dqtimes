

import uuid, random
from dqtimes.endpoint_historico_dqtimes.services.history_service import registrar_historico
from dqtimes.endpoint_historico_dqtimes.models import TaskHistory
from dqtimes.endpoint_historico_dqtimes.database import Base, engine, SessionLocal

# Inicializa o banco
print("Criando tabelas no banco...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas!")

db = SessionLocal()
tasks = ["naive_bayes", "holt_winters", "moving_average"]
statuses = ["SUCCESS", "ERROR", "FAILED"]

def generate_details(task_name):
    if task_name == "naive_bayes":
        return {"probabilidade_subir": random.random(), "bins": [0,1,0,1,1]}
    elif task_name == "holt_winters":
        return {"projecao": [round(random.random()*10,2) for _ in range(10)], "periodos": [3,5,7]}
    elif task_name == "moving_average":
        return {"medias": [round(random.random()*10,2) for _ in range(10)], "periodos": [3,5,7]}
    return {}

print("Populando o banco com 20 registros...")
for i in range(1, 21):
    task = random.choice(tasks)
    status = random.choice(statuses)
    referencia = str(uuid.uuid4())
    details = generate_details(task)
    
    historia = registrar_historico(db, task, referencia, status, details)
    
    # Printando resumo de cada registro criado com todos os campos mesmo n preenchidos
    print(f"Registro {i}: ID={historia.id}, Task={historia.task}, Referencia={historia.referencia}, Status={historia.status}, Created_At={historia.created_at}, Finished_At={historia.finished_at}, Details={historia.details}")
    

db.close()
print("Banco populado com 20 registros simulando DQTimes.")
