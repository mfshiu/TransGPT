import json
import sys

import chatgpt


def _read_group_data(file_path):
    group_data = []
    original_text = ()
    translations = []
    with open(file_path, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.strip()
            if line:
                if len(original_text):
                    translations.append(tuple(line.strip().split('\t')))
                else:
                    original_text = tuple(line.strip().split('\t'))
            else:
                if len(original_text) and len(translations):
                    group_data.append((original_text, translations))
                    original_text = ()
                    translations = []
        if len(original_text) and len(translations):
            group_data.append((original_text, translations))

    return group_data


def _get_statistics(result):
    statistics = {}

    try:
        analysis_result = json.loads(result)
        for analysis in analysis_result:
            # print(f"analysis: {analysis}")
            primary = analysis['primary'] if 'primary' in analysis else ""
            secondary = analysis['secondary'] if 'secondary' in analysis else ""
            if primary and secondary:
                if not primary in statistics:
                    statistics[primary] = {}
                if secondary in statistics[primary]:
                    statistics[primary][secondary] += 1
                else:
                    statistics[primary][secondary] = 1
    except Exception as ex:
        print("Error: " + str(ex).split('\n')[0])

    return statistics


def _merge_statistics(all_statistics, statistics):
    for primary in statistics:
        if primary in all_statistics:
            for secondary in statistics[primary]:
                if secondary in all_statistics[primary]:
                    all_statistics[primary][secondary] += statistics[primary][secondary]
                else:
                    all_statistics[primary][secondary] = statistics[primary][secondary]
        else:
            all_statistics[primary] = statistics[primary]

    return all_statistics


def _get_output_lines(original_text, all_statistics):
    tab = '\t'
    lines = [f"{original_text}\n"]
    for primary in all_statistics:
        for secondary in all_statistics[primary]:
            count = all_statistics[primary][secondary]
            lines.append(f"{primary}{tab}{secondary}{tab}{count}\n")

    return lines


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_group.py input_file output_file")
        exit()

    input_file = sys.argv[1]    # dataset/group-10.tsv
    output_file = sys.argv[2]   # output/group-10.tsv

    tab = '\t'
    group_data = _read_group_data(input_file) 
    # print(f'group data:{group_data}')
    with open(output_file, 'w') as file:        
        for group in group_data:
            all_statistics = {}
            original_text = group[0][1]
            translations = group[1]
            for translation in translations:
                result = chatgpt.analyze_translation(original_text, translation[1])
                # print(f'result: {result}')
                if result:
                    statistics = _get_statistics(result)
                    print(f'statistics: {statistics}')
                    all_statistics = _merge_statistics(all_statistics, statistics)
                    # print(f'all_statistics: {all_statistics}')
            lines = _get_output_lines(original_text, all_statistics)
            if len(lines):
                print(f"{lines}")
                file.writelines(lines)
                file.flush()
            file.writelines('\n')


