# monitoring.py
import psutil
import asyncio
from prometheus_client import start_http_server, Gauge, Counter

# Métricas PgBouncer
pgbouncer_active_connections = Gauge('pgbouncer_active_connections', 'Conexões ativas')
pgbouncer_pool_size = Gauge('pgbouncer_pool_size', 'Tamanho do pool')
pgbouncer_waiting_clients = Gauge('pgbouncer_waiting_clients', 'Clientes esperando')
pgbouncer_queries_total = Counter('pgbouncer_queries_total', 'Total de queries')

async def monitor_pgbouncer():
    while True:
        try:
            # Conectar ao PgBouncer para obter stats
            conn = await asyncpg.connect("postgresql://usuario:senha@localhost:6432/pgbouncer")
            
            # SHOW STATS command
            stats = await conn.fetch("SHOW STATS")
            for stat in stats:
                if stat['database'] == 'fastapi_db':
                    pgbouncer_active_connections.set(stat['total_connections'])
                    pgbouncer_queries_total.inc(stat['total_queries'])
            
            # SHOW POOLS command
            pools = await conn.fetch("SHOW POOLS")
            for pool in pools:
                if pool['database'] == 'fastapi_db':
                    pgbouncer_pool_size.set(pool['cl_active'])
                    pgbouncer_waiting_clients.set(pool['cl_waiting'])
            
            await conn.close()
        except Exception as e:
            print(f"Erro no monitoramento: {e}")
        
        await asyncio.sleep(30)  # Coletar métricas a cada 30 segundos