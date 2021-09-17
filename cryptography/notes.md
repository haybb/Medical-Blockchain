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

#### Chiffrement asymétrique
Utilisation de 2 clés par utilisateur: une publique et une privée. De ce fait, on chiffre avec la clé publique du destinataire qui est donc le seul à pouvoir décrypter le fichier avec sa clé perso. Les clés sont des produits de grands nombres premiers (cf [MAARS](https://maaars.fr/cryptographie-quelques-bases/)).
* __Avantages__
    1. Sécurité de la confidentialité entre chaque utilisateur
    2. On est sûr que le deestinataire est le bon (si c'est le mauvais, il ne pourra pas décrypter)
* __Inconvénients__
    1. Chiffrement à chaque transfert
    2. Lenteur du chiffrement
* __Solutions__
    1. Fichier toujours chiffré par chiffrement symétrique, et chiffrement asymétrique de la clé

#### Chiffrement symétrique
Chiffrement d'un fichier qui génère une clé (cf [MAARS](https://maaars.fr/cryptographie-quelques-bases/)).
* __Avantages__
    1. Fichiers toujours chiffrés
    2. Rapidité
* __Inconvénients__
* __Solutions__


## Lien entre les deux parties
Le protocole IPFS permet un transfert rapide et un stockage facile des fichiers. En effet, aucune donnée n'a besoin d'être stockée sur serveur étant donné qu'elles se trouvent sur les ordinateurs des utilisateurs. De même, ceci assure la plupart du temps une proximité entre ordinateurs qui permet de gagner en temps.

Pour la partie chiffrement, il est possible (même très fortement conseillé) d'en mixer plusieurs. Par exemple, il serait intelligent d'associer chiffrement symétrique et asymétrique:
1. On encode le fichier en chiffrement symétrique, générant ainsi une clé qui lui est associé. Ce processus est assez rapide.
2. On transmet ensuite la clé auparavant chiffrée asymétriquement. En effet, ce dernier est un processus long et coûteux informatiquement (et temporellement) car il faut travailler sur les nombres premiers. Plus le fichier à chiffrer est lourd, plus il faudra de temps pour le crypter. Ainsi, en ne chiffrant qu'une clé de petite taille, on gagne un temps considérable.
Cet enchaînement de chiffrements permet de gagner en temps et d'augmenter la sécurité: tous les fichiers stockés sont cryptés, ainsi quelqu'un qui en fait la demande ne pourra l'ouvrir sans la clé nécéssaire (il est d'ailleurs évident qu'on ne peut stocker les fichiers en clair, donc un cryptage du type du symétrique est nécéssaire). Aussi, ça nous évite de chiffrer asymétriquement le fichier à chaque envoi, ce qui est long et compliqué pour des machines de faible puissance.
