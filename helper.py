# Helper functions for the Blackfoot project

from replit import audio
import time
import wave
import random
import pygame
import numpy


# Main Interface for the User
def main_interface():
    global current_scene
    global current_image
    user_total_scores = {"town": 0,
						 "restaurant": 0,
						 "home": 0,
						 "greetings": 0,
						 "family": 0}
    # The below print statement clears the output screen for the user.
    print('\033c')
    continue_looping = True

    while continue_looping:
        print("What would you like to do?\n"
              "\n1) Learn some words around you (Learn)"
              "\n2) Review your Blackfoot vocabulary (Review)"
              "\n3) Have me test you (Test)"
              "\n4) Go somewhere else (Move)"
              "\n5) View your current test scores (Scores)"
              "\n6) Translate and listen to Blackfoot (Translate)"
              "\n7) Stop learning and exit the program (Exit)\n")

        main_interface_choice = input("► ").lower().strip(" !.?':)(,")

        # Once the user selects their choice, it will display the image
        # for the current scene and call the relevant function

        if main_interface_choice == "learn" or \
			main_interface_choice == "1":
            display_image(current_image)
            learn_option(current_scene)

        elif main_interface_choice == "review" or \
			main_interface_choice == "2":
            display_image(current_image)
            review_option(current_scene)

        elif main_interface_choice == "test" or \
			main_interface_choice == "3":
            display_image(current_image)
            user_total_scores = test_option(current_scene, user_total_scores)

        elif main_interface_choice == "move" or \
			main_interface_choice == "4":
            display_image(current_image)
            # The move function will return a scene title by the user
            # And this will be set as the current scene
            current_scene = move_option()
            current_image = getImage("images/" + current_scene + ".png")
            display_image(current_image)

        elif main_interface_choice == "scores" or \
			main_interface_choice == "5":
            display_image(current_image)
            scores_option(user_total_scores)

        elif main_interface_choice == "translate" or \
			main_interface_choice == "6":
            display_image(speech_synthesis_image)
            speech_synthesis()

        elif main_interface_choice == "exit" or \
			main_interface_choice == "7":
            continue_looping = False
            exit()

        else:
            print('\033c')
            print("Sorry, I don’t understand", main_interface_choice + ".\n")

# The input will be the scene name and the function will
# Create a dictionary of all the Blackfoot/English words for that scene
def vocabulary_file(scene):
    dictionary_words = {}
    scene_file = open("vocabulary/" + scene + ".txt")

    for line in scene_file:
        (blackfoot, english) = line.strip().split(",")
        dictionary_words[blackfoot] = english

    return dictionary_words

# The input is the current image for the scene.
# The output will display that image
def display_image(current_image):
    showImage(current_image, "Let's Learn Blackfoot!")

# The Learn option involves the user typing an English word
# And getting back the Blackfoot word equivalent
def learn_option(scene):
    print('\033c')

    # The vocabulary_file function returns a dictionary of Blackfoot/English words
    vocabulary_words = vocabulary_file(scene)
    print(
        "Great, let's learn! Look around here and tell me a word in English.\n"
        + "What do you want to learn the Blackfoot word for?\n")
    user_learn_word = input("Word: ").lower().strip(" !.':,").capitalize()

    # The display_blackfoot_word will use the English word input by the user
    # And it will display the Blackfoot word equivalent
    display_blackfoot_word(vocabulary_words, user_learn_word)
    continue_learning = True
    while continue_learning:
        input()
        print('\033c')
        print("What Blackfoot word do you want to learn?\n\n"
              "✮ Type the word in English\n"
              "✮ Type 'done' to finish.\n")
        user_learn_word = input("Word: ").lower().strip(" !.':,").capitalize()
        if user_learn_word == "Done":
            continue_learning = False
        else:
            display_blackfoot_word(vocabulary_words, user_learn_word)
    main_interface()


