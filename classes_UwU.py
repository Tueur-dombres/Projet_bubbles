from random import shuffle



class Carte:
    def __init__(self, val, coul):
        self.couleur = coul
        self.valeur = val

    def __str__(self):
        return str(self.valeur) + self.couleur


class Deck:
    def __init__(self):
        couleur = ["\u2666", "\u2665", "\u2663", "\u2660"]
        self.deck = [Carte(v, c) for v in range(1,14) for c in couleur]dddddFFFFF
        self.melanger()

    def melanger(self):
        shuffle(self.deck)

    def afficher(self):
        for carte in self.deck:
            print(carte, end=" - ")
        print("")

    def donne_une(self):
        return self.deck.pop()


d = Deck()
d.afficher()
print(d.donne_une())