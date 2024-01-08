import pygame
import pygame_gui
import random
import speech_recognition as sr
import threading
import csv
import pyttsx3
from gtts import gTTS
import os
import time
from pygame_gui import UIManager, UI_TEXT_ENTRY_CHANGED
from pygame_gui.elements import UIWindow, UITextEntryBox, UITextBox
import data
from emailer import send_email
import smtplib

# Define a flag variable to indicate whether to continue or stop the thread
speech_continue_flag = True
speak_continue_flag = True

score = 0
# Set the delay time to 5000 milliseconds (5 seconds)
delay_time = 2000


def checkAnswer(user_answer):

    if user_answer=="skip":
        speak(f"Skipping question number {(item_number+1)}")
    else:
        global score

        user_answer = user_answer.replace("letter","").strip()    

        user_answer_value=-1

        if user_answer=="a":
            user_answer_value=0

        elif user_answer=="b":
            user_answer_value=1

        elif user_answer=="c":
            user_answer_value=2

        elif user_answer=="d":
            user_answer_value=3

        else:
            return -1

        correct_value = -1
        ls = list(rows[item_number].values())[1:6]
        for i, opt in enumerate(ls):
            if opt==4:
                break
            if opt==ls[4]:
                correct_value=i
                break

        say_value = random.randint(0,2)
        if correct_value==user_answer_value:
            if (say_value==0):
                speak("Correct!")
            if (say_value==1):
                speak("Excellent!")
            if (say_value==2):
                speak("Impressive!")
            score+=1
        else:
            speak(f"Sorry, the answer is actually {ls[4]}")
        


# Get the current time in milliseconds
current_time = pygame.time.get_ticks()


engine = pyttsx3.init()
engine.setProperty('voice', 'english-us')

# Define a function to handle pyttsx3 in a separate thread
def speak(text):
    substrings = text.split(',')
    print(substrings)
    try:
        # question = substrings[0]  # "what is the use of elements"
        # a2 = substrings[2]  # "sadas"
        # b2 = substrings[3]  # "sadas"
        # b2 = substrings[4]  # "sadas"
        # c2 = substrings[6]  # "sadas"
        # d2 = substrings[8]  # "sadas"
        
        # engine.say(question)
        # engine.say("A")
        # engine.say(a2)
        # engine.say("B")
        # engine.say(b2)
        # engine.say("C")
        # engine.say(c2)
        # engine.say("D")
        # engine.say(d2)
        for phrase in substrings:
            engine.say(phrase)
        engine.runAndWait()

    except:
        engine.say(text)
        engine.runAndWait()

    time.sleep(1)

r = sr.Recognizer()
r.quiet = True
recognized_word=""

