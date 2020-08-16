from hashlib import sha1
from hmac import new
from sys import exit
from os import path, rename, makedirs, remove
from gzip import open as open1
from json import loads, dumps

writer2 = open('log.txt', 'w')

packdone = False


def spack(fileuno):
    with open1(fileuno, 'rb') as f:
        file_content = f.readline()
        file_content = f.readline()

    parsed = loads(file_content)
    file_pret = dumps(parsed, indent=4, sort_keys=False)

    writer1 = open('Decrypted/'+fileuno+'.txt', 'w', encoding='utf8')
    writer1.write(file_pret)
    writer1.close()


def pack(fileuno):
    writer1 = open('Decrypted/'+fileuno + '.txt', 'r', encoding='utf8')
    file_pret = writer1.read()
    writer1.close()

    try:
        json_data = loads(file_pret)
    except ValueError as err:
        writer2.write('\n\rjson error in ' + fileuno + '.txt\n\r')
        writer2.write(str(err))
        raise SystemExit(err)

    if fileuno == '8ed9e902c5c024bfb899e99893d4eb525d3ad179':
        try:
            json_data['profileSaveHashes'] = {}
            json_data['profileSaveHashes'] = {'playerID': json_data['userid'], 'CRC': ""}
            writer2.write(': crc updated')
        except:
            writer2.write(': crc not updated')

    json_string = dumps(json_data, ensure_ascii=True, separators=(',', ":"))
    file4crc32 = json_string.encode('utf8')
    secretkeybytes = bytearray([52, 99, 80, 119, 51, 90, 121, 67])
    dig2 = new(secretkeybytes, file4crc32, sha1).hexdigest()

    try:    # Maybe file not exist
        remove('Finished/'+fileuno)
    except:
        pass

    with open1('Finished/'+fileuno, 'a') as f2:
        f2.write(bytes(dig2, 'utf8'))
        f2.write(bytes('\n', 'utf8'))
        f2.write(file4crc32)
        f2.close()


files = ['nsb', 'scb', '8ed9e902c5c024bfb899e99893d4eb525d3ad179', 'trb']

if not path.exists('Original'):
    makedirs('Original')
if not path.exists('Decrypted'):
    makedirs('Decrypted')

for singleFile in files:
    if path.exists(singleFile):
        writer2.write('start: trying to unpack %s...' % singleFile)
        spack(singleFile)
        try:    # Maybe file not exist
            remove('Original/%s.old' % singleFile)
        except:
            pass
        rename(singleFile, 'Original/%s.old' % singleFile)
        writer2.write('done!\n\r')
        packdone = True
    else:
        writer2.write('missing original %s file\n\r' % singleFile)

if packdone:
    writer2.write('unpacking completed\n\r\n\r')
    writer2.close()
    exit()

if not path.exists('Finished'):
    makedirs('Finished')

writer2.write('nothing to unpack:')

for singleFile in files:
    if path.exists('Decrypted/%s.txt' % singleFile):
        writer2.write(' trying to pack %s.txt file' % singleFile)
        pack(singleFile)
        writer2.write(': done\n\r')

    else:
        writer2.write(': missing %s.txt file\n\r' % singleFile)

writer2.close()
