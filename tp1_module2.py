fichier = open("auth.log", "r")
lignes = fichier.readlines()
fichier.close()

lignes_echec = []
for ligne in lignes:
    if "Failed password" in ligne:
        lignes_echec.append(ligne)

import re
ips = []
for ligne in lignes_echec:
    resultat = re.search(r"from ([\d\.]+)", ligne)
    if resultat:
        ip = resultat.group(1)
        ips.append(ip)

compteur_ip = {}
for ip in ips:
    if ip in compteur_ip:
        compteur_ip[ip] += 1
    else:
        compteur_ip[ip] = 1

liste_triee = sorted(compteur_ip.items(), key=lambda x: x[1], reverse=True)

print("Top 5 des IPs avec le plus d'échecs :")
for i in range(5):
    print(liste_triee[i][0], ":", liste_triee[i][1], "échecs")