# The function will use the English word input by the user and it will
# display the Blackfoot word equivalent by using the vocabulary dictionary
def display_blackfoot_word(dictionary_words, word_user_wants_to_learn):
    blackfoot_learn_words = []

    # The list appends all the English vocabulary values in the particular scene
    for (blackfoot_key, english_value) in dictionary_words.items():
        blackfoot_learn_words.append(english_value)

    # If the user's word is in the English values,
    # The Blackfoot equivalent will be displayed
    if word_user_wants_to_learn in blackfoot_learn_words:
        for (blackfoot_key, english_value) in dictionary_words.items():
            if english_value == word_user_wants_to_learn:
                print(blackfoot_key)
                play_audio_blackfoot(blackfoot_key)
                print("\nPress <enter> to continue.")
    else:
        print("Are you sure you typed that correctly?")
        print("\nPress <enter> to continue.")


# The review function will display an English word from the scene
# And ask the user to choose between two Blackfoot words
# This function meets the expectations of the Custom Testing.
def review_option(scene):
    print('\033c')
    continue_review = True

    while continue_review:
        print('\033c')
        # The vocabulary_file function returns a dictionary
        # of Blackfoot/English words
        vocabulary_words = vocabulary_file(scene)

        # The following will first randomize the words for the user
        # and append them to the blackfoot_words list
        blackfoot_words = []
        (blackfoot_answer, english) = (random.choice(
            list(vocabulary_words.items())))

        random_word = True

        while random_word:
            random_blackfoot_word = (random.choice(
                list(vocabulary_words.keys())))

            # We must make sure that the two Blackfoot choices given
            # to the user are not the same
            if random_blackfoot_word != blackfoot_answer:
                random_word = False

        blackfoot_words.append(blackfoot_answer)
        blackfoot_words.append(random_blackfoot_word)

        # Both the random and actual Blackfoot word are added
        # to the list. We must again make sure that the two
        # choices are randomized. The displayed format
        # shouldn't always be "Is it 'Answer_Word' or 'Random_Word'?"

        first_word = random.choice(blackfoot_words)
        blackfoot_words.remove(first_word)
        second_word = random.choice(blackfoot_words)

        print("What is " + english + " in Blackfoot?"
              "\nIs it " + first_word + " or " + second_word + "?")
        print("\nType done to finish reviewing.\n")

        play_audio_blackfoot(first_word)
        play_audio_blackfoot(second_word)

        user_answer = input().lower().strip(" !.':,").capitalize()

        if user_answer == blackfoot_answer:
            input("\nGood job! That was correct ✔\nPress <enter> to continue.")
        elif user_answer == "Done":
            continue_review = False
        else:
            print("\nNope, the correct answer was " + blackfoot_answer + "."
                  "\nPress <enter> to continue.")
            play_audio_blackfoot(blackfoot_answer)
            input()
    main_interface()


# The test function will have the scene name and total scores as input
# The total scores will update after each test as needed.
# The user will be quizzed on the English translation of the words. 
def test_option(scene, total_scores):
    print('\033c')

    # The vocabulary_file function returns a dictionary
    # of Blackfoot/English words
    vocabulary_words = vocabulary_file(scene)

    score = 0
    start_time = time.time()

    # The user will be asked 10 questions and their total time is recorded.
    for i in range(10):
        print('\033c')

        # The following will first randomize and display the test word
        (blackfoot_key, english_value) = (random.choice(
            list(vocabulary_words.items())))

        print("Question " + str(i + 1) + " of 10: What is " + blackfoot_key +
              "? ")
        play_audio_blackfoot(blackfoot_key)

        user_learn_word_guess = input("Your response: ").lower().strip(
            " !.':,").capitalize()

        if user_learn_word_guess == english_value:
            print("\nGood job! That was correct ✔\nPress <enter> to continue.")
            score += 1
            input()
        else:
            print("\nNope, the correct answer was " + english_value +
                  ".\nPress <enter> to continue")
            input()
    # The total seconds elasped will be displayed with 2 decimal places
    end_time = time.time()
    total_time = end_time - start_time
    formatted_time = "{:.2f}".format(total_time)

    print("You got " + str(score) + "/10 right! It took you " +
          formatted_time + " seconds to finish.")
    input("Press <enter> to continue. ")

    print('\033c')

    # If the user scored higher in this test, we will update the top score
    for (scene_name, top_score) in total_scores.items():
        if scene_name == scene:
            if score > top_score:
                total_scores[scene_name] = score
    return total_scores


