def normalize_char(c):
    # Convertir les caractères en majuscules et ignorer les accents
    if 'a' <= c <= 'z':
        return chr(ord(c) - ord('a') + ord('A'))
    return c

def is_letter(c):
    # Vérifie si un caractère est une lettre alphabétique
    return 'A' <= c <= 'Z' or 'a' <= c <= 'z'

def vigenere_cipher(text, key, encrypt=True):
    result = []
    key_len = len(key)
    j = 0  # Index pour parcourir la clé

    for c in text:
        if is_letter(c):
            normalized_c = normalize_char(c)
            normalized_key = normalize_char(key[j % key_len])

            offset = ord(normalized_c) - ord('A')
            key_offset = ord(normalized_key) - ord('A')

            if encrypt:
                new_char = chr((offset + key_offset) % 26 + ord('A'))
            else:
                new_char = chr((offset - key_offset + 26) % 26 + ord('A'))

            result.append(new_char)
            j += 1
        else:
            result.append(c)

    return ''.join(result)

def process_file(input_filename, output_filename, key, encrypt=True):
    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            text = infile.read()
            result = vigenere_cipher(text, key, encrypt)
            outfile.write(result)
            print(f"Opération terminée avec succès. Résultat écrit dans {output_filename}.")
    except FileNotFoundError:
        print(f"Le fichier {input_filename} n'a pas été trouvé.")
    except IOError as e:
        print(f"Erreur lors de l'accès au fichier : {e}")

def main():
    input_filename = input("Entrez le nom du fichier source : ")
    output_filename = input("Entrez le nom du fichier de sortie : ")
    key = input("Entrez la clé : ")

    choice = input("Entrez 1 pour chiffrer ou 0 pour déchiffrer : ")
    encrypt = choice == '1'

    process_file(input_filename, output_filename, key, encrypt)

if __name__ == "__main__":
    main()
