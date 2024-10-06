Metric Clock
============

This program allows the user to play around with different ideas for 
"Metric Time".

A normal day has 86400 seconds, so if a value of hours, minutes, and seconds
are chosen that don't multiply together to give that value then that means
the definition of the second has to be changed.

In that mode of operation then the conversion factor will not be 1:1 and will
either be less than 1 or greater than 1. This program will show the conversion
factor between normal seconds and "metric seconds" that would have to change.

However, if the user chooses hours, minutes, and seconds that total up to 86400
then the conversion will be done 1:1 and the metric clock will display a 
1:1 conversion factor.

By starting the program with command line numeric parameters of
H:M:S (H = Hours, M = Minutes, S = Seconds) the user can choose how many
metric hours per day, minutes per hour, and seconds per minute would be in
their concept of a "Metric Day".

For instance, to choose 10 hours per day, 10 minutes per hour and 864 seconds
per minute, the user would type:

./metriclock.py 10:10:864

With no command-line parameters given, the default is "100:864" 100 hours per
day with 864 minutes per hour and 1 second per minute. 

Please feel free to suggest improvements or suggest changes as GitHub issues.

