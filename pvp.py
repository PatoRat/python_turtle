from turtle import Screen, Turtle
from time import sleep
from random import randint
from manejo_archivos import resource_path

def pvp():
    #shooter
    score = 0
    score2 = 0
    
    #Pantalla
    sc = Screen()
    sc.title('Shooter PVP')
    sc.bgcolor('black')
    sc.setup(width=600,height=600)
    sc.tracer(0)

    balita = resource_path("balita.gif")
    balita2 = resource_path("balita2.gif")
    navecita = resource_path("navecita.gif")
    enemiguito = resource_path("navecita2.gif")

    sc.addshape(balita)
    sc.addshape(balita2)
    sc.addshape(navecita)
    sc.addshape(enemiguito)
    
    #jugador 1
    pl = Turtle()
    pl.speed(0)
    pl.shape(navecita)
    pl.penup()
    pl.goto(0,-200)
    pl.direction = 'stop'
    
    #jugador 2
    pl2 = Turtle()
    pl2.speed(0)
    pl2.shape(enemiguito)
    pl2.penup()
    pl2.goto(0,200)
    pl2.direction = 'stop'

    CANTIDAD_BALAS = 5
    
    #balas 1
    puntero_b1 = 0
    balas1 = []
    for _ in range(CANTIDAD_BALAS):
        bl = Turtle()
        bl.shape(balita2)
        bl.penup()
        bl.hideturtle()
        bl.goto(-400,400)
        bl.direction = 'stop'
        balas1.append(bl)

    #balas 2
    puntero_b2 = 0
    balas2 = []
    for _ in range(CANTIDAD_BALAS):
        bl = Turtle()
        bl.shape(balita)
        bl.penup()
        bl.hideturtle()
        bl.goto(-400,-400)
        bl.direction = 'stop'
        balas2.append(bl)
    
    #texto
    text = Turtle()
    text.speed(0)
    text.color('white')
    text.penup()
    text.hideturtle()
    text.goto(0,-260)
    text.write('Score1: 0\tScore2: 0',align='center',font=('Consolas',20,'normal'))
    
    #Pierde
    gmov = Turtle()
    gmov.speed(0)
    gmov.color('white')
    gmov.penup()
    gmov.hideturtle()
    gmov.goto(0,200)
    gmov.playing = True


    def limpiar_balas():
        for index in range(CANTIDAD_BALAS):
            balas1[index].goto(-400,400)
            balas1[index].direction = 'stop'
            balas1[index].hideturtle()

            balas2[index].goto(-400,-400)
            balas2[index].direction = 'stop'
            balas2[index].hideturtle()
    
    def izq():
        pl.direction = 'left'
    def der():
        pl.direction = 'right'
    def izq2():
        pl2.direction = 'left'
    def der2():
        pl2.direction = 'right'

    def mov():
        if pl.direction == 'left':
            x = pl.xcor()
            pl.setx(x-20)
        elif pl.direction == 'right':
            x = pl.xcor()
            pl.setx(x+20)
        if pl2.direction == 'left':
            x = pl2.xcor()
            pl2.setx(x-20)
        elif pl2.direction == 'right':
            x = pl2.xcor()
            pl2.setx(x+20)
            
    def shoot():
        nonlocal puntero_b1
        if pl.direction != 'stop':
            bala_actual = balas1[puntero_b1]

            x = pl.xcor()
            bala_actual.goto(x, -200)
            bala_actual.direction = 'up'
            bala_actual.showturtle()

            puntero_b1 = (puntero_b1 + 1) % CANTIDAD_BALAS
    
    def shoot2():
        nonlocal puntero_b2
        if pl.direction != 'stop':
            bala_actual = balas2[puntero_b2]

            x = pl.xcor()
            bala_actual.goto(x, 200)
            bala_actual.direction = 'down'
            bala_actual.showturtle()

            puntero_b2 = (puntero_b2 + 1) % CANTIDAD_BALAS
        
        
    def stop():
        gmov.playing = False

    sc.listen()
    sc.onkey(izq,'Left')
    sc.onkey(der,'Right')
    sc.onkey(shoot,'Down')
    sc.onkey(izq2,'a')
    sc.onkey(der2,'d')
    sc.onkey(shoot2,'s')
    sc.onkey(stop,'Escape')

    while gmov.playing:
        sc.update()
        
        #colision con bordes
        if (pl.xcor())<-290 or (pl.xcor())>290:
            sleep(0.05)
            if (pl.xcor())<-290:
                pl.goto(-290,-200)
                pl.direction = 'right'
            if (pl.xcor())>290:
                pl.goto(290,-200)
                pl.direction = 'left'
        if (pl2.xcor())<-290 or (pl2.xcor())>290:
            sleep(0.05)
            if (pl2.xcor())<-290:
                pl2.goto(-290,200)
                pl2.direction = 'right'
            if (pl2.xcor())>290:
                pl2.goto(290,200)
                pl2.direction = 'left'
        
        #manejo de interaccion con las balas 1
        for bl in balas1:
            #impacto con enemigo
            if bl.distance(pl2)<30:
                x = randint(-200,200)
                pl2.goto(x,200)
                score = score + 1
                
                limpiar_balas()
                
                text.clear()
                text.write('Score1: {}\tScore2: {}'.format(score,score2),align='center',font=('Consolas',20,'normal'))
                sleep(0.5)
            
            #movimiento de la bala
            if bl.direction == 'up':
                y = bl.ycor()
                bl.sety(y+20)
            
            #se sale de pantalla
            if bl.ycor()>290:
                bl.goto(-400,400)
                bl.direction = 'stop'
                bl.hideturtle()
                
        
        #manejo de interaccion con las balas 2
        for bl in balas2:
            #impacto con enemigo
            if bl.distance(pl)<30:
                x = randint(-200,200)
                pl.goto(x,-200)
                score2 = score2 + 1

                limpiar_balas()

                text.clear()
                text.write('Score1: {}\tScore2: {}'.format(score,score2),align='center',font=('Consolas',20,'normal'))
                sleep(0.5)
            
            #movimiento de la bala
            if bl.direction == 'down':
                y = bl.ycor()
                bl.sety(y-20)
            
            #se sale de pantalla
            if bl.ycor()<-290:
                bl.goto(-400,-400)
                bl.direction = 'stop'
                bl.hideturtle()
        
        mov()
        sleep(0.08)

pvp()