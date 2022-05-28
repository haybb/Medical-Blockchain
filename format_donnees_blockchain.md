# **Format des données**

## A l'envoi

`objetRequete*SEPARATOR*ipp*SEPARATOR*idMedecin*SEPARATOR*ipMedecin*SEPARATOR*signatureMedecin`
Ce code sera encrypté avec la clé publique du destinataire (le spécialiste par exemple)

## Au retour

`retour*SEPARATOR*cleSymetrique*SEPARATOR*signatureSpecialiste`
Ceci encrypté avec la clé publique de l'émetteur de la 1ere requête (ici le médecin)