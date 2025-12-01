import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

BACKUP_DIR = Path(r"C:\Backups\dqtimes")

def run_command(cmd, shell=True):
    result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def list_backups():
    backups = sorted(BACKUP_DIR.glob("data-backup-*.tar.gz"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not backups:
        print(f"Nenhum backup encontrado em {BACKUP_DIR}")
        return []
    
    print("\nBackups disponiveis:")
    print("-" * 60)
    for i, backup in enumerate(backups, 1):
        file_time = datetime.fromtimestamp(backup.stat().st_mtime)
        size_mb = backup.stat().st_size / (1024 * 1024)
        age = datetime.now() - file_time
        
        print(f"{i}. {backup.name}")
        print(f"   Data: {file_time.strftime('%Y-%m-%d %H:%M:%S')} ({age.days} dias atras)")
        print(f"   Tamanho: {size_mb:.2f} MB\n")
    
    return backups

def select_backup(backup_file=None):
    if backup_file:
        backup_path = Path(backup_file)
        if not backup_path.exists():
            print(f"Arquivo nao encontrado: {backup_file}")
            return None
        return backup_path
    
    backups = list_backups()
    if not backups:
        return None
    
    print("Usando backup mais recente (1) por padrao.")
    choice = input("Digite o numero do backup ou Enter para usar o mais recente: ").strip()
    
    if not choice:
        return backups[0]
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(backups):
            return backups[index]
        else:
            print("Numero invalido")
            return None
    except ValueError:
        print("Entrada invalida")
        return None

def stop_container():
    print("\nParando container...")
    success, stdout, stderr = run_command("docker stop dqtimes-app")
    
    if success or "No such container" in stderr:
        print("Container parado")
        return True
    else:
        print(f"Aviso ao parar container: {stderr}")
        return True

def restore_data(backup_file):
    print(f"\nRestaurando dados de: {backup_file.name}...")
    
    cmd = f'docker run --rm -v dqtimes_data:/data -v {BACKUP_DIR}:/backup alpine tar xzf /backup/{backup_file.name} -C /data'
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print("Dados restaurados com sucesso")
        return True
    else:
        print(f"Erro ao restaurar dados: {stderr}")
        return False

def restore_image():
    print("\nProcurando backup de imagem...")
    
    image_backups = sorted(BACKUP_DIR.glob("dqtimes-app-*.tar.gz"), 
                          key=lambda x: x.stat().st_mtime, 
                          reverse=True)
    
    if not image_backups:
        print("Nenhum backup de imagem encontrado (pulando)")
        return True
    
    image_backup = image_backups[0]
    print(f"Restaurando imagem: {image_backup.name}...")
    
    success, stdout, stderr = run_command(f'docker load -i "{image_backup}"')
    
    if success:
        print(f"Imagem restaurada: {image_backup.name}")
        return True
    else:
        print(f"Erro ao restaurar imagem: {stderr}")
        return False

def start_container():
    print("\nIniciando container...")
    success, stdout, stderr = run_command("docker start dqtimes-app")
    
    if success:
        print("Container iniciado")
        return True
    else:
        print(f"Erro ao iniciar container: {stderr}")
        print("Pode ser necessario criar o container manualmente")
        return False

def validate_restore():
    print("\nValidando restore...")
    time.sleep(5)
    
    success, stdout, stderr = run_command('docker ps --filter "name=dqtimes-app" --format "{{.Names}}"')
    
    if success and "dqtimes-app" in stdout:
        print("Container esta rodando")
        
        success_logs, logs, _ = run_command("docker logs dqtimes-app --tail 10")
        if success_logs:
            print("\nUltimas linhas do log:")
            print("-" * 60)
            print(logs)
        
        return True
    else:
        print("Container nao esta rodando!")
        return False

def main():
    print("=== Restore DQTimes ===")
    
    backup_file_arg = sys.argv[1] if len(sys.argv) > 1 else None
    restore_image_flag = "--with-image" in sys.argv
    
    try:
        backup_file = select_backup(backup_file_arg)
        if not backup_file:
            return 1
        
        print(f"\nBackup selecionado: {backup_file.name}")
        confirm = input("Confirma o restore? (s/N): ").strip().lower()
        
        if confirm not in ['s', 'sim', 'y', 'yes']:
            print("Restore cancelado.")
            return 0
        
        if not stop_container():
            return 1
        
        if not restore_data(backup_file):
            return 1
        
        if restore_image_flag:
            restore_image()
        
        if not start_container():
            print("\nContainer nao iniciou. Tente iniciar manualmente:")
            print("   docker start dqtimes-app")
            return 1
        
        if validate_restore():
            print("\n=== Restore Concluido com Sucesso ===")
            print("\nVerifique a aplicacao em: http://localhost:80/docs")
            print("Para ver logs completos: docker logs dqtimes-app")
            return 0
        else:
            print("\nRestore concluido mas validacao falhou")
            print("Verifique manualmente: docker logs dqtimes-app")
            return 1
        
    except KeyboardInterrupt:
        print("\n\nRestore cancelado pelo usuario.")
        return 1
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
