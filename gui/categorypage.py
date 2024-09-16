import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from bll.categorybll import categorybll
from models.Category import Category
from gui.productpage import productpage

class categorypage(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Gestion des Catégories")
        # self.config(bg="black")
        self.geometry("1200x1200")
        self.selected_category_id = None
        self.create_widgets()

    def create_widgets(self):
        self.widgets = []  # Stocker les widgets pour les masquer facilement

        # Label et entrée pour la désignation
        label_nom = ttk.Label(self, text="Désignation:", bootstyle=INFO)
        label_nom.pack(pady=10, padx=20, anchor='w')
        self.entree_nom = ttk.Entry(self, width=40)
        self.entree_nom.pack(pady=5, padx=20, anchor='w')

        # Ajouter les widgets à la liste
        self.widgets.extend([label_nom, self.entree_nom])

        # Label et entrée pour la description
        label_description = ttk.Label(self, text="Description:", bootstyle=INFO)
        label_description.pack(pady=10, padx=20, anchor='w')
        self.entree_description = ttk.Entry(self, width=40)
        self.entree_description.pack(pady=5, padx=20, anchor='w')

        # Ajouter les widgets à la liste
        self.widgets.extend([label_description, self.entree_description])

        # Cadre pour les boutons
        bouton_frame = ttk.Frame(self)
        bouton_frame.pack(pady=10)
        self.widgets.append(bouton_frame)

        # Bouton de soumission
        bouton_soumettre = ttk.Button(bouton_frame, text="Soumettre", bootstyle=SUCCESS, command=self.soumettre_formulaire)
        bouton_soumettre.pack(side='left', padx=5)
        self.widgets.append(bouton_soumettre)

        # Bouton de suppression
        bouton_supprimer = ttk.Button(bouton_frame, text="Supprimer", bootstyle=DANGER, command=self.supprimer_categorie)
        bouton_supprimer.pack(side='left', padx=5)
        self.widgets.append(bouton_supprimer)

        # Bouton de mise à jour
        bouton_mettre_a_jour = ttk.Button(bouton_frame, text="Mettre à jour", bootstyle=WARNING, command=self.mettre_a_jour_categorie)
        bouton_mettre_a_jour.pack(side='left', padx=5)
        self.widgets.append(bouton_mettre_a_jour)

        # Bouton pour la page de produit
        bouton_produit = ttk.Button(bouton_frame, text="Page produit", bootstyle="secondary", command=self.afficher_product_page)
        bouton_produit.pack(side='left', padx=5)
        self.widgets.append(bouton_produit)

        # Treeview pour afficher les catégories
        self.tree = ttk.Treeview(self, columns=("id", "libele", "description"), show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("libele", text="Libellé")
        self.tree.heading("description", text="Description")
        self.tree.pack(pady=10, padx=20, fill="x")
        self.widgets.append(self.tree)

        # Lier la sélection dans le Treeview à la méthode remplir_formulaire
        self.tree.bind("<<TreeviewSelect>>", self.remplir_formulaire)

        # Charger les catégories existantes
        self.charger_categories()

    def afficher_product_page(self):
        # Masquer les widgets de la page actuelle
        self.masquer_widgets()

        # Créer et afficher la page produit
        self.page_produit = productpage(parent=self)
        self.page_produit.pack(fill="both", expand=True)

    def masquer_widgets(self):
        for widget in self.widgets:
            widget.pack_forget()

    def soumettre_formulaire(self):
        designation = self.entree_nom.get()
        description = self.entree_description.get()

        if designation:
            Cat1 = Category(id=None, libele=designation, description=description)
            categorybll.add_category(Cat1)
            print(f"Catégorie ajoutée: {designation}")
            self.charger_categories()
        else:
            print("La désignation est requise.")

    def charger_categories(self):
        categories = categorybll.get_all_category()
        categories.sort(key=lambda x: x['libele'])

        for item in self.tree.get_children():
            self.tree.delete(item)

        for cat in categories:
            self.tree.insert("", "end", values=(cat["id"], cat["libele"], cat["description"]))

    def supprimer_categorie(self):
        selected_item = self.tree.selection()

        if selected_item:
            category_id = self.tree.item(selected_item)["values"][0]
            categorybll.delete_category(category_id)
            print(f"Catégorie supprimée: ID {category_id}")
            self.charger_categories()
        else:
            print("Veuillez sélectionner une catégorie à supprimer.")

    def mettre_a_jour_categorie(self):
        if self.selected_category_id:
            new_libele = self.entree_nom.get()
            new_description = self.entree_description.get()

            if new_libele and new_description:
                updated_category = Category(id=self.selected_category_id, libele=new_libele, description=new_description)
                categorybll.update_category(self.selected_category_id, updated_category)
                print(f"Catégorie mise à jour: ID {self.selected_category_id}")
                self.charger_categories()
                self.selected_category_id = None
            else:
                print("Veuillez remplir tous les champs.")
        else:
            print("Veuillez sélectionner une catégorie à mettre à jour.")

    def remplir_formulaire(self, event):
        selected_item = self.tree.selection()

        if selected_item:
            category_id, libele, description = self.tree.item(selected_item)["values"]
            self.selected_category_id = category_id
            self.entree_nom.delete(0, 'end')
            self.entree_nom.insert(0, libele)
            self.entree_description.delete(0, 'end')
            self.entree_description.insert(0, description)
        else:
            print("Veuillez sélectionner une catégorie.")
