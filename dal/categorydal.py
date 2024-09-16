class CategoryDal:
    def __init__(self, bd):
        self.bd = bd
        self.bd.connexion()

    def add(self, Category):
        query = "INSERT INTO categorie(libele, description) VALUES (%s, %s)"
        val = (Category.libele, Category.description)
        self.bd.cursor.execute(query, val)
        self.bd.conn.commit()
        print("Catégorie ajoutée avec succès")

    def update(self, category_id , Category):
        query = "UPDATE categorie SET libele = %s , description = %s Where id = %s"
        val = (Category.libele , Category.description, category_id)
        self.bd.cursor.execute(query, val)
        self.bd.conn.commit()
        print("Categorie modifie avec success")

    def getAll(self):
        query = "SELECT * FROM categorie"
        self.bd.cursor.execute(query)
        result = self.bd.cursor.fetchall()
        return result

    def delete(self, category_id):
        query = "DELETE FROM categorie WHERE id = %s"
        val = (category_id,)
        self.bd.cursor.execute(query,  val)
        self.bd.conn.commit()
        print("Categorie supprimee avec success")

    def close(self):
        self.bd.close()