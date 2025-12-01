import subprocess
from datetime import datetime, timedelta
from pathlib import Path

BACKUP_DIR = Path(r"C:\Backups\dqtimes")
RETENTION_DAYS = 7

def run_command(cmd, shell=True):
    result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = f"data-backup-{timestamp}.tar.gz"
    
    print(f"=== Backup DQTimes - {timestamp} ===")
    
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Diretorio de backup: {BACKUP_DIR}")
    
    print(f"\nCriando backup: {backup_file}...")
    cmd = f'docker run --rm -v dqtimes_data:/data -v {BACKUP_DIR}:/backup alpine tar czf /backup/{backup_file} -C /data .'
    
    success, stdout, stderr = run_command(cmd)
    
    if success:
        size_mb = (BACKUP_DIR / backup_file).stat().st_size / (1024 * 1024)
        print(f"Backup criado: {backup_file} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"Erro ao criar backup: {stderr}")
        return False

def cleanup_old_backups():
    print(f"\nLimpando backups antigos (> {RETENTION_DAYS} dias)...")
    
    cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)
    removed_count = 0
    
    for backup_file in BACKUP_DIR.glob("data-backup-*.tar.gz"):
        file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
        
        if file_time < cutoff_date:
            backup_file.unlink()
            print(f"  Removido: {backup_file.name}")
            removed_count += 1
    
    if removed_count > 0:
        print(f"{removed_count} backup(s) antigo(s) removido(s)")
    else:
        print("  Nenhum backup antigo para remover")

def show_summary():
    backups = list(BACKUP_DIR.glob("data-backup-*.tar.gz"))
    total_size = sum(f.stat().st_size for f in backups) / (1024 * 1024)
    
    print("\n=== Backup Concluido ===")
    print(f"Backups disponiveis: {len(backups)}")
    print(f"Espaco total usado: {total_size:.2f} MB")
    print(f"Localizacao: {BACKUP_DIR}")

def main():
    try:
        if create_backup():
            cleanup_old_backups()
            show_summary()
            return 0
        else:
            return 1
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
