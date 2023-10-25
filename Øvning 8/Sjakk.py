import pygame as pg
import time as t 

pg.init()

#variabler
BREDDE = 800
HOYDE = 800
screen = pg.display.set_mode([BREDDE,HOYDE])
pg.display.set_caption("Sjakk")
font = pg.font.Font(None, 80)
timer = pg.time.Clock()
fps = 60

#definerer startposisjon + navn
brikkerHvit = ["torn","springer","loper","konge","dronning","loper","springer","torn",
              "bonde","bonde","bonde","bonde","bonde","bonde","bonde","bonde"]
plasseringHvit = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
brikkerSort = ["torn","springer","loper","konge","dronning","loper","springer","torn",
               "bonde","bonde","bonde","bonde","bonde","bonde","bonde","bonde"]
plasseringSort = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
fjernetBrikkerHvit = []
fjernetBrikkerSort = []

runde = 0
verdi = 1000
lovligTrekk = []
vinner = ""

#henter inn bildene
dronningSort = pg.image.load('bilder/black queen.png')
dronningSort = pg.transform.scale(dronningSort, (80, 80))
kongeSort = pg.image.load('bilder/black king.png')
kongeSort = pg.transform.scale(kongeSort, (80, 80))
tornSort = pg.image.load('bilder/black rook.png')
tornSort = pg.transform.scale(tornSort , (80, 80))
springerSort = pg.image.load('bilder/black knight.png')
springerSort = pg.transform.scale(springerSort, (80, 80))
loperSort = pg.image.load('bilder/black bishop.png')
loperSort = pg.transform.scale(loperSort, (80, 80))
bondeSort = pg.image.load('bilder/black pawn.png')
bondeSort = pg.transform.scale(bondeSort, (65, 65))
dronningHvit = pg.image.load('bilder/white queen.png')
dronningHvit = pg.transform.scale(dronningHvit, (80, 80))
kongeHvit = pg.image.load('bilder/white king.png')
kongeHvit = pg.transform.scale(kongeHvit, (80, 80))
tornHvit = pg.image.load('bilder/white rook.png')
tornHvit = pg.transform.scale(tornHvit, (80, 80))
loperHvit = pg.image.load('bilder/white bishop.png')
loperHvit = pg.transform.scale(loperHvit, (80, 80))
springerHvit = pg.image.load('bilder//white knight.png')
springerHvit = pg.transform.scale(springerHvit, (80, 80))
bondeHvit = pg.image.load('bilder/white pawn.png')
bondeHvit = pg.transform.scale(bondeHvit, (65, 65))

bilderHvit = [bondeHvit,springerHvit,loperHvit,kongeHvit,dronningHvit,tornHvit]
bilderSort = [bondeSort,springerSort,loperSort,kongeSort,dronningSort,tornSort]
brikkerListe = ["bonde","springer","loper","konge","dronning","torn"]

#variabelsjekk
def tegnBrett():
    for i in range(32):
        kolonne = i % 4
        rad = i // 4
        if rad % 2 == 0:
            pg.draw.rect(screen, "white", [700 - (kolonne * 200), rad * 100, 100,100])
        else:
            pg.draw.rect(screen, "white", [600 - (kolonne * 200), rad * 100, 100,100])

def tegnBrikker():
    for i in range(len(brikkerHvit)):
        indeks = brikkerListe.index(brikkerHvit[i])
        if brikkerHvit[i] == "bonde":
            screen.blit(bondeHvit, (plasseringHvit[i][0]*100 + 15, plasseringHvit[i][1] * 100 + 30))
        else:
            screen.blit(bilderHvit[indeks], (plasseringHvit[i][0]*100 + 10, plasseringHvit[i][1] * 100 + 10))
        
        if runde < 2:
            if verdi == i:
                pg.draw.rect(screen,"red", [plasseringHvit[i][0] * 100 + 1,plasseringHvit[i][1] * 100 + 1,100,100],2)
    for i in range(len(brikkerSort)):
            indeks = brikkerListe.index(brikkerSort[i])
            if brikkerSort[i] == "bonde":
                screen.blit(bondeSort, (plasseringSort[i][0]*100 + 22, plasseringSort[i][1] * 100 + 30))
            else:
                screen.blit(bilderSort[indeks], (plasseringSort[i][0]*100 + 10, plasseringSort[i][1] * 100 + 10))    
    
            if runde >= 2:
                    if verdi == i:
                        pg.draw.rect(screen,"blue", [plasseringSort[i][0] * 100 + 1,plasseringSort[i][1] * 100 + 1,100,100],2)   
