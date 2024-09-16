from config.Database import Database
from dal.categorydal import CategoryDal

class categorybll:
    bd = Database("localhost", "root", "", "python1")
    catdal = CategoryDal(bd=bd)

    @classmethod
    def add_category(cls, Category):
        cls.catdal.add(Category)

    @classmethod
    def get_all_category(cls):
        return cls.catdal.getAll()

    @classmethod
    def delete_category(cls, category_id):
        cls.catdal.delete(category_id)

    @classmethod
    def update_category(cls, category_id, updated_category):
        cls.catdal.update(category_id, updated_category)
