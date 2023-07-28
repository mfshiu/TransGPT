import sys


def _read_statistics(file_path):
    statistics = {}
    with open(file_path, 'r', encoding='UTF-8') as file:
        original_text = ""
        translation = ""
        analysis = ()

        for line in file:
            line = line.strip()
            if line:
                if len(translation):
                    analysis = tuple(line.strip().split('\t'))
                    if len(analysis) >= 2:
                        primary, secondary = analysis[0], analysis[1]
                        if not primary in statistics:
                            statistics[primary] = {}
                        if secondary in statistics[primary]:
                            statistics[primary][secondary] += 1
                        else:
                            statistics[primary][secondary] = 1
                elif not original_text:
                    original_text = line
                else:
                    translation = line
            else:
                original_text = ""
                analysis = ()

    return statistics


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python analyze_global.py input_file output_file stat_file")
        exit()

    input_file = sys.argv[1]    # output/global-10.tsv
    output_file = sys.argv[2]   # output/global-stat-10.tsv

    statistics = _read_statistics(input_file)

    tab = '\t'
    with open(output_file, 'w') as file:        
        for primary in statistics:
            for secondary in statistics[primary]:
                count = statistics[primary][secondary]
                line = f"{primary}{tab}{secondary}{tab}{count}\n"
                print(f"{line}")
                file.write(line)
