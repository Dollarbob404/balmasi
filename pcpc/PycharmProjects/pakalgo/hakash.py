import json


JSON_FILENAME = 'hakash.json'


def rewrite_hakash(filename):
    """
    rewrite the hakash file from filename (csv)
    :param filename:
    :return:
    """
    hakash_dict = {}
    with open(filename, 'rb') as my_file:
        for row in my_file:
            key, value = row.decode('utf-8').strip('\r\n').split(',')
            hakash_dict[key] = float(value)
    with open(JSON_FILENAME, 'wb+') as hakash_file:
        hakash_file.write(json.dumps(hakash_dict).encode())


def read_hakash():
    with open(JSON_FILENAME, 'rb') as hakash_file:
        hakash_dict = json.loads(hakash_file.read().decode('utf-8'))
    return hakash_dict


hakash = {}
try:
    hakash = read_hakash()
except FileNotFoundError:
    print('hakash file not exist!')
except Exception as e:
    print(f'could not read hakash file! {e}')