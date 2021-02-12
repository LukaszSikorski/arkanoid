import pygame,sys,time,random

class Clock():
    def __init__(self):
        self.time=0#Czas dlugosci rozgrywki
        self.clock = pygame.time.Clock()#Zmienna dla timerow programowych
        self.seconds=0#Czas rzeczywisty

class Scores:
    def __init__(self):
        try:
            self.file = open("top5.txt", "r")#Otwieram plik z danymi
            self.tmp = self.file.readlines()#Zapis pliku do tmp
            self.txt = [int(x) for x in (self.tmp)]#Konwersja lini pliku do tablicy int
        #Jezeli plik nie istnieje to stworz tablice z piecioma 0, do tablicy wynikow, w zapisie i tak zostanie
        #stwrzony nowy pusty plik(malo efektywne)
        except:
            #self.file = open("top5.txt", "w+")#Otwieram plik z danymi
            #[self.file.write("{}\n".format(x*0)) for x in range(5)]
            self.txt = [int(x*0) for x in range(5)]
    #Zapis punktow do pliku
    def save_scores(self,x):
        #Sprawdzenie czy punkty weza sa wieksze niz te w pliku
        tmp=0
        #Sprawdzanie czy ktorys ze elementow jest mniejszy od wyniku, jesl tak to zamien go z wynikiem weza
        for y in range(len(self.txt)):
            if self.txt[y] <x:
                tmp =self.txt[y]
                self.txt[y]=x
                x=tmp
        try:
            self.file = open("top5.txt", "w+")#Wymazanie zawartosci pliku
            #Zapis zawartosci tablicy do pliku z nowej lini kazda wartosc
            for val in self.txt:
                self.file.write(str("{}\n".format(val)))
            self.file.close()
        except:
            print("Zmiena prawa dotepu do pliku")


class Colors():
    def __init__(self):
        self.white = ((255,255,255))
        self.blue = ((0,0,255))
        self.green = ((0,255,0))
        self.red = (255,0,0)
        self.black = ((0,0,0))
        self.orange = ((255,100,10))
        self.yellow = ((255,255,0))
        self.blue_green = ((0,255,170))
        self.marroon = ((115,0,0))
        self.lime = ((180,255,100))
        self.pink = ((255,100,180))
        self.purple = ((240,0,255))
        self.gray = ((127,127,127))
        self.magenta = ((255,0,230))
        self.brown = ((100,40,0))
        self.forest_green = ((0,50,0))
        self.navy_blue = ((0,0,100))
        self.rust = ((210,150,75))
        self.dandilion_yellow = ((255,200,0))
        self.highlighter = ((255,255,100))
        self.sky_blue = ((0,255,255))
        self.light_gray = ((200,200,200))
        self.dark_gray = ((50,50,50))
        self.tan = ((230,220,170))
        self.coffee_brown =((200,190,140))
        self.moon_glow = ((235,245,255))

class Parameters():
    def __init__(self):
        self.heigth = 600#Wielkosc Y Okna dla samej gry
        self.width = 800#Wielkosc X okna dla samej gry
        self.offset_heigth=0 #Dodatkowy rozmiar dla menu
        self.offset_width=160#Dodatkowy rozmiar dla menu
        self.sizeX_platform=100#Rozmiar platformy dlugosc
        self.sizeY_platform=20#Rozmiar platformy wysokosc
        self.sizeX_box=100#Rozmiar blokow szerekosc
        self.sizeY_box=40#Rozmiar blokow wysokosc
        self.sizeR_ball=15#Promiec kuli
        self.speed_ball_x=-1#Szybkosc kuli(musi byc jeden)
        self.speed_ball_y=-1#Szybkosc kuli(Musi byc jeden)
        self.positionX_platform=400#(Poczatkowa pozycja okna)
        self.positionY_platform=500#Poczatkowa pozycja okna
        self.speed=1#Szybkosc dla rozgrywki

