# Liste de toutes les fonctions pouvant être utilisées extérieurement

## Requêtes
*Remplir ici toutes les fonctions recquises extérieurement.*
Fonction | Rôle
---------|------
exemple | Ceci est un exemple.


## Fichier *files.py*
Fonction `saveFile` :
- **Rôle :** sauvegarde des données dans un fichier donné.
- **Paramètres :** 
    - `data` *(object)* : les données à sauvegarder dans le fichier.
    - `filePath` *(str)* : le chemin vers le fichier.
    - `overwrite` *(bool)* : `True` par défaut; si `True`, écrase le fichier et remplace son contenu par les données; si `False`, ajoute les données à la suite du fichier.
    - `binary` *(bool)* : `False` par défaut; indique si le fichier est binaire ou non.
- **Retour :** `None`.

Fonction `loadFile` :
- **Rôle :** récupère les données d'un fichier donné.
- **Paramètres :** 
    - `filePath` *(str)* : le chemin vers le fichier.
    - `binary` *(bool)* : `False` par défaut; indique si le fichier est binaire ou non.
- **Retour :** *object*; les données stockées dans le fichier.

Fonction `saveJson` :
- **Rôle :** sauvegarde des données au format JSON dans un fichier JSON.
- **Paramètres :** 
    - `data` *(dict or list)* : les données JSON à sauvegarder dans le fichier.
    - `filePath` *(str)* : le chemin vers le fichier.
    - `sortKeys` *(bool)* : `False` par défaut; indique si les données doivent être triées par leur clé ou non.
- **Retour :** `None`.

Fonction `loadJson` :
- **Rôle :** récupère les données d'un fichier JSON.
- **Paramètres :** 
    - `filePath` *(str)* : le chemin vers le fichier.
- **Retour :** *dict or list*; les données stockées dans le fichier.


## Fichier *encryption.py*
Fonction `hash256` :
- **Rôle :** renvoie le hash 256 d'un objet.
- **Paramètres :** 
    - `obj` *(object)* : l'objet à "hasher".
- **Retour :** *bytes*; le hash 256 de l'objet.

Fonction `areTheSame` :
- **Rôle :** vérifie si deux objets sont identiques (au niveau de leur hash 256).
- **Paramètres :** 
    - `obj1` *(object)* : le 1er objet à comparer.
    - `obj2` *(object)* : le 2e objet à comparer.
- **Retour :** *(bool)*; `True` si les deux hash 256 sont identiques.

Fonction `minstd` :
- **Rôle :** renvoie un nouveau nombre aléatoire basé sur l'algorithme minstd, en suivant le "minimum standard" de Park, Miller et Stockmeyer.
- **Paramètres :** 
    - `lastNumber` *(int)* : le dernier nombre avoir été généré par l'algorithme.
    :warning: ATTENTION : le paramètre `lastNumber` doit toujours être présent, sinon l'ancien nombre généré sera récupéré dans un fichier inexistant.
- **Retour :** *int*; le nombre généré.

Fonction `newKeyPair` :  
:information_source: utilise le module [Crypto](https://pycryptodome.readthedocs.io/en/latest/src/introduction.html).
- **Rôle :** génère une nouvelle paire de clés publique/privée.
- **Paramètres :** aucun.
- **Retour :** *tuple\[Crypto.RSA.RsaKey, Crypto.RSA.RsaKey\]*; la première clé est la clé publique, la deuxième la privée.


## Fichier *users.py*
Liste `userTypes`
- **Rôle :** représente tous les types d'utilisateurs possibles.
- **Type :** *list\[str\]*.


Classe `User` : 
- **Rôle :** représente un utilisateur.
- **Paramètres :** 
    - `uniqueID` *(int)* : l'identifiant de l'utilisateur. :warning: DOIT être unique.
    - `userType` *(str)* : le type d'utilisateur. Doit correspondre à un type contenu dans `userTypes`.
    - arguments supplémentaires : les différentes infos supplémentaires concernant l'utilisateur.
- **Méthodes :** 
    - `getID` : renvoie l'ID de l'utilisateur *(int)*.
    - `getInfos(key: str)` : renvoie les infos de l'utilisateur stockées sous la clé `key`.
    - Il est possible de comparer 2 utilisateurs avec `user1 == user2`.