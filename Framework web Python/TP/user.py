
class User:

    # Constructeur
    def __init__(self, nom, prenom, email, mot_de_passe, date_naissance):
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        self.__mot_de_passe = mot_de_passe
        self.__date_naissance = date_naissance

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

    # Accesseur de la date de naissance
    def get_date_naissance(self):
        return self.__date_naissance

    # Mutateur de la date de naissance
    def set_date_naissance(self, date_naissance):
        self.__date_naissance = date_naissance

