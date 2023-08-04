# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import json
import threading

import openai

import config


openai.api_key = config.OPENAI_API_KEY


def analyze_translation(original_text, translation, previous_context):
    # print(f'previous_context: {previous_context}')

    delimiter0 = "@@@@"
    delimiter1 = "####"
    system_message = f"""
You will receive two sentences, one in the original text and one in the user's translation.
The assistant will speak the original text that will be separated by {delimiter0} characters.
The user's translation will be separated by {delimiter1} characters.
Please categorize the translated errors into major and minor categories.
Please analyze as many groups of categories as possible.
Provide output in json list format, where the key value of each element: primary (major category), secondary (minor category) and reason (in brief).
Show an empty list if no obvious errors are found.


Primary (main category): omission or addition, grammar and structure, semantic conversion, or cultural transformation categories.


minor categories of omission or addition:
omission of details
leaving out critical context
skipping entire sentences or paragraphs
adding unnecessary information
incorporating superfluous words or phrases
inserting content not present in the original text


minor categories of grammar and structure:
word order errors
subject-verb agreement errors
tense errors
pronoun errors
preposition errors
missing or misplaced punctuation
article and determiner errors
agreement errors in number or gender
repetition of phrases


minor categories of semantic conversion:
incorrect word choice
mismatched meaning
neglecting to translate essential terms or phrases
failing to adapt idiomatic expressions to the target language


minor categories of cultural transformation:
ignoring cultural taboos or sensitivities
inadequate handling of greetings and etiquette
inaccurately translating humor or sarcasm
misinterpreting cultural references or symbols
misunderstanding historical or social context
misinterpreting religious or traditional practices
inappropriate cultural transformation
"""

    messages = [{'role':'system', 'content': system_message}]
    for sentence in previous_context:
        messages.append({'role':'assistant', 'content': sentence})
    messages.append({'role':'assistant', 'content': f"{delimiter0}{original_text}{delimiter0}"})
    messages.append({'role':'user', 'content': f"{delimiter1}{translation}{delimiter1}"})
    # print(f'messages: {messages}')

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=messages
    )
    content = completion['choices'][0]['message']['content']
    return content


if __name__ == '__main__':
    original_text = "那為什麼陳小姐會說你偷了她的傘呢? "
    translation = "Then why did Ms. Chen accuse that you stole her umbrella?"
    pairs = [
        ("你當時去機場做什麼呢??", "So why do you go to the airport?"),
        ("I went there to pick up a friend who came to Taiwan for a visit.", "我去那裡接機，我有個朋友要來台灣旅遊。"),
        ("所以你是去了航廈接人嗎?", "So you mean that you go to the terminal to pick up a friend?"),
        ("Yes, I took a bus to get to the airport. I got there early and I waited for my friend.", "恩對，我是搭車去機場的，然後因為我提早到了，所以我在那邊等待我朋友。"),
        ("那為什麼後來會發生你拿原告帽子這件事呢?", "So why do you steal the motorcycle cap from the people?"),
        ("I was waiting for my friend but his flight was delayed. I got bored and went around to kill time.", "因為我太早到了而我朋友的班機又會延遲，所以我覺得很無聊，才做了這件事。"),
        ("你後來去了哪裡呢?", "So where do you go latter?"),
        ("I went to the parking lot for motorcycles.", "我去停車場找機車。"),
        ("然後發生了什麼事呢?", "'What happen next'"),
        ("I saw a cap left on one motorcycle.", "我看到一個機車上有一個安全帽。")
    ]


    previous_context = []
    i = 0
    for pair in pairs:
        print(f'{i+1}\n{pairs[i][0]}\n{pairs[i][1]}')
        result = analyze_translation(
            original_text = pair[0], 
            translation = pair[1],
            previous_context=previous_context)
        print(f'{result}\n')
        previous_context.append(pairs[i][0])
        i += 1