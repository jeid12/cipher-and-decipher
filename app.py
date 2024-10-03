import random
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for using session and flash messages


# Function to encrypt the text using a random key
def cipher_text(text, key):
    ciphered_text = []
    for i in range(len(text)):
        if text[i].isalpha():
            # Encrypt uppercase letters
            if text[i].isupper():
                x = (ord(text[i]) - ord('A') + key) % 26 + ord('A')
                ciphered_text.append(chr(x))
            # Encrypt lowercase letters
            else:
                x = (ord(text[i]) - ord('a') + key) % 26 + ord('a')
                ciphered_text.append(chr(x))
        else:
            # Non-alphabetic characters are not changed
            ciphered_text.append(text[i])
    return "".join(ciphered_text)


# Function to decrypt the text using the same random key
def decipher_text(ciphered_text, key):
    original_text = []
    for i in range(len(ciphered_text)):
        if ciphered_text[i].isalpha():
            # Decrypt uppercase letters
            if ciphered_text[i].isupper():
                x = (ord(ciphered_text[i]) - ord('A') - key + 26) % 26 + ord('A')
                original_text.append(chr(x))
            # Decrypt lowercase letters
            else:
                x = (ord(ciphered_text[i]) - ord('a') - key + 26) % 26 + ord('a')
                original_text.append(chr(x))
        else:
            # Non-alphabetic characters are not changed
            original_text.append(ciphered_text[i])
    return "".join(original_text)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_key', methods=['POST'])
def generate_key_route():
    text = request.form['text']
    
    # Generate a random key (an integer between 0 and 25 inclusive)
    random_key = random.randint(0, 25)
    print(random_key)
    
    # Store text and key in session to use in the next step
    session['text'] = text
    session['key'] = random_key

    return redirect(url_for('validate_key'))


@app.route('/validate_key', methods=['GET', 'POST'])
def validate_key():
    if request.method == 'POST':
        entered_key = int(request.form['entered_key'])
        generated_key = session.get('key')

        # Check if the entered key matches the generated key
        if entered_key == generated_key:
            return redirect(url_for('key_generated'))
        else:
            flash("Incorrect key! Please try again.")
            return redirect(url_for('validate_key'))

    return render_template('validate_key.html')


@app.route('/key_generated', methods=['GET', 'POST'])
def key_generated():
    if request.method == 'POST':
        action = request.form['action']
        text = session.get('text')  # Retrieve text from session
        key = session.get('key')    # Retrieve key from session
        
        if action == 'encrypt':
            result = cipher_text(text, key)
            operation = 'Encrypted'
        else:
            result = decipher_text(text, key)
            operation = 'Decrypted'

        return render_template('key_generated.html', text=text, key=key, result=result, operation=operation)
    
    return render_template('key_generated.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

