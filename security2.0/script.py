from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("key","bw") as file:
    file.write(key)
