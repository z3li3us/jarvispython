# Import necessary libraries
import os
import openai
from elevenlabs import generate, play
import speech_recognition as sr
import ffmpeg

# Set the API keys for OpenAI and ElevenLabs
openai.api_key = ()
elevenLabsAPIKey = ()

# Instantiate the recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Initiate a conversation with the system's initial message
conversation = [
        {"role": "system", "content": "Your name is Jarvis and your purpose is to be Zelieus' AI assistant"},
    ]

# The while loop will run indefinitely until you manually stop the program.
while True:
    # Use the microphone as the source for input audio
    with mic as source:
        # Adjust the recognizer sensitivity to ambient noise
        r.adjust_for_ambient_noise(source, duration=0.5) #Set duration if needed 
        # Prompt the user to speak
        print("Talk now")
        audio = r.listen(source)
    try:
        # Attempt to convert the audio into text using Google Speech Recognition
        word = r.recognize_google(audio)

        # If the recognized word contains 'draw', handle it separately
        if "draw" in word:
            # Find the index of "draw" and get the rest of the sentence
            i = word.find("draw")
            i += 5
            # Call OpenAI's image creation API to generate an image based on the text
            response = openai.Image.create(
                prompt=word[i:],
                n=1,
                size="1024x1024"
            )
            # Get the URL of the generated image
            image_url = response['data'][0]['url']
            print(word[i:])
            print(image_url)
        else:
            # If the recognized word does not contain 'draw', add it to the conversation
            conversation.append({"role": "user", "content": word})

            # Use OpenAI's chat model to generate a response to the conversation so far
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
            )

            # Extract the response message from the API response
            message = response["choices"][0]["message"]["content"]
            # Add the AI's response to the conversation
            conversation.append({"role": "assistant", "content": message})
        
            # Use Eleven Labs to generate an audio message from the AI's response
            audio = generate(
                    text=message[:333],
                    voice="Adam",
                    model='eleven_multilingual_v1',
                    api_key=elevenLabsAPIKey
                )
            # Play the generated audio
            play(audio)
    
    # If Google Speech Recognition could not understand the audio, handle the error
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        # Generate an audio message asking the user to speak more clearly or loudly
        audio = generate(
            text="I'm sorry, I couldn't understand that. Could you please speak more clearly or loudly?",
            voice="Adam",
            model='eleven_multilingual_v1',
            api_key=elevenLabsAPIKey
        )
        play(audio)
    # If there was an error in the request to Google Speech Recognition, handle the error
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service; {0}".format())
