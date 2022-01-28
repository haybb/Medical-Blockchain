# Files and config of the server
Here are defintions and explanations about all the files that will be used by the server.


## Files that can be modified by a user
### config.json
This file is used to configurate the server. It is in JSON format.  
__Parameters :__
  * __key-chars :__ all possible characters for the keys. They have to be ASCII. 
  * __max-key-number-of-attempts :__ When creating a key pair, it may already exist. In that case, the algorithm retries, and this is the max number of attempts.


---

## Files that SHALL NOT be modified
### users.dat
A list of all the users and their authorizations.  
__Format :__ A dictionnary of this shape: { ID of user 1: infos, ID of user 2: infos, ... }. Infos is a dictionnary of all additionnal infos. It contains the expored shape of the user object under the key "object".

### keys.dat
A tree that contains the public key of all the users. Therefore it is easier to find one among all the keys that exist.
__Format :__ An ASCIITree class.

### cache
Contains useful infos used by the algorithm. IT MAY NOT BE DELETED.
__Format :__ A dictionnary that contains all the infos under their dedicated key.
