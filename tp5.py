import psutil
import time
import os
import platform

def effacer_ecran():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def afficher_tableau_de_bord():
    while True:
        effacer_ecran()
        
        print("=== Tableau de bord système ===\n")

        print("Utilisation CPU par cœur :")
        for i, pourcent in enumerate(psutil.cpu_percent(percpu=True)):
            print(f"  Coeur {i} : {pourcent}%")
        print(f"Utilisation CPU totale : {psutil.cpu_percent()}%\n")

        memoire = psutil.virtual_memory()
        print("Mémoire RAM :")
        print(f"  Totale : {memoire.total // (1024**2)} Mo")
        print(f"  Utilisée : {memoire.used // (1024**2)} Mo")
        print(f"  Libre : {memoire.available // (1024**2)} Mo\n")

        print("Utilisation disque :")
        partitions = psutil.disk_partitions()
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                print(f"  {p.device} - {usage.percent}% utilisé ({usage.used // (1024**3)} Go / {usage.total // (1024**3)} Go)")
            except PermissionError:
                print(f"  {p.device} - Accès refusé")
        print()

        net = psutil.net_io_counters()
        print("Activité réseau :")
        print(f"  Octets envoyés : {net.bytes_sent}")
        print(f"  Octets reçus : {net.bytes_recv}")
        print(f"  Paquets envoyés : {net.packets_sent}")
        print(f"  Paquets reçus : {net.packets_recv}\n")

        stats_interfaces = psutil.net_io_counters(pernic=True)
        print("Par interface réseau :")
        for iface, stat in stats_interfaces.items():
            print(f"  {iface} : Envoyés = {stat.bytes_sent} | Reçus = {stat.bytes_recv}")
        print()

        print("Tapez Ctrl+C pour quitter.\n")

        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("Arrêt du programme.")
            break

afficher_tableau_de_bord()