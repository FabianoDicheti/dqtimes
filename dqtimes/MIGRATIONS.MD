# 📋 Workflow de Migrações de Banco

## 🛠️ Ferramentas
- **Alembic**: Gerenciamento de migrations
- **SQLAlchemy**: ORM para autogenerate
- **PostgreSQL**: Banco de dados

## 📁 Estrutura
migrations/
├── versions/ # Arquivos de migração
├── env.py # Configuração do Alembic
└── script.py.mako # Template das migrations

text

## 🚀 Comandos Básicos

### Criar Nova Migration
```bash
alembic revision --autogenerate -m "descricao_da_mudanca"
Aplicar Migrations
bash
# Aplicar todas
alembic upgrade head

# Aplicar até versão específica
alembic upgrade +1
Rollback
bash
# Reverter uma migration
alembic downgrade -1

# Reverter para versão específica
alembic downgrade <version_id>
🔄 Fluxo de Trabalho
1. Desenvolvimento
bash
# Criar migration
alembic revision --autogenerate -m "add_user_table"

# Testar localmente
alembic upgrade head
2. Staging
bash
# Aplicar e validar
alembic upgrade head
pytest tests/
3. Produção
bash
# Migração segura com backup
chmod +x scripts/safe_migration.sh
./scripts/safe_migration.sh
🛡️ Rollback Seguro
Todas as migrations devem ter:

upgrade(): Aplica mudanças

downgrade(): Reverte mudanças

📞 Suporte
Em caso de problemas:

Verificar logs: alembic current

Rollback: alembic downgrade -1

Restaurar backup se necessário

text

---

## 💻 PASSO 2: Configurar e Testar Localmente

### 2.1 Instalar dependência (se necessário):
```bash
pip install alembic
2.2 Testar a configuração:
bash
# Verificar se o Alembic funciona
alembic current

# Deve mostrar: "head" (se não houver migrations)
2.3 Tornar o script executável:
bash
chmod +x scripts/safe_migration.sh