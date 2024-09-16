class ProductDal:
    def __init__(self, bd):
        self.bd = bd
        self.bd.connexion()

    def add(self, Product):
        query = "INSERT INTO produit(name, description, price, qte, category_id) VALUES (%s, %s, %s, %s, %s)"
        val = (Product.name, Product.description, Product.price, Product.qte, Product.category_id,)
        self.bd.cursor.execute(query, val)
        self.bd.conn.commit()
        print("Produit creer avec success")

    def update(self, product_id, Product):
        query = "UPDATE produit SET name = %s , description = %s , price = %s , qte = %s , category_id = %s Where id = %s"
        val = (Product.name, Product.description, Product.price, Product.qte, Product.category_id, product_id)
        self.bd.cursor.execute(query, val)
        self.bd.conn.commit()
        print("Produit modifie avec success")

    def getAll(self):
        query = "SELECT * FROM produit"
        self.bd.cursor.execute(query)
        result = self.bd.cursor.fetchall()
        return result

    """ Recuperer les produits par categories
    Args: 
         param1: on recupere l ensemble des produits lies a une categorie dans la base de donnee sql
         param2: on stocks les donnees recuperer dans un dictionnaire que l on devra afficher a l utilisateur
    Returns: 
         le dictionnaire
    """

    def getProductsByCategory(self):
        query = """SELECT p.id, c.libele AS category_name, p.name, p.description, p.price, p.qte 
                   FROM produit p JOIN categorie c ON p.category_id = c.id"""
        self.bd.cursor.execute(query)
        result = self.bd.cursor.fetchall()
        return result

    def delete(self, product_id):
        query = "DELETE FROM produit WHERE id = %s"
        val = (product_id,)
        self.bd.cursor.execute(query, val)
        self.bd.conn.commit()
        print("Produit supprimé avec succès")

    def close(self):
        self.bd.close()