#gyldige trekk
def sjekkMuligheter(brikker,posisjoner,runde):
    trekkListe= []
    alleTrekkListe = []
    for i in range(len(brikker)):
        posisjon = posisjoner[i]
        brikke = brikker[i]
        if brikke == "bonde":
            trekkListe = sjekkBonde(posisjon,runde)  
        elif brikke == "torn":
            trekkListe = sjekkTorn(posisjon,runde)
        elif brikke == "springer":
            trekkListe = sjekkSpringer(posisjon,runde)    
        elif brikke == "loper":
            trekkListe = sjekkLoper(posisjon,runde)
        elif brikke == "dronning":
            trekkListe = sjekkDronning(posisjon,runde)
        elif brikke == "konge":
            trekkListe = sjekkKonge(posisjon,runde)
        alleTrekkListe.append(trekkListe)
    return alleTrekkListe
            
def sjekkBonde(posisjon,farge):
    trekkListe= []
    if farge == "hvit":
        if (posisjon[0], posisjon[1]+1) not in plasseringHvit and (posisjon[0], posisjon[1]+1) not in plasseringSort and posisjon[1] < 7:
            trekkListe.append((posisjon[0],posisjon[1]+1))
        if (posisjon[0], posisjon[1]+1) not in plasseringHvit and (posisjon[0], posisjon[1]+1) not in plasseringSort and  posisjon[1] == 1:
            trekkListe.append((posisjon[0],posisjon[1]+2))
        if (posisjon[0] + 1, posisjon[1]+1) in plasseringSort:
            trekkListe.append((posisjon[0]+1,posisjon[1]+1))
        if (posisjon[0] -1, posisjon[1]+1) in plasseringSort:
            trekkListe.append((posisjon[0]-1,posisjon[1]+1))
    else:
        if (posisjon[0], posisjon[1]-1) not in plasseringHvit and (posisjon[0], posisjon[1]-1) not in plasseringSort and  posisjon[1] > 0:
            trekkListe.append((posisjon[0],posisjon[1]-1))
        if (posisjon[0], posisjon[1]-1) not in plasseringHvit and (posisjon[0], posisjon[1]-1) not in plasseringSort and posisjon[1] == 6:
            trekkListe.append((posisjon[0],posisjon[1]-2))
        if (posisjon[0] + 1, posisjon[1]-1) in plasseringHvit:
            trekkListe.append((posisjon[0]+1,posisjon[1]-1))
        if (posisjon[0] -1, posisjon[1]-1) in plasseringHvit:
            trekkListe.append((posisjon[0]-1,posisjon[1]-1)) 
    return trekkListe
 
def sjekkTorn(posisjon,farge):
    trekkListe= []
    if farge == "hvit":
        motstanderListe = plasseringSort
        vennerListe = plasseringHvit
    else:
        vennerListe = plasseringSort
        motstanderListe = plasseringHvit
    for i in range(4): #0 = opp, #1 ned, hoyre, venstre
        vei = True
        lengde = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else: 
            x = -1
            y = 0
        while vei:
            if (posisjon[0] + (lengde * x), posisjon[1] + (lengde * y)) not in vennerListe and 0 <= posisjon[0] + (lengde*x) <= 7  and 0 <= posisjon[1] + (lengde*y) <= 7:
                trekkListe.append((posisjon[0] + (lengde*x), posisjon[1] + (lengde*y)))
                if (posisjon[0] + (lengde * x), posisjon[1] + (lengde * y)) in motstanderListe:
                    vei = False
                lengde += 1
            else:
                vei = False
    return trekkListe
    
def sjekkSpringer(posisjon, farge):
    trekkListe= []
    if farge == "hvit":
        vennerListe = plasseringHvit
    else:
        vennerListe = plasseringSort
    muligBevegelse = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        bevegelse = (posisjon[0] + muligBevegelse[i][0],posisjon[1] + muligBevegelse[i][1])
        if bevegelse not in vennerListe and 0 <= bevegelse[0]<= 7 and 0 <= bevegelse[1] <= 7:
            trekkListe.append(bevegelse)
    return trekkListe
    
def sjekkLoper(posisjon,farge):
    trekkListe= []
    if farge == "hvit":
        motstanderListe = plasseringSort
        vennerListe = plasseringHvit
    else:
        vennerListe = plasseringSort
        motstanderListe = plasseringHvit
    for i in range(4): #0 = opp-hoyre, opp-venstre, ned-hoyre, ned-venstre
        vei = True
        lengde = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else: 
            x = -1
            y = 1
        while vei:
            if (posisjon[0] + (lengde * x), posisjon[1] + (lengde * y)) not in vennerListe and 0 <= posisjon[0] + (lengde*x) <= 7  and 0 <= posisjon[1] + (lengde*y) <= 7:
                trekkListe.append((posisjon[0] + (lengde*x), posisjon[1] + (lengde*y)))
                if (posisjon[0] + (lengde * x), posisjon[1] + (lengde * y)) in motstanderListe:
                    vei = False
                lengde += 1
            else:
                vei = False   
    return trekkListe

