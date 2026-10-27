from user import User

class Etudiant(User):
    def __init__(self, nom, prenom, email, mot_de_passe, age, niveau, specialite):
        super().__init__(nom, prenom, email, mot_de_passe, age)
        self.__niveau = niveau

    def get_niveau(self):
        return self.__niveau

    def set_niveau(self, niveau):
        self.__niveau = niveau        

    def get_specialite(self):
        return self.__specialite

    def set_specialite(self, specialite):
        self.__specialite = specialite
        