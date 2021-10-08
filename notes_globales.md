# Notes globales
Ce fichier contient toutes les notes utiles pour mettre en relation les 2 parties du TIPE (blockchain et cryptographie)  
Seront notées en _italique_ les nouvelles infos.


## Utilisateurs
Pour gérer les différents utilisateurs, il faudra leur affecter un type parmi les suivants _(à compléter)_:

* _Patient_
* _Médecin_
* _Assurance_
* _Recherche_


## Dossiers médicaux
Pour gérer les autorisations d'accès aux différentes parties d'un dossier, il faudra découper ce dernier en plusieurs parties _(à compléter)_:

* __Infos personnelles:__ _nom, prénom, date de naissance, adresse, numéro de sécurité sociale..._
* __Antécédents:__ _les différentes maladies, blessures, etc. et leurs remèdes, qu'ils aient réussi ou pas_
* __Infos de santé importantes:__ _maladies actuelles, allergies..._




## Blockchain
Cette blockchain regroupera l'ensemble des patients. Ainsi, on ne gérera qu'une seule chaine, et celle-ci sera actualisée très souvent. Cela permet d'éviter son piratage.  
Les hash sont effectués en __sha256__.
Dans chaque bloc de la blockchain seront stockées les infos suivantes:

* Numéro du bloc
* Hash du bloc
* Hash du bloc précédent
* Horodatage
* Numéro de validation du bloc
* Données ajoutées

Dans les données, on trouvera (placées à la création du premier bloc) les infos suivantes:

* _Numéro d'identification du patient_
* _Les différentes autorisations en fonction de chaque type d'utilisateur_
* _Log (dernières actions sur le dossier, par qui et quand)_

Ce seront les seules infos à ajouter dans la blockchain, afin d'éviter qu'elle ne devienne trop lourde.