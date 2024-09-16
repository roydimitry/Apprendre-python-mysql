from config.Database import Database
from dal.ProductDal import ProductDal

class productbll:
    bd = Database("localhost", "root", "", "python1")
    prodal = ProductDal(bd=bd)

    @classmethod
    def add_product(cls, Product):
        cls.prodal.add(Product)

    @classmethod
    def get_all_product_categories(cls):
        return cls.prodal.getProductsByCategory()

    @classmethod
    def delete_product(cls, product_id):
        cls.prodal.delete(product_id)

    @classmethod
    def update_product(cls, product_id, updated_product):
        cls.prodal.update(product_id, updated_product)
