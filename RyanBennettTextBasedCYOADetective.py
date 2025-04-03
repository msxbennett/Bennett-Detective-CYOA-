import sys
import time
import random
import os

# ANSI color codes for a different style to each type of text
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[35m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Money variable
money = 0

# Defines how the game will end after a win or a loss.
def clear_exit():
    time.sleep(15)
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears terminal
    exit()

# Function to print text with a typewriter effect
def slow_print(text, delay=0.025):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Defines one of the goals you are trying to achieve. The tuition goal.
def check_tuition_goal():
    tuition_goal = 1000
    if money >= tuition_goal:
        slow_print(GREEN + f"\nYou collected ${money}! Your son's college tuition is secured!" + RESET)
    else:
        slow_print(RED + f"\nUnfortunately, you only collected ${money}. Your son will need student loans... How are you going to tell him this?" + RESET)
    time.sleep(2)

# Introduction to the game
def intro():
    slow_print(CYAN + "Welcome back to the office, Detective. 🔍" + RESET)
    slow_print("You are a struggling personal investigator willing to do " + RED + "anything to make ends meet" + RESET + ".")
    slow_print("Your son's college tuition needs to be paid next month, so you will need to earn at least $1000.")
    slow_print("You failed your most recent case, and The Department will remove you from this position if you don't solve your next case.")
    slow_print(YELLOW + "Do whatever needs to be done to succeed." + RESET)
    slow_print("It's up to " + GREEN + BOLD + "you" + RESET + " to discern which clues will lead you to the right culprit, and which are meant to throw you off.")
    slow_print("Scrutinise everything, even if it makes you overthink. The Department will not accept a blind accusation.")
    slow_print("Also your magic terminal will reset every 15 seconds so you don't have to worry about a clogged screen.\n")
    time.sleep(2)
    slow_print("Your client will be delivered to your inbox momentarily...." + RESET)
    time.sleep(2)

    # Presents the client
    slow_print(BLUE + "\nNew Case Assigned:" + RESET)
    slow_print("Vincent Holloway - A local businessman found dead under mysterious circumstances.")
    
    # The first choice the user gets - accepting the case
    while True:
        choice = input("\nDo you accept this case? (yes/no): ").strip().lower()
        if choice == "yes":
            slow_print(YELLOW + "\nYou have accepted Vincent Holloway's case." + RESET)
            return True
        elif choice == "no":
            slow_print(RED + "\nYou rejected the case. The Department has fired you. Good going. " + RESET)
            check_tuition_goal()
            clear_exit()  # Ends the game immediately
        else:
            slow_print(RED + "Invalid choice! Please type 'yes' or 'no'." + RESET)

# Case and suspect details - hobbies and height
def assign_case():
    suspects = {
    "Mr Black": "Mr Black: 6'3 - A former security consultant, dismissed for suspicious activity at his posts.\n\n\033[92mHobbies:\033[0m\nCollecting and comparing his suits\nIroning\nDriving\n\033[91mDislikes:\033[0m\nThe double windsor\nLounging at home\n",
    "Ms Green": "Ms Green: 5'6 - A local florist. Financial troubles indicate she may have needed quick money, possible ties to illegal gambling. Uncrackable poker face.\n\n\033[92mHobbies:\033[0m\nCooking\nBluffing\nCleaning\n\033[91mDislikes:\033[0m\nTwo pair aces, two pair eights\n",
    "Dr White": "Dr White: 5'10 - A well-known doctor in town. Had disputes with the victim over unpaid checkups.\n\n\033[92mHobbies:\033[0m\nPart-time tailor\nCooking\nOvercharging\n\033[91mDislikes:\033[0m\nSelf-diagnoses\n",
    "Captain Blue": "Captain Blue: 5'7 - A not very well-respected officer, and rumors of corruption swirl. Known to work closely with the victim on side projects. Possible charges for embezzlement, but that's not your area.\n\n\033[92mHobbies:\033[0m\nSelf-hygiene\nDonuts\nIssuing parking tickets\n\033[91mDislikes:\033[0m\nBeing questioned\n",
    }
    
    # List for location retrieval
    locations = {
        "Crime Scene":["woah what's this doing here"],
        "Victims House": ["I don't know you tell me"],
        "Detectives Office": ["still waiting..."],
    }
    return suspects, locations

# Function to randomly select a murderer
def choose_murderer(suspects):
    random.seed(time.time())  # Ensures randomness across game sessions
    return random.choice(list(suspects.keys()))

# Defines a function that randomly exposes you for committing unlawful actions
def corruption_check():
    """30% chance of getting caught when doing corrupt actions"""
    return random.random() < 0.3  # 30% chance of getting caught

# Defines a function that will make the prime suspect attempt to bribe you to avoid jail time
def bribe_attempt(murderer, bribed_suspects=set()):
    global money
    if murderer in bribed_suspects:
        return False
    
    # Dialogue and user choice for accepting or denying bribe
    amount = random.randint(1000, 2000)
    slow_print(YELLOW + f"\n{murderer} pulls you aside. 'You're getting too close to ratting me out... Let's make a deal.'" + RESET)
    slow_print(YELLOW + f"Forget about this, and I'll give you ${amount}... Far more than the Department will ever pay you.'\n" + RESET)
    choice = input("You consider whether or not the higher-ups will notice it. Do you accept the bribe? (yes/no): ").strip().lower()

    # User gets caught
    if choice == "yes":
        if corruption_check():
            slow_print(RED + "\nA hidden camera captures the exchange! Internal Affairs arrives within minutes. I hope you have a good CV." + RESET)
            check_tuition_goal()
            clear_exit()
        # User escapes - moral dilemmas
        money += amount
        slow_print(GREEN + "\nYou took the money and escaped getting caught! Your badge feels just that little bit heavier." + RESET)
        slow_print(GREEN + f"\nYou now have ${money} and the option to frame someone for an easy case closed. You feel good now?")
        bribed_suspects.add(murderer)
        return True
    # User denies the bribe
    else:
            slow_print(RED + "\nYou wear your badge with integrity. The culprit looks nervous... everything has backfired." + RESET)
            slow_print(RED + "They continue to provide their testimony in the hopes it will throw you off. But you know better." + RESET)
    return False

# Defines one of the 4 main actions - Function to use money
def use_money(murderer, suspects):
    global money
    if money > 0:
        slow_print(YELLOW + f"\nYou have ${money}. Do you want to buy something? (snack - $50, donate - $200, frame - $700, cancel)" + RESET)
        choice = input("> ").strip().lower()

        # Options
        if choice == "snack" and money >= 50:
            slow_print(GREEN + "You bought a ridiculously overpriced snack. It does nothing. Enjoy." + RESET)
            money -= 50
        elif choice == "donate" and money >= 200:
            slow_print(GREEN + "Wow. Mr Philanthropist, please sign my autograph. A very noble deed, but don't you have things of your own to tend to?" + RESET)
            money -= 200
        elif choice == "frame" and money >= 700:
            # Chance for the user to get caught
            if corruption_check():
                slow_print(RED + "\nYour planted evidence is discovered during lab analysis!" + RESET)
                check_tuition_goal()
                clear_exit()
            # User escapes
            framed_suspect = random.choice(list(suspects.keys()))
            slow_print(GREEN + f"You paid off some shady people. The evidence now points to {framed_suspect}." + RESET)
            money -= 700
            return framed_suspect  # Changes the murderer
        else:
            slow_print(GREEN + "\nYou decide to be frugal today. Good on you." + RESET)
    if money == 0:
        slow_print(RED + "\nSorry, you're broke lmao")
    return murderer

# First investigation scene at the crime scene itself
def crime_scene_investigation(murderer, suspects):
    slow_print(RED + "\nYou arrive at the Crime Scene. The air is thick with tension." + RESET)
    slow_print("A small crowd has gathered behind the police tape, whispering theories.")
    slow_print("The crime scene is about a day old, so it's still fresh. You noticed a few blood stains along the pavement ground. A few objects lie scattered nearby.")

    # Options for investigation
    while True:
        slow_print("\nWhat do you want to investigate first?")
        slow_print("1) The blood stain on the ground")
        slow_print("2) The torn piece of cloth")
        slow_print("3) Footprints leading away")
        slow_print("4) Leave the crime scene")
        
        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            # Blood Stain Investigation (DNA Test)
            slow_print(GREEN + "\nYou kneel down beside the blood stain, careful not to touch anything." + RESET)
            slow_print("A forensic officer nearby offers to run a quick DNA test.")

            time.sleep(2)  # Simulate time passing

            # DNA result points to a suspect, but changes depending on who the murderer is
            suspect_dna = random.choice(list(suspects.keys()))
            if suspect_dna == murderer:
                slow_print(YELLOW + f"\nThe DNA results are back. It belongs to {suspect_dna}. This could be major evidence!" + RESET)
            else:
                slow_print(RED + f"\nThe DNA belongs to {suspect_dna}, but further investigation reveals they had a legitimate reason to be here." + RESET)
                slow_print("A dead end... for now.")

        elif choice == "2":
            # Torn Cloth Investigation (Fabric Clue)
            slow_print(GREEN + "\nYou pick up a small, torn piece of cloth near the body." + RESET)
            slow_print("The texture feels expensive, possibly from a suit or a uniform.")
            
            if murderer == "Mr Black":
                slow_print(YELLOW + "\nIt seems to match a fabric from a bespoke Gieves & Hawkes suit. Speke linen... very tasteful. This could be useful." + RESET)
            elif murderer == "Ms Green":
                slow_print(YELLOW + "\nIt seems to be cut from an apron. What type of apron though? I'll keep this." + RESET)
            elif murderer == "Dr White":
                slow_print(YELLOW + "\nI can smell the disinfectant from here. This culprit must love to stay clean..." + RESET)
            elif murderer == "Captain Blue":
                slow_print(YELLOW + "\nIt's a clean blue to black gradient across the strip. But it could belong to anyone. Let's keep going." + RESET)

        elif choice == "3":
            # Footprint Investigation (A little Red Herring)
            slow_print(GREEN + "\nYou follow the footprints leading away from the crime scene." + RESET)
            slow_print("They lead into a dark alleyway before abruptly disappearing.")
            slow_print("Checking the treads, they seem to belong to a pair of running shoes, size 10.")
            slow_print("Unfortunately, that could be anyone. A dead end... for now.")

        elif choice == "4":
            slow_print(RED + "\nYou decide to leave the crime scene for now." + RESET)
            return  # Exits investigation
        
        else:
            slow_print(RED + "\nInvalid choice! Try again." + RESET)

# The second investigation scene in the victim's house
def victims_house_investigation(murderer, suspects):
    slow_print(BLUE + "\nYou enter the victim's house. The air smells faintly of lavender and something metallic." + RESET)
    slow_print("The living room is meticulously clean, with only a few objects out of place.")
    
    # Options for investiation
    while True:
        slow_print("\nWhat do you want to examine?")
        slow_print("1) An expensive-looking painting")
        slow_print("2) The blinking answering machine")
        slow_print("3) A partial fingerprint on a wine glass")
        slow_print("4) Leave the house")
        
        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "2":
            # Phone call analysis
            slow_print(GREEN + "\nYou press play on the answering machine. A distorted voice message plays:" + RESET)
            slow_print("\"'We need to talk about...' *static* '...meet me...' *static* '...dangerous...'\"" + RESET)
            slow_print("\nThe recording ends abruptly with a loud click.")
            
            # Choose analysis method
            slow_print("\nHow do you want to analyse the recording?")
            method = input("1) Enhance it yourself\n2) Call in an audio expert\n> ").strip()
            
            if method == "1":
                slow_print(YELLOW + "\nYou put on headphones and carefully clean up the audio..." + RESET)
                time.sleep(2)
                # Narrows suspects down to masculine or feminine based on their voice frequency
                voice_clue = "masculine" if murderer in ["Mr Black", "Dr White"] else "feminine"
                slow_print(f"\nThe enhanced voice is clearly {voice_clue}.")
                
                if murderer in ["Mr Black", "Dr White"]:
                    slow_print(YELLOW + "This eliminates Ms Green and Captain Blue as suspects!" + RESET)
                else:
                    slow_print(YELLOW + "This eliminates Mr Black and Dr White as suspects!" + RESET)

            # Bad ending for deciphering the recording        
            elif method == "2":
                slow_print("\nYou call the department's audio expert. As you wait, you hear a floorboard creak...")
                time.sleep(2)
                slow_print(RED + f"\nYou turn around only to see {murderer}, poised, with a calm smile on their face and a kitchen knife in their hand." + RESET)
                slow_print(RED + f"You realise too late that {murderer} had intercepted the message." + RESET)
                time.sleep(3)
                slow_print(RED + "Everything fades to black as you bleed out..." + RESET)
                slow_print("\nYou think of your son one final time.")
                clear_exit()  # Game over
            else:
                slow_print(RED + "Invalid choice! The moment passes." + RESET)
        
        # Another user decision that cross checks with previously found profles to narrow down more suspects     
        elif choice == "3":
            # Fingerprint analysis
            slow_print(GREEN + "\nYou notice a partial fingerprint on a crystal wine glass." + RESET)
            slow_print("How do you want to collect it?")
            method = input("1) Use sticky tape\n2) Use silver nitrate\n> ").strip()
            
            if method == "1":
                slow_print(RED + "\nThe tape smudges the print! The evidence is ruined." + RESET)
                slow_print("You return to examining the house...")
                continue
            elif method == "2":
                # Eliminate one wrong suspect
                wrong_suspects = [s for s in suspects if s != murderer]
                eliminated = random.choice(wrong_suspects)
                slow_print(YELLOW + f"\nYou cross check with your suspect profiles and conclude the print doesn't match {eliminated}'s. Good find." + RESET)
            else:
                slow_print(RED + "Invalid choice! Try again." + RESET)
                continue
                
        elif choice == "1":
            # Red herring
            slow_print(GREEN + "\nYou examine the painting - a landscape of the countryside." + RESET)
            slow_print("It's beautifully rendered with exquisite brushwork. Rather mesmerising this one...")
            time.sleep(5)
            slow_print("After 20 minutes of staring, you realise this has nothing to do with the case. But, you make a mental note on who the painter is for later.")

        # Option to leave    
        elif choice == "4":
            slow_print(RED + "\nYou decide to leave the house for now." + RESET)
            return
        else:
            slow_print(RED + "\nInvalid choice! Try again." + RESET)

# The third and final investigation scene at the user's own office
def detectives_office_investigation(murderer, suspects):
    slow_print(BLUE + "\nYou enter your dimly lit office. Papers are strewn across your desk, and the smell of stale coffee lingers in the air." + RESET)
    slow_print("Your terminal blinks with unread messages. The case files from earlier sit in a neat stack.")
    
    # More user options for investigation
    while True:
        slow_print("\nWhat do you want to examine in your office?")
        slow_print("1) Listen to your boss's urgent voicemail")
        slow_print("2) Mysterious can of shoe polish on your desk")
        slow_print("3) Reread the case files for missed details")
        slow_print("4) Leave the office")
        
        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            # Boss's message with height clue
            slow_print(GREEN + "\nYou press play on your voicemail. Your boss's gruff voice comes through:" + RESET)
            slow_print("\"'Listen up... got some intel from forensics. The perp's height is between...' *static*")
            
            # Determine height range based on murderer
            if murderer in ["Ms Green", "Captain Blue"]:  # Shorter suspects
                height_range = "5'3 and 5'8"
            elif murderer in ["Dr White"]:  # Medium height
                height_range = "5'6 and 5'11"
            else:  # Mr Black (tall)
                height_range = "5'9 and 6'5"
            
            slow_print(f"\nThe message clears up: '...between {height_range}. Keep this quiet.'" + RESET)
            slow_print(YELLOW + "The files from earlier should help me narrow it down further..." + RESET)

        elif choice == "3":
            # Case file review with tip
            slow_print(GREEN + "\nYou carefully go through the case files again. A small sticky note falls out from one of them:" + RESET)
            
            # Choose a non-murderer to eliminate
            innocent_suspects = [s for s in suspects if s != murderer]
            if innocent_suspects:  # Ensure there are innocent suspects left
                cleared_suspect = random.choice(innocent_suspects)
                slow_print(YELLOW + f"\nIt's from your mate in Forensics: 'Hey, double-checked {cleared_suspect}'s alibi. They're clean.'" + RESET)
                slow_print(YELLOW + f"Nice, you can safely eliminate {cleared_suspect} from your suspicions." + RESET)
            else:
                slow_print(RED + "\nAll other suspects have already been eliminated! The murderer must be the remaining one..." + RESET)

        elif choice == "2":
            # Red herring - shoe polish
            slow_print(GREEN + "\nYou pick up the can of shoe polish. It's an expensive brand, barely used." + RESET)
            slow_print("You spend the next 20 minutes polishing your shoes to a mirror shine.")
            time.sleep(3)
            slow_print("While polishing, you notice one of the posters reads: 'Minimum 2 scene investigations and 2 suspect interviews required for indictment.'")
            slow_print("You wonder when that was nailed up... huh.")
            time.sleep(5)
            slow_print("\nYour shoes look fantastic! But you come to your senses and realise what a waste of time that was." + RESET)

        # Option to leave
        elif choice == "4":
            slow_print(RED + "\nYou leave the office, the weight of the case still heavy on your shoulders." + RESET)
            return
        else:
            slow_print(RED + "\nInvalid choice! Try again." + RESET)

# Defines one of the 4 main actions in the game - investigation
def investigate(murderer, locations, suspects):
    slow_print(BLUE + "\nWhere would you like to investigate?" + RESET)
    for place in locations:
        slow_print(f"- {place}")
    
    choice = input("\nType a location: ").title()

    # Directs users to each scene
    if choice == "Crime Scene":
        crime_scene_investigation(murderer, suspects)
    elif choice == "Victims House":
        victims_house_investigation(murderer, suspects)
    elif choice == "Detectives Office":
        detectives_office_investigation(murderer, suspects)

# Second main action - function to question a suspect
def question_suspect(murderer, suspects, bribed_suspects=set()):
    slow_print(BLUE + "\nWho would you like to question?" + RESET)
    for suspect in suspects:
        slow_print(f"- {suspect}")
    
    choice = input("\nType a suspect's name: ").title()
        # Check for bribe first (for any murderer)
    if choice == murderer and random.randint(1, 10) <= 3:  # 30% chance
        if bribe_attempt(murderer, bribed_suspects):
            return choice
    
        # Scenario specific to each suspect
    if choice == "Mr Black":
        if choice == murderer:
            # Mr Black is the murderer, add contradictions to his responses
            slow_print("\nMr Black looks increasingly agitated as you press him. He stumbles over his words, claiming he had been home the whole time.")
            slow_print("He stumbles over his words and avoids eye contact. His phone rings, and he abruptly hangs up. ")
        else:
            slow_print("\nMr Black looks visibly nervous. He avoids eye contact, but his words are confident and he maintains his composure.")
            slow_print("However, you notice a smear on his suit... That is unlike him.")
        
    elif choice == "Ms Green":
        if choice == murderer:
            # Ms Green is the murderer, add contradictions to her responses
            slow_print("\nMs Green fidgets with her bracelet as you question her.")
            slow_print("Her hands are shaking, and she keeps looking at her watch, almost as if waiting for something.")
            slow_print("You recall seeing her leave the scene just after the crime. The timing doesn't add up.")
        else:
            slow_print("\nMs Green looks around cautiously as she speaks. She says she was at the market, but no one recalls seeing her there.")
            slow_print("The timing doesn't add up.")
        
    elif choice == "Dr White":
        if choice == murderer:
            # Dr White is the murderer, add contradictions to his responses
            slow_print("\nDr White's calm demeanor seems forced.'")
            slow_print("You notice a small scratch on his hand that he quickly tries to hide.")
            slow_print("When asked about the victim's last appointment, he hesitates too long, looking around the room nervously.")
        else:
            slow_print("\nDr White acts calm and composed, stating he was just passing by the crime scene when he saw the commotion.")
            slow_print("But when you ask him about the victim's last appointment, he avoids the question.")
        
    elif choice == "Captain Blue":
        if choice == murderer:
            # Captain Blue is the murderer, add contradictions to her responses
            slow_print("\nCaptain Blue is not eager to help at all. She claims to have arrived first to report the crime.")
            slow_print("But when you press her on the details, her story shifts slightly, as if she's trying to cover up something.")
            slow_print("Her eagerness to explain every detail only makes you more suspicious.")
        else:
            slow_print("\nCaptain Blue is not eager to help. She claims to have arrived first to report the crime.")
            slow_print("But her story doesn't match the police logs. Why was she the first one there?")

        return choice
    else:
        slow_print(RED + "Invalid choice! Try again." + RESET)
        return question_suspect(murderer, suspects)

# Function to randomly determine commission earnings
def earn_commission():
    return random.randint(500, 1000)

#Defines one of the 4 main actions - the final accusation
def accuse(murderer, suspects):
    global money
    slow_print(RED + "\nWho do you think is the murderer?" + RESET)
    for suspect in suspects:
        slow_print(f"- {suspect}")
    
    choice = input("\nType a name: ").title()
    
    # Makes sure the accusation is a suspect - ultimate accusation scene
    if choice in suspects:
        if choice == murderer:
            commission = earn_commission()
            money += commission
            slow_print(MAGENTA + "\nYou SLAM your fist on the table." + BOLD + f"'It was {choice}!'" + RESET)
            time.sleep(2)
            slow_print(GREEN + f"\nCongratulations, {choice} was the murderer! Your career has been saved!" + RESET)
            slow_print(YELLOW + f"\nThe Department has paid you a commission of ${commission} for your excellent work!" + RESET)
            slow_print(GREEN + f"\n💰Final Money Balance: ${money}💰\n" + RESET)
            check_tuition_goal()
            clear_exit()  # Directly exit on win
        else:
            slow_print(MAGENTA + f"\nYou SLAM your fist on the table. It was {choice}!" + RESET)
            slow_print(RED + f"\nIncorrect! {choice} was not the murderer. The real culprit was {murderer}." + RESET)
            slow_print(RED + "The Department has fired you for incompetence." + RESET)
            check_tuition_goal()
            clear_exit()  # Directly exit on lose
    else:
        slow_print(RED + "Invalid name! Try again." + RESET)
        return False
    
# Mechanic for learning about suspects in the intro - gain understanding of the suspects
def learn_about_suspects():
    slow_print(BLUE + "\nWould you like to learn more about the suspects before proceeding?" + RESET)
    choice = input("1) Check their case files in the office.\n2) No need, get it going.\n> ").strip().lower()

    if choice == "1":
        return office_investigation()
    elif choice == "2":
        slow_print(RED + "\nAlright calm down if you say so..." + RESET)
        return
    else:
        slow_print(RED + "Invalid choice! Please type '1' or '2'." + RESET)
        return learn_about_suspects()

# Office investigation for suspect files
def office_investigation():
    slow_print(BLUE + "\nYou head to the Detective's Office to cross-check the information." + RESET)
    suspects, _ = assign_case()
    slow_print("\nWhich suspect's file would you like to review?\n")
    
    # Prints suspects
    while True:
        slow_print(RED + "Suspects" + RESET)
        for suspect in suspects:
            slow_print(f"- {suspect}")
        
        # User decides which case files they want to open
        choice = input("\nType a suspect's name to read their file, or type 'done' to finish: ").title()
        if choice in suspects:
            slow_print(YELLOW + f"\nYou open {choice}'s case file and learn the following:\n" + RESET)
            slow_print(f"{suspects[choice]}")
        elif choice == 'Done':
            break  # Stop reviewing files
        else:
            slow_print(RED + "\nInvalid choice! Try again.\n" + RESET)

# Function to randomly find money to boost towards the tuition goal
def find_money():
    global money
    if random.randint(1, 5) == 1:  # 20% chance to find money with every interaction
        amount = random.randint(10, 40)
        money += amount
        slow_print(GREEN + f"\n💰 You found ${amount} on the ground! You now have ${money}." + RESET)

# Mechanises the game itself - links up every action 
def play_game():
    global money
    if not intro():
        clear_exit()

    suspects, locations = assign_case()
    murderer = choose_murderer(suspects)

    learn_about_suspects()

    investigated_locations = 0  # Track how many locations we've investigated
    questioned_suspects = 0 # Track how any suspects we've questioned

    # Asks user every time a scene ends
    while True:
        slow_print(BLUE + "\nWhat would you like to do? (investigate, question, accuse, use money)" + RESET)
        action = input("> ").strip().lower()

        # Main actions of the game are printed and user decides
        if action == "investigate":
            investigate(murderer, locations, suspects)
            investigated = True
            investigated_locations += 1  
        elif action == "question":
            question_suspect(murderer, suspects)
            questioned_suspects +=1
            questioned = True
        elif action == "use money":
            murderer = use_money(murderer, suspects)
        elif action == "accuse":
            # Making sure user can't accuse without proper evidence
            if investigated_locations == 0 and questioned_suspects == 0 :
                slow_print(RED + "\nYou made a blind accusation without any investigation or questioning!" + RESET)
                slow_print(RED + "The Department has fired you for incompetence." + RESET)
                check_tuition_goal()
                clear_exit()  # Directly exit on invalid accusation
            
            # Require at least 2 investigations AND at least 1 questioning
            elif investigated_locations < 2 or questioned_suspects < 2:
                slow_print(RED + "\nYou try to deliver a verdict, but The Department requires more evidence before making an accusation!" + RESET)
                slow_print(RED + f"They say you need to investigate at least 2 locations. You've been to {investigated_locations} so far..." + RESET)
                slow_print(RED + "You also need to question at least 2 suspects.")
                continue
            
            result = accuse(murderer, suspects)
            if not result:  # Only continues if accusation was invalid (wrong name)
                continue
        else:
            slow_print(RED + "\nInvalid choice! Try again." + RESET)

        find_money()