# **Format des données**

## A l'envoi

**Dictionnaire :**
- _minstd_ : entier associé à la dernière valeur de minstd générée,
- _message_: string sous la forme:`objetRequete*DEL*ipp*DEL*rpps*DEL*ipMedecin*SEP*signatureMedecin*`

La valeur associée à data sous message sera encryptée avec la clé publique du destinataire (le spécialiste par exemple).

**2 numéros uniques** suivant les personnes à vie, ne donnant aucune info en les lisant:
- _IPP_ = identifiant permanent du patient
- _RPPS_ = répertoire partagé des professionnels de santé

`*DEL*` pour séparer les données et `*SEP*` pour séparer données et signature

## Au retour

Dictionnaire:
- minstd : entier associé à la dernière valeur de minstd générée,
- message: string sous la forme: `retour*DEL*cleSymetrique*SEP*signatureSpecialiste`

La valeur associée à data sous message sera encrypté avec la clé publique de l'émetteur de la 1ere requête (ici le médecin).