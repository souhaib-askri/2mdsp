
class User:

    # Constructeur
    def __init__(self, nom, prenom, email, mot_de_passe, age):
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        self.__mot_de_passe = mot_de_passe
        self.__age = age

    # Accesseur du nom
    def get_nom(self):
        return self.__nom

    # Mutateur du nom
    def set_nom(self, nom):
        self.__nom = nom

    # Accesseur du prénom
    def get_prenom(self):
        return self.__prenom

    # Mutateur du prénom
    def set_prenom(self, prenom):
        self.__prenom = prenom

    # Accesseur de l'email
    def get_email(self):
        return self.__email

    # Mutateur de l'email
    def set_email(self, email):
        self.__email = email

    # Accesseur du mot de passe
    def get_mot_de_passe(self):
        return self.__mot_de_passe

    # Mutateur du mot de passe
    def set_mot_de_passe(self, mot_de_passe):
        self.__mot_de_passe = mot_de_passe

    # Accesseur de l'age
    def get_age(self):
        return self.__age

    # Mutateur de l'age
    def set_age(self, age):
        self.__age = age

