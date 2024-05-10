#!/usr/bin/env python
import turtle
import time

def Draw_Clock( hourr_, minutee_, secondd_, t_ ):
#{
    t_.up( )  # not ready to draw
    t_.goto( 0, 210 )  # positioning the turtle
    t_.setheading( 180 )   # setting the heading to 180
    t_.color( "red" )  # setting the color of the pen to red
    t_.pendown( )     # starting to draw
    t_.circle( 210 )    # a circle with the radius 210

    t_.up( )  # not ready to draw
    t_.goto( 0, 0 )    # positioning the turtle
    t_.setheading( 90 )    # same as seth(90) in newer version

    for z in range( 24 ):     # loop
    #{
        t_.fd( 190 )   # moving forward at 190 units
        t_.pendown( )     # starting to draw
        t_.fd( 20 )    # forward at 20
        t_.penup( )   # not ready to draw
        t_.goto( 0, 0 )    # positioning the turtle
        t_.rt( 15 )    # right at an angle of 15 degrees
    #}

    hands = [ ( "black",  80, 24 ),
              ( "black", 150, 60 ),
              ( "black", 110, 60 ) ]     # the color and the hands set
    time_set = ( hourr_, minutee_, secondd_ )  # setting the time

    for hand in hands:
    #{
        time_part = time_set[ hands.index( hand )]
        angle = ( time_part / hand[ 2 ] ) * 360     # setting the angle for the clock
        t_.penup( )   # not ready to draw
        t_.goto( 0, 0 )    # positioning the turtle
        t_.color( hand[ 0 ] )    # setting the color of the hand
        t_.setheading( 90 )    # same as seth(90)
        t_.rt( angle )     # right at an angle of "right"
        t_.pendown( )     # ready to draw
        t_.fd( hand[ 1 ] )   # forward at a unit of 1st index of the hand var
    #}
#}

def main( ):
#{
    screen = turtle.Screen( )    # Loading Canvas
    screen.bgcolor( "white" )     # Bg
    screen.setup( width = 600, height = 600 )
    screen.title( "Analog Clock" )
    screen.tracer( 0 )

    t = turtle.Turtle( )
    #t.hideturtle( ) # Make the turtle invisible
    t.speed( 0 )  # Setting the speed to 0
    t.pensize( 3 )    # Setting the pensize to 3

    while True:
    #{
        hourr   = int( time.strftime( "%H" ) )
        minutee = int( time.strftime( "%M" ) )
        secondd = int( time.strftime( "%S" ) )

        print( f"Hour={hourr}, Minute={minutee}, Second={secondd}" )

        Draw_Clock( hourr, minutee, secondd, t )
        screen.update( )     # updating the screen
        time.sleep( 1 )
        t.clear( )
    #}
#}

if ( __name__ == "__main__" ):
#{
    main( )
#}
