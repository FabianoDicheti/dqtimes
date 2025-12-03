from typing import List, Dict, Any

class Minha_Classe:
    """Classe para análise de séries temporais (exemplo3)"""
    
    def exemplo3_medias_moveis(self, lista: List[float], qnt: int, tam_grupo: int = 5) -> Dict[str, Any]:
        """Método de médias móveis"""
        data = lista.copy()
        predictions = []

        for _ in range(qnt):
            window = data[-tam_grupo:] if len(data) >= tam_grupo else data
            next_val = sum(window) / len(window)
            predictions.append(round(next_val, 2))
            data.append(next_val)

        return {"lista": predictions, "qnt": str(qnt)}