import pandas as pd
import re

fichier = open("access.log", "r")
lignes = fichier.readlines()
fichier.close()

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
            status = match.group(4)
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
            statuses.append(int(status))
            user_agents.append(user_agent)

    except:
        pass

donnees = pd.DataFrame({
    "ip": ips,
    "datetime": datetimes,
    "method": methods,
    "url": urls,
    "status": statuses,
    "user_agent": user_agents
})

print("Aperçu du DataFrame :")
print(donnees.head())

erreurs_404 = donnees[donnees["status"] == 404]

ips_top = erreurs_404["ip"].value_counts().head(5)

print("\nTop 5 des IPs avec le plus d'erreurs 404 :")
print(ips_top)

import matplotlib.pyplot as plt

plt.bar(ips_top.index, ips_top.values)
plt.title("Top 5 des IPs générant des erreurs 404")
plt.xlabel("Adresse IP")
plt.ylabel("Nombre d'erreurs 404")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
