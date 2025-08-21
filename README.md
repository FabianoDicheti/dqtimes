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


Uso do React no Docker Compose para o Frontend
Por que usar React?
A escolha do React foi baseada em sua flexibilidade, desempenho e ampla adoção no mercado.
Além disso, ele se adapta bem a arquiteturas modernas baseadas em microserviços e APIs REST, como o backend deste projeto (FastAPI + Rust).

Vantagens principais
Integração com APIs
Consome facilmente serviços REST ou GraphQL.
Suporte a bibliotecas como Axios, React Query e SWR.
Ecossistema maduro
Grande variedade de bibliotecas e frameworks de UI (Tailwind, Material UI, Chakra).
Suporte consolidado da comunidade e atualizações frequentes.
Flexibilidade arquitetural
Não impõe uma estrutura rígida, permitindo que a equipe defina o padrão de organização mais adequado.

Componentização
Código mais organizado e fácil de manter..
Reuso de componentes em diferentes telas.
Curva de aprendizado acessível
Baseado em JavaScript e JSX, o que facilita para quem já conhece JS/TS.
Documentação rica e comunidade ativa.
Por que usar Docker no frontend?
Padronização
Garante que a aplicação rode de forma idêntica em qualquer ambiente.

Facilidade de deploy
O frontend pode ser integrado ao backend no mesmo fluxo de containers.

Isolamento de dependências
Evita conflitos com outras aplicações instaladas na máquina.

Escalabilidade
Containers podem ser replicados para atender a mais usuários.

React dentro do Docker Compose
O React será utilizado para construir a interface web do sistema, permitindo que os usuários interajam de forma intuitiva com os microserviços.
No docker-compose, o React terá um contêiner dedicado, o que traz benefícios como:

Isolamento e portabilidade
A aplicação front-end roda em seu próprio ambiente, sem dependências externas do host.

Integração facilitada
Comunicação direta com o backend em FastAPI e Rust via rede interna do Docker.

Escalabilidade
O contêiner pode ser replicado conforme a demanda de acessos cresce.

Padronização do ambiente
Garante que todos no time usem a mesma versão de Node/React, evitando problemas de compatibilidade.

Resumo da escolha
O React se mostrou a melhor opção porque:

Integra facilmente com microserviços em FastAPI.
Oferece flexibilidade sem engessar a equipe.
Apresenta boa performance e tem uma das maiores comunidades do mercado.
É mais simples de aprender e manter do que alternativas como Angular.
Vamos usar React no front porque ele facilita criar uma interface interativa, dinâmica e desacoplada do back-end. Como o microserviço em FastAPI vai expor APIs, o React permite consumir essas APIs de forma eficiente, mantendo o front separado do back, o que garante escalabilidade, manutenção mais simples e melhor experiência do usuário.

# Grupo 3
# Docker

## O que é o Docker 

O Docker é uma plataforma de código aberto para desenvolvimento, envio e execução de aplicações em contêineres. Ele permite que desenvolvedores embalem aplicações e suas dependências em contêineres, garantindo que funcionem de forma consistente em diferentes ambientes. Basicamente, o Docker facilita a criação, implantação e gerenciamento de aplicações, promovendo a portabilidade e escalabilidade. 

## Instalação

