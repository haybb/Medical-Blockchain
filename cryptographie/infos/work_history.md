# Historique de la partie cryptographie
Ce document est utilisé pour retracer l'historique du travail effectué dans la partie cryptographie.


## Commit n°1
*(Commit 55d88a5a6e2124cd5d7791b640f4602a1d15dd6e)*

Étape | Description
----- |-------------
Fichier *files.py* |Fonction *saveFile* : sauvegarde des données dans un fichier; fonction *loadJson* : lit in fichier json; fonction *saveJson* : sauvegarde un json dans un fichier json.
Fichier *data_manager.py* | Classe *DataManager* : sert à gérer des données. Contient les fonctions *createUser* (deviendra *newUser*) (crée un nouvel utilisateur, pas encore implémentée) et *_saveFile* (sauvegarde un fichier dans les données).
Fichier *encryption.py* | Fonction *hash256* : retourne le hash 256 d'un objet; fonction *areTheSame* : compare le hash 256 de 2 objets; fonction *minstd* : génère un noveau nombre basé sur l'algorithme *minstd*.
Fichier *medical_parts.py* | Quelques classes inutiles utilisées pour représenter un dossier médical : *HealthData*, *MedicalBackground*, *Prescription*, *PrivateData*.
Fichier *medical_record.py* | Classe *MedicalRecord* : représente le dossier médical d'un patient (pour l'illustration).



## Commit n°2
*(Commit 11b7e82850f6c245614179289409afa3da1d2154)*

Étape | Description
----- |-------------
Comte-rendu ingé | Compte-rendu de l'appel avec la tante d'Hugo qui travaille comme ingénieur informatique à l'hôpital de Besançon.
Fichier *data_manager.py* | Création d'un log utilisé dans tous les fichiers, initialisé dans la fonction *initializeLogger*; manipulation des utilisateurs avec les fonctions *newUser*, *_createUser*, *_getUser*, *_modifyUser* et *_deleteUser*; ajout de la fonction *_loadFile*; implémentation de la fonction *loadFile*.
Fichier *files.py* | Complément de la fonction *saveFile*.
Fichier *tree.py* | Création d'un arbre utilisé pour stocker des clés. Accepte uniquement des caractères [ASCII](https://www.ascii-code.com/) (pas étendu); fonction *isASCII*: vérifie qu'une *string* est bien composée uniquement de caractères ASCII; classe *ASCIITree* : représente un arbre ASCII. Contient les fonctions *append* (ajoute une clé), *remove* (retire une clé), *getInfos* (récupère les infos stockées avec une clé), *_allStrings* (renvoie une liste contenant toutes les clés), *\_\_contains\_\_*, *\_\_repr\_\_*.
Fichier *encryption.py* | Complément de la fonction *minstd* (stocke désormais le dernier nombre dans un fichier); fonction *newKeyPair*: renvoie une paire de clés publique/privée; fonction *containsKey*: vérifie si une clé est déjà stockée dans un arbre.


## Commit n°3
*(Commit en cours)*

Étape | Description
----- |-------------
Fichier *data_manager.py* | Fonction *getDirectories* : renvoie tous les "path" de la liste menant a un dossier.
Fichier *files.py* | Fonction *saveToBlockchain* : sauvegarde des données dans la blockchain; fonction *loadFromBlockchain* : récupère des données depuis la blockchain.
