#!/usr/bin/env python
import turtle
import time

class Time:
#{
    def __init__( self, hour_ : int, minute_: int, second_: int ) -> None:
    #{
        self.hour   = hour_
        self.minute = minute_
        self.second = second_
    #}
#}

def Draw_Clock( color_ : str, radius_ : float, hour_divisions_ : int, hands_, current_time_ : Time, t_ ):
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
    
    time_set = ( current_time_.hour, current_time_.minute, current_time_.second )  # setting the time

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

    legacy_color = "red"

    legacy_hands = [ ( legacy_color,  80, 24 ),
                     ( legacy_color, 150, 60 ),
                     ( legacy_color, 110, 60 ) ]     # the color and the hands set

    normal_seconds_per_hour   = legacy_hands[ 1 ][ 2 ] * legacy_hands[ 2 ][ 2 ]
    normal_seconds_per_minute = legacy_hands[ 2 ][ 2 ]

    metric_color = "green"
    
    # 86400 seconds is 2^7 * 3^3 * 5^2

    metric_hands = [ ( metric_color,  80,  10 ),
                     ( metric_color, 150,  10 ),
                     ( metric_color, 110, 864 ) ]     # the color and the hands set

    metric_seconds_per_hour   = metric_hands[ 1 ][ 2 ] * metric_hands[ 2 ][ 2 ]
    metric_seconds_per_minute = metric_hands[ 2 ][ 2 ]

    # legacy_seconds_per_metric_second = 1.157407407407407407407

    # total_metric_seconds_per_day = 60 * 60 * 24 * legacy_seconds_per_metric_second

    # print( f"Total Metric Seconds per day = {total_metric_seconds_per_day}" )

    legacy = Time( 0, 0, 0 )
    normal = Time( 0, 0, 0 )
    metric = Time( 0, 0, 0 )

    while True:
    #{
        legacy.hour   = int( time.strftime( "%H" ) )
        legacy.minute = int( time.strftime( "%M" ) )
        legacy.second = int( time.strftime( "%S" ) )

        total_seconds = legacy.hour * 3600 + legacy.minute * 60 + legacy.second

        normal.hour   = int( total_seconds / normal_seconds_per_hour )
        normal.minute = int( ( total_seconds - normal_seconds_per_hour * normal.hour ) / normal_seconds_per_minute )
        normal.second = total_seconds - normal_seconds_per_hour * normal.hour - normal_seconds_per_minute * normal.minute

        metric.hour   = int( total_seconds / metric_seconds_per_hour )
        metric.minute = int( ( total_seconds - metric_seconds_per_hour * metric.hour ) / metric_seconds_per_minute )
        metric.second = total_seconds - metric_seconds_per_hour * metric.hour - metric_seconds_per_minute * metric.minute

        print( f"Legacy Hour={legacy.hour}, Minute={legacy.minute}, Second={legacy.second}" )
        print( f"Normal Hour={normal.hour}, Minute={normal.minute}, Second={normal.second}" )
        print( f"Metric Hour={metric.hour}, Minute={metric.minute}, Second={metric.second}" )
        print( f"TotalSeconds={total_seconds}, PercentDay%={total_seconds / 86400 }" )
        print( "" )

        Draw_Clock( legacy_color, 210, 24, legacy_hands, normal, t )

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
