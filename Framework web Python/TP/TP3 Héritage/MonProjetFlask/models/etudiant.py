from models.user import User

class Etudiant(User):

    def __init__( self, nom, prenom, email, mot_de_passe, age, niveau, specialite):
        # Appel du constructeur de la classe mère User
        super().__init__( nom, prenom, email, mot_de_passe, age)

        # Attributs spécifiques à la classe Etudiant
        self.__niveau = niveau
        self.__specialite = specialite

    def get_niveau(self):
        return self.__niveau

    def set_niveau(self, niveau):
        self.__niveau = niveau

    def get_specialite(self):
        return self.__specialite

    def set_specialite(self, specialite):
        self.__specialite = specialite