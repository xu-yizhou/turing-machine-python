""" Une machine de Turing traduite de celle de M. Claude del Vigna.

Classes:
    Compilateur: Trauduit le programme en une table de transitions.
    Execution: Interprète les actions des quadruplets.
    Machine: Le programme source et le programme Turing.
    Quadruplet: Fonction de transition.
    Ruban: Le ruban et la tête de lecture de la machine de Turing.

    TODO(Yizhou, yizhou.xu8859@gmail.com):
        DIM setter, extension dynamique du ruban

"""
import sys


class Ruban:
    """Le ruban et la tête de lecture de la machine de Turing.

    Attributes:
        DIM(int): La longeur du ruban.
        ruban(list(str)): Une liste de string qui représente le ruban.
        oeil(int): La tête de lecture.

    Methods:
        cellule(): Méthode getter de la case du ruban.
        affecter(): Méthode setter de la case du ruban.
        afficher(): Affiche le ruban et la tête de lecture.

    """
    DIM = 70

    def __init__(
            self,
            n1:int = -1,
            n2:int = -1,
            p:int = DIM//2
    ):
        """Instancie un Ruban.

        Construit un ruban à partir des nombres entrés.
        Les nombres sont représentés en base 1.

        Args:
            n1(int): Le premier nombre sur le ruban, -1 par defaut.
            n2(int): Le deuxième nombre sur le ruban, -1 par defaut.
            p(int): La position initiale de la tête de lecture,
                    Au milieu du ruban par defaut.

        Examples:
            R1 = Ruban(2)
            0000000000000000000000000000000000011100000000000000000000000000000000
                                               X
            R2 = Ruban(2,3)
            0000000000000000000000000000000000011100111100000000000000000000000000
                                               X
            R3 = Ruban(2,3,5)
            0000011100111100000000000000000000000000000000000000000000000000000000
                 X

        """
        self.ruban = ['0' for _ in range(Ruban.DIM)]
        k = p
        try:
            for _ in range(0, n1+1):
                self.ruban[k] = '1'
                k += 1
            k += 2
            for _ in range(0, n2+1):
                self.ruban[k] = '1'
                k += 1
        except IndexError:
            print("Les valeurs sont trops grandes pour notre petit ruban!")
            sys.exit(2)
        self.oeil = p

    def cellule(
            self,
            i:int
    ):
        """Obtient la valeur de l'ième case sur le ruban.

        Args:
            i(int): L'indice de la case.

        Returns:
            str, la valeur('1'/'0') dans l'ième case.

        """
        return self.ruban[i]

    def affecter(
            self,
            i:int,
            v:str
    ):
        """Affecte la valeur(1/0) donné par v à l'ième case.

        Args:
            i(int): L'indice de la case.
            v(str): La valeur('1'/'0') à écrire.

        """
        self.ruban[i] = v

    def afficher(self):
        """Affiche le ruban et la tête de lecture."""
        print("".join(self.ruban))
        print(" " * self.oeil + "X")


class Quadruplet:
    """Quadruplet (transition) de la machine de Turing.
    
    Une instance de Quadruplet repésente une transition.
    Une liste de transition forme une table de transition, i.e. programme Turing

    Attributes:
        etat_i(int): L'état d'entrée.
        caractere(str): {'1','0'}, la valeur de la case courrente.
        action(str): {'D','G','1','0','I'}, l'action de la tếte de lecture.
        etat_f(int): L'état de sortie.
        provenance(): L'instruction qui produit la transition.
                    {'BCL','IMP','GAU','DRO','SI',...}

    Method:
        afficher(): Affiche le quadruplet.

    """
    def __init__(
            self,
            etat_i,
            caractere,
            action,
            etat_f,
            provenance
    ):
        self.etat_i = etat_i
        self.caractere = caractere
        self.action = action
        self.etat_f = etat_f
        self.provenance = provenance

    def afficher(self):
        """Affiche le quadruplet."""
        print("{} {} {} {} {}".format(
            self.etat_i,
            self.caractere,
            self.action,
            self.etat_f,
            self.provenance,
        ))


class Machine:
    """Intègre le programme source et le programme compilé.

    Attributes:
        __nom_fichier(str): Le nom du fichier source.
        __programme_source(str): Le fichier source (*.TS).
        programme_turing(list(Quadruplet)): Une liste de Quadruplet.

    Method:
        afficher(): Affiche les transitions de la machine.

    """
    def __init__(
        self,
        nom_fichier:str,
        programme_source:str,
        *programme_turing:list
    ):
        self.__nom_fichier = nom_fichier
        self.__programme_source = programme_source
        self.programme_turing = programme_turing[0]

    def afficher(self):
        """Affiche les transitions de la machine."""
        for prg in self.programme_turing:
            prg.afficher()


