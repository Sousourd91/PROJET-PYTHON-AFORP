import random
import os

fichier_path = "mots_de_passe.txt"
if os.path.exists(fichier_path):
    with open(fichier_path, "r") as fichier:
        mots_de_passe_faibles = [ligne.strip() for ligne in fichier.readlines() if ligne.strip()]
    if not mots_de_passe_faibles:
        mots_de_passe_faibles = ["123456", "password", "admin", "123456789", "qwerty", "abc123", "letmein", "welcome", "monkey", "football"]
else:
    mots_de_passe_faibles = ["123456", "password", "admin", "123456789", "qwerty", "abc123", "letmein", "welcome", "monkey", "football"]

mot_secret = random.choice(mots_de_passe_faibles)

max_essais = input("Entrez le nombre maximum d'essais (ou appuyez sur Entrée pour illimité) : ")
if max_essais.isdigit():
    max_essais = int(max_essais)
else:
    max_essais = None  

triche = input("Voulez-vous activer le mode triche ? (oui/non) : ")
if triche.lower() == "oui":
    print(f"[Triche] Le mot de passe est : {mot_secret}")

print("\nEssayez de deviner le mot de passe faible !")

trouve = False
essais = 0
historique = []

while not trouve:
    tentative = input("Mot de passe ? ")
    essais += 1
    historique.append(tentative)

    if tentative == mot_secret:
        trouve = True
        print("\n✅ Bravo ! Vous avez trouvé le mot de passe.")
        print(f"Nombre total d'essais : {essais}")
        break
    else:
        if len(tentative) > len(mot_secret):
            print("Indice : le mot est plus court.")
        elif len(tentative) < len(mot_secret):
            print("Indice : le mot est plus long.")
        if tentative and tentative[0] == mot_secret[0]:
            print("Indice : il commence par la même lettre.")
        lettres_communes = set(tentative) & set(mot_secret)
        print(f"Indice : {len(lettres_communes)} lettre(s) en commun.\n")

    if max_essais is not None and essais >= max_essais:
        print("\n❌ Échec. Nombre maximum d'essais atteint.")
        print(f"Le mot de passe était : {mot_secret}")
        break

print("\nHistorique des tentatives :")
for i, essai in enumerate(historique, 1):
    print(f"{i}. {essai}")