import re
import os

ignore_list = ['.git']

dirs_patterns = re.compile(
    '(?:DfeConfig)|'
    '(?:result[0-9])|'
    '(?:^data$)'
)

files_pattern = re.compile(
    '(?:.+\.bak)|'
    '(?:.+\.tmp)|'
    '(?:.+\.log)|'
    '(?:.+\.idx)|'
    '(?:.+\.har)|'
    '(?:.+\.shunra)|'
    '(?:.+\.c.pickle)|'
    '(?:.+\.prm\.bak)|'
    '(?:.+\.sdf)|'
    '(?:.+\.ci)|'
    '(?:output\.txt)|'
    '(?:options\.txt)|'
    '(?:mdrv_cmd\.txt)|'
    '(?:serTasks\.xml)|'
    '(?:Bookmarks\.xml)|'
    '(?:Breakpoints\.xml)|'
    '(?:Watches\.xml)|'
    '(?:UserTasks\.xml)|'
    '(?:ReplaySummaryReport\.xml)|'
    '(?:CompilerLogMetadata\.xml)|'
    '(?:ScriptUploadMetadata\.xml)|'
    '(?:pre_cci\.c)|'
    '(?:combined_.+\.c)|'
    '(?:lrw_custom_body\.h)|'
    '(?:TransactionsData\.db)|'
    '(?:OutputColoringDatabase\.json)'
)


def clear_folder(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def clear(path):
    for dir in os.listdir(path):
        if dir in ignore_list:
            continue
        if os.path.isdir(f'{path}/{dir}'):
            if dirs_patterns.match(dir):
                clear_folder(f'{path}/{dir}')
                os.rmdir(f'{path}/{dir}')
            else:
                print(dir)
                clear(f'{path}/{dir}')
        elif files_pattern.match(dir):
            os.remove(f'{path}/{dir}')

    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            if not os.listdir(os.path.join(root, dir)):
                os.rmdir(os.path.join(root, dir))


if __name__ == '__main__':
    clear(os.getcwd())
    print('----finished----')