class Game():
    def __init__(self):
        pygame.init()#Inicjalizacja parametrow pygame
        pygame.font.init()#Inicjalizacja fontow
        #self.scores =0
        self.colors = Colors()#Obiekt z kolorami
        self.parameters = Parameters()#Obiekt z parametrami gry
        self.ball = Ball(self)#Kula
        self.window = Window(self)#Tworzenie okna z klasy window
        self.platform = Platform(self)#Platforma do odbijania
        self.box = Box(self)#Bloki do odbicia
        self.clock = Clock()#Zegar do odmierzania czasu
        self.delta =0#Odmierzenie roznicy pomiedzy obiegami petli
        self.list_timers=[self.platform,self.box,self.ball]#Lista zegarow obiektow
        self.scores = Scores()#Plik z punktmai
        self.scr = 0#Zebrane punkty
        while True:
            self.timers()#Wywolanie metody timers
            self.window.window.fill((0,0,0))#Wypelnienie tla na czarno
            pygame.draw.rect(self.window.window,self.platform.color,self.platform.platform)#Rysowanie platformy
            [pygame.draw.rect(self.window.window,(255,0,0),self.box.body[x]) for x in range(len(self.box.body))]#Rysowanie blokow
            pygame.draw.circle(self.window.window,self.ball.color,self.ball.position,self.parameters.sizeR_ball)#Rysowanie pilki
            #pygame.draw.rect(self.window.window,self.ball.color,self.ball.ball)
            pygame.draw.line(self.window.window,(255,255,255),(self.parameters.width,0),(self.parameters.width,self.parameters.heigth))
            self.window.menu(self)#Rysowanie bocznego menu
            pygame.display.flip()#Zamiana buforow
            self.get_event()#Pobieranie wydarzen
            if self.ball.flag_move:#Jesli poszuno platforma czas rozpoczac naliczanie czasu
                self.clock.time+=self.clock.clock.get_rawtime()#Zwiekszenie czasu rozgrywki
    def get_event(self):#Funkcja odpowiedzialna za pobieranie zdarzen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#Jesli krzyzyk, wykonaj funkcje Exit()
                EXIT(self)
                print("Test")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:#Jesli ESCAPE to funkcja Exit()
                EXIT(self)      
        #Jesli pilka nizej niz platforma koniec gry
        if self.ball.position[1]-self.parameters.sizeR_ball >self.parameters.positionY_platform:
           EXIT(self)
        if self.platform.timer>5:#Szybkosc platformy
            self.platform.move(self)#Ruch platformy
            self.platform.timer=0#Zerowanie timera platformy
        if self.ball.timer >=1 and self.ball.flag_move :#Jesli timer wiekszy niz 1 i poruszano klawiszem to rusz kule
            #i generuj pudelka
            self.ball.move(self)#Rusz kule
            self.ball.timer= 0#Timer rowna sie 0
            self.box.add_boxs(self)
    def timers(self):
        self.delta+=self.clock.clock.tick()#Zwiekszenie delty wzgledem poprzednim obiegiem petli
        if self.delta>self.parameters.speed:#Jesli petla wieksza od x to timery zostana zwiekszone
            for obj in self.list_timers:
                obj.timer+=1
            self.delta=0

        

class Window():#Class window
    def __init__(self,game):
        self.font = pygame.font.SysFont("comicsansms", 24)
        pygame.display.set_caption('Arcanoid by Lukasz :)')
        #Tworzenie okna o rozmiarze 500x500
        self.window = pygame.display.set_mode((game.parameters.width+game.parameters.offset_width,game.parameters.heigth+game.parameters.offset_heigth))#Tworzenie okna o wymiar 500x500
    def menu(self,game):
        game.clock.seconds = time.time()#Aktualizacja sekund dla czasu rzeczywistego
        #Wypisywanie zdobytych punktow
        self.window.blit(self.font.render(str("Scories {}".format(game.scr)), True, game.colors.red),(game.parameters.width+5,10))
        #Wypisywanie czasu rozgrywki
        self.window.blit(self.font.render(str("Time of game"), True, game.colors.white),(game.parameters.width+5,40))
        self.window.blit(self.font.render(str("{}".format(round(game.clock.time/1000,2))), True, game.colors.white),(game.parameters.width+5,65))
         #Wypisywanie czasy rzeczywistego
        self.window.blit(self.font.render(str("{}".format(time.ctime(game.clock.seconds))[11:20]), True, game.colors.green),(game.parameters.width+5,100))
        #Wypisywanie 5 najlepszych wynikow z pliku
        self.window.blit(self.font.render(str("TOP5"), True, game.colors.white),(game.parameters.width+5,130))
        for ind, txt in enumerate(game.scores.txt):
            self.window.blit(self.font.render(str("{}. {}".format(ind+1,txt)).encode('utf-8'), True, game.colors.white),(game.parameters.width+5,150+ind*20))
