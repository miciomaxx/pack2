from hashlib import sha1
from hmac import new
from sys import exit
from os import path, rename, makedirs
from gzip import open as open1
from json import loads, dumps
from zlib import crc32

writer2 = open('log.txt', 'w')

workdone = False
nsbcrc32 = 0

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
            json_data['profileSaveHashes'] = {'playerID': json_data['userid'], 'CRC': str(nsbcrc32)}
            writer2.write(': crc updated')
        except:
            writer2.write(': crc not updated')

    json_string = dumps(json_data, ensure_ascii=True, separators=(',', ":"))
    file4crc32 = json_string.encode('utf8')
    crc32_file = crc32(file4crc32)
    secretkeybytes = bytearray([52, 99, 80, 119, 51, 90, 121, 67])
    dig2 = new(secretkeybytes, file4crc32, sha1).hexdigest()

    with open1('Finished/'+fileuno, 'a') as f2:
        f2.write(bytes(dig2, 'utf8'))
        f2.write(bytes('\n', 'utf8'))
        f2.write(file4crc32)
        f2.close()
    return crc32_file

if path.exists('nsb'):
    if not path.exists('Original'):
        makedirs('Original')
    if not path.exists('Decrypted'):
        makedirs('Decrypted')

    writer2.write('start: trying to unpack nsb...')
    spack('nsb')
    rename('nsb', 'Original/nsb.old')
    writer2.write('done!\n\r')
    workdone = True
else:
    writer2.write('missing original nsb file\n\r')

if path.exists('scb'):
    writer2.write('trying to unpack nsb...')
    spack('scb')
    rename('scb', 'Original/scb.old')
    writer2.write('done!\n\r')
else:
    writer2.write('missing original scb file\n\r')

if path.exists('8ed9e902c5c024bfb899e99893d4eb525d3ad179'):
    writer2.write('trying to unpack 3rd...')
    spack('8ed9e902c5c024bfb899e99893d4eb525d3ad179')
    rename('8ed9e902c5c024bfb899e99893d4eb525d3ad179', 'Original/8ed9e902c5c024bfb899e99893d4eb525d3ad179.old')
    writer2.write('done!\n\r')
else:
    writer2.write('missing original 3rd file: ok if you are on Ios\n\r')

if workdone:
    writer2.write('unpacking completed\n\r\n\r')
    writer2.close()
    exit()
    
if path.exists('Decrypted/nsb.txt'):
    writer2.write('nothing to unpack: trying to pack nsb.txt file')
    if not path.exists('Finished'):
        makedirs('Finished')
    nsbcrc32 = pack('nsb')
    writer2.write(': done\n\r')

else:
    writer2.write(': missing nsb.txt file\n\r')

if path.exists('Decrypted/scb.txt'):
    writer2.write('trying to pack scb.txt file')
    pack('scb')
    writer2.write(': done\n\r')

else:
    writer2.write(': missing scb.txt file\n\r')

if path.exists('Decrypted/8ed9e902c5c024bfb899e99893d4eb525d3ad179.txt'):
    writer2.write('trying to pack 3rd file')
    pack('8ed9e902c5c024bfb899e99893d4eb525d3ad179')
    writer2.write(': done\n\r')

else:
    writer2.write(': missing 3rd file\n\r')

writer2.close()
