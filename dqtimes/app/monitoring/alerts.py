# alerts.py
ALERT_THRESHOLDS = {
    'max_connections': 800,  # 80% de 1000
    'waiting_clients': 50,
    'pool_utilization': 0.9  # 90%
}

async def check_alerts():
    health = await check_pgbouncer_health()
    
    if health['status'] == 'healthy':
        if health['active_connections'] > ALERT_THRESHOLDS['max_connections']:
            # Enviar alerta
            print("ALERTA: Conexões próximas do limite máximo")