# TIPE - Medical Blockchain

## Propos
Ceci est mon TIPE réalisé lors de ma 3/2 en MP.  
Ma partie fut de créer une blockchain pour transmettre des clés de chiffrements, de manière sécurisée.  
Ces dernières étaient associées aux dossiers médicaux des patients.  
  
  
## Explications
Les explications *complètes* figurent dans **PrésentationTIPE.pdf**.  
**TL;DR** : j'ai tout d'abord crée une blockchain à l'aide de Solana (installation expliquée dans *PrésentationTIPE.pdf*), cf *blockchain/solana_blockchain.py*
Puis j'ai implémenté à la main une blockchain dans *blockchain/python_blockchain.py*  

Mon binôme s'est intéressé à la partie cryptographique du système en implémentant notamment le RSA et AES. 
  
   
## Exemple de fonctionnement de la blockchain
Conversation entre un médecin demandant des résultats d'analyse d'un de ses patients et un spécialiste ayant ces derniers.  

### Transaction aller
![Message déchiffré par le spécialiste](/Screens/mess%20spe.PNG "Message Spécialiste")  

### Transaction retour
![Message déchiffré par le médecin](/Screens/mess%20medecin.PNG "Message Médecin")  
  
### Transfert du fichier encrypté symétriquement
![Analyse sanguine](/Screens/m%20dupont.PNG "Analyse M.Dupont")  
  
![Analyse sanguine AES](/Screens/m%20dupont%20analyse%20python.PNG "Analyse M.Dupont chiffré puis déchiffré") 

