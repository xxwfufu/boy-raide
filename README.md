# Discord Bot - Lanceur Bot Discord

Un bot Discord écrit en Python utilisant `discord.py` avec une interface graphique Tkinter pour lancer le bot facilement.

---

## Fonctionnalités

- Commandes pour créer/supprimer des salons, rôles
- Bannir ou expulser tous les membres
- Envoyer des messages en DM à tous les membres
- Spam de messages dans les salons ou via webhook
- Changer le nom du serveur
- Interface simple avec logs en temps réel

---

## Commandes disponibles (préfixe `+`)

| Commande     | Description                                                       |
|--------------|------------------------------------------------------------------|
| `+ping`      | Vérifie que le bot est actif, répond "Pong!"                    |
| `+crchannels`| Crée plusieurs salons (textuels ou vocaux)                      |
| `+spamchannels` | Envoie un message en spam dans tous les salons textuels      |
| `+banall`    | Bannis tous les membres non-bots (sauf exclusions)              |
| `+kickall`   | Expulse tous les membres non-bots (sauf exclusions)             |
| `+dmmembers` | Envoie un message privé (DM) à tous les membres non-bots        |
| `+createroles` | Crée plusieurs rôles avec un nom donné                        |
| `+servname`  | Change le nom du serveur                                         |
| `+webhookspam` | Spam un webhook avec un message choisi (5 fois)                |
| `+dlchannels` | Supprime tous les salons du serveur                             |

---

## Installation & Utilisation

1. Cloner ce dépôt

```bash
git clone https://github.com/ton-utilisateur/ton-depot.git
cd ton-depot
Installer les dépendances

bash
Copier
Modifier
pip install -r requirements.txt
Lancer le script Python

bash
Copier
Modifier
python main.py
Entrer le token de votre bot Discord dans l’interface, puis cliquer sur Lancer le bot.

Prérequis
Python 3.10 ou supérieur

Bibliothèques Python : discord.py, tkinter (inclus par défaut dans Python sous Windows/Mac)

Token de bot Discord (à créer sur https://discord.com/developers/applications)

Notes
Le bot doit avoir les permissions nécessaires (gestion des salons, rôles, membres) dans votre serveur Discord.

Certaines commandes peuvent prendre du temps selon la taille du serveur.

Utilisez les commandes avec précaution, certaines (banall, kickall, dlchannels) sont destructrices.

Licence
Ce projet est libre, à utiliser à vos risques et périls.

Auteur
xxwfufu
