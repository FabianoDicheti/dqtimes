E_30
# Grupo 1

# Projeto de Migração de Software: Rust → Biblioteca Python

## Objetivo
Contratar uma empresa especializada para **realizar a transição de um software atualmente em Rust para uma biblioteca em Python**. A ideia é manter todas as funcionalidades existentes, mas transformar o software em uma **ferramenta modular, reutilizável e fácil de conectar com outros projetos**.

---

## Contexto
- O software atual foi desenvolvido em **Rust**, uma linguagem rápida e segura, mas pouco acessível para nossa equipe fazer alterações ou adaptações.
- Queremos migrar para **Python**, criando uma **biblioteca** que possa ser facilmente utilizada em outros sistemas que usamos.
- A biblioteca deve **preservar todas as funcionalidades** do software original e ser simples de manter.

---

## Escopo do Projeto
1.  **Análise do Código Existente**
    -   Entender todas as funcionalidades atuais do software em Rust.
    -   Mapear quais funções se tornarão as ferramentas principais da nova biblioteca.

2.  **Planejamento da Migração**
    -   Definir as etapas e prioridades da transição para a biblioteca Python.
    -   Garantir que as funcionalidades mais importantes sejam testadas ao longo do processo.

3.  **Desenvolvimento da Biblioteca Python**
    -   Reescrever o programa em Python, criando uma biblioteca com funções claras e bem organizadas.
    -   Garantir que a biblioteca possa ser facilmente instalada e utilizada em outros projetos.

4.  **Testes e Validação**
    -   Validar se a biblioteca em Python funciona **tão bem ou melhor** que o programa original.
    -   Testar todas as funções para garantir que **não existam erros críticos**.

5.  **Documentação e Entrega**
    -   Entregar a biblioteca Python completa, com um manual claro de como usar suas funções.
    -   Fornecer instruções e exemplos práticos de como integrar a biblioteca em outros projetos.

---

## Requisitos Gerais
- Manter todas as funcionalidades do software atual.
- Garantir que a biblioteca seja **reutilizável e fácil de entender**.
- Fornecer suporte durante a migração e testes finais.
- Entregar uma documentação prática para nossa equipe.

---

## Resultados Esperados
- Uma biblioteca Python completa e funcional.
- Todas as funcionalidades preservadas.
- Uma ferramenta acessível e fácil de integrar com outros sistemas.
- Um manual claro com exemplos de uso da biblioteca.

---

## Critérios de Aceitação
- A biblioteca pode ser instalada de forma simples em um computador com Python.
- Todas as funcionalidades estão documentadas e funcionam conforme o esperado.
- Os exemplos de uso fornecidos no manual são práticos e funcionais.
- O resultado final entregue pela biblioteca é o mesmo que o programa original produzia.

---

## Padrões de Entrega
- O código-fonte final deve ser entregue de forma organizada.
- A biblioteca deve ser estruturada de um modo que facilite seu uso e futuras atualizações.
- A entrega deve incluir um guia de início rápido com instruções de instalação e exemplos de uso.

---

## Observações
- **Não temos conhecimento técnico em programação**, por isso precisamos de **orientação e sugestões da empresa contratada** durante todo o processo.
- A comunicação deve ser clara e objetiva, usando uma linguagem acessível para nossa equipe.

# Grupo 2

# Grupo 3

# Grupo 4
# Celery, Flower e Redis: Guia Completo

## O que é o Celery?
O **Celery** é um task queue (fila de tarefas) que permite rodar tarefas assíncronas e agendadas. Ele funciona em conjunto com um broker de mensagens (como RabbitMQ ou Redis) que distribui as tarefas para os workers (processos que executam o trabalho).

### Principais vantagens:
- Simplicidade e integração com Python/Django/FastAPI/Flask.
- Permite rodar tarefas em paralelo, escalando horizontalmente.
- Suporta agendamento de tarefas (como cron jobs).
- Muito usado e consolidado na comunidade (grande confiabilidade).

## O que é o Flower?
O **Flower** é uma ferramenta de monitoramento e gerenciamento em tempo real para o Celery.

### Com ele é possível:
- Visualizar o status dos workers (quantos estão ativos).
- Acompanhar as tarefas em tempo real (sucesso, falha, tempo de execução).
- Reexecutar ou revogar tarefas.
- Ter métricas úteis de performance.

Ou seja, o Flower dá visibilidade e controle, algo essencial para a gente evitar "tarefas fantasmas" e conseguir analisar gargalos.

## Por que não usar apenas alternativas?
Existem outras soluções no mercado (como RQ, Huey, Dramatiq), mas o Celery + Flower se destaca por:

- **Maturidade**: é a solução mais usada em produção no ecossistema Python.
- **Recursos completos**: suporta retries automáticos, task chaining (tarefas em sequência), groups (rodar várias em paralelo), crontab para agendamento.
- **Monitoramento robusto**: Flower entrega um painel pronto e confiável, enquanto em outras soluções teríamos que construir algo manualmente.
- **Escalabilidade**: usado em grandes empresas, comprovadamente suporta alto volume.

