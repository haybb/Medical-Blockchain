# Notes
Fichier contenant les notes relatives à la partie cryptographie.


## Stockage des données

### Protocole IPFS
Protocole pair-à-pair fonctionnant sur le principe de stockage chez chaque utilisateur (cf [IPFS](https://ipfs.io/)).
* __Avantages__
  1. Transferts rapide
  2. Stockage sans serveur
* __Inconvénients__
  1. Chaque node est visible
  2. Chaque identifiant de fichier est visible
* __Solutions__
  1. Chiffrement des données
* Connexion avec la blockchain:
  1. [iCommuty](https://icommunity.io/en/what-is-ifps-the-hard-drive-for-blockchain/)



## Chiffrement des données

### Chiffrement asymétrique
Utilisation de 2 clés par utilisateur: une publique et une privée. De ce fait, on chiffre avec la clé publique du destinataire qui est donc le seul à pouvoir décrypter le fichier avec sa clé perso. Les clés sont des produits de grands nombres premiers (cf [MAARS](https://maaars.fr/cryptographie-quelques-bases/)).
* __Avantages__
    1. Sécurité de la confidentialité entre chaque utilisateur
    2. On est sûr que le deestinataire est le bon (si c'est le mauvais, il ne pourra pas décrypter)
* __Inconvénients__
    1. Chiffrement à chaque transfert
    2. Lenteur du chiffrement
* __Solutions__
    1. Fichier toujours chiffré par chiffrement symétrique, et chiffrement asymétrique de la clé

### Chiffrement symétrique
Chiffrement d'un fichier qui génère une clé (cf [MAARS](https://maaars.fr/cryptographie-quelques-bases/)).
* __Avantages__
    1. Fichiers toujours chiffrés
    2. Rapidité
* __Inconvénients__
* __Solutions__


            
