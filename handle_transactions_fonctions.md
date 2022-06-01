## Fichier *handle_transactions.py*

Fonction `request_info` :
- **Rôle :** format du message à mettre dans la blockchain pour la demande d'informations par le médecin au spécialiste.
- **Paramètres :**
  - `minstd` *(int)* : dernier minstd.
  - `requestedObject` *(str)* : objet de la requête.
  - `ipp` *(int)*: identifiant permanent du patient.
  - `rpps` *(int)*: répertoire partagé des professionnels de santé (identifiant professionnel).
  - `ip` *(int)*: addresse ip de l'envoyeur.
  - `recipientPublicKey` *(object)* : clé publique RSA du destinataire.
  - `senderPrivateKey` *(object)* : clé privée RSA de l'envoyeur.
- **Retour :** dictionnaire avec le message et le minstd, afin d'établir une transaction 'aller' dans la blockchain.


Fonction `send_symmetric_key` :
- **Rôle :** format du message à mettre dans la blockchain pour l'envoi de la clé symétrique par le spécialiste au médecin.
- **Paramètres :**
  - `minstd` *(int)* : dernier minstd.
  - `symmetricKey` *(object)* : clé symétrique à envoyer.
  - `tag` *(bytes)*: attribut tag associé.
  - `nonce` *(bytes)*: attribut nonce associé.
  - `recipientPublicKey` *(object)* : clé publique RSA du destinataire.
  - `senderPrivateKey` *(object)* : clé privée RSA de l'envoyeur.
- **Retour :** dictionnaire avec le message et le minstd, afin d'établir une transaction 'retour' dans la blockchain.


Fonction `decrypt_info` :
- **Rôle :** décrypte le message donné.
- **Paramètres :**
  - `data` *(bytes)* : message à décoder
  - `recipientPublicKey` *(object)* : clé publique RSA du destinataire.
  - `senderPrivateKey` *(object)* : clé privée RSA de l'envoyeur.
- **Retour :** liste contenant les différents éléments décryptés dans le message, une liste contenant l'erreur si la 
signature RSA est invalide.


Fonction `send_transaction` :
- **Rôle :** envoi de la transaction dans le réseau blockchain avec les paramètres donnés.
- **Paramètres :**
  - `blockchain` *(object)* : blockchain où la transaction sera ajoutée.
  - `sender` *(str)* : portefeuille associé à la blockchain, le 'wallet', de l'envoyeur.
  - `recipient` *(str)*: wallet du receveur.
  - `quantity` *(float)*: quantité de tokens à transférer.
  - `data` *(object)* : message à attacher à la transaction.
- **Retour :** None.


Fonction `read_transaction` :
- **Rôle :** lecture des dernières transactions qui nous sont adressés dans le réseau blockchain.
- **Paramètres :**
  - `stored_blockchain` *(object)* : copie de la blockchain sur le pc de l'envoyeur.
  - `new_blockchain` *(object)* : nouvelle blockchain, qui peut avoir changé s'il y a une/des nouvelle(s) transaction(s).
  - `address` *(str)*: wallet de l'envoyeur.
- **Retour :** la nouvelle blockchain et une liste des nouvelles transactions.


Fonction `last_minstd` :
- **Rôle :** cherche le dernier numéro minstd enregistré dans la blockchain.
- **Paramètres :**
  - `blockchain` *(object)* : blockchain donnée.
- **Retour :** dernier minstd trouvé *(int)* ou *None*