from turtle import *

#This function draws the vertex at the given co-ordinates
def draw_vertex(colour,x,y):
    up()               
    color(colour)
    setpos(x,y-5)
    down()
    pensize(1)
    circle(4)
    s=str(round(x))+','+str(round(y))
    up()

def draw_base_station(colour,x1,y1,x2,y2,x3,y3,x,y):
	begin_fill()
	draw_line('red',x1,y1,x2,y2)
	draw_line('red',x2,y2,x3,y3)
	draw_line('red',x3,y3,x1,y1)
	end_fill()
	up()
	setpos(x,y)
	down()
	pensize(2)
	s='Base Station'
	write(s,align='center',font=("Arial",8, "normal"))
	up()	

#This function draws the edge from one vertex to other with the help of co-ordinates given
def draw_line(colour,x1,y1,x2,y2):
    up()
    color(colour)
    setpos(x1,y1)
    pensize(2)
    down()
    setpos(x2,y2)

def draw_grid(factor):
	draw_line('blue',-50*factor,-50*factor,50*factor,-50*factor)
	draw_line('blue',50*factor,-50*factor,50*factor,50*factor)
	draw_line('blue',50*factor,50*factor,-50*factor,50*factor)
	draw_line('blue',-50*factor,50*factor,-50*factor,-50*factor)
	for i in range(0,100,20):
		draw_line('blue',(-50+i)*factor,-50*factor,(-50+i)*factor,50*factor)
	for i in range(0,100,20):
		draw_line('blue',-50*factor,(-50+i)*factor,50*factor,(-50+i)*factor)

def draw_grid_without_cell(factor):
    draw_line('blue',-50*factor,-50*factor,50*factor,-50*factor)
    draw_line('blue',50*factor,-50*factor,50*factor,50*factor)
    draw_line('blue',50*factor,50*factor,-50*factor,50*factor)
    draw_line('blue',-50*factor,50*factor,-50*factor,-50*factor)
