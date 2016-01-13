# Cahier des charges
## Projet de serveur REST pour le robot Tardis

### Schéma de principe
![alt text](https://bytebucket.org/gostmasterys/web-tardis/raw/de2e72dd163250635503c681693c18de7ed9c585/Basic_block_diagram.png "block diagram")

### Client Web
#### Interface pour:
- Afficher les valeurs des capteurs (données brutes/ graph)
- Modifier les actuateurs
- Permettre l'envoi de scripts d'actions à effectuer par le robot (format des scripts à définir)
- Visualiser certain capteurs sous forme personalisée (ex: obstacles autour du robot)
- Créer facilement des scripts d'actions

### Serveur Web (Raspberry Pi)
- Fournit une API REST pour dialoguer avec le client web
- Route les commande du client avec les cartes Arduino et les données entre les cartes Arduino
- Enregistre et execute des scripts

### Cartes Arduino
- Utilisation de l'USB pour dialoger avec le serveur
- Serialisation des données via JSON

## Principal matériel à disposition
- (Arduino) carte de contrôle pour déplacement omnidirectionnel
- (Arduino) detecteur d'obstacles par ultrason
- (Arduino) système de récupération d'objets cylindriques
- (Raspberry Pi 2) caméra
- (Routeur Wifi) Dialogue avec le raspberry pi via TCP/UDP

## Data sensors channels (JSON)

    {
        "obstacles":[Vx,Vy]
    }

    {
        "new_pos":[x,y,teta]
    }

    {
        "mesured_pos":[x,y,teta]
    }

## Data script
    
    {
        "1":{{"channel_to_write":val},{"channel_to_read",condition_val}},
        "2":{{"channel_to_write":val},{"channel_to_read",condition_val}},
        "3":{{"channel_to_write":val},{"channel_to_read",condition_val}},
        "4":{{"channel_to_write":val},{"channel_to_read",condition_val}}
    }

## API routes

### Get

| Routes                        | Descrition                                                                            |
|---                            |---                                                                                    |
| /channels                     | Retourne la liste des canaux avec la dernière valeur écrite dedans en format JSON     |
| /channels/channel_name        | Retourne la valeur correspondante au nom du canal                                     |

### Post
| Routes                        | Descrition                                        |
|---                            |---                                                |
| /channels/channel_name        | Ecrit la valeur val sur le canal correspondant    |