# Audio-Visual Language Learning App for Blackfoot
# This project is an interactive text, image and audio-based language
# learning app for people to learn Blackfoot, an endangered Canadian language.

import helper

# Clear the output screen for the user.
print('\033c')

# To begin,load up the default image and set the scene to "Town" for the user.
current_scene = "town"
current_image = helper.getImage("images/" + current_scene + ".png")
helper.display_image(current_image)

print("Oki (Hello)! Welcome to Brocket, Alberta!"
      "\nI can teach you some Blackfoot while you are here!\n"
      "\nPress <enter> to begin learning.")
input()

helper.main_interface()
