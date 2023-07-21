#Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import json
import threading

import openai


openai.api_key = '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'


def xanalyze_translation(original_text, translation):
    delimiter0 = "@@@@"
    delimiter1 = "####"
    system_message = f"""
You will receive two sentences, one in the original text and one in the student's translation.
The original text will be separated by {delimiter0} characters.
The student's translation will be separated by {delimiter1} characters.
Please count errors made by this translated sentence with very strict standards, and classfy them into different types.
Provide your output in json format with key values: the key is type and the value is count.

Error types: "Semantic Conversion", "Grammar and Structure", "Omission or Addition" or "Cultural Transformation".
    """
    messages =  [  
        {'role':'system', 'content': system_message},    
        {'role':'user', 'content': f"{delimiter0}{original_text}{delimiter0}"},  
        {'role':'user', 'content': f"{delimiter1}{translation}{delimiter1}"},  
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=messages
    )
    content = completion['choices'][0]['message']['content']
    print(f'Result:\n{content}')


    def _process_result(result):
        if result:
            result = result.strip()
            if result[0] == "(":
                result = result[1:]
            if result[-1] == ")":
                result = result[:-1]
        print(f"result: {result}")
        return result


def analyze_translation(original_text, translation):
    delimiter0 = "@@@@"
    delimiter1 = "####"
    system_message = f"""
You will receive two sentences, one in the original text and one in the student's translation.
The original text will be separated by {delimiter0} characters.
The student's translation will be separated by {delimiter1} characters.
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
        {'role':'user', 'content': f"{delimiter0}{original_text}{delimiter0}"},  
        {'role':'user', 'content': f"{delimiter1}{translation}{delimiter1}"},  
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=messages
    )
    content = completion['choices'][0]['message']['content']
    print(f'Result:\n{content}')


    def _process_result(result):
        if result:
            result = result.strip()
            if result[0] == "(":
                result = result[1:]
            if result[-1] == ")":
                result = result[:-1]
        print(f"result: {result}")
        return result


if __name__ == '__main__':
    original_text = "她對我大叫，說我偷了她的雨傘。我想要告訴她，我只是拿到錯的傘。我並沒有想要偷她的傘，我想要解釋，但她根本不聽。"
    translation = "She yelled at me, saying that I stole her umbrella. I tried to tell her that I must have taken the wrong one. I did not steal her umbrella. I tried to apologize to her, but she wouldn’t listen."
    original_text = "She yelled at me, saying that I stole her umbrella. I tried to tell her that I must have taken the wrong one. I did not steal her umbrella. I tried to apologize to her, but she wouldn’t listen."
    translation = "她對我大叫，說我偷了她的雨傘。我想要告訴她，我只是拿到錯的傘。我並沒有想要偷她的傘，我想要解釋，但她根本不聽。"
    original_text = "那他們三位應該能夠到庭幫你佐證剛剛所說的話，對吧?"
    translation = "Therefore, perhaps, the professor and those two classmates can come to the court to verify what you said is true."
    original_text = "Yes, when I came out from the museum, my professor and other two classmates were with me. My professor even offered to lend me her umbrella; since her umbrella was quite small, I didn’t take it. I didn’t want her to get wet. The other two classmates were there too."
    translation = "是的，我出博物館的時候，我是跟老師還有兩位同學一起的。我的老師也有提議要借我的傘，因為她的傘有點小，我並沒有拿。我不想要她被淋濕，然後也有兩位同學在旁邊。"
    original_text = "Yes"
    translation = "是的"
    original_text = "1.你有權保持緘默，毋需違背意志做任何陳述。"
    translation = "First, you have the right to remain silent and do not have to make any statement against your will."
    original_text = "我想要解釋，但她根本不聽。"
    translation = "I tried to apologize to her, but she wouldn’t listen."
    original_text = "那支傘全部是藍色的嗎?"
    translation = "Is the entire umbrella blue?"
    original_text = "我喜歡吃蘋果和香蕉。"
    translation = "I like to eat banana."
    original_text = "那為什麼陳小姐會說你偷了她的傘呢? "
    translation = "Then why did Ms. Chen accuse that you stole her umbrella?"
    # translation = "Why did Ms. Chen think that you stole her umbrella?"
    analyze_translation(original_text, translation)