def recognize_speech():
    global speech_continue_flag, r
    if speech_continue_flag==False:
        return

    time.sleep(15)
    global recognized_word 
    """Recognize speech and update recognized_word"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("Choose letter a to d")
        while speech_continue_flag:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source,  phrase_time_limit=1)
            try:
                recognized_word = r.recognize_google(audio)
                print(recognized_word)
            except sr.UnknownValueError:
                pass

# Open the CSV file
with open('quiz.csv', newline='') as csvfile:
    
    # Create a CSV reader object
    reader = csv.DictReader(csvfile)
    
    # Initialize an empty list to store the rows
    rows = []
    
    # Iterate over each row in the CSV file
    for row in reader:
        
        # Append the row to the list of rows
        rows.append(row)

# Print the list of rows
#print(rows)


item_number = 0


prompt = rows[item_number]['question']
prompt += ",A," + rows[item_number]['opt1']
prompt += ",B," + rows[item_number]['opt2']
prompt += ",C," + rows[item_number]['opt3']
prompt += ",D," + rows[item_number]['opt4']

pygame.init()


# Set up the Pygame window and manager
display_size = (700, 400)
window_surface = pygame.display.set_mode(display_size)
pygame.display.set_caption("QuizkPy: CITE012A-CS32S1-HCI")

manager = pygame_gui.UIManager(display_size)

# Load the logo image
logo_image = pygame.image.load("tip_logo.png")

# Create the image element
logo_element = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((270, 15), (150, 150)),
    image_surface=logo_image,
    manager=manager,
)

# Create the email entry box
email_text_box = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((50, 180), (600, 50)),
    placeholder_text='username@tip.edu.ph',
    manager=manager)

# Create the email entry box
email_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((50, 150), (50, 50)),
    text='Email ',
    manager=manager)

# Create the OTP entry box
otp_text_box = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((50, 250), (600, 50)),
    placeholder_text='******',
    manager=manager)

# Create the OTP entry box
otp_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((50, 220), (50, 50)),
    text='OTP   ',
    manager=manager)


# Create the login button
login_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 320), (600, 50)),
    manager=manager,
    text='Send OTP to Email')

otp_text_box.disable()

my_email = ""

# Run the game loop
clock = pygame.time.Clock()

start = []
end = []

OTPnumber = 328749

def randomxy():
    return [random.randint(600,640),random.randint(0,0)]

for i in range(0,5):
    s = randomxy()
    start.append(s)
    end.append([-s[1],s[0]])
    
is_running = True
while is_running:

    window_surface.fill((37, 41, 46))

    for i in range(0,5):
        pygame.draw.line(window_surface, (102, 204, 255), start[i], end[i] , 2)

    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Process GUI events
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == email_text_box:
                    my_email = email_text_box.text
                    otp = otp_text_box.text
                    
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == login_button:
                    if login_button.text=="Send OTP to Email":
                        if email_text_box.text.endswith("@tip.edu.ph")==True:
                            try:
                                send_email("QuizkPy OTP",f"The QuizkPy OTP Number is {OTPnumber}", my_email)
                                OTPnumber = random.randint(1000000,1900000)
                                my_email = email_text_box.text
                                otp_text_box.enable()
                                email_text_box.disable()
                                email_text_box.set_text(my_email)
                                login_button.set_text("Login and Start Quiz")
                            except smtplib.SMTPDataError:
                                speak("There was an error in the system. Please communicate the issue with the administrator")
                            except:
                                speak("Incorrect, OTP number")
                        else:
                            print(email_text_box.text)
                            engine.say("Input your valid TIP email address")
                            engine.runAndWait()

                    if login_button.text=="Login and Start Quiz":
                        print(OTPnumber)
                        if otp_text_box.text==str(OTPnumber):
                            is_running=False
                        elif otp_text_box.text=="":
                            speak("Input the OTP number")
                        else:
                            speak("Wrong, OTP number")  
                       

        manager.process_events(event)

    manager.update(time_delta)

    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()

pygame.init()

# Set up the Pygame window and manager
display_size = (700, 400)
display = pygame.display.set_mode(display_size)
pygame.display.set_caption("QuizkPy: CITE012A-CS32S1-HCI")

manager = pygame_gui.UIManager(display_size)

# Create and start the speech recognition thread
speech_thread = threading.Thread(target=recognize_speech)
speech_thread.start()

# Create the question label
question_label =  pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((50, 20), (500, 50)),
    html_text=rows[item_number]['question'],

    manager=manager,
    wrap_to_height=True 
)

# Create the answer buttons
answer1_button = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((50, 150), (600, 50)),
    html_text= "",
    manager=manager
)

answer2_button = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((50, 200), (600, 50)),
    html_text= "",
    manager=manager
)
answer3_button = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((50, 250), (600, 50)),
    html_text= "",
    manager=manager
)
answer4_button = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((50, 300), (600, 50)),
    html_text= "",
    manager=manager
)
# Load the logo image
logo_image = pygame.image.load("tip_logo.png")

# Create the image element
logo_element = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((550, 15), (100, 100)),
    image_surface=logo_image,
    manager=manager,
)

question_label.set_text(f" <font size=5>{item_number+1}.) {rows[item_number]['question']}")

answer1_button.set_text(" A) " + rows[item_number]['opt1'])
answer2_button.set_text(" B) " + rows[item_number]['opt2'])
answer3_button.set_text(" C) " + rows[item_number]['opt3'])
answer4_button.set_text(" D) " + rows[item_number]['opt4'])

# Create a Pygame font object for rendering text
font = pygame.font.Font(None, 24)

# Run the Pygame loop
clock = pygame.time.Clock()
running = True
said = False

last_number = len(rows)-1
last_word = recognized_word

while running:
    display.fill((37, 41, 46))
    for i in range(0,5):
        pygame.draw.line(display, (102, 204, 255), start[i], end[i] , 2)

    manager.draw_ui(display)
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)
        manager.update(time_delta)


    if item_number>last_number:    
        logo_element.rect.width = 150
        logo_element.rect.height = 150
        break

    try:
        if recognized_word!="":

            if checkAnswer(recognized_word)==-1:    
                recognized_word=""
                speak("Please choose only the letters from A to D")
                prompt = ""

                continue
            else:
                prompt = "Next question,"

            item_number+=1
            
            recognized_word=""          

            prompt += rows[item_number]['question']
            prompt += ",A," + rows[item_number]['opt1']
            prompt += ",B," + rows[item_number]['opt2']
            prompt += ",C," + rows[item_number]['opt3']
            prompt += ",D," + rows[item_number]['opt4']
            
            said=False
            # Reset the current time
            current_time = pygame.time.get_ticks()
            question_label.set_text(f" <font size=5>{item_number+1}. ) {rows[item_number]['question']}</font>")
            answer1_button.set_text(" A) " + rows[item_number]['opt1'])
            answer2_button.set_text(" B) " + rows[item_number]['opt2'])
            answer3_button.set_text(" C) " + rows[item_number]['opt3'])
            answer4_button.set_text(" D) " + rows[item_number]['opt4'])

    except:
        pass

    # Check if it's time to run the function
    if pygame.time.get_ticks() - current_time >= delay_time and said==False:
        # Call the function
        # Reset the current time
        speak_thread = threading.Thread(target=speak(prompt))
        current_time = pygame.time.get_ticks()    
        said=True

    pygame.display.update()

pygame.quit()



pygame.init()

# Set up the Pygame window and manager
display_size = (700, 400)
display2 = pygame.display.set_mode(display_size)
pygame.display.set_caption("QuizkPy: CITE012A-CS32S1-HCI")

ui_manager = pygame_gui.UIManager(display_size)

# Create the question label
last_message =  pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((50, 20), (500, 50)),
    html_text="",
    manager=ui_manager,
    wrap_to_height=True 
)


# Load the logo image
logo_image2 = pygame.image.load("tip_logo.png")

# Create the image element
logo_element2 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((550, 0), (150, 150)),
    image_surface=logo_image,
    manager=ui_manager,
)

ending = False
running = True

speech_continue_flag = False
speech_thread.join()
current_time = pygame.time.get_ticks()    
delay_time = 5000

while running:
    display2.fill((37, 41, 46))
    
    msg = f"{my_email}, Thank you for answering, your score is, {score} out of, {len(rows)} items"

    logo_element2.rect.x = 350 -  logo_element2.rect.width // 2 
    logo_element2.rect.y = 20

    try:
        send_email("QuizkResult", msg, "mrmartinez01@tip.edu.ph")
        msg+="\nQuiz results is already sent to your class instructor, mrmartinez01@tip.edu.ph"
        if ending==False and pygame.time.get_ticks() - current_time >= delay_time:
            speak(msg)
            speak_continue_flag = False
            speak_thread.join()
            ending=True

        msg = msg.replace(",","")
        last_message.set_text(f"<font size=5>{msg}</font>")
        last_message.rect.x = 350 - last_message.rect.width // 2
        last_message.rect.y = 250 - last_message.rect.height // 2
        
    except smtplib.SMTPDataError:
        msg="There was an error in the system. Please communicate the issue with your instructor"
        speak(msg)
       
    ui_manager.update(time_delta)
    ui_manager.draw_ui(display2)
    pygame.display.update()
