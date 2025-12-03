"""Cria tabelas de histórico (parte 1)

Requisitos da Issue 1:
- Criar tabela tarefas
- Criar tabela series
- Persistir request_payload (JSONB)
- Criar índices por usuário e data
"""

# Importa a função `op` para executar SQL diretamente (sem ORM)
from alembic import op


# Identificadores de migration usados pelo Alembic
revision = "001_history_tables"
down_revision = None  # primeira migration do projeto
branch_labels = None
depends_on = None


def upgrade():
    """
    Executado quando rodamos: alembic upgrade head

    Cria:
    - tabela tarefas
    - índices por usuário e criação
    - tabela series
    """

    # --- TABELA TAREFAS ---
    # Armazena o histórico de requisições feitas à API
    op.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            task_id SERIAL PRIMARY KEY,                  -- identificador único
            usuario_id INTEGER,                          -- ID do usuário que enviou a requisição
            status VARCHAR(50) NOT NULL,                 -- status da task (pendente, concluída, erro...)
            request_payload JSONB,                       -- payload da requisição recebido via API
            created_at TIMESTAMP NOT NULL DEFAULT NOW(), -- timestamp de criação
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()  -- timestamp de última atualização
        );
    """)

    # Índice para acelerar buscas por usuário
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_tarefas_usuario
            ON tarefas (usuario_id);
    """)

    # Índice para acelerar buscas e ordenações por data
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_tarefas_created_at
            ON tarefas (created_at);
    """)

    # --- TABELA SERIES ---
    # Guarda metadados das séries temporais enviadas
    op.execute("""
        CREATE TABLE IF NOT EXISTS series (
            serie_id SERIAL PRIMARY KEY,                 -- chave primária
            referencia TEXT NOT NULL,                    -- referência da série
            origem TEXT NOT NULL,                        -- origem/descrição ou identificador
            created_at TIMESTAMP NOT NULL DEFAULT NOW()  -- timestamp de criação
        );
    """)


def downgrade():
    """
    Executado quando rodamos: alembic downgrade -1

    Remove as tabelas criadas por esta migration.
    """

    # Remove tabela series (não tem dependências)
    op.execute("DROP TABLE IF EXISTS series;")

    # Remove tabela tarefas com CASCADE para remover dependências futuras se existirem
    op.execute("DROP TABLE IF EXISTS tarefas CASCADE;")
