#!/bin/bash
set -e

echo "🔄 Iniciando migração segura..."

# Variáveis (ajuste conforme seu ambiente)
DB_HOST=${DB_HOST:-localhost}
DB_USER=${DB_USER:-user}
DB_NAME=${DB_NAME:-faculdade_db}

# Backup
echo "📦 Criando backup..."
BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
pg_dump -h $DB_HOST -U $DB_USER $DB_NAME > $BACKUP_FILE
echo "✅ Backup salvo como: $BACKUP_FILE"

# Migração
echo "🚀 Aplicando migrações..."
alembic upgrade head

echo "✅ Migração concluída com sucesso!"