def sjekkDronning(posisjon,farge):
    trekkListe = sjekkLoper(posisjon, farge)
    trekkListe2 = sjekkTorn(posisjon, farge)
    for i in range(len(trekkListe2)):
        trekkListe.append(trekkListe2[i])
    return trekkListe
    
def sjekkKonge(posisjon,farge):
    trekkListe = []
    if farge == "hvit":
        vennerListe = plasseringHvit
    else:
        vennerListe = plasseringSort
    muligBevegelse = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        bevegelse = (posisjon[0] + muligBevegelse[i][0],posisjon[1] + muligBevegelse[i][1])
        if bevegelse not in vennerListe and 0 <= bevegelse[0]<= 7 and 0 <= bevegelse[1] <= 7:
            trekkListe.append(bevegelse)
    return trekkListe

def sjekkLovligMuligheter():
    if runde < 2:
        mulighetListe = mulighetHvit
    else:
        mulighetListe = mulighetSort
    mulighetListe = mulighetListe[verdi]
    return mulighetListe

def tegnTrekk(trekk):
    if runde < 2:
        farge = "red"
    else:
        farge = "blue"
    for i in range(len(trekk)):
        pg.draw.circle(screen,farge,(trekk[i][0] * 100 + 50,trekk[i][1] * 100 + 50),5)
            
def sjakkMatt():
    if runde < 2:
        if "konge" in brikkerHvit:
            kongeIndeks = brikkerHvit.index("konge")
            kongePosisjon = plasseringHvit[kongeIndeks]
            for i in range(len(mulighetSort)):
                if kongePosisjon in mulighetSort[i]:
                    pg.draw.rect(screen,"dark red",[plasseringHvit[kongeIndeks][0]*100 + 1, plasseringHvit[kongeIndeks][1]*100 + 1,100,100],5)
    else:
        if "konge" in brikkerSort:
            kongeIndeks = brikkerSort.index("konge")
            kongePosisjon = plasseringSort[kongeIndeks]
            for i in range(len(mulighetHvit)):
                if kongePosisjon in mulighetHvit[i]:
                    pg.draw.rect(screen,"dark red",[plasseringSort[kongeIndeks][0]*100 + 1, plasseringSort[kongeIndeks][1]*100 + 1,100,100],5)
                    
def tegnGameOver():
    pg.draw.rect(screen, "black",[0,250,800,300])
    screen.blit(font.render(f"{vinner} vant enkelt", True, "white"),(210,300))
    screen.blit(font.render("Trykk ENTER for å restarte", True, "white"),(30,400))

def sjekkPromotering():
    bondeIndeks = []
    hvitPromotering = False
    sortPromotering = False
    promoteringIndeks = 100
    for i in range(len(brikkerHvit)):
        if brikkerHvit[i] == 'bonde':
            bondeIndeks.append(i)
    for i in range(len(bondeIndeks)):
        if plasseringHvit[bondeIndeks[i]][1] == 7:
            hvitPromotering = True
            promoteringIndeks = bondeIndeks[i]
    bondeIndeks = []
    for i in range(len(brikkerSort)):
        if brikkerSort[i] == 'bonde':
            bondeIndeks.append(i)
    for i in range(len(bondeIndeks)):
        if plasseringSort[bondeIndeks[i]][1] == 0:
            sortPromotering = True
            promoteringIndeks = bondeIndeks[i]
    return hvitPromotering, sortPromotering, promoteringIndeks

hvitPromotering = ["springer","loper","dronning","torn"]
sortPromotering = ["springer","loper","dronning","torn"]

def tegnPromotering():
    pg.draw.rect(screen, 'dark gray', [300, 190, 200, 420]) 
    if hvitPromoter:  
        farge = 'white'
        for i in range(len(hvitPromotering)):
            brikke = hvitPromotering[i]
            index = brikkerListe.index(brikke)
            screen.blit(bilderHvit[index], (360, 200 + 100 * i))  
    elif sortPromoter:
        farge = 'black'
        for i in range(len(sortPromotering)):
            brikke = sortPromotering[i]
            index = brikkerListe.index(brikke)
            screen.blit(bilderSort[index], (360, 200 + 100 * i)) 
    pg.draw.rect(screen, farge, [300, 190, 200, 420], 8)  

