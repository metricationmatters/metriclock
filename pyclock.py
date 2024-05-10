#!/usr/bin/env python
import turtle
import time

def Draw_Clock( color_, radius_, hour_divisions_, hour_, minute_, second_, t_ ):
#{
    # Draw clock
    t_.up( )  # not ready to draw
    t_.goto( 0, 210 )  # positioning the turtle
    t_.setheading( 180 )   # setting the heading to 180
    t_.color( color_ )  # setting the color of the pen.
    t_.pendown( )     # starting to draw
    t_.circle( radius_ )    # a circle with the radius.

    t_.up( )  # not ready to draw
    t_.goto( 0, 0 )    # positioning the turtle
    t_.setheading( 90 )    # same as seth(90) in newer version

    for z in range( hour_divisions_ ):     # loop
    #{
        t_.fd( 190 )   # moving forward at 190 units
        t_.pendown( )     # starting to draw
        t_.fd( 20 )    # forward at 20
        t_.penup( )   # not ready to draw
        t_.goto( 0, 0 )    # positioning the turtle
        t_.rt( 360 / hour_divisions_ )    # right at an angle of 15 degrees
    #}

    hands = [ ( color_,  80, 24 ),
              ( color_, 150, 60 ),
              ( color_, 110, 60 ) ]     # the color and the hands set
    
    time_set = ( hour_, minute_, second_ )  # setting the time

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
        hour   = int( time.strftime( "%H" ) )
        minute = int( time.strftime( "%M" ) )
        second = int( time.strftime( "%S" ) )

        metric_time = hour * 60 * 60 + minute * 60 + second

        metric_hour   = metric_time / 1000
        metric_minute = metric_time % 1000
        metric_second = metric_time % 60

        print( f"Normal Hour={hour}, Minute={minute}, Second={second}" )
        print( f"Metric Hour={metric_hour}, Minute={metric_minute}, Second={metric_second}" )
        print( f"TotalDaySeconds={metric_time}, MetricTime%={metric_time / 86400 }" )
        print( "" )

        Draw_Clock( "red", 210, 24, hour, minute, second, t )

        # Draw_Clock( "green", 250, 1000, metric_hour, metric_minute, metric_second, t )

        screen.update( )     # updating the screen
        time.sleep( 1 )
        t.clear( )
    #}
#}

if ( __name__ == "__main__" ):
#{
    main( )
#}
