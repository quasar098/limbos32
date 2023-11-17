import threading
import subprocess

def run_server():
    subprocess.run(['python', 'server.py'])

def run_spawn_all():
    subprocess.run(['python', 'spawn-all.py'])

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    spawn_all_thread = threading.Thread(target=run_spawn_all)

    server_thread.start()
    spawn_all_thread.start()

    server_thread.join()
    spawn_all_thread.join()
