text = "NYZKVSFRIU"

for shift in range(26):
    result = ""
    for char in text:
        if char.isalpha():
            char_code = ord(char) - shift
            if char_code < ord('A'):
                char_code += 26
            result += chr(char_code)
        else:
            result += char
    print(f"Shift {shift}: {result}")