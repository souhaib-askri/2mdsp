
from werkzeug.security import generate_password_hash, check_password_hash


class User:

    def __init__(self, nom, prenom, email, mot_de_passe, age):
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        self.__mot_de_passe = generate_password_hash(mot_de_passe)
        self.__age = age

    def get_nom(self):
        return self.__nom

    def set_nom(self, nom):
        self.__nom = nom

    def get_prenom(self):
        return self.__prenom

    def set_prenom(self, prenom):
        self.__prenom = prenom

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

    def get_mot_de_passe(self):
        return self.__mot_de_passe
        
    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(
            self.__mot_de_passe,
            mot_de_passe
    )
