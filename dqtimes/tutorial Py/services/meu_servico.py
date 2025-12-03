import time
from typing import Dict, List, Any

class Minha_Classe:
    
    def exemplo_variaveis_tipos(self) -> Dict[str, Any]:
  
        numero_inteiro = 42
        numero_decimal = 3.14159
        texto = "aoba sô"
        booleano = True
        lista_numeros = [1, 2, 3, 4, 5]
        
        soma = numero_inteiro + 10
        multiplicacao = numero_decimal * 2
        texto_maiusculo = texto.upper()
        
        return {
            "conceito": "xablau",
            "explicacao": "faça o trabalho",
            "exemplos": {
                "inteiro": {
                    "valor": numero_inteiro,
                    "tipo": type(numero_inteiro).__name__,
                    "operacao": f"{numero_inteiro} + 10 = {soma}"
                },
                "float": {
                    "valor": numero_decimal,
                    "tipo": type(numero_decimal).__name__,
                    "operacao": f"{numero_decimal} * 2 = {multiplicacao}"
                },
                "string": {
                    "valor": texto,
                    "tipo": type(texto).__name__,
                    "operacao": f"'{texto}'.upper() = '{texto_maiusculo}'"
                },
                "boolean": {
                    "valor": booleano,
                    "tipo": type(booleano).__name__,
                    "operacao": f"not {booleano} = {not booleano}"
                },
                "lista": {
                    "valor": lista_numeros,
                    "tipo": type(lista_numeros).__name__,
                    "tamanho": len(lista_numeros)
                }
            }
        }
    
    def exemplo_performance_for(self, iteracoes: int = 10000) -> Dict[str, Any]:

        if iteracoes <= 0:
            iteracoes = 10000
        
        start_time = time.time()
        resultado_for = []
        for i in range(iteracoes):
            resultado = (i+i) ** 2
            resultado_for.append(resultado)
        tempo_for = time.time() - start_time
        
        start_time = time.time()
        resultado_comprehension = [(i+i) ** 2 for i in range(iteracoes)]
        tempo_comprehension = time.time() - start_time
        
        diferenca_percentual = ((tempo_for - tempo_comprehension) / tempo_for) * 100
        mais_rapido = "List Comprehension" if tempo_comprehension < tempo_for else "For Normal"
        
        return {
            "conceito": "Comparação de Performance: For vs List Comprehension",
            "explicacao": "List comprehension geralmente é mais rápida que loops for tradicionais",
            "parametros": {
                "iteracoes": iteracoes,
                "operacao": "Calcular quadrado dos números (i²)"
            },
            "resultados": {
                "for_normal": {
                    "tempo_segundos": round(tempo_for, 6),
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
                "conclusao": f"List comprehension foi {round(abs(diferenca_percentual), 2)}% mais rápida" if tempo_comprehension < tempo_for else f"For normal foi {round(abs(diferenca_percentual), 2)}% mais rápido"
            },
            "verificacao": {
                "resultados_iguais": resultado_for == resultado_comprehension,
                "tamanho_resultado": len(resultado_for)
            }
        }

