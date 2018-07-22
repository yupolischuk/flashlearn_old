import os
import re
import MySQLdb

dir_to_scan = '/home/yura/test'
filetype_to_scan = 'txt'


'Get content of directory'


# TODO add directories scan recursively
def dir_content(scan_dir):
    if os.path.exists(scan_dir) and os.path.isdir(scan_dir):
        os.chdir(scan_dir)
        return os.listdir(scan_dir)

# print(dir_content(dir_to_scan))


def select_needed_files(file_list, needed_type):
    '''Get list of needed files'''
    res = []
    for file in file_list:
        if os.path.exists(dir_to_scan + '/' +  file) \
                and os.path.isfile(dir_to_scan + '/' + file) \
                and file.split('.')[1] == needed_type:
            res.append(file)
    return res

# print(select_needed_files(['test3.txt', 'test2.txt', 'dir', 'test1.txt'], 'txt'))


def parse_file(path):
    '''Return dictionary or questions and answers'''
    # file = open('/home/junior/test/needed/cheat_sheet.txt')
    file = open(path)
    lines = file.readlines()
    res = {}
    questions = []
    answers = []

    for line in lines:
        if line[0].isupper():
            questions.append(line.rstrip())
        if re.match(r'[ \t]', line):
            answers.append(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', line.rstrip(), flags=re.M))

    if len(questions) == len(answers):
        res = dict(zip(questions, answers))
    else:
        print('Number of questions not equals to number of answers')

    return res

# print(parse_file())

# Iterate dictionary
# fcards = parse_file()
# for q, a in fcards.items():
#     print(q)
#     print(a)


def write_to_db(data):
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='',
                         db='')

    cur = db.cursor()
    # INSERT INTO `cheat_sheet`(`question`, `number`) VALUES ('sdfsd1234','qwerqwe56743')
    # sql = "INSERT INTO `cheat_sheet`(`question`, `number`) VALUES ('sdfsd1234','qwerqwe56743')"

    # sql = "insert into city VALUES(null, '%s', '%s')" % \
    #  (question, answer)
    for q, a in data.items():
        # sql = "insert into cheat_sheet VALUES(null, '%s', '%s')" % (q, a)
        # cur.execute(sql)

        # escaping values before insert
        sql = "INSERT INTO cheat_sheet (question, answer) VALUES (%s, %s)"
        cur.execute(sql, (q, a))
        db.commit()  # call commit() method to save

    db.close()
    print('Fin!')


'''RUN'''
file_list = dir_content(dir_to_scan)
needed_file = select_needed_files(file_list, filetype_to_scan)
data = parse_file(dir_to_scan + '/' + needed_file[0])
# print(data)
write_to_db(data)
