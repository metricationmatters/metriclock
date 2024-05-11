#!/usr/bin/env python
# Analog Clock
# Based on https://github.com/Arthur-101/CTkClock/tree/main

from datetime import datetime
import math
import string
import sys
from typing import Optional, Tuple

import tkinter as tk

class Time:
#{
    def __init__( self,
                  hour  : int = 0,
                  minute: int = 0,
                  second: int = 0,
                  seconds_per_day: int = 86400,
                  hours_per_day     : int = 24,
                  minutes_per_hour  : int = 60,
                  seconds_per_minute: int = 60 ) -> None:
    #{
        self.hour   = hour
        self.minute = minute
        self.second = second

        self.total_seconds = 0

        self.seconds_factor = seconds_per_day / 86400

        self.seconds_per_day = seconds_per_day

        self.hours_per_day      = hours_per_day
        self.minutes_per_hour   = minutes_per_hour
        self.seconds_per_minute = seconds_per_minute

        self.seconds_per_hour = self.minutes_per_hour * self.seconds_per_minute

        assert self.seconds_per_day == self.hours_per_day * self.minutes_per_hour * self.seconds_per_minute
    #}

    def __str__( self ) -> str:
    #{
        return str( self.hour ) + ":" + str( self.minute ) + ":" + str( self.second )
    #}

    def SetSeconds( self, seconds_: int ) -> None:
    #{
        self.total_seconds = seconds_ * self.seconds_factor

        self.hour   = int( self.total_seconds / self.seconds_per_hour )
        self.minute = int( ( self.total_seconds - self.seconds_per_hour * self.hour ) / self.seconds_per_minute )
        self.second = self.total_seconds - self.seconds_per_hour * self.hour - self.seconds_per_minute * self.minute
    #}
#}

