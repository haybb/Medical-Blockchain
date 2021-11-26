# Notes
Fichier contenant les notes relatives à la partie cryptographie.

## Important

* Une idée d'utilisation de la blockchain pour les dossiers médicaux: [Wikipedia](https://en.wikipedia.org/wiki/Privacy_and_blockchain#Health_care_records)




## Sommaire

* __Stockage des données__
  1. Protocole IPFS
* __Chiffrement des données__
  1. Chiffrement asymétrique
  2. Chiffrement symétrique
* __Lien entre les 2 parties__
* __Sécurité et confidentialité__
  1. Première idée
* __Projet final__
  1. Structure globale
  2. Chiffrement
  3. Transfert des fichiers

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
* __Algorithmes__
    1. [RSA](https://fr.wikipedia.org/wiki/Chiffrement_RSA) (chiffrement et signature)
    2. [DSA](https://fr.wikipedia.org/wiki/Digital_Signature_Algorithm) (signature)

#### Chiffrement symétrique

Chiffrement d'un fichier qui génère une clé (cf [MAARS](https://maaars.fr/cryptographie-quelques-bases/)).  
Il existe 2 types de chiffrement symétrique: [par flot](https://fr.wikipedia.org/wiki/Chiffrement_par_flot) et [par bloc](https://fr.wikipedia.org/wiki/Chiffrement_par_bloc) (pour plus d'infos: [PDF](http://iml.univ-mrs.fr/~rodier/Cours/Blocs.pdf)). Le premier chiffre l'entièreté du fichier, peu importe sa longueur. Le deuxième va séparer le fichier en blocs (norme actuelle 128 bits) et les chiffrer séparément.
* __Avantages__
    1. Fichiers toujours chiffrés
    2. Rapidité
* __Inconvénients__
    1. Les clés doivent être à usage unique
    2. Les clés doivent être transmises de manière cryptée
* __Solutions__
    1. Réencoder le fichier pour chaque nouvel utilisateur
    2. Transmettre les clés à l'aide d'un chiffrement asymétrique
* __Algorithmes__
    1. [linux.goffinet.org](https://linux.goffinet.org/administration/confidentialite/chiffrement-symetrique)
    2. [AES](https://fr.wikipedia.org/wiki/Standard_de_chiffrement_avanc%C3%A9)


## Lien entre les deux parties
Le protocole IPFS permet un transfert rapide et un stockage facile des fichiers. En effet, aucune donnée n'a besoin d'être stockée sur serveur étant donné qu'elles se trouvent sur les ordinateurs des utilisateurs. De même, ceci assure la plupart du temps une proximité entre ordinateurs qui permet de gagner en temps.

Pour la partie chiffrement, il est possible (même très fortement conseillé) d'en mixer plusieurs. Par exemple, il serait intelligent d'associer chiffrement symétrique et asymétrique:

  1. On encode le fichier en chiffrement symétrique, générant ainsi une clé qui lui est associé. Ce processus est assez rapide.
  2. On transmet ensuite la clé auparavant chiffrée asymétriquement. En effet, ce dernier est un processus long et coûteux informatiquement (et temporellement) car il faut travailler sur les nombres premiers. Plus le fichier à chiffrer est lourd, plus il faudra de temps pour le crypter. Ainsi, en ne chiffrant qu'une clé de petite taille, on gagne un temps considérable.  

Cet enchaînement de chiffrements permet de gagner en temps et d'augmenter la sécurité: tous les fichiers stockés sont cryptés, ainsi quelqu'un qui en fait la demande ne pourra l'ouvrir sans la clé nécéssaire (il est d'ailleurs évident qu'on ne peut stocker les fichiers en clair, donc un cryptage du type du symétrique est nécéssaire). Aussi, ça nous évite de chiffrer asymétriquement le fichier à chaque envoi, ce qui est long et compliqué pour des machines de faible puissance.


## Sécurité et confidentialité
Le but de ce TIPE étant d'obtenir une grande flexibilité sur la gestion de la vie privée des personnes, il est nécéssaire de construire les dossiers médicaux en plusieurs parties indépendantes les unes des autres afin de pouvoir modifier les autorisations d'accès à ces parties à tout moment.

#### Première idée

Une des possibilités est de découper chaque dossier en plusieurs parties, qui seront stockées ensemble ou non.  
Par exemple, il est possible de distinguer les données identitaires d'une personne, les maladies qu'elle a eu (contenant donc les symptômes et éventuels traitemens aboutissant ou non à une guérison), les interventions chirurgicales, les problèmes de santé ne nécéssitant pas spécialement de recherche (fractures, entorses...). On peut ainsi obtenir un dossier complet constitué de différentes parties qui ne serait accessibles qu'en fonction de l'utilisateur: un médecin et le patient devraient avoir accès à toutes les données, un centre de recherches qu'aux parties rapportant les maladies sans connaître l'identité du malade, les assurances qu'à la liste des opérations et traitement (avec l'identité) sans savoir les résultats...  
Il devient ainsi possible de modifier la confidentialité à tout moment: si une personne qui avait donné son identité avec la partie maladie à un centre de recherche veut réobtenir son anonymat, il suffit de changer l'autorisation d'accès à la partie identité. Ainsi, ces centres ne seront plus en capacité de recevoir ces données, ou tout du moins de les décrypter.  

* __Première méthode:__ on classe chaque utilisateur dans des types: patient, médecin, recherche... Et chaque type possède sa propre clé - une sorte d'identificateur - qui permet ou non d'ouvrir chaque dossier. Mais il faudrait donc avoir une seule clé qui puisse déchiffrer chaque partie du dossier. Ainsi, la sécurité serait réduite. Et ce n'est donc plus du chiffrage symétrique classique puisqu'une clé n'est pas unique à un fichier.
* __Deuxième méthode:__ même principe pour les types, mais on en crée aussi pour les parties des dossiers. Ainsi chaque type d'utilisateur possède une clé correspondant à chaque type du dossier. On a ainsi juste à changer le chiffrement d'une partie du dossier lorsqu'on veut modifier qui y a accès. Mais il faudrait que chaque fichier soit dupliqué et chiffré differemment, ce qui nécéssite beaucoup plus d'espace de stockage.

Le principal problème réside dans la méthode de chiffrerment des données. En effet, un algorithme de chiffrement symétrique impose de changer la clé à chaque nouvel envoi: on ne peut donc pas gérer la confidentiatlié grâce à elle. Et si on ne le changeait pas à chaque nouvel envoi, la sécurité serait d'un coup réduite de manière conséquente. Il faut donc privilégier soit la sécurité, soit la facilité *(spoil: on va chercher d'autres méthodes de chiffrement)*.


## Projet final
#### Structure globale
Les utilisateurs seront classés selon différentes catégories afin de pouvoir identifier les autorisations de chacun (cf [notes_globales.md](../notes_globales.md)).  
Chaque dossier médical sera divisé en plusieurs parties (cf [notes_globales.md](../notes_globales.md)). Elles seront regroupées ensemble et une clé d'identification y sera attribuée, c'est cette dernière qui sera envoyé dans la blockchain.  
Ainsi, il est plus facile d'identifier chaque changement sur les fichiers, de n'envoyer uniquement les fichiers auxquels un utilisateur à le droit d'avoir accès, etc.  

Pour identifier chaque utilisateur, une paire clé publique / clé privée sera attribuée à chacun. La clé publique sera stockée dans une base de données avec l'identifiant de l'utilisateur et son type.  
Lorsqu'un utilisateur voudra accéder à un fichier, il lui faudra transmettre la clé d'identification du dossier médical, chiffrée avec sa clé privée. Ainsi le serveur pourra l'identifier en retrouvant sa clé publique dans la base de données, et ensuite vérifier les autorisations en fonction de son type et du dernier bloc de la blockchain. Il pourra ensuite transmettre les fichiers chiffrés avec la clé publique de l'utilisateur (cf [cette image](diagramme_requetes.jpeg)).  
Lors de l'envoi d'un fichier, le même principe de requête est effectué, avec le fichier chiffré. Le serveur vérifie alors les autorisations de modification et le cas échéant, modifie le fichier stocké (cf [la même image](diagramme_requetes.jpeg)).

#### Chiffrement
Les dossiers médicaux stockés dans le(s) serveurs(s) seront divisés en plusieurs parties et chiffrés de manière symétrique, seul le serveur aura accès aux clés pour les rassembler et les déchiffrer. Le chiffrement symétrique sera par blocs, ce qui permet de chiffrer les différents blocs d'un dossier séparément. On utilisera l'algorithme [AES](https://fr.wikipedia.org/wiki/Standard_de_chiffrement_avanc%C3%A9) qui est aujourd'hui le plus répandu et donc plus simple à étudier pour ce TIPE.  
Les couples de clés publique/privée seront générées via l'algorithme [RSA](https://fr.wikipedia.org/wiki/Chiffrement_RSA), choix fait pour les mêmes raisons que pour AES.
Les requêtes entre utilisateurs et serveur seront chiffrées en asymétrique afin de pouvoir identifier chaque utilisateur, et ainsi son type. Le message sera constitué de l'identification de l'utilisateur concaténée avec la requête chiffrée. De ce fait, il sera plus rapide de l'identifier (et si ce n'est pas le bon, on cherchera quand même partout).

#### Transfert des fichiers
Méthode classique: combinaison des chiffrements symétrique et asymétrique.
En ce qui concerne l'asymétrique, on utilisera un [mécanisme d'authentification](https://fr.wikipedia.org/wiki/Cryptographie_asym%C3%A9trique#M%C3%A9canismes_d'authentification).