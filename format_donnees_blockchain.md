# **Format des données**

## A l'envoi

**Dictionnaire :**
- _minstd_ : entier associé à la dernière valeur de minstd générée,
- _message_: string sous la forme:`objetRequete*DELIMITER*ipp*DELIMITER*rpps*DELIMITER*ipMedecin*DELIMITER*signatureMedecin`

La valeur associée à data sera encryptée avec la clé publique du destinataire (le spécialiste par exemple).

**2 numéros uniques** suivant les personnes à vie, ne donnant aucune info en les lisant:
- _IPP_ = identifiant permanent du patient
- _RPPS_ = répertoire partagé des professionnels de santé

## Au retour

Dictionnaire:
- minstd : entier associé à la dernière valeur de minstd générée,
- message: string sous la forme: `retour*DELIMITER*cleSymetrique*DELIMITER*signatureSpecialiste`

Ce dernier sera encrypté avec la clé publique de l'émetteur de la 1ere requête (ici le médecin).