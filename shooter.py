from turtle import Screen, Turtle
from time import sleep
from random import randint
from pygame import mixer
from manejo_archivos import escribir_al_final, leer_y_obtener_max_score, resource_path

def shooter():
    #Sonidos
    mixer.init()
    sonido_disparo = mixer.Sound("shooting.wav")
    disparo_enemigo = mixer.Sound("disparo_enemigo.wav")

    #Pantalla
    sc = Screen()
    sc.title('Shooter')
    sc.bgcolor('black')
    sc.setup(width=600,height=600)
    sc.tracer(0)

    player = sc.textinput("Jugador", "Ingrese nombre de jugador:")

    if player or player.strip() != '':

        x = randint(-280,280)
        y = randint(0,280)
        score = 0
        highscore = leer_y_obtener_max_score("shooter.csv", player)

        balita = resource_path("balita.gif")
        balita2 = resource_path("balita2.gif")
        navecita = resource_path("navecita.gif")
        enemiguito = resource_path("enemiguito.gif")

        sc.addshape(balita)
        sc.addshape(balita2)
        sc.addshape(navecita)
        sc.addshape(enemiguito)

        #Nave
        pl = Turtle()
        pl.speed(0)
        pl.shape(navecita)
        pl.penup()
        pl.goto(0,-200)
        pl.direction = 'stop'
        actual_pl_dir = 'stop'

        #proyectil enemigo
        py = Turtle()
        py.shape(balita)
        py.penup()
        py.goto(x,y)
        py.direction = 'down'
        actual_py_dir = 'down'

        #enemie
        en=Turtle()
        en.speed(0)
        en.shape(enemiguito)
        en.penup()
        en.goto(x,y)

        CANTIDAD_BALAS = 20

        #balas
        puntero_b1 = 0
        balas = []
        for _ in range(CANTIDAD_BALAS):
            bl = Turtle()
            bl.shape(balita2)
            bl.penup()
            bl.hideturtle()
            bl.goto(-400,400)
            bl.direction = 'stop'
            balas.append(bl)
        actual_bl_dir = 'stop'
        
        #texto 1
        text = Turtle()
        text.speed(0)
        text.color('white')
        text.penup()
        text.hideturtle()
        text.goto(0,-260)
        text.write('Score: 0\tHighscore: {}'.format(highscore),align='center',font=('Consolas',20,'normal'))

        #texto 2
        text2 = Turtle()
        text2.speed(0)
        text2.color('white')
        text2.penup()
        text2.hideturtle()
        text2.goto(0,0)
        text2.write('',align='center',font=('Consolas',20,'normal'))

        playing = True

        enemy_cooldown = 0
        
        def izq():
            pl.direction = 'left'
        def der():
            pl.direction = 'right'

        def mov():
            if pl.direction != 'stop':
                if py.direction == 'down' and enemy_cooldown == 0:
                    ygriega = py.ycor()
                    if(score <= 30):
                        velocidad_proyectil = 20 * (1 + 0.05 * (score // 10))
                        py.sety(ygriega - velocidad_proyectil)
                    else:
                        py.sety(ygriega - 30)
                if pl.direction == 'left':
                    x = pl.xcor()
                    pl.setx(x - 20)
                elif pl.direction == 'right':
                    x = pl.xcor()
                    pl.setx(x + 20)
                
        def shoot():
            nonlocal puntero_b1
            if pl.direction != 'stop':
                sonido_disparo.play()
                bala_actual = balas[puntero_b1]

                x = pl.xcor()
                bala_actual.goto(x, -200)
                bala_actual.direction = 'up'
                bala_actual.showturtle()

                puntero_b1 = (puntero_b1 + 1) % CANTIDAD_BALAS
            
        def stop():
            nonlocal playing
            escribir_al_final("shooter.csv", score, player)
            playing = False

        def pause():
            nonlocal actual_pl_dir
            nonlocal actual_py_dir
            nonlocal actual_bl_dir
            puntero_anterior = (puntero_b1 - 1) % CANTIDAD_BALAS
            bala_actual = balas[puntero_anterior]
            if pl.direction != 'stop':
                actual_pl_dir = pl.direction
                actual_py_dir = py.direction
                actual_bl_dir = bala_actual.direction
                pl.direction = 'stop'
                py.direction = 'stop'
                bala_actual.direction = 'stop'
                text2.clear()
                text2.write('Pause',align='center',font=('Consolas',20,'normal'))
            elif pl.direction == 'stop' and py.direction == 'stop' and bl.direction == 'stop':
                pl.direction = actual_pl_dir
                py.direction = actual_py_dir
                bala_actual.direction = actual_bl_dir
                text2.clear()
                text2.write('',align='center',font=('Consolas',20,'normal'))


        
        sc.onkey(izq,'Left')
        sc.onkey(der,'Right')
        sc.onkey(shoot,'space')
        sc.onkey(stop, 'Escape')
        sc.onkey(pause, 'p')

        sc.listen()
        
        while playing:
            sc.update()

            if enemy_cooldown > 0:
                enemy_cooldown -= 1
            
            #colision con bordes
            if (pl.xcor())<-290 or (pl.xcor())>290:
                sleep(0.05)
                if (pl.xcor())<-290:
                    pl.goto(-290,-200)
                    pl.direction = 'right'
                if (pl.xcor())>290:
                    pl.goto(290,-200)
                    pl.direction = 'left'
            if py.distance(pl) < 20:
                sleep(0.5)
                pl.goto(0,-200)
                pl.direction = 'stop'
                x = en.xcor()
                y = en.ycor()
                py.goto(x,y)
                text.clear()
                
                escribir_al_final("shooter.csv", score, player)
                score = 0
                text.write('Score: {}\tHighscore: {}'.format(score,highscore),align='center',font=('Consolas',20,'normal'))
                
                #esconder
                for bala in balas:
                    bala.goto(-400,400)
                    bala.direction = 'stop'
                    bala.hideturtle()
                
                sleep(0.5)
            
            #manejo de interaccion con las balas
            for bl in balas:
                
                #impacto con enemigo
                if bl.distance(en) < 20:
                    x = randint(-280,280)
                    y = randint(60,280)
                    en.goto(x,y)
                    py.goto(x,y)
                    disparo_enemigo.play()
                    
                    enemy_cooldown = 8

                    score = score + 1
                    if score > highscore:
                        highscore = score
                    bl.goto(400,400)
                    bl.direction = 'stop'
                    bl.hideturtle()
                    
                    text.clear()
                    text.write('Score: {}\tHighscore: {}'.format(score,highscore),align='center',font=('Consolas',20,'normal'))
                
                #movimiento de la bala
                if bl.direction == 'up':
                    y = bl.ycor()
                    bl.sety(y+20)
                
                #se sale de pantalla
                if bl.ycor()>290:
                    bl.goto(-400,400)
                    bl.direction = 'stop'
                    bl.hideturtle()
                    
            if py.ycor()<-290:
                x = en.xcor()
                y = en.ycor()
                py.goto(x,y)
                disparo_enemigo.play()
            mov()
            
            sleep(0.055555)

shooter()