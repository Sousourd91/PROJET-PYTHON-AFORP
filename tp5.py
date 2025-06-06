import psutil
import os
import time
import platform
import csv
from datetime import datetime

def effacer_ecran():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def barre_cpu(pourcentage):
    taille_max = 30
    nb_blocs = int(pourcentage / 100 * taille_max)
    return "[" + "#" * nb_blocs + "-" * (taille_max - nb_blocs) + f"] {pourcentage:.1f}%"

fichier_log = "log_systeme.csv"
with open(fichier_log, "w", newline="") as fichier:
    writer = csv.writer(fichier)
    writer.writerow(["Horodatage", "CPU total", "Mémoire utilisée (Mo)", "Disque utilisé (Go)", "Octets envoyés", "Octets reçus"])

def display_dashboard():
    while True:
        effacer_ecran()
        print("=== Tableau de bord système (actualisé toutes les 5 sec) ===\n")

        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cpu_total = psutil.cpu_percent()
        print("Utilisation CPU par cœur :")
        for i, pourcent in enumerate(psutil.cpu_percent(percpu=True)):
            print(f"  Coeur {i} : {barre_cpu(pourcent)}")
        print(f"\nCPU total : {barre_cpu(cpu_total)}")

        try:
            temp = psutil.sensors_temperatures()
            if temp:
                for nom, valeurs in temp.items():
                    for entree in valeurs:
                        print(f"Température {nom} ({entree.label or 'n/a'}) : {entree.current}°C")
            else:
                print("Température CPU : non disponible")
        except:
            print("Température CPU : erreur ou non prise en charge")

        print()

        mem = psutil.virtual_memory()
        mem_total = mem.total // (1024**2)
        mem_used = mem.used // (1024**2)
        mem_free = mem.available // (1024**2)
        print("Mémoire RAM :")
        print(f"  Totale : {mem_total} Mo")
        print(f"  Utilisée : {mem_used} Mo")
        print(f"  Libre : {mem_free} Mo\n")

        print("Utilisation disque :")
        disque_total_utilise = 0
        partitions = psutil.disk_partitions()
        for part in partitions:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                utilise = usage.used // (1024**3)
                disque_total_utilise += utilise
                print(f"  {part.device} : {usage.percent}% utilisé ({utilise} Go)")
            except PermissionError:
                print(f"  {part.device} : accès refusé")

        print()

        net = psutil.net_io_counters()
        print("Réseau (total) :")
        print(f"  Octets envoyés : {net.bytes_sent}")
        print(f"  Octets reçus : {net.bytes_recv}")
        print(f"  Paquets envoyés : {net.packets_sent}")
        print(f"  Paquets reçus : {net.packets_recv}\n")

        print("Interfaces réseau :")
        interfaces = psutil.net_io_counters(pernic=True)
        for nom, stats in interfaces.items():
            print(f"  {nom} : Envoyés = {stats.bytes_sent}, Reçus = {stats.bytes_recv}")

        with open(fichier_log, "a", newline="") as fichier:
            writer = csv.writer(fichier)
            writer.writerow([
                horodatage,
                cpu_total,
                mem_used,
                disque_total_utilise,
                net.bytes_sent,
                net.bytes_recv
            ])

        print("\nTapez Ctrl+C pour quitter.")
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nProgramme terminé proprement.")
            break

display_dashboard()