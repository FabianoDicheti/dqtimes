"""Cria tabela previsoes (parte 2 das tabelas de histórico)

Requisitos da Issue 2:
- Criar tabela previsoes
- FK para tarefas(task_id)
- Garantir unicidade por task_id
- Criar índice parcial para status = 'concluída'
"""

from alembic import op
import sqlalchemy as sa


# Identificadores da migration
# Usados pelo Alembic para controlar a ordem das migrations
revision = "002_previsoes"
down_revision = "001_history_tables"   # depende da Issue 1
branch_labels = None
depends_on = None


def upgrade():
    """
    Executado ao rodar alembic upgrade head.

    Cria:
    - tabela previsoes
    - constraint de FK
    - constraint de unicidade
    - índice parcial para status 'concluída'
    """

    # --- TABELA PREVISOES ---
    op.execute("""
        CREATE TABLE IF NOT EXISTS previsoes (
            id SERIAL PRIMARY KEY,                     -- chave primária
            task_id INTEGER NOT NULL,                 -- FK para tarefas
            resultado JSONB,                           -- resultado previsto
            status VARCHAR(50) NOT NULL DEFAULT 'pendente',  -- status da previsão
            criado_em TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(), -- timestamp
            atualizado_em TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(), -- timestamp

            -- Relaciona previsões → tarefas
            CONSTRAINT fk_task
                FOREIGN KEY (task_id)
                REFERENCES tarefas (task_id)
                ON DELETE CASCADE,     -- se a task for removida, remove previsões também

            -- Garante 1 previsão por task_id
            CONSTRAINT uq_task UNIQUE (task_id)
        );
    """)

    # Índice parcial: acelera buscas APENAS quando status = 'concluída'
    # Isso reduz custo de armazenamento e melhora desempenho
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_previsoes_status_concluida
        ON previsoes (task_id)
        WHERE status = 'concluída';
    """)


def downgrade():
    """
    Executado ao rodar alembic downgrade -1.

    Remove tudo que esta migration criou.
    """

    # Remove índice primeiro
    op.execute("DROP INDEX IF EXISTS idx_previsoes_status_concluida;")

    # Depois remove a tabela
    op.execute("DROP TABLE IF EXISTS previsoes;")