def sjekkMuligPromotering():
    musPosisjon = pg.mouse.get_pos()
    venstreKlikk = pg.mouse.get_pressed()[0]
    x_pos = musPosisjon[0] // 100
    y_pos = musPosisjon[1] // 100
    # Check if y_pos is within the valid range for hvitPromotering
    if hvitPromoter and venstreKlikk and 5 >= x_pos >= 2 and 5 >= y_pos >= 2:
        brikkerHvit[promotering_index] = hvitPromotering[int(y_pos)-2]
    # Check for sortPromoter in a similar way
    if sortPromoter and venstreKlikk and 5 >= x_pos >= 2 and  5 >= y_pos >= 2:
        brikkerSort[promotering_index] = sortPromotering[int(y_pos)-2]


#spillets gang
mulighetSort = sjekkMuligheter(brikkerSort,plasseringSort, "sort")
mulighetHvit = sjekkMuligheter(brikkerHvit,plasseringHvit, "hvit")
gameOver = False
kjor = True
while kjor:
    timer.tick(fps)
    screen.fill("black")
    tegnBrett()
    tegnBrikker()
    sjakkMatt()   
    if not gameOver:
        hvitPromoter, sortPromoter, promotering_index = sjekkPromotering()
        if hvitPromoter or sortPromoter:
            tegnPromotering()
            sjekkMuligPromotering()  
    if verdi != 1000:
        lovligTrekk = sjekkLovligMuligheter()
        tegnTrekk(lovligTrekk)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            kjor = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            xKoordinat = event.pos[0] // 100
            yKoordinat = event.pos[1] // 100
            tastKoordinat = (xKoordinat, yKoordinat)
            if runde < 2:
                if tastKoordinat in plasseringHvit:
                    verdi = plasseringHvit.index(tastKoordinat)
                    if runde == 0:
                        runde = 1
                if tastKoordinat in lovligTrekk and verdi != 1000:
                    plasseringHvit[verdi] = tastKoordinat
                    if tastKoordinat in plasseringSort:
                        brikkeSort = plasseringSort.index(tastKoordinat)
                        fjernetBrikkerHvit.append(brikkerSort[brikkeSort])
                        if brikkerSort[brikkeSort] == "konge":
                            vinner = "HVIT"
                        brikkerSort.pop(brikkeSort)
                        plasseringSort.pop(brikkeSort)
                    mulighetSort = sjekkMuligheter(brikkerSort,plasseringSort, "sort")
                    mulighetHvit = sjekkMuligheter(brikkerHvit,plasseringHvit, "hvit")
                    runde = 2
                    verdi = 1000
                    lovligTrekk = []
                    
            if runde >= 2:
                if tastKoordinat in plasseringSort:
                    verdi = plasseringSort.index(tastKoordinat)
                    if runde == 2:
                        runde = 3
                if tastKoordinat in lovligTrekk and verdi != 1000:
                    plasseringSort[verdi] = tastKoordinat
                    if tastKoordinat in plasseringHvit:
                        brikkeHvit = plasseringHvit.index(tastKoordinat)
                        fjernetBrikkerSort.append(brikkerHvit[brikkeHvit])
                        if brikkerHvit[brikkeHvit] == "konge":
                            vinner = "SORT"
                        brikkerHvit.pop(brikkeHvit)
                        plasseringHvit.pop(brikkeHvit)
                    mulighetSort = sjekkMuligheter(brikkerSort,plasseringSort, "sort")
                    mulighetHvit = sjekkMuligheter(brikkerHvit,plasseringHvit, "hvit")
                    runde = 0
                    verdi = 1000
                    lovligTrekk= []
        if event.type == pg.KEYDOWN and gameOver:
            if event.key == pg.K_RETURN:
                gameOver = False
                vinner = ""
                brikkerHvit = ["torn","springer","loper","konge","dronning","loper","springer","torn",
              "bonde","bonde","bonde","bonde","bonde","bonde","bonde","bonde"]
                plasseringHvit = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                brikkerSort = ["torn","springer","loper","konge","dronning","loper","springer","torn",
               "bonde","bonde","bonde","bonde","bonde","bonde","bonde","bonde"]
                plasseringSort = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                runde = 0
                verdi = 1000
                lovligTrekk = []
                fjernetBrikkerHvit = []
                fjernetBrikkerSort = []
                mulighetSort = sjekkMuligheter(brikkerSort,plasseringSort, "sort")
                mulighetHvit = sjekkMuligheter(brikkerHvit,plasseringHvit, "hvit")
    if vinner != "":
        gameOver = True
        tegnGameOver()  
    pg.display.flip()
pg.quit()       