# The Move function will allow the user to move between scenes
def move_option():
    continue_asking_to_move = True

    while continue_asking_to_move:
        print('\033c')
        print("Where do you want to go?\n"
              "\n✮ Town"
              "\n✮ Restaurant"
              "\n✮ Home"
              "\n✮ Greetings"
              "\n✮ Family\n")

        move_scene = input("► ").lower().strip("!.,?")

        if move_scene in ["town", "restaurant", "home", "greetings", "family"]:
            print('\033c')
            # The user's movie_scene title is returned by the function
            return move_scene
    main_interface()


# This function takes the total scores as input
# And displays each scene title with its top score
def scores_option(scene_score):
    print('\033c')

    for (scene_name, top_score) in scene_score.items():
        print("Scene: " + str(scene_name).capitalize() + "\nTop Score: " +
              str(top_score) + "/10\n")

    print("Press <enter> to return to the main menu.")
    input()
    print('\033c')


# The user provides phrases in English that are translated
# And spoken in the Blackfoot language
def speech_synthesis():
    print('\033c')

    # The vocabulary_file function returns a dictionary
    # of Blackfoot/English words
    all_words = open("vocabulary/all_words.txt")

    continue_speech_synthesis = True

    while continue_speech_synthesis:
        view_words()
        # seek(0) will return the pointer to the start
        # of the file after each run
        all_words.seek(0)

        sentence_wav = []
        blackfoot_time_word = ""
        blackfoot_verb = ""
        blackfoot_noun = ""

        print("Follow the instructions to create your own sentence "
              "in Blackfoot translated from English.\n"
              "Press <enter> if the word category is not applicable.\n")

        time_word = input(
            "Enter a time or greeting word ('Today', 'This morning', Hello'): "
			).lower().strip(" !,.").capitalize()

        verb = input("Enter a verb ('I will go', 'I will eat'): "
		).lower().strip(" !,.").capitalize()

        input("Enter any filler words before the noun ('to the', 'to a'): "
              ).lower().strip(" !,.").capitalize()

        noun = input("Enter an applicable noun ('Bread', 'Girl', 'House'): "
                     ).lower().strip(" !,.").capitalize()

        # If the English word is also present in the vocabulary file,
        # append the names of the words to sentence_wav
        for line in all_words:
            word_pair = line.strip().split(",")

            if time_word == word_pair[1]:
                blackfoot_time_word = word_pair[0]
                sentence_wav.insert(0, "sounds/" + time_word.lower().strip("?") + ".wav")

            if verb == word_pair[1]:
                blackfoot_verb = word_pair[0]
                sentence_wav.insert(1, "sounds/" + verb.lower().strip("?") + ".wav")

            if noun == word_pair[1]:
                blackfoot_noun = word_pair[0]
                sentence_wav.insert(2, "sounds/" + noun.lower().strip("?") + ".wav")

        print("\nBlackfoot Translation: " + blackfoot_time_word,
              blackfoot_verb, blackfoot_noun)

        # We need to make sure that the user provided at least one word
        if len(sentence_wav) > 0:
            # Test if playing the audio file produces an error
            try:
                concat(sentence_wav, "sentence_sound.wav")
                audio.play_file("sentence_sound.wav")
			# If there are no errors, the sound file will play
			# Otherwise, the following will help us handle the error.
            except:
                print("Please try again. Your sentence could not be created at this time")
        else:
            print("Please try again. Your sentence could not be created at this time")

		# Ask if the user would like to continue speech synthesis
        continue_audio = input(
            "\nPress <enter> to continue.\n"
            "Type 'Exit' to return to the main interface. ").lower().strip(
                " !.'?")
        if continue_audio == "exit":
            print('\033c')
            display_image(current_image)
            continue_speech_synthesis = False


