def read_classfication(file_path):
    with open(file_path, 'r') as class_file: 
        lines = class_file.readlines()

    classfication = {}
    major_class = ""
    minor_classes = []
    for line in lines:
        line = line.strip()
        if line:
            if major_class:
                minor_classes.append(line)
            else:
                major_class = line[:-1]
                continue
        elif major_class:
            if len(minor_classes):
                classfication[major_class] = minor_classes
            major_class = ""
            minor_classes = []

    if major_class:
            # print(f'len: {len(minor_classes)}')
            if len(minor_classes):
                classfication[major_class] = minor_classes

    return classfication


if __name__ == '__main__':
    classfication = read_classfication('classfication.txt')
    for major in classfication:
        print(f'{major}:\n{classfication[major]}')
        print()