Para a instalação do docker é importante antes a sua máquina ser de sistema operacional Linux, ou ser Windows com o WSL ([Segue um tutorial de como instalar o WSL em sua máquina](https://learn.microsoft.com/pt-br/windows/wsl/install)) para conseguir fazer ela.
Para instalar o docker, seguem dois tutorias da documentação oficial sobre
Ubuntu: https://docs.docker.com/engine/install/ubuntu/
Windows: https://docs.docker.com/desktop/setup/install/windows-install/

## Comandos Essenciais do Docker

### Informações do sistema

```bash
docker --version           # Mostra a versão do Docker
docker info                # Mostra informações detalhadas do sistema e containers
```

### Imagens

```bash
docker pull <imagem>       # Baixa uma imagem do Docker Hub (ex: docker pull nginx)
docker images              # Lista as imagens baixadas
docker rmi <imagem>        # Remove uma imagem
```

### Containers

```bash
docker run <imagem>                 # Cria e executa um container
docker run -it <imagem> bash        # Executa com terminal interativo
docker run -d -p 8080:80 <imagem>   # Executa em background, mapeando porta
docker ps                           # Lista containers ativos
docker ps -a                        # Lista todos containers (ativos e parados)
docker stop <id ou nome>            # Para um container
docker start <id ou nome>           # Inicia um container parado
docker restart <id ou nome>         # Reinicia um container
docker rm <id ou nome>              # Remove um container
docker logs <id ou nome>            # Mostra os logs do container
docker exec -it <id ou nome> bash   # Entra dentro do container
```

### Volumes e arquivos

```bash
docker volume ls                    # Lista volumes
docker volume rm <nome>             # Remove um volume
docker run -v /meu/diretorio:/app <imagem>   # Monta um volume local no container
```

### Redes

```bash
docker network ls                   # Lista redes
docker network create <nome>        # Cria uma rede
docker network rm <nome>            # Remove uma rede
```

### Limpeza

```bash
docker system prune -a              # Remove containers, imagens e redes não usados
docker volume prune                 # Remove volumes não usados
```

# Containerização

## O que é a **Containerização**?

A **containerização** é uma tecnologia que permite empacotar uma aplicação junto com todas as suas dependências (bibliotecas, configurações, variáveis de ambiente etc.) dentro de um **contêiner**.

Esse contêiner é leve, portátil e isolado, garantindo que a aplicação funcione sempre da mesma forma, não importa em qual ambiente esteja sendo executada (notebook do dev, servidor de testes ou nuvem em produção).

## Por que **containerizar** uma aplicação?

1. **Consistência entre ambientes**

   * “Funciona na minha máquina” deixa de ser problema, já que o contêiner é idêntico em qualquer lugar.

2. **Portabilidade**

   * Pode rodar no Windows, Linux, Mac ou em qualquer provedor de nuvem sem ajustes.

3. **Escalabilidade**

   * É fácil replicar contêineres para lidar com maior demanda (ex: subir várias instâncias do mesmo app em segundos).

4. **Isolamento**

   * Cada contêiner tem seu próprio ambiente, sem conflito de dependências entre aplicações diferentes.

5. **Eficiência**

   * Mais leves que máquinas virtuais: consomem menos recursos, iniciam rápido e permitem alta densidade de aplicações no mesmo servidor.

6. **Ciclo de entrega mais ágil**

   * Integra bem com CI/CD, permitindo testes, deploys e rollbacks de forma rápida e previsível.

# Imagem Docker

## O que é uma Imagem Docker?

Uma **imagem Docker** é um **modelo imutável** que define tudo o que um contêiner precisa para rodar: sistema operacional base, bibliotecas, dependências, variáveis de ambiente e o próprio código da aplicação. Ela funciona como uma **fotografia congelada** do ambiente, garantindo que o contêiner seja sempre executado da mesma forma, independente da máquina ou servidor.

## Como as imagens são criadas?

Existem duas formas principais de trabalhar com imagens Docker:

1. **Imagens oficiais/prontas (padrões):**

   * Disponíveis no [Docker Hub](https://hub.docker.com/), como `nginx`, `mysql`, `node`, `python` etc.
   * São mantidas por comunidades ou pelas próprias empresas e já vêm configuradas para uso imediato.
   * Exemplo: rodar `docker run nginx` já cria um contêiner com o Nginx pronto para uso.

2. **Imagens personalizadas (via Dockerfile):**

   * Criadas pelo desenvolvedor para atender às necessidades específicas da aplicação.
   * O **Dockerfile** é um script com instruções que define como a imagem será construída.
   * Exemplo: criar uma imagem baseada em `python:3.12`, copiar o código da aplicação, instalar dependências e expor a porta do serviço.

## Relação entre imagens e contêineres

* Imagem é o modelo estático, imutável.
* Contêiner é a instância em execução dessa imagem.
* A partir de uma mesma imagem, você pode subir vários contêineres idênticos.

Isso permite misturar imagens **padrões** (como um banco de dados MySQL) com imagens **customizadas** (como o backend da sua aplicação), criando ambientes completos, reproduzíveis e portáveis.

# Dockerfile

## O que é o Dockerfile?
O *Dockerfile* é um arquivo de configuração usado pelo Docker para automatizar a criação de imagens.  
Ele contém instruções passo a passo que definem:
- Qual sistema base utilizar (ex: Ubuntu, Alpine).
- Quais dependências instalar.
- Como copiar arquivos para dentro da imagem.
- Como configurar variáveis de ambiente.
- Qual comando deve ser executado quando o container iniciar.

## Por que usar o Dockerfile?
- *Automatização*: evita configurações manuais, tudo está documentado no arquivo.  
- *Reprodutibilidade*: garante que qualquer pessoa consiga criar a mesma imagem com o mesmo resultado.  
- *Padronização*: mantém consistência entre ambientes (desenvolvimento, testes e produção).  
- *Escalabilidade*: facilita a criação de múltiplos containers iguais.  
- *Portabilidade*: o mesmo Dockerfile pode ser usado em diferentes sistemas operacionais e servidores.  
- *Documentação viva*: o próprio arquivo serve como registro das dependências e configurações necessárias para a aplicação.

## Como usar Dockerfile

### Comandos Mais Importantes
- FROM: Define a imagem base. Exemplo: `FROM python:3.11-slim`
- RUN: Executa comandos no processo de build. Exemplo: `RUN apt-get update && apt-get install -y curl`
- COPY: Copia arquivos do host para dentro da imagem. Exemplo: `COPY requirements.txt /app/`
- WORKDIR: Define o diretório de trabalho dentro do container. Exemplo: `WORKDIR /app`
- CMD: Define o comando padrão ao rodar o container. Exemplo: `CMD ["python", "app.py"]`
- EXPOSE: Documenta a porta que o container vai usar. Exemplo: `EXPOSE 5000`
- ENV: Define variáveis de ambiente. Exemplo: `ENV APP_ENV=production`
- ENTRYPOINT: Define o comando principal que não deve ser substituído facilmente. Exemplo: `ENTRYPOINT ["python", "app.py"]`

### Outros Comandos Úteis
- ADD: Similar ao `COPY`, mas aceita arquivos `.tar.gz` e URLs. Exemplo: `ADD app.tar.gz /app/`
- ARG: Define variáveis de build (diferente de `ENV`). Exemplo: `ARG VERSION=1.0`
- VOLUME: Cria ponto de montagem para volumes. Exemplo: `VOLUME /data`
- USER: Define o usuário que executará os processos no container. Exemplo: `USER node`
- LABEL: Adiciona metadados à imagem (ex: autor, versão). Exemplo: `LABEL maintainer="thiago@exemplo.com"`
- HEALTHCHECK: Define um comando para verificar a saúde do container. Exemplo: `HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1`

### Fluxo Típico de um Dockerfile

```yaml
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

# Docker Compose

## O que é o **Docker Compose**

O **Docker Compose** é uma ferramenta que permite **definir e executar aplicações Docker multi-contêiner** de forma fácil.
Em vez de criar e gerenciar contêineres manualmente com vários comandos `docker run`, você cria um arquivo (`docker-compose.yml`) que descreve **todos os serviços, redes e volumes** necessários para sua aplicação.

Exemplo de casos comuns:

* Aplicação web + banco de dados
* Backend + frontend + cache
* Microserviços interdependentes

## Por que usar o **Docker Compose**

1. **Simplifica o gerenciamento**

   * Com um único arquivo YAML, você define toda a infraestrutura da aplicação.

2. **Reprodutibilidade**

   * Toda a equipe pode rodar a aplicação com os mesmos serviços e configurações, evitando problemas de “funciona na minha máquina”.

3. **Escalabilidade**

   * Permite subir múltiplas instâncias de um serviço com apenas um comando.

4. **Integração com CI/CD**

   * Facilita testes automatizados e deploy em múltiplos ambientes.

5. **Gerenciamento de dependências**

   * Define a ordem de inicialização dos serviços (`depends_on`) e redes/volumes compartilhados.


## Como usar o Docker Compose

### 1. Estrutura do `docker-compose.yml`

```yaml
version: "3.9"

services:
  frontend:
    image: nginx:latest
    container_name: frontend
    ports:
      - "8080:80"                    
    volumes:
      - ./frontend/html:/usr/share/nginx/html   
    networks:
      - frontend_network
    depends_on:
      - backend                        

  backend:
    build:
      context: ./backend              
      dockerfile: Dockerfile
    container_name: backend
    ports:
      - "5000:5000"
    environment:                       
      DATABASE_HOST: db
      DATABASE_USER: root
      DATABASE_PASSWORD: root123
      CACHE_HOST: redis
    volumes:
      - backend_data:/app/data       
    networks:
      - frontend_network
      - backend_network
    depends_on:
      - db
      - redis

  db:
    image: mysql:8
    container_name: db
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: appdb
    volumes:
      - db_data:/var/lib/mysql       
    networks:
      - backend_network

  redis:
    image: redis:7
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data              
    networks:
      - backend_network

volumes:
  db_data:
    driver: local
  backend_data:
    driver: local
  redis_data:
    driver: local

networks:
  frontend_network:
    driver: bridge
  backend_network:
    driver: bridge
```

### 2. Explicando cada parte

| Elemento                             | O que faz / Para que serve                                                                 |
| ------------------------------------ | ------------------------------------------------------------------------------------------ |
| `version`                            | Define a versão do Docker Compose file, garantindo compatibilidade com recursos do Docker. |
| `services`                           | Agrupa todos os serviços (contêineres) da aplicação.                                       |
| `frontend`, `backend`, `db`, `redis` | Nome dos serviços, referência para redes, volumes e comandos.                              |
| `image`                              | Define qual imagem Docker será usada para o serviço.                                       |
| `build`                              | Define diretório e Dockerfile para criar imagem customizada.                               |
| `container_name`                     | Nome do contêiner no Docker para facilitar identificação.                                  |
| `ports`                              | Mapeia portas do host para portas do contêiner.                                            |
| `volumes`                            | Monta volumes para persistência de dados ou bind mounts do host.                           |
| `environment`                        | Define variáveis de ambiente dentro do contêiner.                                          |
| `networks`                           | Define em quais redes o contêiner estará conectado.                                        |
| `depends_on`                         | Define a ordem de inicialização entre serviços.                                            |
| `volumes:`                           | Declara volumes nomeados usados pelos serviços.                                            |
| `networks:`                          | Declara redes customizadas e seus drivers.                                                 |
| `driver`                             | Define como o volume ou rede será gerenciado (ex.: `local`, `bridge`).                     |
| `ipam`                               | Configura sub-rede e gateway da rede Docker.                                               |
| `context`                            | Diretório onde está o Dockerfile para build de imagens customizadas.                       |
| `dockerfile`                         | Nome do Dockerfile a ser usado para criar a imagem.                                        |

* **frontend**: Serve arquivos HTML via Nginx. Conectado à rede `frontend_network` para falar com o backend.
* **backend**: Serviço customizado com Dockerfile. Conectado a `frontend_network` e `backend_network` para acessar frontend e banco/cache. Variáveis de ambiente configuram conexões.
* **db**: MySQL, conectado à `backend_network`. Volume `db_data` mantém os dados persistentes.
* **redis**: Cache Redis, também na `backend_network`. Volume `redis_data` opcional para persistência.

#### **Volumes**

* **db\_data**: Persistência do MySQL
* **backend\_data**: Persistência do backend
* **redis\_data**: Persistência do Redis

Podem ser nomeados ou bind mounts. Nomeados são gerenciados pelo Docker automaticamente.

#### **Networks**

* **frontend\_network** → Conecta frontend ao backend
* **backend\_network** → Conecta backend ao db/redis, isolando do host e do frontend
* **driver: bridge** é padrão e permite comunicação interna entre contêineres


### 3. Comandos Docker Compose

| Comando                                   | Descrição                                                     |
| ----------------------------------------- | ------------------------------------------------------------- |
| `docker-compose up`                       | Cria e inicia contêineres. Use `-d` para rodar em background. |
| `docker-compose down`                     | Para e remove contêineres, redes e volumes nomeados.          |
| `docker-compose stop`                     | Para contêineres sem removê-los.                              |
| `docker-compose start`                    | Inicia contêineres parados.                                   |
| `docker-compose restart`                  | Reinicia contêineres.                                         |
| `docker-compose build`                    | Constrói imagens a partir do Dockerfile do serviço.           |
| `docker-compose up --build`               | Rebuild + up em um único comando.                             |
| `docker-compose logs`                     | Mostra logs dos contêineres; `-f` segue em tempo real.        |
| `docker-compose ps`                       | Lista contêineres gerenciados pelo Compose.                   |
| `docker-compose exec <serviço> <comando>` | Executa comando dentro de contêiner em execução.              |
| `docker-compose run <serviço> <comando>`  | Executa comando em um novo contêiner temporário.              |
| `docker-compose pull`                     | Baixa imagens sem subir contêineres.                          |
| `docker-compose push`                     | Envia imagens para um registry.                               |
| `docker-compose up --scale <serviço>=<n>` | Sobe múltiplas instâncias do mesmo serviço.                   |

### 4. Boas práticas

1. **Use volumes para persistência** (banco, backend, logs)
2. **Use redes para isolar serviços** e limitar exposição
3. **Use depends\_on** para definir a ordem de inicialização
4. **Separe arquivos de configuração por ambiente** (ex: `docker-compose.dev.yml`, `docker-compose.prod.yml`)
5. **Use build para serviços customizados** e image para serviços padrão

### 5. Resumo do fluxo

* **Frontend** acessa backend via `frontend_network`.
* **Backend** acessa MySQL e Redis via `backend_network`.
* **Volumes** garantem persistência de dados.
* **Redes** isolam serviços, aumentando segurança e organização.
* Tudo pode ser iniciado com **um único comando**:

```bash
docker-compose up -d
```

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



#Guia de Desenvolvimento com FastAPI

## 1. O que é o FastAPI
O **FastAPI** é um framework moderno, rápido (de alta performance) para criação de APIs em Python.  
Ele utiliza **tipagem estática** (type hints) para validação automática de dados e geração de documentação interativa (Swagger e ReDoc) sem esforço adicional.

- **Criado por:** Sebastián Ramírez  
- **Baseado em:** Starlette (para a parte web) e Pydantic (para validação de dados)

## 2. Para que serve
O FastAPI é ideal para:

- Criar **APIs REST** de alta performance
- Desenvolver **microserviços**
- Projetos que precisam de **validação automática** de dados
- Aplicações que exigem **documentação automática**
- Sistemas que precisam escalar facilmente

## 3. Por que usar o FastAPI e não o Django

O FastAPI é rápido, leve e ideal para criar APIs modernas e microserviços, já vem com documentação automática e permite escolher como usar banco de dados.

O Django é mais completo, traz ORM, painel admin e templates, sendo melhor para projetos maiores e sites completos.


**Resumo:**  
Use **FastAPI** se precisa de APIs rápidas, assíncronas e fáceis de documentar.  
Use **Django** se precisa de um sistema web completo com painel administrativo pronto.

## 4. Requisitos e Dependências Fortes

**Python 3.8+**  
**FastAPI** (framework principal)  
**Uvicorn** (servidor ASGI recomendado para rodar o projeto)  

**Instalação mínima:**
bash
pip install fastapi uvicorn

**Fortemente atrelado ao FastAPI:**
**Pydantic** → validação e serialização de dados (internamente já usado pelo FastAPI)  
**Starlette** → manipulação HTTP, rotas e middlewares (também interno)  

> Não é obrigatório usar ORM, mas se for preciso, geralmente recomenda-se **SQLAlchemy** ou **Tortoise ORM**.

## 5. Arquitetura Recomendada

**Estrutura básica de projeto**

project/
│
 ── app/
│   ├── main.py           # Ponto de entrada da aplicação
│   ├── config.py         # Configurações do projeto
│   ├── models/           # Modelos do banco de dados
│   ├── schemas/          # Schemas Pydantic (validação)
│   ├── routers/          # Rotas organizadas por módulo
│   ├── services/         # Lógica de negócio
│   ├── database.py       # Conexão com o banco
│   └── utils/            # Funções auxiliares
│
├── requirements.txt      # Dependências
└── README.md

## 6. Passos para Desenvolvimento (Fluxo Sugerido)

### **1. Preparar o ambiente**
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install fastapi uvicorn

### **2. Criar o arquivo principal (`main.py`)**
python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API rodando com FastAPI!"}


Rodar o servidor:
bash
uvicorn app.main:app --reload

### **3. Definir rotas**
Criar `routers/` e adicionar rotas separadas por funcionalidade.
Usar `@app.get`, `@app.post`, etc.

### **4. Criar Schemas (Pydantic)**
Definir a estrutura dos dados esperados e retornados.

python
from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str

### **5. Integrar com Banco de Dados**
Escolher um ORM ou conexão direta (ex.: SQLAlchemy).
Criar `models/` para as tabelas.

### **6. Adicionar Lógica de Negócio (services/)**
Centralizar funções que tratam regras do sistema.

### **7. Configurações**
Centralizar no `config.py` variáveis como URL do banco e chaves secretas.

### **8. Testes**
Usar `pytest` ou `unittest`.

### **9. Deploy**
Rodar com `uvicorn` ou `gunicorn` + `uvicorn.workers.UvicornWorker`
Hospedar em **Heroku**, **Railway**, **Render**, **AWS**, **Azure** ou **GCP**.

## 7. Links Úteis
- [📚 Documentação oficial do FastAPI](https://fastapi.tiangolo.com/)
- [🚀 Guia do Uvicorn](https://www.uvicorn.org/)
- [🐍 Pydantic](https://docs.pydantic.dev/)



# Grupo 7
