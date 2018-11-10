from classes.lemmings import *
# help(Lemming.__init__)
# help(Lemming)
lem1 = Lemming(1, 12)
lem2 = Lemming(1, 12, -1)
# lemS = LemmingStopper(24, 13)
# lemT = Lemming(10, 2, )

print("Lem1:", lem1.posX, lem1.posY)
print("Lem2:", lem2.posX, lem2.posY)
# print(lemS.posX, lemS.posY)
lem1.move_x()
lem2.move_x()
lem2.move_x()
print("Lem1:", lem1.posX, lem1.posY)
print("Lem2:", lem2.posX, lem2.posY)

