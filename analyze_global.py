import json
import sys

import chatgpt


def _read_global_data(file_path):
    global_data = []
    original_text = ()
    translation = ()
    with open(file_path, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.strip()
            if line:
                if len(original_text):
                    translation = tuple(line.strip().split('\t'))
                else:
                    original_text = tuple(line.strip().split('\t'))
            else:
                if len(original_text) and len(translation):
                    global_data.append((original_text, translation))
                    original_text = ()
                    translation = ()
        if len(original_text) and len(translation):
            global_data.append((original_text, translation))

    return global_data


def _get_output_lines(result, original_text, translation):
    lines = []
    # print(f"result: {result}")

    try:
        analysis_result = json.loads(result)
        lines.append(f"{original_text}\n")
        lines.append(f"{translation}\n")
        if isinstance(analysis_result, list):
            for analysis in analysis_result:
                # print(f"analysis: {analysis}")
                primary = analysis['primary'] if 'primary' in analysis else ""
                secondary = analysis['secondary'] if 'secondary' in analysis else ""
                reason = analysis['reason'] if 'reason' in analysis else ""
                if primary and secondary:
                    line = f"{primary}{tab}{secondary}{tab}{reason}"
                    # print(f"write: {line}")
                    lines.append(f"{line}\n")
        else:
            print(f'Warning: no result.')
        lines.append(f"\n")
    except Exception as ex:
        print("Error: " + str(ex).split('\n')[0])
        print(f"result: {result}")

    return lines


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_global.py input_file output_file")
        exit()

    input_file = sys.argv[1]    # dataset/global-10.tsv
    output_file = sys.argv[2]   # output/global-10.tsv

    tab = '\t'
    global_data = _read_global_data(input_file) 
    with open(output_file, 'w', encoding='utf-8') as file:        
        for trans in global_data:
            try:
                original_text = trans[0][1]
                translation = trans[1][1]
                result = chatgpt.analyze_translation(original_text, translation)
                if result:
                    lines = _get_output_lines(result, original_text, translation)
                    if len(lines):
                        print(f"{lines}", flush=True)
                        file.writelines(lines)
                        file.flush()
            except Exception as ex:
                print(f"{ex}")

