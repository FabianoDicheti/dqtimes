# Estrategia de Backup & Restore - DQTimes

## Visao Geral

Estrategia simplificada de backup focada em containers Docker e volumes de dados.

---

## Abordagem de Backup

### 1. Backup de Volumes Docker (Dados)

Os dados da aplicação ficam em volumes Docker que precisam ser salvos.

**Script Python:**
```python
# Executar backup
python backup_daily.py
```

**Ou comando Docker direto:**
```bash
docker run --rm -v dqtimes_data:/data -v C:\Backups\dqtimes:/backup alpine tar czf /backup/data-backup-$(date +%Y%m%d-%H%M%S).tar.gz -C /data .
```

### 2. Backup de Imagem Docker

Salvar a imagem Docker buildada para restore rápido.

**Comando:**
```bash
# Exportar e compactar imagem
docker save dqtimes-app:latest | gzip > C:\Backups\dqtimes\dqtimes-app-$(date +%Y%m%d).tar.gz
```

### 3. Backup de Código-Fonte (Git)

O código já está versionado no Git - backup automático via push.

```bash
git add .
git commit -m "Backup checkpoint"
git push origin main
```

---

## Politica de Retencao

### Regras Simples

| Tipo de Backup | Frequencia | Manter |
|----------------|------------|--------|
| **Volumes de Dados** | Diario (02:00) | 7 dias |
| **Imagem Docker** | Semanal | 4 semanas |
| **Codigo (Git)** | Continuo | Ilimitado |

### Limpeza Automatica

A limpeza e feita automaticamente pelo script `backup_daily.py` (mantem ultimos 7 dias).

---

## Procedimentos de Restore

### Restore Completo

**Cenario:** Recuperar aplicacao completa apos falha

**Script Python (Recomendado):**
```python
python restore.py

python restore.py C:\Backups\dqtimes\data-backup-20251201-020000.tar.gz

python restore.py --with-image
```

**Ou comandos Docker diretos:**
```bash
docker stop dqtimes-app

docker run --rm -v dqtimes_data:/data -v C:\Backups\dqtimes:/backup alpine tar xzf /backup/data-backup-20251201-020000.tar.gz -C /data

docker start dqtimes-app
```

**Tempo de Recuperacao:** 5-10 minutos

### Rollback de Codigo (Git)

**Cenario:** Bug apos deploy

```bash
git log --oneline -5

git reset --hard <commit-hash>

docker build -t dqtimes-app:latest .
docker stop dqtimes-app
docker rm dqtimes-app
docker run -d --name dqtimes-app -p 80:80 -p 8787:8787 -v dqtimes_data:/app/data dqtimes-app:latest
```

**Tempo de Recuperacao:** 5-10 minutos

---

## Validacao Pos-Restore

### Checklist Simples

O script `restore.py` ja faz validacao automatica, mas voce pode verificar manualmente:

```bash
docker ps | grep dqtimes-app

docker logs dqtimes-app --tail 50

curl http://localhost:80/docs

docker exec dqtimes-app ls -lh /app/data
```

Se todos os comandos retornarem OK: Restore validado

---

## Responsabilidades

### Matriz Simples

| Tarefa | Responsavel | Frequencia |
|--------|-------------|------------|
| **Executar backup diario** | DevOps / Automacao | Diario |
| **Verificar backups** | Tech Lead | Semanal |
| **Testar restore** | Desenvolvedor | Mensal |
| **Restore de emergencia** | Tech Lead + DevOps | Quando necessario |
| **Atualizar documentacao** | Tech Lead | Trimestral |

### Contatos de Emergencia

```
1 Contato: Tech Lead - [NOME] - [TELEFONE]
2 Contato: DevOps    - [NOME] - [TELEFONE]
3 Contato: CTO       - [NOME] - [TELEFONE]
```

---

## Automacao com Python

### Scripts Python Criados

**`backup_daily.py`** - Backup automatico com limpeza  
**`restore.py`** - Restore interativo com validacao

### Agendar Backup Automatico

**Opcao 1: Windows Task Scheduler**
```bash
schtasks /create /tn "DQTimes Backup" /tr "python C:\Faculdade_4P\dqtimes\dqtimes\dqtimes\backup\backup_daily.py" /sc daily /st 02:00 /ru SYSTEM
```

**Opcao 2: Cron (Linux/WSL)**
```bash
0 2 * * * cd /caminho/dqtimes && python3 backup_daily.py
```

**Opcao 3: Executar manualmente**
```bash
python backup_daily.py
```

---

## Estrutura de Arquivos

```
C:\Backups\dqtimes\
├── data-backup-20251201-020000.tar.gz
├── data-backup-20251202-020000.tar.gz
├── data-backup-20251203-020000.tar.gz
└── dqtimes-app-20251201.tar.gz
```

---

## Seguranca

- Backups armazenados em `C:\Backups\dqtimes`
- Permissoes restritas apenas para administradores
- Para producao: sincronizar com cloud storage (Azure Blob/AWS S3)

---

## Comandos Rapidos de Referencia

### Scripts Python (Recomendado)

```bash
python backup_daily.py

python restore.py

python restore.py C:\Backups\dqtimes\data-backup-20251201-020000.tar.gz

python restore.py --with-image
```

### Comandos Docker Diretos

```bash
docker run --rm -v dqtimes_data:/data -v C:\Backups\dqtimes:/backup alpine tar czf /backup/data-backup-$(date +%Y%m%d-%H%M%S).tar.gz -C /data .

docker save dqtimes-app:latest | gzip > C:\Backups\dqtimes\dqtimes-app-$(date +%Y%m%d).tar.gz

docker run --rm -v dqtimes_data:/data -v C:\Backups\dqtimes:/backup alpine tar xzf /backup/data-backup-YYYYMMDD-HHMMSS.tar.gz -C /data

docker ps | grep dqtimes
docker logs dqtimes-app --tail 50
```

---

## Procedimento de Emergencia

### Se a aplicacao parar:

1. **Verificar status:** `docker ps -a | grep dqtimes`
2. **Ver logs:** `docker logs dqtimes-app`
3. **Reiniciar:** `docker restart dqtimes-app`
4. **Se nao resolver:** `python restore.py`

### Telefone de Emergencia

**Tech Lead:** [TELEFONE] - Disponivel 24/7

---

## Requisitos Python

```bash
python --version
```

Os scripts usam apenas bibliotecas padrao Python (`subprocess`, `pathlib`, `datetime`), entao nao precisam de instalacao adicional.

---

**Ultima Atualizacao:** 2025-12-01  
**Proxima Revisao:** 2026-03-01  
**Status:** Ativo
