import gradio as gr
import openai
import nltk
from google.cloud import translate_v2 as translate

# Initialize Google Cloud Translation client
translate_client = translate.Client()

openai.api_key = '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'


# Initialize chat history with a system message
messages = [{"role": "system", "content": "you are an virtual assistant you have to guide the passengers in the railway station by detailing the directions and locations"
                                          "platform location: go right and take stairs following the steps you can find restroom"
                                          }]

# Define the chatbot function
def CustomChatGPT(questions_here, target_language='en'):
    # Detect the language of the user input
    user_language = detect_language(questions_here)

    # Translate user input to English if not already in English
    if user_language != 'en':
        questions_here = translate_text(questions_here, 'en')

    messages.append({"role": "user", "content": questions_here})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    Chatbot_reply = response["choices"][0]["message"]["content"]

    # Translate the chatbot's reply back to the user's language
    if user_language != 'en':
        Chatbot_reply = translate_text(Chatbot_reply, user_language)

    messages.append({"role": "assistant", "content": Chatbot_reply})
    return Chatbot_reply

# Define a function for language detection
def detect_language(text):
    try:
        lang = nltk.detect(text)
    except:
        lang = 'en'
    return lang

# Define a function for text translation
def translate_text(text, target_language):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']

# Create a Gradio interface for the chatbot
demo = gr.Interface(
    fn=CustomChatGPT,
    inputs=["text", "text"],
    outputs="text",
    title="Intelligent chatbot for clearing queries in Railway station",
    description="Virtual assistant",
)
# Launch the Gradio interface
demo.launch(share=True)
