# for windows only

import os
import sys
import time
import traceback

def decode(s: str) -> str:
  try:
    return s.encode('gbk').decode('shift_jisx0213')
  except:
    return s

 
def rename(old_path, new_path):
  # print("===")
  # print(old_path);print(new_path)
  os.rename(old_path, new_path)

def split(path: str) -> tuple[str, str]:   
  if os.path.isfile(path):
    return os.path.split(path)
  if os.path.isdir:    
    # 使用 os.path.normpath() 去掉多余的斜杠
    path = os.path.normpath(path)
    # 使用 os.path.dirname() 获取除了最后一个文件夹之外的其他部分
    path_without_last_folder = os.path.dirname(path)    
    # 使用 os.path.basename() 获取最后一个文件夹名
    last_folder = os.path.basename(path)
    return path_without_last_folder, last_folder
  raise OSError("path neither file or dir")


def rename_all(path):
  path = os.path.normpath(path)
  if os.path.isfile(path):
    # if it comes to a normal file, then just rename it 
    head, tail = split(path)
    new_path = os.path.join(head, decode(tail))
    rename(path, new_path)
    return
  if os.path.isdir(path):
    # if it is a folder, recursive it
    filename_list = os.listdir(path)
    for fileame in filename_list:
      # travel all the sub files and folders.
      rename_all(os.path.join(path, fileame))
    head, tail = split(path)
    new_path = os.path.join(head, decode(tail))
    rename(path, new_path)

try:
  for arg in sys.argv:
    print(arg)
    rename_all(arg)
except Exception as e:
  traceback.print_exc()
finally:
  time.sleep(123)

# fn = r'c:\Users\Lumin\Downloads\棦帯傔偺涋彈\www\audio\bgs\拞弌偟嘆.ogg'
# rename_all(fn)

encoding_list = ['ascii',
 'big5',
 'big5hkscs',
 'cp037',
 'cp273',
 'cp424',
 'cp437',
 'cp500',
 'cp720',
 'cp737',
 'cp775',
 'cp850',
 'cp852',
 'cp855',
 'cp856',
 'cp857',
 'cp858',
 'cp860',
 'cp861',
 'cp862',
 'cp863',
 'cp864',
 'cp865',
 'cp866',
 'cp869',
 'cp874',
 'cp875',
 'cp932',
 'cp949',
 'cp950',
 'cp1006',
 'cp1026',
 'cp1125',
 'cp1140',
 'cp1250',
 'cp1251',
 'cp1252',
 'cp1253',
 'cp1254',
 'cp1255',
 'cp1256',
 'cp1257',
 'cp1258',
 'euc_jp',
 'euc_jis_2004',
 'euc_jisx0213',
 'euc_kr',
 'gb2312',
 'gbk',
 'gb18030',
 'hz',
 'iso2022_jp',
 'iso2022_jp_1',
 'iso2022_jp_2',
 'iso2022_jp_2004',
 'iso2022_jp_3',
 'iso2022_jp_ext',
 'iso2022_kr',
 'latin_1',
 'iso8859_2',
 'iso8859_3',
 'iso8859_4',
 'iso8859_5',
 'iso8859_6',
 'iso8859_7',
 'iso8859_8',
 'iso8859_9',
 'iso8859_10',
 'iso8859_11',
 'iso8859_13',
 'iso8859_14',
 'iso8859_15',
 'iso8859_16',
 'johab',
 'koi8_r',
 'koi8_t',
 'koi8_u',
 'kz1048',
 'mac_cyrillic',
 'mac_greek',
 'mac_iceland',
 'mac_latin2',
 'mac_roman',
 'mac_turkish',
 'ptcp154',
 'shift_jis',
 'shift_jis_2004',
 'shift_jisx0213',
 'utf_32',
 'utf_32_be',
 'utf_32_le',
 'utf_16',
 'utf_16_be',
 'utf_16_le',
 'utf_7',
 'utf_8',
 'utf_8_sig']

# for encoding in encoding_list:
#   try:
#     encoded = '拞弌偟嘆'.encode('gbk').decode(encoding=encoding)
#     # if encoded == '\x82\xb5':
#     #   print("!!",end=" ")
#     print(encoded, encoding)
#   except Exception as e:
#     print(e)
#     pass