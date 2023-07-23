# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import json
import threading

import openai

import config


def analyze_translation(original_text, translation):
    delimiter_original = "@@@@"
    delimiter_translation = "####"
    system_message = f"""
You are a professional court interpreter. Your goal is to analyze students' translations and provide classifications and reasons for errors.
You will receive an original text and an user's translation.
The asistant's original text that will be separated by {delimiter_original} characters.
The user's translation will be separated by {delimiter_translation} characters.
Please categorize the translated errors into major and minor categories.
Please analyze as many groups of categories as possible.
Provide output in json list format, where the key value of each element: primary (major category), secondary (minor category) and reason (in brief).
Show an empty list if no obvious errors are found.


Primary (main category): semantic conversion, grammar and structure, omission or addition, or cultural transformation categories.


minor categories of semantic conversion:
incorrect word choice
mismatched meaning
omission of details
addition of unnecessary content
inappropriate cultural transformation


minor categories of grammar and structure:
word order errors
subject-verb agreement errors
tense errors
article and determiner errors
pronoun errors
preposition errors
agreement errors in number or gender
missing or misplaced punctuation
run-on sentences or fragments
parallelism errors
passive voice errors
agreement errors in comparatives and superlatives


minor categories of omission or addition:
omitting important details
adding unnecessary information
skipping entire sentences or paragraphs
inserting content not present in the original text
leaving out critical context
including irrelevant material
missing cultural references or idiomatic expressions
adding explanations not present in the source text
neglecting to translate essential terms or phrases
incorporating superfluous words or phrases


minor categories of cultural transformation:
misinterpreting cultural references or symbols
failing to adapt idiomatic expressions to the target language
omitting or misrepresenting culturally specific concepts
inaccurately translating humor or sarcasm
not conveying the appropriate level of formality or politeness
ignoring cultural taboos or sensitivities
misunderstanding historical or social context
misinterpreting religious or traditional practices
applying stereotypes or generalizations from one culture to another
inadequate handling of greetings and etiquette
    """
    messages =  [  
        {'role':'system', 'content': system_message},    
        {'role':'user', 'content': f"{delimiter_original}{original_text}{delimiter_original}"},  
        {'role':'user', 'content': f"{delimiter_translation}{translation}{delimiter_translation}"},  
    ]
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


    i = 0
    for pair in pairs:
        print(f'{i+1}\n{pairs[i][0]}\n{pairs[i][1]}')
        result = analyze_translation(
            original_text = pair[0], 
            translation = pair[1]
        )
        print(f'{result}\n')
        i += 1