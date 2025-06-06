import pandas as pd
import re
import matplotlib.pyplot as plt

try:
    with open("access.log", "r") as f:
        lignes = f.readlines()
except FileNotFoundError:
    print("Fichier 'access.log' introuvable.")
    exit()

ips = []
datetimes = []
methods = []
urls = []
statuses = []
user_agents = []

for ligne in lignes:
    try:
        match = re.match(r'(\S+) - - \[(.*?)\] "(.*?)" (\d{3}) .* "(.*?)"$', ligne)
        if match:
            ip = match.group(1)
            datetime = match.group(2)
            request = match.group(3)
            status = int(match.group(4))
            user_agent = match.group(5)

            parts = request.split()
            if len(parts) >= 2:
                method = parts[0]
                url = parts[1]
            else:
                method = ""
                url = ""

            ips.append(ip)
            datetimes.append(datetime)
            methods.append(method)
            urls.append(url)
            statuses.append(status)
            user_agents.append(user_agent)
    except:
        pass

df = pd.DataFrame({
    "ip": ips,
    "datetime": datetimes,
    "method": methods,
    "url": urls,
    "status": statuses,
    "user_agent": user_agents
})

print("\nAperçu des données :")
print(df.head())

erreurs_404 = df[df["status"] == 404]

top_5 = erreurs_404["ip"].value_counts().head(5)
print("\nTop 5 IPs avec le plus d'erreurs 404 :")
print(top_5)

plt.figure()
plt.bar(top_5.index, top_5.values, color='orange')
plt.title("Top 5 des IPs responsables d'erreurs 404")
plt.xlabel("Adresse IP")
plt.ylabel("Nombre d'erreurs 404")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

bot_keywords = ["bot", "crawler", "spider"]
def est_bot(ua):
    ua = ua.lower()
    for mot in bot_keywords:
        if mot in ua:
            return True
    return False

df["is_bot"] = df["user_agent"].apply(est_bot)

erreurs_404_bots = df[(df["status"] == 404) & (df["is_bot"] == True)]

total_404 = len(erreurs_404)
total_404_bots = len(erreurs_404_bots)

pourcentage_bots = (total_404_bots / total_404 * 100) if total_404 > 0 else 0

print(f"\nNombre total d’erreurs 404 : {total_404}")
print(f"Erreurs 404 provenant de bots : {total_404_bots}")
print(f"Pourcentage des 404 causées par des bots : {pourcentage_bots:.2f}%")

ips_bots = erreurs_404_bots["ip"].value_counts()
print("\nIPs suspectes (bots ayant généré des erreurs 404) :")
print(ips_bots.head(5))

print("\n--- Discussion ---")
print("Certaines IPs génèrent un grand nombre d'erreurs 404.")
print("Une part non négligeable provient de bots.")
print("Il serait pertinent de bloquer ces IPs via firewall ou config Apache.")
print("Ce type de script peut être automatisé pour tourner régulièrement.")
