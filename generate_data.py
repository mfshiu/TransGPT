import csv


ORIGINAL_TEXT_TSV = 'raw/original_text.tsv'
TRANSLATION_TSV = 'raw/translation.tsv'
GLOBAL_TRANSLATION_FILE = 'dataset/global.txt'
GROUP_TRANSLATION_FILE = 'dataset/group.txt'


def read_original_tsv(file_path):
    original_texts = {}
    with open(file_path, 'r', newline='') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        next(tsv_reader)
        for row in tsv_reader:
            # 原文ID	對話序號	人物別	語言	是否翻譯	內容
            if len(row):
                try:
                    original_id, number, charator, language, need_translate, content = row
                    if 'Y' == need_translate:
                        if not original_id in original_texts:
                            original_texts[original_id] = {}
                        original_texts[original_id][number] = (charator, language, content)
                except Exception as ex:
                    print("Error: " + str(ex).split('\n')[0])
    return original_texts


def read_translation_tsv(file_path):
    translations = {}
    with open(file_path, 'r', newline='') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        next(tsv_reader)
        for row in tsv_reader:
            # 譯文ID	作業ID	原文ID	原文對話序號	語言別	內容
            if len(row):
                try:
                    _, _, original_id, original_number, language, content = row
                    if not original_id in translations:
                        translations[original_id] = {}
                    if not original_number in translations[original_id]:
                        translations[original_id][original_number] = []
                    translations[original_id][original_number].append((language, content))
                except Exception as ex:
                    print("Error: " + str(ex).split('\n')[0])
    return translations


def write_global_translation(file_path, original_texts, translations):
    with open(file_path, 'w') as output_file:
        for i, oid in enumerate(original_texts):
            key = next(iter(translations[oid]))
            trans_count = len(translations[oid][key])
            for i in range(trans_count):
                for number in original_texts[oid]:
                    output_file.write(f'{original_texts[oid][number][1]}\t{original_texts[oid][number][2]}\n')
                    trans = translations[oid][number][i]
                    output_file.write(f'{trans[0]}\t{trans[1]}\n\n')


def write_group_translation(file_path, original_texts, translations):
    with open(file_path, 'w') as output_file:
        for oid in translations:
            for number in translations[oid]:
                output_file.write(f'{original_texts[oid][number][1]}\t{original_texts[oid][number][2]}\n')
                for trans in translations[oid][number]:
                    output_file.write(f'{trans[0]}\t{trans[1]}\n')
                output_file.write(f'\n')


if __name__ == "__main__":
    original_texts = read_original_tsv(ORIGINAL_TEXT_TSV)
    # for oid in original_texts:
    #     for number in original_texts[oid]:
    #         print(f'{oid} {number} {original_texts[oid][number]}')

    translations = read_translation_tsv(TRANSLATION_TSV)
    # for oid in translations:
    #     for number in translations[oid]:
    #         for trans in translations[oid][number]:
    #             print(f'{oid} {number} {trans}')

    write_global_translation(GLOBAL_TRANSLATION_FILE, original_texts, translations)
    write_group_translation(GROUP_TRANSLATION_FILE, original_texts, translations)
