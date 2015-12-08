# Cahier des charges - Projet serveur REST pour le robot Tardis


## Client Web
### Interface pour:
- Afficher les valeurs des capteurs (données brutes/ graph)
- Modifier les actuateurs
- Permettre l'envoi de scripts d'actions à effectuer par le robot (format des scripts à définir)
- Visualiser certain capteurs sous forme personalisée (ex: obstacles autour du robot)
- Créer facilement des scripts d'actions

## Serveur Web (Raspberry Pi)
- Fournit une API REST pour dialoguer avec le client web
- Route les commande du client avec les cartes Arduino et les données entre les cartes Arduino
- Enregistre et execute des scripts

## Cartes Arduino
- Utilisation de l'USB pour dialoger avec le serveur
- Serialisation des données via JSON

# Principal matériel à disposition
- (Arduino) carte de contrôle pour déplacement omnidirectionnel
- (Arduino) detecteur d'obstacles par ultrason
- (Arduino) système de récupération d'objets cylindriques
- (Raspberry Pi 2) caméra
- (Routeur Wifi) Dialogue avec le raspberry pi via TCP/UDP


![alt text](./basic_block_diagram.png "block diagram")