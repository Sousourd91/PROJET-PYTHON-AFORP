import re

adresse_pattern = (r"^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}$")
adresse = input("Entrez une adresse IP")

if re.match(adresse_pattern, adresse):
        print("Adresse Valide")

else:
        print("Adresse non Valide") 