import sqlite3


def createDataBase(dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    return c, conn


def createTable(c, conn, tableName):
    try:
        with conn:
            comm = "CREATE TABLE " + tableName + " (cle publique text, nom text, portefeuille text)"
            # this syntax prevents SQL injections
            c.execute(comm)

    except Exception as e:
        print(e)


def insertValue(c, conn, tableName, publicKey, personName, wallet):
    with conn:
        comm = "INSERT INTO " + tableName + " VALUES ( '" + publicKey + "', '" + personName + "', '" + wallet + "' )"
        c.execute(comm)


def showTable(c, conn, tableName):
    with conn:
        comm = "SELECT * FROM " + tableName
        c.execute(comm)
        print(c.fetchall())


def deleteRow(c, conn, tableName, nameToDelete):
    with conn:
        comm = "DELETE FROM '" + tableName + "' WHERE nom = '" + nameToDelete + "'"
        c.execute(comm)


if __name__ == '__main__':
    c, conn = createDataBase("ListeSpecialistes.db")
    createTable(c,conn,"Liste")

    insertValue(c, conn, "Liste", "cléPublique1", "Médecin", "Chup9he48sSAuPKGF7M2eXNVJXYbxDWFnrC6dSbDqkgi")
    insertValue(c, conn, "Liste", "cléPublique2", "Laboratoire", "9xcCpz4Y3BVSFiM7ZWZvS3uT5tUo9xsqpLJadCmEAM7Y")
    insertValue(c, conn, "Liste", "cléPublique3", "Patient", "AfzPooLwjpmhjjo7KR44fSivhwuxCsgHiEPAuhNgakvw")
    showTable(c, conn, "Liste")

    deleteRow(c, conn, "Liste", "Patient")
    showTable(c, conn, "Liste")

    conn.close()