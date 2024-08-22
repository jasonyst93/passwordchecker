import requests 
import hashlib
import sys

def request_api_data(query_char):
    url ='https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api again')
    return res


def get_password_leak_count(hashes,hash_to_check):
    hashes = (line.split(':')for line in hashes.text.splitlines()) 
    # if our tail found in tails from the matched list -> return count
    for h ,count in hashes:
        if h == hash_to_check: 
            return count 
    return 0


def pwned_api_check(password):    
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5] , sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leak_count(response,tail) 

# A main function recieve args and print the result
def main(args):
    for password in args: #loop via all the passwords 
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times in pwned.... Please use another password')
        else:
            print(f'{password} is good')
    return 'done!'

#python3 checkmypass.py[0] password[1] abcd1234[2] #all the args from 1 
main(sys.argv[1:]) 

