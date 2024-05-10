#!/usr/bin/env python
import turtle
import time

def Draw_Clock( color_, radius_, hour_divisions_, hands_, hour_, minute_, second_, t_ ):
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
    
    time_set = ( hour_, minute_, second_ )  # setting the time

    for hand in hands_:
    #{
        time_part = time_set[ hands_.index( hand )]
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

    normal_color = "red"

    normal_hands = [ ( normal_color,  80, 24 ),
                     ( normal_color, 150, 60 ),
                     ( normal_color, 110, 60 ) ]     # the color and the hands set

    normal_seconds_per_hour = normal_hands[ 1 ][ 2 ] * normal_hands[ 2 ][ 2 ]
    normal_seconds_per_minute = normal_hands[ 2 ][ 2 ]

    metric_color = "green"
    
    metric_hands = [ ( metric_color,  80,  10 ),
                     ( metric_color, 150,  10 ),
                     ( metric_color, 110, 864 ) ]     # the color and the hands set

    metric_seconds_per_hour   = metric_hands[ 1 ][ 2 ] * metric_hands[ 2 ][ 2 ]
    metric_seconds_per_minute = metric_hands[ 2 ][ 2 ]

    while True:
    #{
        hour   = int( time.strftime( "%H" ) )
        minute = int( time.strftime( "%M" ) )
        second = int( time.strftime( "%S" ) )

        total_seconds = hour * 3600 + minute * 60 + second

        normal_hour   = int( total_seconds / normal_seconds_per_hour )
        normal_minute = int( ( total_seconds - normal_seconds_per_hour * normal_hour ) / normal_seconds_per_minute )
        normal_second = total_seconds - normal_seconds_per_hour * normal_hour - normal_seconds_per_minute * normal_minute


        metric_hour   = int( total_seconds / metric_seconds_per_hour )
        metric_minute = int( ( total_seconds - metric_seconds_per_hour * metric_hour ) / metric_seconds_per_minute )
        metric_second = total_seconds - metric_seconds_per_hour * metric_hour - metric_seconds_per_minute * metric_minute

        print( f"Old    Hour={hour}, Minute={minute}, Second={second}" )
        print( f"Normal Hour={normal_hour}, Minute={normal_minute}, Second={normal_second}" )
        print( f"Metric Hour={metric_hour}, Minute={metric_minute}, Second={metric_second}" )
        print( f"TotalSeconds={total_seconds}, PercentDay%={total_seconds / 86400 }" )
        print( "" )

        Draw_Clock( normal_color, 210, 24, normal_hands, normal_hour, normal_minute, normal_second, t )

        metric_color = "green"

        metric_hands = [ ( metric_color,  80, 24 ),
                         ( metric_color, 150, 60 ),
                         ( metric_color, 110, 60 ) ]     # the color and the hands set

        # Draw_Clock( metric_color, 250, 1000, metric_hands, metric_hour, metric_minute, metric_second, t )

        screen.update( )     # updating the screen
        time.sleep( 1 )
        t.clear( )
    #}
#}

if ( __name__ == "__main__" ):
#{
    main( )
#}