class AnalogClock(tk.Canvas):
#{
    """An analog clock widget"""
    
    def __init__(
        self,
        frame,
        clock_title: str,
        time: Time,
        radius: int = 160,
        border_width: int = 3,
        border_color: str = '#ffffff',
        clock_face_style: str = 'digit', # Options: 'digit or 'tick' or 'none'
        
        fg_color: str = "white",
        bg_color: str = "black",
        
        font: Tuple[str, int, str] = ('Calibri', 12, 'normal'),
        font_color: str = 'black',
        
        hour_color:   str = '#ff0000', # red
        minute_color: str = '#00ff00', # greem
        second_color: str = '#0000ff', # blue
        
        hour_hand_width: int = 7,
        minute_hand_width: int = 5,
        second_hand_width: int = 3,
        
        start_time: Optional[str] = None,
        quarter_hour: bool = False,
        quarter_symbol: Optional[str] = None,   # Can be given any letter or symbol in string form
        quarter_symbol_color: Optional[str] = None,
        # **kwargs
        ):
    #{
        ###  Parameter variables
        self.frame = frame
        self.clock_title = clock_title
        self.time = time
        self.radius = radius
        self.border_width = border_width
        self.border_color = border_color
        self.clock_face_style = clock_face_style

        self.font = font
        self.font_color = font_color
        
        self.hour_color = hour_color
        self.minute_color = minute_color
        self.second_color = second_color
        
        self.hour_hand_width = hour_hand_width
        self.minute_hand_width = minute_hand_width
        self.second_hand_width = second_hand_width
        
        self.start_time = start_time
        self.quarter_hour = quarter_hour
        self.quarter_symbol = quarter_symbol
        self.quarter_symbol_color = quarter_symbol_color
        
        self.fg_color = fg_color
        self.bg_color = bg_color
        
        #  Other Variables
        self.initial_time_set = False
        self.base_time = datetime.now( ) if ( not start_time ) else ( datetime.strptime( start_time, "%H:%M:%S" ) )
        self.last_update_time = datetime.now( )

        # Handling the `fg_color = "transparent"` argument
        if ( fg_color.lower( ) == 'transparent' ):
        #{
            try:
            #{
                if ( self.frame.winfo_name( ).startswith( "!ctkframe" ) ):
                #{
                    # getting bg_color of customtkinter frames
                    self.fg_color = self.frame._apply_appearance_mode( self.frame.cget( "fg_color" ) )
                #}
                else:
                #{
                    self.fg_color = self.frame.cget( "bg" )
                #}
            #}
            except:
            #{
                self.fg_color = "white"
            #}
        #}
        else:
        #{
            self.fg_color = fg_color
        #}

        self.__transparent_bg( )
        
        super( ).__init__( self.frame, bg = self.bg_color, width = 2 * radius, height = 2 * radius, bd = 0, highlightthickness = 0 )


        # Starting the clock update loop
        self.__update_clock( )
    #}

    def __transparent_bg( self, ):
    #{
        # Setting the canvas background color to match the parent's background color
        if ( self.bg_color.lower( ) == 'transparent' ):
        #{
            try:
            #{
                if ( self.frame.winfo_name( ).startswith( "!ctkframe" ) ):
                #{
                    # getting bg_color of customtkinter frames
                    self.bg_color = self.frame._apply_appearance_mode( self.frame.cget( "fg_color" ) )
                #}
                else:
                #{
                    self.bg_color = self.frame.cget( "bg" )
                #}
            #}
            except:
            #{
                self.bg_color = "white"
            #}
        #}
    #}
        

    def __update_clock( self ):
    #{
        """
        Update the clock display with the current time, and schedule the next update.
        """
        now = datetime.now( )

        if ( not self.initial_time_set ):
        #{
            # Set the initial time based on start_time or the current time
            self.initial_time_set = True
            self.last_update_time = now
        #}

        # Calculating the time difference since the last update
        time_difference = now - self.last_update_time
        # Incrementing the base time by this difference
        self.base_time += time_difference
        # Updating the last update time for the next cycle
        self.last_update_time = now

        total_seconds = self.base_time.hour * ( 60 * 60 ) + \
                        self.base_time.minute * ( 60 ) + \
                        self.base_time.second

        self.time.SetSeconds( total_seconds )

        percent_time = self.time.total_seconds / self.time.seconds_per_day

        print( f"{self.clock_title}:  -> {self.time.hours_per_day}:{self.time.minutes_per_hour}:{self.time.seconds_per_minute} -> {self.time} -> Seconds={total_seconds} -> {percent_time:.5f} -> factor {self.time.seconds_factor}" )

        self.__draw_clock( self.time, self.radius )
        self.after( 1000, self.__update_clock )
    #}

    def __draw_clock( self, time_: Time, radius_ ) -> None:
    #{
        """
        Draw a clock on the canvas based on the given seconds, minutes, and hours.
        Parameters:
            time: The current time in hours, minutes, seconds.
            radius: The radius of the circle.
        """
        self.delete( "all" )

        self.__draw_clock_shape( )
       
        # Drawing clock numbers
        self.__draw_clock_numbers( self.time.hours_per_day,    self.hour_color,   radius_, radius_ * 1.0 ) # Hours
        self.__draw_clock_numbers( self.time.minutes_per_hour, self.minute_color, radius_, radius_ * 1.1 ) # minutes

        # Drawing hour hand
        hour_angle = math.radians( time_.hour * ( 360 / time_.hours_per_day ) )
        hour_x = radius_ + radius_ * 0.4 * math.sin( hour_angle )
        hour_y = radius_ - radius_ * 0.4 * math.cos( hour_angle )
        self.create_line(
                          radius_, radius_,
                          hour_x, hour_y,
                          width = self.hour_hand_width,
                          fill = self.hour_color
                        )

        # Drawing minute hand
        minute_angle = math.radians( time_.minute * ( 360 / time_.minutes_per_hour ) )
        minute_x = radius_ + radius_ * 0.6 * math.sin( minute_angle )
        minute_y = radius_ - radius_ * 0.6 * math.cos( minute_angle )
        self.create_line(
                          radius_, radius_, 
                          minute_x, minute_y,
                          width = self.minute_hand_width,
                          fill = self.minute_color
                        )

        # Drawing second hand
        second_angle = math.radians( time_.second * ( 360 / self.time.seconds_per_minute ) )
        second_x = radius_ + radius_ * 0.7 * math.sin( second_angle )
        second_y = radius_ - radius_ * 0.7 * math.cos( second_angle )
        self.create_line(
                          radius_, radius_,
                          second_x, second_y,
                          width = self.second_hand_width,
                          fill = self.second_color
                        )
    #}

    def __draw_clock_numbers( self, total_numbers_: int, color_, length_, radius_ ) -> None:
    #{
        if ( not self.quarter_hour ):           ## If `quarter_hour` is False.
        #{
            for i in range( 1, total_numbers_ + 1 ):
                x, y = self.__coordinate_clock_numbers( i, length_, radius_, total_numbers_ )
                self.__assign_clock_face_style( color_, i, x, y )
        #}
        elif ( self.quarter_hour and not self.quarter_symbol ): ## If `quarter_hour` is True and `quarter_symbol` is False.
        #{
            for i in range( 3, total_numbers_ + 1, 3 ):                             ## Only for 3, 6, 9, 12
                x, y = self.__coordinate_clock_numbers( i, length_, radius_, total_numbers_ )
                self.__assign_clock_face_style( color_, i,  x, y )
        #}                
        elif ( self.quarter_hour and self.quarter_symbol ):         ## If `quarter_hour` is True and `quarter_symbol` is True.
        #{
            for i in range( 1, total_numbers_ + 1 ):                              ## For all numbers
            #{
                x, y = self.__coordinate_clock_numbers( i, length_, radius_, total_numbers_ )
                    
                if ( i % 3 == 0 ):                   ## Writing Only 3, 6, 9, 12
                #{
                    self.__assign_clock_face_style( color_, i, x, y )
                #}
                else:                            ## Drawing Symbols on place of numbers not divisible by `3`
                #{
                    if ( self.quarter_symbol_color ):   ## Using given color for symbols, If `quarter_symbol_color` is given
                    #{
                        self.create_text( x, y, text = self.quarter_symbol, font = self.font, fill = self.quarter_symbol_color )
                    #}
                    else:          ##  If `quarter_symbol_color` is NOT given, using same color as text
                    #{
                        self.create_text( x, y, text = self.quarter_symbol, font = self.font, fill = color_ )
                    #}
                #}
            #}
        #}
    #}
            
    def __draw_clock_shape( self ):
    #{
        # Drawing clock face with a slight padding to not touch the canvas border
        padding = 5
        self.create_oval( padding, padding, 2 * ( self.radius - padding ), 2 * ( self.radius - padding ),
                          width = self.border_width, fill = self.fg_color, outline = self.border_color )
    #}

    def __coordinate_clock_numbers( self, i, length_, radius_, total_number_ ):
    #{
        # Getting Coordinates for clock numbers
        angle = math.radians( i * ( 360 / total_number_ ) )
        x = length_ + radius_ * 0.8 * math.sin( angle )
        y = length_ - radius_ * 0.8 * math.cos( angle )
            
        return x, y
    #}

    def __assign_clock_face_style( self, color_, i_, x_, y_ ):
    #{
        #####   Some constants   #####
        TICKS = { 1: '', 2: '', 3: '/', 4: '', 5: '', 6: '-', 7: '', 8: '', 9: '\\', 10: '', 11: '', 12: '|', 13: '', 14: '', 15: '/', 16: '', 17: '', 18: '-', 19: '', 20: '', 21: '\\', 22: '', 23: '', 24: '|' }
        if ( self.clock_face_style == 'digit' or self.clock_face_style == 'DIGIT' or self.clock_face_style == 'Digit' ):
        #{
            self.create_text( x_, y_, text = str( i_ ), font = self.font, fill = color_ )
        #}
        elif ( self.clock_face_style == 'tick' or self.clock_face_style == 'TICK' or self.clock_face_style == 'Tick' ):
        #{
            self.create_text( x_, y_, text = TICKS[ i_ ], font = self.font, fill = color_ )
        #}
        elif ( self.clock_face_style == None or self.clock_face_style == 'none' or self.clock_face_style == 'None' or self.clock_face_style == 'NONE' ):
        #{
            self.create_text( x_, y_, text = '', font = self.font, fill = color_ )
        #}
    #}


    ####################        METHODS        ####################
    def get_current_time( self ):
    #{
        '''
        This method returns the current time of the clock as a datetime object
        '''
        return self.base_time
    #}

    def get_current_strftime( self, format_string = "%H:%M:%S" ):
    #{
        ''' 
        This method returns the current time of the clock as a formatted string
        The default format is HH:MM:SS, but you can pass another format if desired
        '''
        return self.base_time.strftime( format_string )
    #}

    def configure( self, **kwargs ):
    #{
        '''
        To configure some options of the clock
        radius: int = 150,
        border_width: int = 3,
        border_color: str = '#a6a6a6',
        clock_face_style: str = 'digit', # Options: 'digit or 'tick' or 'none'
        
        fg_color: str = "transparent",
        bg_color: str = "transparent",
        
        font: Tuple[str, int, str] = ('Calibri', 12, 'regular'),
        font_color: str = 'black',
        
        hour_color: str = '#383838',
        minute_color: str = '#454545',
        second_color: str = '#ff3e3e',
        
        hour_hand_width: int = 4,
        minute_hand_width: int = 3,
        second_hand_width: int = 1,
        
        start_time: Optional[str] = None,
        quarter_hour: bool = False,
        quarter_symbol: Optional[str] = None,   # Can be given any letter or symbol in string form
        quarter_symbol_color: Optional[str] = None,
        '''
        if ( 'radius' in kwargs ):
        #{
            self.radius = kwargs.pop( 'radius' )
            self.config( width = 2 * self.radius, height = 2 * self.radius )
        #}
        
        if ( 'border_width' in kwargs ):
        #{
            self.border_width = kwargs.pop( 'border_width' )
        #}

        if ( 'border_color' in kwargs ):
        #{
            self.border_color = kwargs.pop( 'border_color' )
        #}

        if ( 'clock_face_style' in kwargs ):
        #{
            self.clock_face_style = kwargs.pop( 'clock_face_style' )
        #}

        if ( 'fg_color' in kwargs ):
        #{
            self.fg_color = kwargs.pop( 'fg_color' )
        #}

        if ( 'bg_color' in kwargs ):
        #{
            self.bg_color = kwargs.pop( 'bg_color' )
            self.__transparent_bg( )
            self.config( bg = self.bg_color )
        #}
        
        if ( 'font' in kwargs ):
        #{
            self.font = kwargs.pop( 'font' )
        #}

        if ( 'font_color' in kwargs ):
        #{
            self.font_color = kwargs.pop( 'font_color' )
        #}

        if ( 'hour_color' in kwargs ):
        #{
            self.hour_color = kwargs.pop( 'hour_color' )
        #}

        if ( 'minute_color' in kwargs ):
        #{
            self.minute_color = kwargs.pop( 'minute_color' )
        #}

        if ( 'second_color' in kwargs ):
        #{
            self.second_color = kwargs.pop( 'second_color' )
        #}

        if ( 'hour_hand_width' in kwargs ):
        #{
            self.hour_hand_width = kwargs.pop( 'hour_hand_width' )
        #}

        if ( 'minute_hand_width' in kwargs ):
        #{
            self.minute_hand_width = kwargs.pop( 'minute_hand_width' )
        #}

        if ( 'second_hand_width' in kwargs ):
        #{
            self.second_hand_width = kwargs.pop( 'second_hand_width' )
        #}

        if ( 'start_time' in kwargs ):
        #{
            self.start_time = kwargs.pop( 'start_time' )
            self.base_time = datetime.strptime( self.start_time, "%H:%M:%S" )
        #}

        if ( 'quarter_hour' in kwargs ):
        #{
            self.quarter_hour = kwargs.pop( 'quarter_hour' )
        #}

        if ( 'quarter_symbol' in kwargs ):
        #{
            self.quarter_symbol = kwargs.pop( 'quarter_symbol' )
        #}

        if ( 'quarter_symbol_color' in kwargs ):
        #{
            self.quarter_symbol_color = kwargs.pop( 'quarter_symbol_color' )
        #}

        # Update the clock appearance
        self.__update_clock( )
    #}
