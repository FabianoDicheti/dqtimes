from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import asyncio
from .config.database import (
    AsyncSessionLocal, 
    get_pgbouncer_stats, 
    test_connections
)

app = FastAPI(title="Projeto Faculdade - Connection Pooling")

@app.on_event("startup")
async def startup_event():
    """Executar na inicialização da aplicação"""
    await test_connections()
    print("🚀 Aplicação iniciada com Connection Pooling")

# Dependência para obter sessão do banco
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@app.get("/")
async def root():
    return {"message": "Sistema com Connection Pooling - Projeto Faculdade"}

@app.get("/health/pgbouncer")
async def health_pgbouncer():
    """Health check completo do PgBouncer"""
    try:
        stats = await get_pgbouncer_stats()
        
        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])
        
        # Analisar métricas importantes
        total_connections = sum([s['total_connections'] for s in stats['stats']])
        active_pools = len([p for p in stats['pools'] if p['cl_active'] > 0])
        
        health_status = {
            "status": "healthy",
            "total_connections": total_connections,
            "active_pools": active_pools,
            "databases": len(stats['databases']),
            "timestamp": datetime.now().isoformat()
        }
        
        return health_status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/pgbouncer")
async def detailed_pgbouncer_stats():
    """Estatísticas detalhadas do PgBouncer"""
    stats = await get_pgbouncer_stats()
    return stats

@app.get("/test/database")
async def test_database_connection(db: AsyncSession = Depends(get_db)):
    """Teste de conexão com o banco através do PgBouncer"""
    try:
        result = await db.execute(text("SELECT version(), current_timestamp, pg_database_size('faculdade_db') as db_size"))
        row = result.fetchone()
        
        return {
            "postgres_version": row[0],
            "current_timestamp": row[1],
            "database_size_bytes": row[2],
            "connection_test": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Exemplo de uso em uma rota de negócio
@app.get("/dados/contagem")
async def get_data_count(db: AsyncSession = Depends(get_db)):
    """Exemplo de rota que usa connection pooling"""
    try:
        result = await db.execute(text("SELECT COUNT(*) as total FROM information_schema.tables"))
        count = result.scalar()
        return {"total_tables": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))