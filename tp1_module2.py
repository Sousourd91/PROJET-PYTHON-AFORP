import re
import matplotlib.pyplot as plt
import csv

nom_fichier = "auth.log"

try:
    fichier = open(nom_fichier, "r")
    lignes = fichier.readlines()
    fichier.close()
except FileNotFoundError:
    print("Erreur : le fichier auth.log est introuvable.")
    exit()

ips_failed = []
ips_success = []

for ligne in lignes:
    if "Failed password" in ligne:
        ip_match = re.search(r"from ([\d\.]+)", ligne)
        if ip_match:
            ips_failed.append(ip_match.group(1))
    elif "Accepted password" in ligne:
        ip_match = re.search(r"from ([\d\.]+)", ligne)
        if ip_match:
            ips_success.append(ip_match.group(1))

compteur_failed = {}
compteur_success = {}

for ip in ips_failed:
    if ip in compteur_failed:
        compteur_failed[ip] += 1
    else:
        compteur_failed[ip] = 1

for ip in ips_success:
    if ip in compteur_success:
        compteur_success[ip] += 1
    else:
        compteur_success[ip] = 1

top_failed = sorted(compteur_failed.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 des IPs avec le plus d'échecs de connexion :")
for ip, count in top_failed:
    print(f"{ip} : {count} échecs")

ips = [ip for ip, _ in top_failed]
values = [count for _, count in top_failed]

plt.bar(ips, values)
plt.xlabel("Adresse IP")
plt.ylabel("Nombre d'échecs")
plt.title("Top 5 des IPs ayant échoué")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\nComparaison des tentatives réussies et échouées par IP commune :")
for ip in set(ips_failed + ips_success):
    echec = compteur_failed.get(ip, 0)
    succes = compteur_success.get(ip, 0)
    print(f"{ip} : {echec} échec(s), {succes} succès")

with open("resultats_logs.csv", "w", newline='') as fichier_csv:
    writer = csv.writer(fichier_csv)
    writer.writerow(["IP", "Échecs", "Succès"])
    for ip in set(compteur_failed.keys()).union(compteur_success.keys()):
        writer.writerow([ip, compteur_failed.get(ip, 0), compteur_success.get(ip, 0)])

print("\nLes résultats ont été enregistrés dans 'resultats_logs.csv'.")

while True:
    choix = input("\nEntrez une IP à analyser (ou tapez 'exit' pour quitter) : ")
    if choix.lower() == "exit":
        break
    if choix in compteur_failed or choix in compteur_success:
        print(f"\n{choix} :")
        print(f"  Échecs : {compteur_failed.get(choix, 0)}")
        print(f"  Succès : {compteur_success.get(choix, 0)}")
    else:
        print("IP inconnue.")
