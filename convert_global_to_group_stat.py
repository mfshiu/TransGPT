import json
import sys

import chatgpt


def _read_group_stat(file_path):
    group_stat = {}
    original_text = ""
    translation = ""
    with open(file_path, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.strip()
            if line:
                # print(f"line: {line}")
                if translation:
                    analysis = tuple(line.strip().split('\t'))
                    if len(analysis) >= 2:
                        primary, secondary = analysis[0], analysis[1]
                        # print(f"original_text:{original_text}, primary: {primary}, secondary: {secondary}")
                        if not primary in group_stat[original_text]:
                            group_stat[original_text][primary] = {}
                        if secondary in group_stat[original_text][primary]:
                            group_stat[original_text][primary][secondary] += 1
                        else:
                            group_stat[original_text][primary][secondary] = 1
                elif original_text:
                    translation = line
                    # print(f"translation: {translation}")
                else:
                    original_text = line
                    # print(f"original_text: {original_text}")
                    if not original_text in group_stat:
                        group_stat[original_text] = {}
            else:
                original_text = ""
                translation = ""
                # print(f"reset: {True}, original_text: {original_text}, translation: {translation}")

    return group_stat


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_global_to_group_stat.py global_file group_file")
        exit()

    input_file = sys.argv[1]  
    output_file = sys.argv[2]  

    tab = '\t'
    group_stat = _read_group_stat(input_file) 
    # print(f'group data:{group_data}')
    with open(output_file, 'w') as file:        
        for original_text in group_stat:
            file.write(f'{original_text}\n')
            for primary in group_stat[original_text]:
                for secondary in group_stat[original_text][primary]:
                    file.write(f'{primary}\t{secondary}\t{group_stat[original_text][primary][secondary]}\n')
            file.write('\n')

