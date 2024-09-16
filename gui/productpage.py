import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from bll.productbll import productbll
from bll.categorybll import categorybll
from models.Product import Product


class productpage(ttk.Frame):  # Utiliser ttk.Frame pour intégrer dans une fenêtre principale
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.themename = "flatly"
        self.title = "Gestion des Produits"
        self.geometry = "1200x1200"
        self.selected_product_id = None
        self.create_widgets()

    def create_widgets(self):
        # Champs d'entrée pour les propriétés du produit
        ttk.Label(self, text="Désignation:", bootstyle=INFO).pack(pady=10, padx=20, anchor='w')
        self.entree_nom = ttk.Entry(self, width=40)
        self.entree_nom.pack(pady=5, padx=20, anchor='w')

        ttk.Label(self, text="Description:", bootstyle=INFO).pack(pady=10, padx=20, anchor='w')
        self.entree_description = ttk.Entry(self, width=40)
        self.entree_description.pack(pady=5, padx=20, anchor='w')

        ttk.Label(self, text="Prix:", bootstyle=INFO).pack(pady=10, padx=20, anchor='w')
        self.entree_prix = ttk.Entry(self, width=40)
        self.entree_prix.pack(pady=5, padx=20, anchor='w')

        ttk.Label(self, text="Quantité:", bootstyle=INFO).pack(pady=10, padx=20, anchor='w')
        self.entree_qte = ttk.Entry(self, width=40)
        self.entree_qte.pack(pady=5, padx=20, anchor='w')

        ttk.Label(self, text="Catégorie:", bootstyle=INFO).pack(pady=10, padx=20, anchor='w')
        self.entree_cat = ttk.Combobox(self, width=40)
        self.entree_cat.pack(pady=5, padx=20, anchor='w')

        # Charger les catégories dans le combobox
        self.charger_categories()

        # Cadre pour les boutons
        bouton_frame = ttk.Frame(self)
        bouton_frame.pack(pady=10)

        # Boutons
        ttk.Button(bouton_frame, text="Ajouter", bootstyle=SUCCESS, command=self.ajouter_produit).pack(side='left',
                                                                                                       padx=5)
        ttk.Button(bouton_frame, text="Mettre à jour", bootstyle=WARNING, command=self.mettre_a_jour_produit).pack(
            side='left', padx=5)
        ttk.Button(bouton_frame, text="Supprimer", bootstyle=DANGER, command=self.supprimer_produit).pack(side='left',
                                                                                                          padx=5)

        # Treeview pour afficher les produits
        self.tree = ttk.Treeview(self, columns=("id","name", "description", "price", "qte", "category_name"),
                                 show="headings", height=8)

        self.tree.heading("id", text="Product Id", )
        self.tree.heading("name", text="Nom")
        self.tree.heading("description", text="Description")
        self.tree.heading("price", text="Prix")
        self.tree.heading("qte", text="Quantité")
        self.tree.heading("category_name", text="Nom Catégorie")
        self.tree.column("id", width=0, stretch=ttk.NO)
        self.tree.pack(pady=10, padx=20, fill="x")

        # Lier la sélection dans le Treeview à la méthode remplir_formulaire
        self.tree.bind("<<TreeviewSelect>>", self.remplir_formulaire)

        # Charger les produits existants
        self.charger_produits()

        ttk.Button(self, text="Retour", bootstyle="secondary", command=self.retour_category_page).pack(pady=10, padx=20,
                                                                                                       anchor='w')

    def charger_categories(self):
        categories = categorybll.get_all_category()
        # Remplir le combobox avec les libellés des catégories
        self.entree_cat['values'] = [cat['libele'] for cat in categories]

    def ajouter_produit(self):
        name = self.entree_nom.get()
        description = self.entree_description.get()
        price = self.entree_prix.get()
        qte = self.entree_qte.get()
        selected_category = self.entree_cat.get()

        # Trouver l'ID de la catégorie sélectionnée
        categories = categorybll.get_all_category()
        category_id = next((cat['id'] for cat in categories if cat['libele'] == selected_category), None)

        if name and price and qte and category_id:
            new_product = Product(id=None, name=name, description=description, price=float(price), qte=int(qte),
                                  category_id=category_id)
            productbll.add_product(new_product)
            print(f"Produit ajouté: {name}")
            self.charger_produits()
        else:
            print("Tous les champs sont requis et la catégorie doit être valide.")

    def charger_produits(self):
        produits = productbll.get_all_product_categories()
        for item in self.tree.get_children():
            self.tree.delete(item)

        for prod in produits:
            self.tree.insert("", "end", values=(prod["id"],prod["name"],
                prod["description"], prod["price"], prod["qte"], prod["category_name"],))

    def mettre_a_jour_produit(self):
        if self.selected_product_id:
            new_name = self.entree_nom.get()
            new_description = self.entree_description.get()
            new_price = self.entree_prix.get()
            new_qte = self.entree_qte.get()
            new_selected_category = self.entree_cat.get()

            categories = categorybll.get_all_category()
            category_id = next((cat['id'] for cat in categories if cat['libele'] == new_selected_category), None)

            if new_name and new_price and new_qte and category_id:
                updated_product = Product(id=self.selected_product_id, name=new_name, description=new_description,
                                          price=float(new_price), qte=int(new_qte), category_id=category_id)
                productbll.update_product(self.selected_product_id, updated_product)
                print(f"Produit mis à jour: ID {self.selected_product_id}")
                self.charger_produits()
                self.selected_product_id = None
            else:
                print("Tous les champs sont requis pour la mise à jour et la catégorie doit être valide.")
        else:
            print("Veuillez sélectionner un produit à mettre à jour.")

    def supprimer_produit(self):
        selected_item = self.tree.selection()

        if selected_item:
            product_id = self.tree.item(selected_item)["values"][0]
            productbll.delete_product(product_id)
            print(f"Produit supprimé: ID {product_id}")
            self.charger_produits()
        else:
            print("Veuillez sélectionner un produit à supprimer.")

    def remplir_formulaire(self, event):
        selected_item = self.tree.selection()

        if selected_item:
            product_id ,name, description, price, qte, category_name = self.tree.item(selected_item)["values"]
            self.selected_product_id = product_id
            self.entree_nom.delete(0, 'end')
            self.entree_nom.insert(0, name)
            self.entree_description.delete(0, 'end')
            self.entree_description.insert(0, description)
            self.entree_prix.delete(0, 'end')
            self.entree_prix.insert(0, str(price))
            self.entree_qte.delete(0, 'end')
            self.entree_qte.insert(0, str(qte))
            self.entree_cat.set(category_name)
        else:
            print("Veuillez sélectionner un produit.")

    def retour_category_page(self):
        self.pack_forget()
        for widget in self.parent.widgets:
            widget.pack()
        print("Retour à la page de gestion des catégories")