class Platform():
    def __init__(self,game):
        #Tworzenie platformy do odbijania kulki
        self.platform = pygame.Rect((game.parameters.positionX_platform,game.parameters.positionY_platform,game.parameters.sizeX_platform,game.parameters.sizeY_platform))
        self.color = (0,0,255)#Niebieska platforma
        self.timer=0#Timer platformy, zlicza tykniecia zegara
        self.position=[0,0]
        #Metoda do poruszania pilki
    def move(self,game):
        pressed = pygame.key.get_pressed()#Pobieranie wcisnietego klawisza
        if pressed[pygame.K_d] and self.platform.x<game.parameters.width-game.parameters.sizeX_platform:#Jesli d to przesun w prawo
            self.platform.x+=10#Jesli wciniety klawisz przesun w prawo
            game.ball.flag_move=1#Jesli przesunieto to flaga 1, flaga jest do rozpoczecia liczenia czasu
        elif pressed[pygame.K_a] and self.platform.x>0:#Jesli a to przesun w lewo
            self.platform.x-=10#Jesli wcisniete a to porusz w lewo o 10 pixeli    
            game.ball.flag_move=1#Jesli przesunieto to flaga 1, flaga jest do rozpoczecia liczenia czasu
        self.position=[self.platform.x,self.platform.y]#Zapamietanie polozenia platformy
class Box():
    def __init__(self,game):
        self.body=[]#Lista przechowujaca pudelka
        #self.body.append(pygame.Rect((100,100,game.parameters.sizeX_box,game.parameters.sizeY_box)))#Pierwszy element
        #self.body.append(pygame.Rect((400,100,game.parameters.sizeX_box,game.parameters.sizeY_box)))#Pierwszy element
        self.timer=0
        self.position=[200,200]
    def add_boxs(self,game):
        #Generowanie pudelek
        if game.ball.position[1] > 400:#Jesli kulka nizej niz 400 punktow
            if len(self.body) == 0:#Jesli brak juz pudelke do zbiia
                for y in range(3):#Trzy rzedy
                    for x in range(5):#Trzy kolumny
                      self.body.append(pygame.Rect((x*(game.parameters.sizeX_box+50),y*(game.parameters.sizeY_box+60),game.parameters.sizeX_box,game.parameters.sizeY_box)))
