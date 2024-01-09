import os

def main():
    secret_key = os.urandom(24)
    hex_key = secret_key.hex()
    print(hex_key)

if __name__ == '__main__':
    main()