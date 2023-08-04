# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import json
import threading

import openai

import config
import helper


openai.api_key = config.OPENAI_API_KEY
_delimiter_original = "@@@@"
_delimiter_translation = "####"


def _get_system_message():
    classfication = helper.read_classfication('classfication.txt')
    class_text = ""
    for major in classfication:
        class_text += f'minor categories of {major}:\n'
        for minor in classfication[major]:
            class_text += f'{minor}:\n'
        class_text += '\n'
    system_message = f"""
You are a professional court interpreter. Your goal is to analyze students' translations and provide classifications and reasons for errors.
You will receive an original text and a user's translation.
The assistant's original text that will be separated by {_delimiter_original} characters.
The user's translation will be separated by {_delimiter_translation} characters.
Please categorize the translated errors into major and minor categories.
Please analyze as many groups of categories as possible.
Provide output in json list format, where the key value of each element: primary (major category), secondary (minor category) and reason (in brief).
Show an empty list if no obvious errors are found.

Primary (main category): semantic conversion, grammar and structure, omission or addition, or cultural transformation categories.

{class_text}"""
    return system_message
_system_message = _get_system_message()


def analyze_translation(original_text, translation, try_count=0):
    if try_count > 0:
        print(f"Try {try_count}")
    if try_count > 9:
        return ""
    
    messages =  [  
        {'role':'system', 'content': _system_message},    
        {'role':'user', 'content': f"{_delimiter_original}{original_text}{_delimiter_original}"},  
        {'role':'user', 'content': f"{_delimiter_translation}{translation}{_delimiter_translation}"},  
    ]

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=messages
        )
        content = completion['choices'][0]['message']['content']
    except Exception as ex:
        content = ""
        print("Error: " + str(ex).split('\n')[0])
        content = analyze_translation(original_text, translation, try_count+1)

    return content


def xanalyze_translation(original_text, translation):
    delimiter_original = "@@@@"
    delimiter_translation = "####"
    system_message = f"""
難·
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
    print(f'system_message: {_system_message}')

if __name__ == 'x__main__':
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