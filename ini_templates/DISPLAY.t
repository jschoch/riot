##doc:  This is a test of cheetah templates for rio post generation processing
[DISPLAY]
# a test prepended comment to the display section
$riogen

EMBED_TAB_NAME=Cycles
EMBED_TAB_LOCATION = ntb_preview
EMBED_TAB_COMMAND = halcmd loadusr -Wn gladevcp gladevcp -c gladevcp -U notouch=1 -U norun=1 -u /home/schoch/lathemacros/LatheMacros/lathehandler.py -x {XID} /home/schoch/lathemacros/LatheMacros/lathemacro.ui


#  good example of custimization depending on which ui is selected and configured in RIO
#EMBED_TAB_NAME = JOGGIE
#EMBED_TAB_LOCATION = ntb_preview
#EMBED_TAB_COMMAND = gladevcp  -H g_pendant.hal -x {XID} pendant.ui
