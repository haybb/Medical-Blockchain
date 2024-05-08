import sqlite3
from data_manager import *

def _createDataBase(self, dbName: str) -> (object, object):
    """
    Creates a database, or opens it if already existing

    :param str dbName: name of the database
    :return: c the cursor and conn the connection
    :rtype: tuple of cursor and connection sqlite objects
    """
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    return c, conn


def _createTable(self, c: object, conn: object, tableName: str) -> None:
    """
    Create a table in given databse, or raise an error
    :param cursor c: cursor of the given database
    :param connection conn: connection of the given databse
    :param str tableName: name of the table
    :raise: Error if table already exists
    """
    try:
        with conn:
            comm = "CREATE TABLE " + tableName + " (cle integer, nom text, portefeuille text)"
            # this syntax prevents SQL injections
            c.execute(comm)

    except Exception as e:
        print(e)


def _insertValue(self, c: object, conn: object, tableName: str, publicKey: str, personName: str,
                 wallet: str) -> None:
    """
    Insert value into given table

    :param cursor c: cursor
    :param connection conn: connection
    :param str tableName: name of the table
    :param publicKey: public RSA key of the person
    :param personName: person's name
    :param str wallet: wallet of the person for the given token of blockchain
    """
    with conn:
        comm = "INSERT INTO " + tableName + " VALUES ( '" + publicKey + "', '" + personName + "', '" + wallet + "' )"
        c.execute(comm)


def _showTable(self, c: object, conn: object, tableName: str) -> None:
    """
    Show the given table

    :param object c: cursor
    :param object conn: connection
    :param str tableName: name of the table
    """
    with conn:
        comm = "SELECT * FROM " + tableName
        c.execute(comm)
        print(c.fetchall())


def _deleteRow(self, c: object, conn: object, tableName: str, nameToDelete: str) -> None:
    """
    Delete one row for a given name

    :param object c: cursor
    :param object conn: connection
    :param str tableName: name of the table
    :param str nameToDelete: name to delete
    """
    with conn:
        comm = "DELETE FROM '" + tableName + "' WHERE nom = '" + nameToDelete + "'"
        c.execute(comm)



if __name__ == "__main__":
    initializeLogger()

    try:
        manager = DataManager()
        manager.newUser("patient", encryption.newKeyPair()[0])

        # publicKey, privateKey = encryption.newKeyPair()
        # log.debug("publicKey : %s\nprivateKey : %s", publicKey, privateKey)
        # stringKeyWithEnter = publicKey.export_key().decode().split("-----")[2] # Because RSA.RsaKey.export returns:
        # stringKey = "".join(stringKeyWithEnter.split("\n"))
        # log.debug("stringKey : %s", stringKey)

        # TEST DATABASE
        c, conn = manager.createDataBase("ListeSpecialistes.db")
        manager.createTable(c, conn, "Liste")

        manager.insertValue(c, conn, "Liste", 48271, "Médecin", "Chup9he48sSAuPKGF7M2eXNVJXYbxDWFnrC6dSbDqkgi")
        manager.insertValue(c, conn, "Liste", 2147483647, "Laboratoire", "9xcCpz4Y3BVSFiM7ZWZvS3uT5tUo9xsqpLJadCmEAM7Y")
        manager.showTable(c, conn, "Liste")

        manager.deleteRow(c, conn, "Liste", "Patient")
        manager.showTable(c, conn, "Liste")

        conn.close()


    except Exception as e:
        log.error(e)
        # raise e