class Ball():
    def __init__(self,game):
        #self.position = [545,450]#Pozycja policzeki startowa [0] to X [1] to Y
        self.position = [game.parameters.positionX_platform+random.randint(0,game.parameters.sizeX_platform),game.parameters.positionY_platform-20]#Pozycja policzeki startowa [0] to X [1] to Y
        self.color = (0,255,0)#Kolor pileczki
        self.timer=0#Timer odpowiedzialny za tykanie zegara od ruchu
        self.flag_move=0#Flaga, czy pilka ma sie ruszac
    def move(self,game):
        flag = 0
        #Pierwszy if odpowiada za odbicie pileczki jesli trafi w platforme
        if (self.position[0] > game.platform.platform.x - game.parameters.sizeR_ball and#Czy pilka jest w obrebie X
            self.position[0] < game.platform.platform.x+ game.parameters.sizeX_platform +game.parameters.sizeR_ball#Czy pilka w obrebie x
            and (self.position[1]+game.parameters.sizeR_ball == game.platform.platform.y+game.parameters.sizeY_platform)):#Czy pilka jest na wysokosci platformy w Y
            game.parameters.speed_ball_y*=(-1)#Jesli trafi pileczka to odbija sie, i zmienia sie tylko parametr y
        #Jesli pileczka odbije sie od sciany lewej lub prawej to zmienia sie parametr X
        elif self.position[0] -game.parameters.sizeR_ball < 0 or self.position[0] > game.parameters.width -game.parameters.sizeR_ball:
            game.parameters.speed_ball_x*=(-1)
        #Jesli pileczka odbije sie od sufitu to zmienai sie parametr Y
        elif self.position[1] -game.parameters.sizeR_ball < 0:
            game.parameters.speed_ball_y*=(-1)
        #Odbicia od pudelek
        for boxs in game.box.body:
            #Odbicie gdy pileczk leci z gory na dol
            if (int((self.position[1] +game.parameters.sizeR_ball )) == boxs.y and #Odbicie od od gory przeszkody
                self.position[0] +game.parameters.sizeR_ball >= boxs.x and#Odbicie od lewej strony
                self.position[0]-game.parameters.sizeR_ball <= boxs.x + game.parameters.sizeX_box): #Odbicie odp rawej strony
                    game.parameters.speed_ball_y*=(-1)#Zmiana predkosci y na przeciwna)
                    flag=1
            #Odbicie kiedy pileczka leci z dol do gory
            elif (int(self.position[1] - game.parameters.sizeR_ball ) == boxs.y+game.parameters.sizeY_box and #Odbicie od dolu
                self.position[0] +game.parameters.sizeR_ball >= boxs.x and #Odbicie od lewej
                self.position[0]-game.parameters.sizeR_ball <= boxs.x + game.parameters.sizeX_box): #Odbicie od prawej 
                    game.parameters.speed_ball_y*=(-1)#Zamiana predkosci na przeciwna
                    flag=1
            #Odibcia od lewej krawedzi pudelka
            elif (self.position[0] +game.parameters.sizeR_ball  == boxs.x and # Odboicie od lewej
                self.position[1] +game.parameters.sizeR_ball >= boxs.y and #Ograniczenie pilka nizej niz gora pudelka
                self.position[1] -game.parameters.sizeR_ball<= boxs.y +game.parameters.sizeY_box):#Ogrniaczenie pilka wyzej niz dol pudelka
                    flag=1
                    game.parameters.speed_ball_x*=(-1)#Zamiana predkosci x na przecwina
            #Odbicie od prawej krawedzi pudelka
            elif (self.position[0] - game.parameters.sizeR_ball  == boxs.x +game.parameters.sizeX_box and #Odbicie od prawej
                self.position[1] +game.parameters.sizeR_ball>= boxs.y and#Odbicie nizej niz dol pudelka
                self.position[1]-game.parameters.sizeR_ball <= boxs.y +game.parameters.sizeY_box):#Odbicie powyzej niz gora pudelka
                    game.parameters.speed_ball_x*=(-1)#Zamiana predkosci x na przeciwna
                    flag=1
            if flag:#Jesli dotknieto pudelka to usuniecie
                game.box.body.remove(boxs)#Usniecie pudelka z pola body
                flag=0#Wyzerowanie flagi
                game.scr+=1#Dodanie punkta do puli
        self.position[0] +=game.parameters.speed_ball_x#Zmiana polozenia pilki w X o zmienna zapisana w parametrach
        self.position[1] +=game.parameters.speed_ball_y#Zmiana polozenia pilki w Y o zmienna zapisana w parametrach
def EXIT(game):
    E_font = pygame.font.SysFont("comicsansms", 72)
    game.scores.save_scores(game.scr)#Zapis pliku
    game.window.window.fill((0,0,0))#Tlo jest czarne
    game.window.window.blit(E_font.render(str(game.scr), True, game.colors.red),(450,200))
    pygame.display.flip()#Zamiana buforow
    flag =1

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                flag=0
    time.sleep(0.100)
    sys.exit(0)#Koniec aplikacji

#Zrobic poprawne odbijanie


Game()