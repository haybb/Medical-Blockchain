import sqlite3
from cryptographie.code.src.encryption import *

# to do : changer valeurs pubkey

conn = sqlite3.connect('ListeSpecialistes.db')
c = conn.cursor()

# c.execute('''CREATE TABLE Liste (
#             cle publique text,
#             nom text,
#             portefeuille text
#             )''')
#
# c.execute("INSERT INTO Liste VALUES('pubkey','Medecin','Chup9he48sSAuPKGF7M2eXNVJXYbxDWFnrC6dSbDqkgi')")
# c.execute("INSERT INTO Liste VALUES('pubkey','Laboratoire','9xcCpz4Y3BVSFiM7ZWZvS3uT5tUo9xsqpLJadCmEAM7Y')")
# c.execute("INSERT INTO Liste VALUES('pubkey','Patient','AfzPooLwjpmhjjo7KR44fSivhwuxCsgHiEPAuhNgakvw')")

c.execute("SELECT * FROM Liste")
print(c.fetchall())

conn.commit()
conn.close()
