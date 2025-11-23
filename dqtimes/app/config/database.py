import os
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from contextlib import asynccontextmanager

# Configurações de conexão
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://fastapi_user:senha_segura_123@localhost:6432/faculdade_db"
)

PGBOUNCER_STATS_URL = os.getenv(
    "PGBOUNCER_STATS_URL",
    "postgresql://stats:stats_senha@localhost:6432/pgbouncer"
)

# Engine principal para a aplicação
engine = create_async_engine(
    DATABASE_URL,
    # Configurações otimizadas para PgBouncer
    pool_size=10,           # Tamanho do pool no SQLAlchemy
    max_overflow=20,        # Conexões extras temporárias
    pool_pre_ping=True,     # Verificar conexões antes de usar
    pool_recycle=3600,      # Reciclar conexões a cada 1h
    echo=False,             # Desabilitar logs SQL (produção)
    future=True
)

# Session factory para dependências do FastAPI
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

@asynccontextmanager
async def get_db_connection():
    """Context manager para conexões diretas com o banco"""
    connection = None
    try:
        connection = await asyncpg.connect(
            "postgresql://fastapi_user:senha_segura_123@localhost:6432/faculdade_db"
        )
        yield connection
    finally:
        if connection:
            await connection.close()

async def get_pgbouncer_stats():
    """Obter estatísticas do PgBouncer"""
    try:
        conn = await asyncpg.connect(PGBOUNCER_STATS_URL)
        
        # Estatísticas gerais
        stats = await conn.fetch("SHOW STATS")
        pools = await conn.fetch("SHOW POOLS")
        databases = await conn.fetch("SHOW DATABASES")
        
        await conn.close()
        
        return {
            "stats": [dict(record) for record in stats],
            "pools": [dict(record) for record in pools],
            "databases": [dict(record) for record in databases]
        }
    except Exception as e:
        return {"error": str(e)}

# Teste de conexão inicial
async def test_connections():
    """Testar todas as conexões na inicialização"""
    try:
        # Testar conexão principal
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Conexão principal com PgBouncer estabelecida")
        
        # Testar estatísticas
        stats = await get_pgbouncer_stats()
        if "error" not in stats:
            print("✅ Conexão de estatísticas do PgBouncer estabelecida")
        else:
            print("⚠️  Conexão de estatísticas falhou")
            
    except Exception as e:
        print(f"❌ Erro nas conexões: {e}")
        raise