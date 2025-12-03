from datetime import datetime

from dqtimes.endpoint_historico_dqtimes.models import TaskHistory


def registrar_historico(
    db,
    task: str,
    referencia: str | None,
    status: str,
    details: dict | list | None = None
):
    """
    Cria um registro de histórico.
    Pode ser chamada em qualquer ponto da função.
    """

    historia = TaskHistory(
        task=task,
        referencia=referencia,
        status=status,
        details=details,
        created_at=datetime.utcnow(),
        finished_at=datetime.utcnow() if status in ("SUCCESS", "FAILED") else None
    )

    db.add(historia)
    db.commit()
    db.refresh(historia)

    return historia
