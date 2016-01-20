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

### External publisher
Canaux sur lesquels les différents capteurs du robot publient leurs mesures.

    {
        "avoid_direction":[Vx,Vy]
    }

    {
        "mesured_pos":[x,y,teta]
    }

    {
        "ultrasonic":[u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11]
    }

### External subscriber
Canaux permetant de donner des consignes aux péripheriques du robot.

### External subscriber

    {
        "new_pos":[x,y,teta]
    }

## API routes
Les différentes routes suivantes nous permet d'accèder à nos canaux et permet de changer les valeurs qui y sont ou de monitorer les valeurs.
### Get

| Routes                        | Descrition                                                                            |
|---                            |---                                                                                    |
| /channels                     | Retourne la liste des canaux avec la dernière valeur écrite dedans en format JSON     |
| /channels/channel_name        | Retourne la valeur correspondante au nom du canal                                     |

### Post
| Routes                        |Descrition                                     |
|---                            |---                                            |
| /channels/channel_name        | Indique sur quel canal on change la valeur    |

#### Contenu de la requète POST
Les données de la requète HTTP POST contiennent une valeur en JSON comme suit:
{"nom_canal": valeur}


# Raspberry Pi Configuration
This is the configuration used for the hosting raspberry pi

## Network Interface
In /etc/network/intefaces:

No changes to the loopback interface

    auto lo
    iface lo inet loopback

Configure a static ip on eth0

    iface eth0 inet static
    address 192.168.0.5
    netmask 255.255.255.0
    gateway 192.168.0.1
    dns-nameserver 8.8.8.8

## Retrive project sources
> mkdir ~/Prog
> cd ~/Prog
> git clone https://github.com/thierryme

## Install python dependencys
> sudo apt-get install && sudo apt-get update

> sudo apt-get install python-pip

> sudo pip install -r ~/Prog/tardis-rest/requirements.txt

## Consistent naming of Arduino tty
In order to have the same tty name at each reboot of the raspberry pi for each Arduino card, a special Udev rule is created.

First plug an Arduino card into an USB port.
Then retrive the KERNELS informaton with the following command:
> udevadm info -a -n /dev/ttyACM0 | grep KERNELS

Get the first line without a ':'. If for exemple you have "1-1.2.4"  then edit/create the following file accordingly:
> sudo vim /etc/udev/rules.d/99-arduino.rules

    SUBSYSTEM=="tty", KERNEL=="ttyACM*", KERNELS=="1-1.2.4", SYMLINK+="ttyACM0001"

Where 'ttyACM0001' is a tty name wich will refer to the port you pluged your Arduino in. Change this name to fit to your need.
Now the Arduino serial port should be accessible trough '/dev/ttyACM0001'.
Repeat this operation for each port and give an appropriate tty name (...0002).
(see: http://hintshop.ludvig.co.nz/show/persistent-names-usb-serial-devices/ or https://wiki.archlinux.org/index.php/arduino)

## Arduino dependencys
- ArduinoJson
- Mecanum4WD
- Sonicsense
- Spots
