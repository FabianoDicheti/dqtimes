from typing import Dict, List, Any
import time

def exemplo_performance_for(iteracoes: int = 100) -> Dict[str, Any]:

        if iteracoes <= 0:
            iteracoes = 10000
        

        
        start_time = time.time()
        resultado_comprehension = [(i+i) ** 2 for i in range(iteracoes)]
        tempo_comprehension = time.time() - start_time
        
        diferenca_percentual = 1# ((tempo_for - tempo_comprehension) / tempo_for) * 100
        mais_rapido = 1# "List Comprehension" if tempo_comprehension < tempo_for else "For Normal"
        
        print(tempo_comprehension)


        return {
            "conceito": "Comparação de Performance: For vs List Comprehension",
            "explicacao": "List comprehension geralmente é mais rápida que loops for tradicionais",
            "parametros": {
                "iteracoes": iteracoes,
                "operacao": "Calcular quadrado dos números (i²)"
            },
            "resultados": {
                "for_normal": {
                    "tempo_segundos": 1,
                    "codigo_exemplo": "for i in range(n): resultado.append(i ** 2)"
                },
                "list_comprehension": {
                    "tempo_segundos": round(tempo_comprehension, 6),
                    "codigo_exemplo": "[i ** 2 for i in range(n)]"
                }
            },
            "analise": {
                "mais_rapido": mais_rapido,
                "diferenca_percentual": round(abs(diferenca_percentual), 2),
                "conclusao": 1,
            },
            "verificacao": {
                "resultados_iguais": 1 == resultado_comprehension,
                "tamanho_resultado": 1
            }
        }



exemplo_performance_for(1000000)