## O que é o Redis?
O **Redis** é um banco de dados em memória (ou seja, ele guarda tudo direto na RAM, não em disco).
Por isso, ele é extremamente rápido.

### Ele é muito usado como:
- Cache (guardar coisas que você acessa toda hora, tipo resultado de consultas no banco).
- Fila de mensagens (que é o que nos interessa com o Celery).
- Armazenamento temporário de dados que expiram (ex.: tokens de login com prazo de validade).

### Redis no Celery:
O Celery precisa de um broker (intermediário).
Esse broker é quem recebe a tarefa, guarda numa fila e entrega para um worker disponível executar.

#### Fluxo resumido com Redis:
1. Sua aplicação dispara uma tarefa → "manda um e-mail para fulano".
2. O Redis recebe essa tarefa e guarda na fila.
3. O worker Celery fica escutando o Redis.
4. Assim que vê uma nova tarefa, ele pega e executa.
5. Quando terminar, ele manda o resultado de volta para o Redis (que também serve como backend de resultados).

## Instalando:
Antes de mais nada, precisamos instalar o Celery e o Flower. Vamos usar o Redis como broker (o cara que vai segurar as tarefas até os workers executarem).

### Instala o Celery com suporte a Redis
```bash
pip install celery[redis]
```

### Instala o Flower
```bash
pip install flower
```

### Instala o Redis (se não tiver)
#### Linux (Ubuntu/Debian)
```bash
sudo apt install redis
```

#### Windows → usar WSL ou Docker
```bash
docker run -d -p 6379:6379 redis
```

Depois de rodar, garanta que o Redis está funcionando:

```bash
redis-cli ping
```

Deve retornar: `PONG`

## Criando a configuração do Celery:
Dentro do seu projeto (pode ser Flask, FastAPI, Django, ou até um script Python simples), crie um arquivo chamado `celery.py`.

### Exemplo (celery.py):
```python
from celery import Celery

# cria a instância do Celery
app = Celery(
    "meu_projeto",
    broker="redis://localhost:6379/0",  # quem segura as tarefas
    backend="redis://localhost:6379/0"  # onde salvar resultados
)

# algumas configs básicas
app.conf.update(
    task_serializer="json",  # formato das mensagens
    result_serializer="json",  # formato dos resultados
    accept_content=["json"],  # só aceita JSON
    timezone="America/Sao_Paulo",
    enable_utc=True,
)
```

## Criando a primeira tarefa:
Agora criamos um arquivo `tasks.py` onde ficam nossas tarefas.

```python
from .celery import app

@app.task
def soma(a, b):
    print(f"Somando {a} + {b}")
    return a + b

@app.task
def enviar_email(destinatario, mensagem):
    print(f"Enviando email para {destinatario}...")
    # simulação
    return f"Email enviado para {destinatario} com sucesso!"
```

## Rodando os workers:
Agora precisamos colocar os workers (os "trabalhadores") pra escutar a fila e executar as tarefas.

No terminal:
```bash
celery -A celery worker -l info
```

- `-A celery` → nome do arquivo (celery.py) sem extensão.
- `-l info` → nível de log.

Se tudo estiver certo, você verá algo como:

```
[tasks]
. tasks.soma
. tasks.enviar_email
```

Isso significa que o worker já conhece nossas tarefas.

## Executando Tarefas:
No Python (pode ser via shell interativo ou no código do sistema):

```python
from tasks import soma, enviar_email

# executa de forma assíncrona
resultado = soma.delay(5, 7)
print("Tarefa enviada!")

# recupera o resultado depois
print(resultado.get(timeout=10))  # deve imprimir 12

# outra tarefa
email = enviar_email.delay("teste@email.com", "Bem-vindo!")
print(email.get(timeout=10))
```

**Importante**: `.delay()` sempre retorna imediatamente, sem travar o programa. Isso é o que deixa o sistema rápido.

## Monitorando com Flower:
O Flower dá uma visão completa de tudo isso.

No terminal, rode:
```bash
celery -A celery flower
```

Por padrão ele abre em http://localhost:5555.

### O que você vai ver lá:
- Lista de workers ativos.
- Cada tarefa que entrou, com status: recebida, executando, sucesso, erro.
- Estatísticas de quantas tarefas rodaram.
- Possibilidade de revogar tarefas (cancelar) ou até reexecutar.

## Estrutura:
```
meu_projeto/
│
├── celery.py  # configuração do Celery
├── tasks.py   # tarefas criadas
├── app.py     # sua aplicação (Flask, FastAPI, Django, etc.)
```

## Fluxo resumido:
1. Instala Celery + Redis + Flower.
2. Configura o celery.py.
3. Cria suas tarefas no tasks.py.
4. Roda os workers (celery -A celery worker -l info).
5. Do código, chama as tarefas com .delay().
6. Monitora tudo com o Flower.

# Grupo 5

# Grupo 6

# Grupo 7

