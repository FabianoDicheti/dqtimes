-- Configuração de usuários e permissões PostgreSQL para DQTimes

-- Criar usuário de aplicação (acesso read/write normal)
CREATE USER dqtimes_app WITH PASSWORD 'changeme_app_password';

-- Criar usuário de migração (acesso admin para DDL)
CREATE USER dqtimes_migration WITH PASSWORD 'changeme_migration_password';

-- Conectar ao banco dqtimes
\c dqtimes

-- Permissões para usuário de aplicação (mínimo privilégio)
GRANT CONNECT ON DATABASE dqtimes TO dqtimes_app;
GRANT USAGE ON SCHEMA public TO dqtimes_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dqtimes_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO dqtimes_app;

-- Garantir permissões em tabelas futuras
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dqtimes_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO dqtimes_app;

-- Permissões para usuário de migração (DDL completo)
GRANT CONNECT ON DATABASE dqtimes TO dqtimes_migration;
GRANT ALL PRIVILEGES ON SCHEMA public TO dqtimes_migration;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dqtimes_migration;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dqtimes_migration;

-- Garantir permissões em objetos futuros
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO dqtimes_migration;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO dqtimes_migration;