class Compilateur:
    """Compilateur pour traduire le programme source en programme Turing.

    Attributes:
        p_turing(list(Quadruplet)): Le programme Turing, une liste de
                transitions.
        __programme(str): Le programme source (*.TS).
        __pile(list(int)): utile pour réaliser la boucle.
        __p(int): La position dans le programme source.
        __etat_entree(str): L'état d'entrée.
        __XX(int) : permet de générer de nouveaux états à la demande

    Methods:
        init_compiler(): Initialise le compilateur.
        compiler: Compile le programme source (*.TS).

    """
    def __init__(
            self,
            c:str
    ):
        self.__programme = c
        self.init_compiler()

    def init_compiler(self):
        self.p_turing = list()
        self.__pile =list()
        self.__p = 0
        self.__XX = -1

    def compiler(self):
        """Compile le programme source.

        Traduit le programme de source (*.TS) en langage de la machine de
        Turing, c'est-à-dire une liste de transitions.

        """
        self.init_compiler()
        self.__pile.append(self.__nouvel_etat())
        self.__etat_entree = self.__nouvel_etat()
        erreurs = {
            2: "mot clé <si> attendu",
            3: "caractère ( attendu",
            4: "caractère ) attendu",
            5: "caractère } attendu",
            7: "caractère G attendu",
            8: "caractère D attendu",
            9: "mot clé <fin> attendu",
            10: "caractère 1 attendu",
            11: "caractère 0 attendu",
            12: "caractère P attendu",
            13: "caractère I attendu",
            14: "caractère # attendu",
            15: "mot clé <boucle> attendu",
            19: "instruction attendue",
            20: "caractère % attendu",
            22: "caractère 0 ou 1 attendu",
        }
        e = self.__AXIOME()
        if e:
            print("erreur de syntaxe : ", end="")
            print(erreurs[e] if e in erreurs else "erreur inconnue", end=" ")
            print("à la position", end=" ")
            print(self.__p, end=" ")
            print("du programme source :")
            print(self.__programme[:self.__p])
            sys.exit()

    def __AXIOME(self):
        """AXIOME -> PROGRAMME ESPACES '#'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        e = self.__PROGRAMME()
        if e:
            return e
        e = self.__ESPACES()
        if self.__programme[self.__p] != '#':
            return 14
        self.__p += 1
        return 0

    def __PROGRAMME(self):
        """PROGRAMME -> '#' | '}' | INSTRUCTION ESPACES PROGRAMME

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] == '#':
            return 0
        if self.__programme[self.__p] == '}':
            return 0
        e = self.__INSTRUCTION()
        if e:
            return e
        e = self.__ESPACES()
        e = self.__PROGRAMME()
        if e:
            return e
        return 0

    def __INSTRUCTION(self):
        """INSTRUCTION -> GAUCHE | BOUCLE | ... | COMMENTAIRE

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        instructions = {
            'G': self.__GAUCHE,
            'b': self.__BOUCLE,
            's': self.__SI,
            'f': self.__FIN,
            'D': self.__DROITE,
            '1': self.__BATON,
            '0': self.__ZERO,
            'P': self.__PAUSE,
            'I': self.__IMPRIMER,
            '%': self.__COMMENTAIRE,
        }
        if self.__programme[self.__p] in instructions:
            e = instructions[self.__programme[self.__p]]()
            return e
        return 19

    def __FIN(self):
        """FIN -> 'fin'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != 'f':
            return 9
        self.__p += 1
        if self.__programme[self.__p] != 'i':
            return 9
        self.__p += 1
        if self.__programme[self.__p] != 'n':
            return 9
        self.__p += 1

        # génération du code cible
        q0 = self.__etat_entree
        etat_sortie = self.__nouvel_etat()
        q1 = self.__pile[-1]
        self.p_turing.append(Quadruplet(q0, '0', '0', q1, "FIN"))
        self.p_turing.append(Quadruplet(q0, '1', '1', q1, "FIN"))
        self.__etat_entree = etat_sortie

        return 0

    def __COMMENTAIRE(self):
        """COMMENTAIRE -> '%.[^'\n']'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != '%':
            return 20
        while True:
            self.__p += 1
            if self.__programme[self.__p] == chr(10):
                break
        return 0

    def __BOUCLE(self):
        """BOUCLE -> 'boucle' ESPACES* PROGRAMME ESPACES* ACCOLADE_FERMANTE

        Implémentation de boucle à l'aide d'un pile.

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != 'b':
            return 15
        self.__p += 1
        if self.__programme[self.__p] != 'o':
            return 15
        self.__p += 1
        if self.__programme[self.__p] != 'u':
            return 15
        self.__p += 1
        if self.__programme[self.__p] != 'c':
            return 15
        self.__p += 1
        if self.__programme[self.__p] != 'l':
            return 15
        self.__p += 1
        if self.__programme[self.__p] != 'e':
            return 15
        self.__p += 1

        q0 = self.__etat_entree
        etat_sortie = self.__nouvel_etat()
        self.__pile.append(etat_sortie)

        e = self.__ESPACES()
        e = self.__PROGRAMME()
        if e:
            return e
        e = self.__ESPACES()
        e = self.__ACCOLADE_FERMANTE()
        if e:
            return e
        
        # génération du code cible
        self.p_turing.append(Quadruplet(self.__etat_entree, '0', '0', q0, "BCL"))
        self.p_turing.append(Quadruplet(self.__etat_entree, '1', '1', q0, "BCL"))
        self.__etat_entree = etat_sortie
        self.__pile.pop()

        return 0

    def __SI(self):
        """Instruction Conditionnelle.

        SI -> 'si' ESPACES* PARENTHESE_OUVRANTE ZERO_OU_UN ESPACES*
                PARENTHESE_FERMANTE

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != 's':
            return 2
        self.__p += 1
        if self.__programme[self.__p] != 'i':
            return 2
        self.__p += 1

        q0 = self.__etat_entree
        etat_sortie = self.__nouvel_etat()
        q1 = self.__nouvel_etat()

        e = self.__ESPACES()
        e = self.__PARENTHESE_OUVRANTE()
        if e:
            return e
        e = self.__ESPACES()
        e = self.__ZERO_OU_UN()
        c0 = self.__ZU
        e = self.__ESPACES()
        e = self.__PARENTHESE_FERMANTE()
        if e:
            return e
        if c0 == '0':
            # génération du code cible
            self.p_turing.append(Quadruplet(q0, '0', '0', q1, "SI"))
            self.p_turing.append(Quadruplet(q0, '1', '1', etat_sortie, "SI"))
        else:
            # génération du code cible
            self.p_turing.append(Quadruplet(q0, '0', '0', etat_sortie, "SI"))
            self.p_turing.append(Quadruplet(q0, '1', '1', q1, "SI"))

        e = self.__ESPACES()
        self.__etat_entree = q1
        e = self.__PROGRAMME()
        if e:
            return e

        e = self.__ESPACES()
        e = self.__ACCOLADE_FERMANTE()
        if e:
            return e
        
        # génération du code cible
        self.p_turing.append(Quadruplet(self.__etat_entree, '0', '0', etat_sortie, "SI"))
        self.p_turing.append(Quadruplet(self.__etat_entree, '1', '1', etat_sortie, "SI"))
        self.__etat_entree = etat_sortie

        return 0

    def __GAUCHE(self):
        """GAUCHE -> 'G'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != 'G':
            return 7
        self.__p += 1

        # génération du code cible
        q0 = self.__etat_entree
        etat_sortie = self.__nouvel_etat()
        self.p_turing.append(Quadruplet(q0, '0', 'G', etat_sortie, "GAU"))
        self.p_turing.append(Quadruplet(q0, '1', 'G', etat_sortie, "GAU"))
        self.__etat_entree = etat_sortie

        return 0

    def __DROITE(self):
        """DROITE -> 'D'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != 'D':
            return 8
        self.__p += 1
        
        # génération du code cible
        q0 = self.__etat_entree
        etat_sortie = self.__nouvel_etat()
        self.p_turing.append(Quadruplet(q0, '0', 'D', etat_sortie, "DRO"))
        self.p_turing.append(Quadruplet(q0, '1', 'D', etat_sortie, "DRO"))
        self.__etat_entree = etat_sortie

        return 0


    def __BATON(self):
        """BATON -> '1'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != '1':
            return 10
        self.__p += 1
        
        # génération du code cible
        q0 = self.__etat_entree
        etat_sortie = self.__nouvel_etat()
        self.p_turing.append(Quadruplet(q0, '0', '1', etat_sortie, "BAT"))
        self.p_turing.append(Quadruplet(q0, '1', '1', etat_sortie, "BAT"))
        self.__etat_entree = etat_sortie

        return 0


    def __ZERO(self):
        """ZERO -> '0'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != '0':
            return 11
        self.__p += 1
        q0 = self.__etat_entree
        etat_sortie = self.__nouvel_etat()
        self.p_turing.append(Quadruplet(q0, '0', '0', etat_sortie, "ZER"))
        self.p_turing.append(Quadruplet(q0, '1', '0', etat_sortie, "ZER"))
        self.__etat_entree = etat_sortie

        return 0


    def __PAUSE(self):
        """PAUSE -> 'P'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != 'P':
            return 12
        self.__p += 1
        # génération du code cible
        q0 = self.__etat_entree
        etat_sortie = self.__nouvel_etat()
        self.p_turing.append(Quadruplet(q0, '0', 'P', etat_sortie, "PAU"))
        self.p_turing.append(Quadruplet(q0, '1', 'P', etat_sortie, "PAU"))
        self.__etat_entree = etat_sortie

        return 0

    def __IMPRIMER(self):
        """IMPRIMER -> 'I'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != 'I':
            return 13
        self.__p += 1
        # génération du code cible
        q0 = self.__etat_entree
        etat_sortie = self.__nouvel_etat()
        self.p_turing.append(Quadruplet(q0, '0', 'I', etat_sortie, "IMP"))
        self.p_turing.append(Quadruplet(q0, '1', 'I', etat_sortie, "IMP"))
        self.__etat_entree = etat_sortie

        return 0

    def __PARENTHESE_OUVRANTE(self):
        """PARENTHESE_OUVRANTE -> '('

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != '(':
            return 3
        self.__p += 1

        return 0

    def __PARENTHESE_FERMANTE(self):
        """PARENTHESE_FERMANTE -> ')'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != ')':
            return 4
        self.__p += 1
        return 0

    def __ACCOLADE_FERMANTE(self):
        """ACCOLADE_FERMANTE -> '}'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] != '}':
            return 5
        self.__p += 1
        return 0

    def __ZERO_OU_UN(self):
        """ZERO_OU_UN -> '1' | '0'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        if self.__programme[self.__p] not in ['1', '0']:
            return 22
        self.__ZU = self.__programme[self.__p]
        self.__p += 1
        return 0

    def __ESPACES(self):
        """ESPACES -> ' ' | '\r' | '\n'

        Returns:
            int: 0 pour succes, e (clé du dictionnaire erreurs) pour erreur

        """
        while True:
            if self.__programme[self.__p] not in [chr(10), chr(13), chr(32)]:
                break
            self.__p += 1
        return 0


    def __nouvel_etat(self):
        """Génère de nouveaux états.

        Returns:
            numéro du nouvel état.

        """
        self.__XX += 1
        return self.__XX


class Execution:
    """Excution du programme Turing produit par le compilateur.

    Attributes:
        MT(Machine): Le programme Turing produit par le compilateur.
        etatCrt(int): L'état initial de la machine.
        ruban(Ruban): Le ruban de la machine.

    Method:
        interprete: Interprete le langage du programme Turing.
    """
    def __init__(
            self,
            machine:Machine,
            etatCrt:int,
            ruban:Ruban,
            priorite:int = 10
    ):
        self.MT = machine
        self.etatCrt = etatCrt
        self.ruban = ruban
        self.priorite = priorite

    def interprete(self):
        """Interprete le programme Turing.

        Effectue les opérations selon la liste des transitions.

        """
        while True:
            c = self.ruban.cellule(self.ruban.oeil)
            i = 0
            b1 = False
            while True:
                if i >= len(self.MT.programme_turing):
                    b1 = True
                    break
                quad = self.MT.programme_turing[i]
                if (quad.etat_i == self.etatCrt) and (quad.caractere == c):
                    break
                # self.MT.programme_turing[i].afficher()
                i += 1
            if b1:
                break
            if quad.action == 'G':
                self.ruban.oeil -= 1
                if self.ruban.oeil <= 0:
                    print("La tête de lecture arrive à l'extrémité gauche du "
                          "ruban")
                    self.ruban.afficher()
                    sys.exit(3)
            elif quad.action == 'D':
                self.ruban.oeil += 1
                if self.ruban.oeil >= Ruban.DIM:
                    print("La tête de lecture arrive à l'extrémité droite du ruban")
                    self.ruban.afficher()
                    sys.exit(3)
            elif quad.action == '1':
                self.ruban.affecter(self.ruban.oeil,'1')
            elif quad.action == '0':
                self.ruban.affecter(self.ruban.oeil,'0')
            elif quad.action == 'P':
                print("appuyer sur une touche pour continuer : ")
                try:
                    input()
                except IOError:
                    pass
            elif quad.action == 'I':
                self.ruban.afficher()

            self.etatCrt = quad.etat_f

