#!/usr/bin/env python3
"""Console client de la machine Turing"""
from machine_turing import *

def main():
    # lecture et normalisation du fichier source
    # lit le fichier comme fichier binaire
    try:
        TSFile = open(sys.argv[1],'rb')
    except IndexError:
        print("paramètres d'appel incorrects")
        sys.exit(1)
    except FileNotFoundError:
        print("le fichier source '{}' n'existe pas.".format(sys.argv[1]))
        sys.exit(1)
    else:
        try:
            chaine = ""
            # encode en utf-8
            for byte in TSFile.read():
                chaine += chr(byte)
        except IOError:
            print("erreur en lecture du fichier source")
            sys.exit(2)
        finally:
            TSFile.close()
    
    # compile le programme source
    c = Compilateur(chaine)
    c.compiler()
    
    # consruit la machine turing à partir du prgramme compilé
    MT = Machine(sys.argv[1], chaine, c.p_turing)
    c = None

    # lecture et controle des arguments
    n1 = 0
    n2 = 0
    try:
        if sys.argv.__len__() == 4:
            n1 = int(sys.argv[2])
            n2 = int(sys.argv[3])
        elif sys.argv.__len__() == 3:
            n1 = int(sys.argv[2])
            n2 = -1
        elif sys.argv.__len__() == 2:
            n1 = -1
            n2 = -1
    except ValueError as e_value:
        print(e_value)
        sys.exit(2)
    
    # construit un ruban à partir des arguments
    R = Ruban(n1, n2)
    exec = Execution(MT, 1, R, 0)
    exec.interprete()


if __name__ == "__main__":
    main()