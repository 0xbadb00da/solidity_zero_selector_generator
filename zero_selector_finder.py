from Crypto.Hash import keccak
import sys
import datetime

ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters_length = len(ascii_letters)

def main():
    init_function_definition='mintWL(uint256,uint256[])'
    init_selector = get_hash(init_function_definition)[:4].hex()

    function_definition_parts=init_function_definition.split('(')
    best_length = len(get_hash(init_function_definition).lstrip(b'\x00'))

    counter=0

    start_ts = datetime.datetime.now().timestamp()

    print(f'0\t{init_selector} : {init_function_definition}')

    while True:
        new_function_definition=function_definition_parts[0]+'_'+pick_letter(counter)+'('+function_definition_parts[1]
        function_hash = get_hash(new_function_definition)
        length = len(function_hash.lstrip(b'\x00'))
        if length < best_length:
            best_length=length
            print(f"{int(datetime.datetime.now().timestamp()-start_ts)}\t{function_hash[:4].hex()} : {new_function_definition}")
            if length==28:  #32 digest bytes - 4 x00
                break
        counter+=1

def pick_letter(num):
    global ascii_letters, ascii_letters_length
    res = ""
    while num > 0:
        num,m = divmod(num, ascii_letters_length)
        res += ascii_letters[m]
    return res[::-1]

def get_hash(func):
    k = keccak.new(digest_bits=256)
    k.update(func.encode('utf-8'))
    return k.digest()

main()