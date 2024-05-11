#!/usr/bin/env python
# Analog Clock

import tkinter as tk
import math
from datetime import datetime
from typing import Optional, Tuple

class Time:
#{
    def __init__( self,
                  hour  : int,
                  minute: int,
                  second: int,
                  hours_per_day     : tuple[ int, float ] = 24,
                  minutes_per_hour  : tuple[ int, float ] = 60,
                  seconds_per_minute: tuple[ int, float ] = 60 ) -> None:
    #{
        self.hour   = hour
        self.minute = minute
        self.second = second

        self.hours_per_day      = hours_per_day
        self.minutes_per_hour   = minutes_per_hour
        self.seconds_per_minute = seconds_per_minute

        self.seconds_per_day  = self.hours_per_day * self.minutes_per_hour * self.seconds_per_minute
        self.seconds_per_hour = self.minutes_per_hour * self.seconds_per_minute
    #}
#}

class AnalogClock(tk.Canvas):
#{
    """An analog clock widget"""
    
    def __init__(
        self,
        master,
        hours_per_day: int = 24,
        minutes_per_hour: int = 60,
        seconds_per_minute: int = 60,
        radius: int = 150,
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
        self.master = master
        self.hours_per_day = hours_per_day
        self.minutes_per_hour = minutes_per_hour
        self.seconds_per_minute = seconds_per_minute
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
                if ( master.winfo_name( ).startswith( "!ctkframe" ) ):
                #{
                    # getting bg_color of customtkinter frames
                    self.fg_color = master._apply_appearance_mode( master.cget( "fg_color" ) )
                #}
                else:
                #{
                    self.fg_color = master.cget( "bg" )
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
        
        super( ).__init__( self.master, bg = self.bg_color, width = 2 * radius, height = 2 * radius, bd = 0, highlightthickness = 0 )


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
                if ( self.master.winfo_name( ).startswith( "!ctkframe" ) ):
                #{
                    # getting bg_color of customtkinter frames
                    self.bg_color = self.master._apply_appearance_mode( self.master.cget( "fg_color" ) )
                #}
                else:
                #{
                    self.bg_color = self.master.cget( "bg" )
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

        legacy = Time( 0, 0, 0 )
        normal = Time( 0, 0, 0 )
        metric = Time( 0, 0, 0, hours_per_day = 100 )

        legacy.second = self.base_time.second
        legacy.minute = self.base_time.minute
        legacy.hour   = self.base_time.hour
        
        total_seconds = legacy.hour * (legacy.seconds_per_minute * legacy.minutes_per_hour ) + \
                        legacy.minute * ( legacy.seconds_per_minute ) + \
                        legacy.second

        percent_time = total_seconds / legacy.seconds_per_day

        normal.hour   = int( total_seconds / normal.seconds_per_hour )
        normal.minute = int( ( total_seconds - normal.seconds_per_hour * normal.hour ) / normal.seconds_per_minute )
        normal.second = total_seconds - normal.seconds_per_hour * normal.hour - normal.seconds_per_minute * normal.minute


        print( f"Legacy {legacy.hour}:{legacy.minute}:{legacy.second} -> TotalSeconds={total_seconds} -> {percent_time:.5f}" )

        self.__draw_clock( legacy.second, legacy.minute, legacy.hour )
        self.after( 1000, self.__update_clock )
    #}

    def __draw_clock( self, seconds, minutes, hours ):
    #{
        """
        Draw a clock on the canvas based on the given seconds, minutes, and hours.
        Parameters:
            hours (int): The hours component of the time.
            minutes (int): The minutes component of the time.
            seconds (int): The seconds component of the time.
        """
        self.delete( "all" )

        self.__draw_clock_shape( )
       
        # Drawing clock numbers
        if ( not self.quarter_hour ):           ## If `quarter_hour` is False.
        #{
            for i in range( 1, self.hours_per_day + 1 ):
                x, y = self.__coordinate_clock_numbers( i )
                self.__assign_clock_face_style( i, x, y )
                # self.create_text(x, y, text=str(i), font=self.font, fill=self.font_color)
        #}
        elif ( self.quarter_hour and not self.quarter_symbol ): ## If `quarter_hour` is True and `quarter_symbol` is False.
        #{
            for i in range( 3, self.hours_per_day + 1, 3 ):                             ## Only for 3, 6, 9, 12
                x, y = self.__coordinate_clock_numbers( i )
                self.__assign_clock_face_style( i, x, y )
                # self.create_text(x, y, text=str(i), font=self.font, fill=self.font_color)
        #}                
        elif ( self.quarter_hour and self.quarter_symbol ):         ## If `quarter_hour` is True and `quarter_symbol` is True.
        #{
            for i in range( 1, self.hours_per_day + 1 ):                              ## For all numbers
            #{
                x, y = self.__coordinate_clock_numbers( i )
                    
                if ( i % 3 == 0 ):                   ## Writing Only 3, 6, 9, 12
                #{
                    self.__assign_clock_face_style( i, x, y )
                    # self.create_text(x, y, text=str(i), font=self.font, fill=self.font_color)
                #}
                else:                            ## Drawing Symbols on place of numbers not divisible by `3`
                #{
                    if ( self.quarter_symbol_color ):   ## Using given color for symbols, If `quarter_symbol_color` is given
                    #{
                        self.create_text( x, y, text = self.quarter_symbol, font = self.font, fill = self.quarter_symbol_color )
                    #}
                    else:          ##  If `quarter_symbol_color` is NOT given, using same color as text
                    #{
                        self.create_text( x, y, text = self.quarter_symbol, font = self.font, fill = self.font_color )
                    #}
                #}
            #}
        #}
                        

        # Drawing hour hand
        hour_angle = math.radians( hours * ( 360 / self.hours_per_day ) )
        hour_x = self.radius + self.radius * 0.4 * math.sin( hour_angle )
        hour_y = self.radius - self.radius * 0.4 * math.cos( hour_angle )
        self.create_line(
                          self.radius, self.radius,
                          hour_x, hour_y,
                          width = self.hour_hand_width,
                          fill = self.hour_color
                        )

        # Drawing minute hand
        minute_angle = math.radians( minutes * ( 360 / self.minutes_per_hour ) )
        minute_x = self.radius + self.radius * 0.6 * math.sin( minute_angle )
        minute_y = self.radius - self.radius * 0.6 * math.cos( minute_angle )
        self.create_line(
                          self.radius, self.radius, 
                          minute_x, minute_y,
                          width = self.minute_hand_width,
                          fill = self.minute_color
                        )

        # Drawing second hand
        second_angle = math.radians( seconds * ( 360 / self.seconds_per_minute ) )
        second_x = self.radius + self.radius * 0.7 * math.sin( second_angle )
        second_y = self.radius - self.radius * 0.7 * math.cos( second_angle )
        self.create_line(
                          self.radius, self.radius,
                          second_x, second_y,
                          width = self.second_hand_width,
                          fill = self.second_color
                        )
    #}
        
    def __draw_clock_shape( self, ):
    #{
        # Drawing clock face with a slight padding to not touch the canvas border
        padding = 5
        self.create_oval( padding, padding, 2 * ( self.radius - padding ), 2 * ( self.radius - padding ),
                          width = self.border_width, fill = self.fg_color, outline = self.border_color )
    #}

    def __coordinate_clock_numbers( self, i ):
    #{
        # Getting Coordinates for clock numbers
        angle = math.radians( i * ( 360 / self.hours_per_day ) )
        x = self.radius + self.radius * 0.8 * math.sin( angle )
        y = self.radius - self.radius * 0.8 * math.cos( angle )
            
        return x, y
    #}

    def __assign_clock_face_style( self, i, x, y ):
    #{
        #####   Some constants   #####
        TICKS = { 1: '', 2: '', 3: '/', 4: '', 5: '', 6: '-', 7: '', 8: '', 9: '\\', 10: '', 11: '', 12: '|', 13: '', 14: '', 15: '/', 16: '', 17: '', 18: '-', 19: '', 20: '', 21: '\\', 22: '', 23: '', 24: '|' }
        if ( self.clock_face_style == 'digit' or self.clock_face_style == 'DIGIT' or self.clock_face_style == 'Digit' ):
        #{
            self.create_text( x, y, text = str( i ), font = self.font, fill = self.font_color )
        #}
        elif ( self.clock_face_style == 'tick' or self.clock_face_style == 'TICK' or self.clock_face_style == 'Tick' ):
        #{
            self.create_text( x, y, text = TICKS[ i ], font = self.font, fill = self.font_color )
        #}
        elif ( self.clock_face_style == None or self.clock_face_style == 'none' or self.clock_face_style == 'None' or self.clock_face_style == 'NONE' ):
        #{
            self.create_text( x, y, text = '', font = self.font, fill = self.font_color )
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
    frame = tk.Tk( )
    frame.title( 'Analog Clock' )

    clock = AnalogClock( frame, radius = 150, )
    clock.pack( )

    frame.mainloop( )
#}