# The input is the blackfoot word
# The output will be the sound file played for that word
def play_audio_blackfoot(blackfoot_word):
    all_words = open("vocabulary/all_words.txt")

    # Translate the Blackfoot word to English
    # The sound file names are in English
    for line in all_words:
        word_pair = line.strip().split(",")
        if blackfoot_word == word_pair[0]:
            english_word = word_pair[1].lower().strip(" ?")
	# Test if playing the audio file produces an error
    try:
        audio.play_file("sounds/" + english_word + ".wav")
        time.sleep(1)
	# If there is an error, no sound will be played.
    except:
        pass


# Allows user to view all applicable words for the speech synthesis
# User can choose which word category to view
def view_words():
	print('\033c')
	noun_words = open("vocabulary/noun_words.txt")
	time_words = open("vocabulary/time_words.txt")
	verb_words = open("vocabulary/verb_words.txt")

	print("Do you want to see what you can type before you start creating sentences?"
	"(Yes/No)")
	view_words = input().lower().strip(" !.':,")

	continue_viewing_words = True

	while continue_viewing_words:
		print('\033c')
		# seek(0) will return the pointer to the start
		# of the files after each run
		noun_words.seek(0)
		time_words.seek(0)
		verb_words.seek(0)
		if view_words == "yes":
			print("Which words do you want to see? (time/verb/noun)?\n\n"
			"Type 'all' to view all the words.\n"
			"Type 'exit' to start creating sentences.\n")

			view_which_words = input().lower().strip(" !.':,")

			# Show the user all the vocabulary words depending on whether they 
			# want to view a specific category or all of them together
			if view_which_words == "all":
				print("\nTime and Greeting words:")
				for time_word in time_words:
					print(time_word.strip())

				print("\nVerbs:")
				for verb in verb_words:
					print(verb.strip())

				print("\nNouns:")
				for noun in noun_words:
					print(noun.strip())
				input("\nPress <enter> to continue. ")

			elif view_which_words == "time":
				print("\nTime words:")
				for time_word in time_words:
					print(time_word.strip())
				input("\nPress <enter> to continue. ")

			elif view_which_words == "verb":
				print("\nVerbs:")
				for verb in verb_words:
					print(verb.strip())
				input("\nPress <enter> to continue. ")

			elif view_which_words == "noun":
				print("\nNouns:")
				for noun in noun_words:
					print(noun.strip())
				input("\nPress <enter> to continue. ")

			elif view_which_words == "exit":
				continue_viewing_words = False
				print('\033c')

			else:
				print("\nSorry, I don't understand",view_which_words+
				". Please <enter> to try again.")
				input()
		else:
			continue_viewing_words = False
			print('\033c')

def concat(infiles, outfile):
    """
  Input: 
  - infiles: a list containing the filenames of .wav files to concatenate,
    e.g. ["hello.wav","there.wav"]
  - outfile: name of the file to write the concatenated .wav file to,
    e.g. "hellothere.wav"
  Output: None
  """
    data = []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()
    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()


def getImage(filename):
    """
  Input: filename - string containing image filename to open
  Returns: 2d array of RGB values
  """
    image = pygame.image.load(filename)
    return pygame.surfarray.array3d(image).tolist()


def showImage(pixels, title):
    """
    Input:  pixels - 2d array of RGB values
            title - title of the window
    Output: show the image in a window
    """
    nparray = numpy.asarray(pixels)
    surf = pygame.surfarray.make_surface(nparray)
    (width, height, colours) = nparray.shape
    pygame.display.init()
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((width, height))
    screen.fill((225, 225, 225))
    screen.blit(surf, (0, 0))
    pygame.display.update()


# Most of the above funtions make use of the following information
current_scene = "town"
current_image = getImage("images/" + current_scene + ".png")
speech_synthesis_image = getImage("images/translate.png")
