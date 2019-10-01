import cv2 as cv
import numpy as np
from math import *

# ------------------------------- Couleur ------------------------------

# lecture de plusieurs images
def readimages(lenght):
    listimages=[]
    for i in range(lenght):
        img = cv.imread("imgColor/ref/0"+str(i+1)+".jpg",1)
        listimages.append(img)
    return listimages

# calcule de l'histogramme d'une image
def calchist(image):
    color = ('b','g','r')
    listhist=[]
    for i,col in enumerate(color):
        histr = cv.calcHist([image],[i],None,[256],[0,256])
        listhist.append(histr)
    return listhist

# calcule de la distance entre deux images 
def calcDist(histsource,histrequet):
    listdist=[]
    for i in range(len(histsource)):
        som = 0
        for j in range(len(histsource[i])):
            som += min(histsource[i][j],histrequet[i][j])
        dis = 1 - (som/min(sum(histsource[i]),sum(histrequet[i])))
        listdist.append(dis)
    return listdist

# calcule de distance final est l'affichage des images les plus similaires
def imagesSimil(distim, nubchoix):
    simil = {}
    # calcule des distances % à l'origine '0'
    for i in range(len(distim)):
        dis = sqrt(float(distim[i][0])**2 + float(distim[i][1])**2+ float(distim[i][2])**2)
        simil[i+1] = dis
    # ordonner les images par ordre crois
    sortedsimil = sorted(simil.items(), key=lambda simil: simil[1])
    # tester si le nombre des images similaires demandé est > le nombre des images sources
    s = min(len(distim), nubchoix)
    print("=="*10)
    # affichage des noms des images les plus similaires avec leurs distance
    for i in range(s):
        print("{} => l'image similaire est {} avec distance de {}".format(i+1,sortedsimil[i][0],sortedsimil[i][1]))
    print("=="*10)

# fonction principal
def main():
    choiximage = str(input("choisir une image: "))
    choixsimil = int(input("choisir le nombre des images plus simil : "))
    choixtaille = int(input("choisir le nombre des images sources: "))
    # lecture et traitement de l'image requet
    img = cv.imread("imgColor/req/0"+choiximage+".jpg",1)
    imgs1 = calchist(img)
    # lecture des images de reference
    imagessource = readimages(choixtaille)
    histimages = []
    distimages = []
    # calcule de l'histo de tout les images
    for item in imagessource:
        histimages.append(calchist(item))
    # calcule de distance entre chaque image et l'image requet
    for hist in histimages:
        distimages.append(calcDist(hist, imgs1))
    # les images les plus similaires
    imagesSimil(distimages, choixsimil)

#main()

# ------------------------------- Texture ------------------------------

# lecture des image en grix
def Grisimages(lenght):
    listimages=[]
    for i in range(lenght):
        img = cv.imread("imgTexture/ref/0"+str(i+1)+".jpg",0)
        listimages.append(img)
    return listimages

# calcule de matrice de co-occurence (distance=1, direction = 45)
def CalcOccu(mat):
    dictio = {}
    for i in range(len(mat)-1):
        for j in range(len(mat[i])-1):
            
            if dictio.get(mat[i][j]):
                if dictio[mat[i][j]].get(mat[i+1][j+1]):
                    dictio[mat[i][j]][mat[i+1][j+1]] += 1 
                else:
                    dictio[mat[i][j]][mat[i+1][j+1]] = 1
            else:
                dictio[mat[i][j]] ={mat[i+1][j+1]:1}
    return dictio

# calcule de l'uniformité
def Uniformite(dic):
    somme = 0
    for value in dic.values():
        for val in value.values():
            somme += int(val)**2
    return somme

# les images les plus similaires
def similTexture(distimg, NBsimil):
    sortedsimilT = sorted(distimg.items(), key=lambda distimg: distimg[1])
    s = min(len(distimg), NBsimil)
    print("=="*10)
    # affichage des noms des images les plus similaires avec leurs distance
    for i in range(s):
        print("{} => l'image similaire est {} avec distance de {}".format(i+1,sortedsimilT[i][0],sortedsimilT[i][1]))
    print("=="*10)

# fonction principal
def mainTexture():
    choiximage = str(input("choisir une image requet: "))
    NBsimil = int(input("choisir le nombre des images plus simil: "))
    choixtaiile = int(input("choisir le nombre des images sources: "))
    mat = cv.imread("imgTexture/req/0"+choiximage+".jpg",0)
    unifReq = Uniformite(CalcOccu(mat))
    imageRef = Grisimages(choixtaiile)
    distReqRef = {}
    for i in range(choixtaiile):
        distReqRef[i+1] = abs(int(Uniformite(CalcOccu(imageRef[i])))-int(unifReq))
    similTexture(distReqRef, NBsimil)

mainTexture()

# ------------------------------- Globale ------------------------------

cv.waitKey(0)
cv.destroyAllWindows()