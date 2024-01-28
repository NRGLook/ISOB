import string


def caesar_cipher(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted_index = (string.ascii_lowercase.index(char.lower()) + shift) % 26
            if char.islower():
                encrypted_text += string.ascii_lowercase[shifted_index]
            else:
                encrypted_text += string.ascii_uppercase[shifted_index]
        else:
            encrypted_text += char
    return encrypted_text


def vigenere_cipher(text, key):
    key_length = len(key)
    encrypted_text = ""
    for i, char in enumerate(text):
        if char.isalpha():
            key_shift = string.ascii_lowercase.index(key[i % key_length].lower())
            shift = string.ascii_lowercase.index(char.lower()) + key_shift
            shifted_index = shift % 26
            if char.islower():
                encrypted_text += string.ascii_lowercase[shifted_index]
            else:
                encrypted_text += string.ascii_uppercase[shifted_index]
        else:
            encrypted_text += char
    return encrypted_text


def encrypt_file_caesar(input_file, output_file, shift):
    with open(input_file, 'r') as file:
        plaintext = file.read()
    encrypted_text = caesar_cipher(plaintext, shift)
    with open(output_file, 'w') as file:
        file.write(encrypted_text)


def decrypt_file_caesar(input_file, output_file, shift):
    with open(input_file, 'r') as file:
        ciphertext = file.read()
    decrypted_text = caesar_cipher(ciphertext, -shift)
    with open(output_file, 'w') as file:
        file.write(decrypted_text)


def encrypt_file_vigenere(input_file, output_file, key):
    with open(input_file, 'r') as file:
        plaintext = file.read()
    encrypted_text = vigenere_cipher(plaintext, key)
    with open(output_file, 'w') as file:
        file.write(encrypted_text)


def decrypt_file_vigenere(input_file, output_file, key):
    with open(input_file, 'r') as file:
        ciphertext = file.read()
    decrypted_text = vigenere_cipher(ciphertext, key)
    with open(output_file, 'w') as file:
        file.write(decrypted_text)


encrypt_file_caesar("input.txt", "caesar_encrypted.txt", 3)
decrypt_file_caesar("caesar_encrypted.txt", "caesar_decrypted.txt", 3)

encrypt_file_vigenere("input.txt", "vigenere_encrypted.txt", "key")
decrypt_file_vigenere("vigenere_encrypted.txt", "vigenere_decrypted.txt", "key")
