import base64
SALT = 'tickettest'
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

KEY = 'TICKETTEST987654'
EVENT_NAME = 'TESTEVENT'
PATH = 'main.xlsx'

def aes_encrypt(plaintext, key=KEY):
    key = key.encode('utf-8')
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be either 16, 24, or 32 bytes long")
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    encrypted_text = base64.b64encode(iv + ciphertext).decode('utf-8')
    return encrypted_text

def aes_decrypt(encrypted_text, key=KEY):
    key = key.encode('utf-8')
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be either 16, 24, or 32 bytes long")
    encrypted_data = base64.b64decode(encrypted_text)
    iv = encrypted_data[:AES.block_size]
    ciphertext = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
    return decrypted_text


def genTicketID(id:int,username:str,other_info:str=None):
    '''
    接收给定参数，生成票面id。
    参数：id/用户名/其他信息，其中其他信息缺省为None。
    '''
    StringOrigin = f"{EVENT_NAME}By-PyTicketManager {id} {username}"
    if other_info:
        StringOrigin = StringOrigin + f" {other_info}"
    return aes_encrypt(StringOrigin,KEY)

print(aes_decrypt('1tIUJ8zJ8EAbXJKEJiJzSvUkpmP9NxIUbOuF2qDh+dKW9nU/t2ZIxxwlcIH9BhTl1rDgmu0tjVXDbrA5iVdvqg=='))
print(aes_decrypt('z6Tafr8GjOb5MpmxjLNJV1TBJeEpp21oA3ddBKadfVkm8j8ilE9FuOsL2bHg1H1vAmH2kjwewZWB+0YxfrRTcQ=='))