#}

########
# MAIN #
########
if ( __name__ == "__main__" ):
#{
    # Default metric values:

    metric_hours_per_day = 100
    metric_minutes_per_hour = 100
    metric_seconds_per_minute = 100

    if ( len( sys.argv ) > 1 ):
    #{
       metric_hours_per_day, metric_minutes_per_hour, metric_seconds_per_minute = str.split( sys.argv[ 1 ], ":" )
       metric_hours_per_day = int( metric_hours_per_day )
       metric_minutes_per_hour = int( metric_minutes_per_hour )
       metric_seconds_per_minute = int( metric_seconds_per_minute )
    #}

    metric_seconds_per_day = metric_hours_per_day * metric_minutes_per_hour * metric_seconds_per_minute

    frame = tk.Tk( )
    frame.title( 'Analog Clock' )

    legacy_clock = Time( )
    clock1 = AnalogClock( frame, "Legacy", legacy_clock )
    clock1.pack( )

    metric_clock = Time( seconds_per_day = metric_seconds_per_day,
                         hours_per_day = metric_hours_per_day,
                         minutes_per_hour = metric_minutes_per_hour,
                         seconds_per_minute = metric_minutes_per_hour )
    
    # Radius 320 is good for clock face of 100 numbers.
    clock2 = AnalogClock( frame, "Metric", metric_clock, radius = 320 )
    clock2.pack( )

    frame.mainloop( )
#}
