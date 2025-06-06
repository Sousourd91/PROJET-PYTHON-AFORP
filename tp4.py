import socket
import argparse
import threading
import csv

resultats_ouverts = []
resultats_fermes = []

def scanner_port(ip, port, verbose):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            print(f"[OUVERT] Port {port}")
            resultats_ouverts.append(port)
        elif verbose:
            print(f"[FERMÉ] Port {port}")
            resultats_fermes.append(port)
    except socket.gaierror:
        print("Erreur : adresse IP invalide.")
    except socket.timeout:
        if verbose:
            print(f"[TIMEOUT] Port {port}")
    except Exception as e:
        print(f"Erreur sur le port {port} : {e}")
    finally:
        s.close()

parser = argparse.ArgumentParser(description="Scanner de ports TCP")
parser.add_argument("--ip", required=True, help="Adresse IP à scanner")
parser.add_argument("--start-port", type=int, required=True, help="Port de début")
parser.add_argument("--end-port", type=int, required=True, help="Port de fin")
parser.add_argument("--verbose", action="store_true", help="Afficher aussi les ports fermés")
parser.add_argument("--output", help="Nom du fichier de sortie CSV", default="resultats_ports.csv")
args = parser.parse_args()

print(f"Scan en cours de {args.ip} de {args.start_port} à {args.end_port}...\n")

threads = []

for port in range(args.start_port, args.end_port + 1):
    t = threading.Thread(target=scanner_port, args=(args.ip, port, args.verbose))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nPorts ouverts trouvés :")
for port in sorted(resultats_ouverts):
    print(f"  - {port}")

with open(args.output, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Port", "État"])
    for port in sorted(resultats_ouverts):
        writer.writerow([port, "OUVERT"])
    if args.verbose:
        for port in sorted(resultats_fermes):
            writer.writerow([port, "FERMÉ"])

print(f"\nRésultats enregistrés dans : {args.output}")