from turtle import Screen, Turtle
from time import sleep
from random import randint
from manejo_archivos import escribir_al_final, leer_y_obtener_max_score, resource_path

def bbreaker():
    #Pantalla
    sc = Screen()
    sc.title('Brick Breaker')
    sc.bgcolor('blue')
    sc.setup(width=600,height=600)
    sc.tracer(0)

    player = sc.textinput("Jugador", "Ingrese nombre de jugador:")

    if player or player.strip() != '':

        posp = 0.11
        x = randint(-280,280)
        y = randint(-280,280)
        score = 0
        highscore = leer_y_obtener_max_score("brick_breaker.csv", player)

        carita = resource_path("carita.gif")
        cuerpito = resource_path("cuerpito.gif")
        comidita = resource_path("comidita.gif")

        sc.addshape(carita)
        sc.addshape(cuerpito)
        sc.addshape(comidita)
        
        #Cabeza
        hd = Turtle()
        hd.speed(0)
        hd.shape(carita)
        hd.penup()
        hd.goto(0,0)
        hd.direction = 'stop'
        
        #Food
        fd = Turtle()
        fd.speed(0)
        fd.shape(comidita)
        fd.penup()
        fd.goto(x,y)

        #Cuerpo
        cuerpo = []
        
        #Score
        text = Turtle()
        text.speed(0)
        text.color('white')
        text.penup()
        text.hideturtle()
        text.goto(0,260)
        text.write('Score: 0\tHighscore: {}'.format(highscore),align='center',font=('Consolas',20,'normal'))
        
        #Pierde
        gmov = Turtle()
        gmov.speed(0)
        gmov.color('white')
        gmov.penup()
        gmov.hideturtle()
        gmov.goto(0,200)
        gmov.playing = True

        def arriba():
            if hd.direction != 'down':
                hd.direction = 'up'
        def abajo():
            if hd.direction != 'up':
                hd.direction = 'down'
        def izq():
            if hd.direction != 'right':
                hd.direction = 'left'
        def der():
            if hd.direction != 'left':
                hd.direction = 'right'

        def mov():
            if hd.direction == 'up':
                y = hd.ycor()
                hd.sety(y+20)
            elif hd.direction == 'down':
                y = hd.ycor()
                hd.sety(y-20)
            elif hd.direction == 'left':
                x = hd.xcor()
                hd.setx(x-20)
            elif hd.direction == 'right':
                x = hd.xcor()
                hd.setx(x+20)
        
        def stop():
            escribir_al_final("brick_breaker.csv", score, player)
            gmov.playing = False

        sc.listen()
        sc.onkey(arriba,'Up')
        sc.onkey(abajo,'Down')
        sc.onkey(izq,'Left')
        sc.onkey(der,'Right')
        sc.onkey(stop, 'Escape')

        while gmov.playing:
            sc.update()
            if hd.distance(fd) < 20:
                x = randint(-280, 280)
                y = randint(-280, 280)
                fd.goto(x,y)
                newseg = Turtle()
                newseg.speed(0)
                newseg.shape(cuerpito)
                newseg.penup()
                cuerpo.append(newseg)

                sc.getcanvas().tag_raise(hd.turtle._item)

                score += 1
                if score > highscore:
                    highscore = score
                text.clear()
                text.write('Score: {}\tHighscore: {}'.format(score,highscore),align='center',font=('Consolas',20,'normal'))
            
            #colision con bordes
            if (hd.xcor())<-290 or (hd.xcor())>290 or (hd.ycor())<-290 or (hd.ycor())>290:
                sleep(0.5)
                hd.goto(0,0)
                hd.direction = 'stop'
                
                #esconder
                for seg in cuerpo:
                    seg.goto(400,400)
                cuerpo.clear()
                text.clear()
                escribir_al_final("brick_breaker.csv", score, player)
                score = 0
                text.write('Score: {}\tHighscore: {}'.format(score,highscore),align='center',font=('Consolas',20,'normal'))
                while ((hd.xcor())==0 and (hd.ycor())==0):
                    gmov.write('Game Over',align='center',font=('Consolas',20,'normal'))
                    break
                sleep(0.5)
                gmov.clear()
            
            #movercuerpo
            totalseg = len(cuerpo)
            for index in range(totalseg - 1, 0, -1):
                x = cuerpo[index - 1].xcor()
                y = cuerpo[index - 1].ycor()
                cuerpo[index].goto(x,y)
            if totalseg > 0:
                x = hd.xcor()
                y = hd.ycor()
                cuerpo[0].goto(x,y)
            mov()
            
            #colisiones con cuerpo
            for seg in cuerpo:
                if seg.distance(hd) < 20:
                    sleep(0.5)
                    hd.goto(0,0)
                    hd.direction = 'stop'
                    
                    #esconder
                    for seg in cuerpo:
                        seg.goto(400,400)
                    
                    cuerpo.clear()
                    text.clear()
                    
                    escribir_al_final("brick_breaker.csv", score, player)
                    score = 0
                    text.write('Score: {}\tHighscore: {}'.format(score,highscore),align='center',font=('Consolas',20,'normal'))
                    while ((hd.xcor())==0 and (hd.ycor())==0):
                        gmov.write('Game Over',align='center',font=('Consolas',20,'normal'))
                        break
                    sleep(0.5)
                    gmov.clear()
            sleep(posp)

bbreaker()