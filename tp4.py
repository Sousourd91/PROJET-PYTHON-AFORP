import socket
import argparse

parser = argparse.ArgumentParser(description="Scanner de ports TCP simple")
parser.add_argument("--ip", required=True, help="Adresse IP à scanner")
parser.add_argument("--start-port", type=int, required=True, help="Port de début")
parser.add_argument("--end-port", type=int, required=True, help="Port de fin")
args = parser.parse_args()

ip = args.ip
port_debut = args.start_port
port_fin = args.end_port

print(f"Scan de l'adresse {ip} de {port_debut} à {port_fin}")

for port in range(port_debut, port_fin + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        resultat = s.connect_ex((ip, port))
        if resultat == 0:
            print(f"Port {port} est OUVERT")
    except socket.gaierror:
        print("Erreur : adresse IP invalide")
        break
    except socket.timeout:
        print(f"Timeout sur le port {port}")
    except Exception as e:
        print(f"Erreur sur le port {port} : {e}")
    finally:
        s.close()