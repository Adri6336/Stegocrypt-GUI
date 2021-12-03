# Handle encryption++
import secrets  # Needed to enable cryptographically secure random number generation
from stegano import lsb as steg  # Needed to enable steganography
from secrets import randbelow  # Needed for cryptographically secure password generation
from threading import Thread as th  # Needed to allow me to run threads
from subprocess import run  # Allows me to call the Go-derived encryption exe
from platform import system

# Handle GUI
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog


class Stegocrypt:
    """
    This is the GUI. It has many of the functions needed for this app to work.
    """

    whereami = os.getcwd()  # Determine the current working directory.

    # Determine operating system
    whatami = system()
    if whatami == 'Windows':  # Windows, use backslashes & exe
        program = '.\\stegocrypt.exe'
        plainPath = 'Data\\Messages\\1.scg'
        ciphPath = 'Data\\Messages\\2.scg'

    else:  # Else, use forward slashes & no exe
        program = './stegocrypt'
        plainPath = 'Data/Messages/1.scg'
        ciphPath = 'Data/Messages/2.scg'


    workLock = False  # Prevents multiple threads from running
    special = ['!', '@', '#', '$', '%',
               '^', '&', '*', '(', ')',
               '+', '=', '\\', '/', ':'
               ';', '"', "'", '<', '>',
               '?', '|', '{', '}']  # Special symbols, for use with randGen

    def __init__(self, master=None):
        # build ui
        self.frame1 = ttk.Frame(master)

        # Encrypt image button
        self.encry_but = ttk.Button(self.frame1)
        self.encry_but.configure(text='Encrypt', width='20')
        self.encry_but.place(anchor='nw', height='60', relx='0.05', rely='0.05', width='200', x='0', y='0')
        self.encry_but.configure(command=lambda: self.workThread(op='encrypt'))

        # Decrypt image button
        self.decry_but = ttk.Button(self.frame1)
        self.decry_but.configure(text='Decrypt')
        self.decry_but.place(anchor='nw', height='60', relx='.05', rely='.2', width='200', y='0')
        self.decry_but.configure(command=lambda: self.workThread(op='decrypt'))

        # Separator
        self.separator1 = ttk.Separator(self.frame1)
        self.separator1.configure(orient='vertical')
        self.separator1.place(anchor='nw', height='600', relx='0.39', x='0', y='0')

        # Password Text Entry
        self.passEntry = ttk.Entry(self.frame1)
        self.passEntry.place(anchor='nw', relx='0.025', rely='.5', width='235', x='0', y='0')

        # Password Label
        self.passLabel = ttk.Label(self.frame1)
        self.passLabel.configure(font='TkDefaultFont', text='Password')
        self.passLabel.place(anchor='nw', relx='0.14', rely='0.45', x='0', y='0')

        # File Name Label
        self.label2 = ttk.Label(self.frame1)
        self.label2.configure(text='File Name')
        self.label2.place(anchor='nw', relx='.14', rely='0.6', x='0', y='0')

        # File Name Entry
        self.nameEntry = ttk.Entry(self.frame1)
        self.nameEntry.place(anchor='nw', relx='0.025', rely='.65', width='235', x='0', y='0')

        # Generate Password Button
        self.genPass = ttk.Button(self.frame1)
        self.genPass.configure(text='Generate Password')
        self.genPass.place(anchor='nw', height='60', relx='0.05', rely='0.8', width='200', x='0', y='0')
        self.genPass.configure(command=lambda: self.workThread(op='randGen'))

        # Separator
        self.separator2 = ttk.Separator(self.frame1)
        self.separator2.configure(orient='horizontal')
        self.separator2.place(anchor='nw', relx='0.39', rely='0.08', width='600', x='0', y='0')

        # Warning Display Textbox
        self.displayWin = tk.Text(self.frame1)
        self.displayWin.configure(height='2', width='52', wrap='word')
        self.displayWin.place(anchor='nw', relx='0.3925', y='0')

        # Message / Display Label
        self.messDisp = ttk.Label(self.frame1)
        self.messDisp.configure(text='Message Entry / Display')
        self.messDisp.place(anchor='nw', relx='0.40', rely='0.09', x='0', y='0')

        # Message Textbox
        self.messEntry = tk.Text(self.frame1)
        self.messEntry.configure(height='24', width='49', wrap='word')
        self.messEntry.place(anchor='nw', relx='.4', rely='0.14', x='0', y='0')

        # Textbox scrollbar
        self.scrollbar1 = ttk.Scrollbar(self.frame1)
        self.scrollbar1.configure(cursor='arrow', orient='vertical')
        self.scrollbar1.place(anchor='nw', height='415', relx='0.97', rely='.14', x='0', y='0')
        self.scrollbar1.config(command=self.messEntry.yview)

        self.frame1.configure(height='500', width='700')
        self.frame1.pack(side='top')

        # Main widget
        self.mainwindow = self.frame1

        # Set up directories and files if not already made
        self.folder(name='Data')
        self.folder(name='Data/Messages')
        self.isFile(path=self.plainPath)
        self.isFile(path=self.ciphPath)

        # Welcome message (small box, so keep it short)
        self.setText(where=self.displayWin, text=('Please enter a password to encrypt / decrypt messages ' +
                                                  'with Stegocrypt-GUI. Filename is optional.'))

    def workThread(self, op):
        """
        This function directs commands to their threads, or rejects them if currently working.

        :param op: Specifies the type of operation
        :return: None
        """

        # Generate password
        if op == 'randGen' and not self.workLock:
            work = th(self.randGen(size=16))
            try:
                work.start()

            except Exception as e:
                self.setText(self.displayWin, str(e))
                self.workLock = False

            return

        # Encrypt
        elif op == 'encrypt' and not self.workLock:
            work = th(self.encryPic())
            try:
                work.start()

            except Exception as e:
                self.setText(self.displayWin, str(e))
                self.workLock = False

            return

        # Decrypt
        elif op == 'decrypt' and not self.workLock:
            work = th(self.decryPic())
            try:
                work.start()

            except Exception as e:
                self.setText(self.displayWin, str(e))
                self.workLock = False

            return


    def encryPic(self):
        """
        This will encrypt a message, then pass it over to embed to make it part of an image.

        :return: None
        """

        try:

            # 0. Get worklock
            self.workLock = True
            print('\n=======START ENCRY=======\n')

            # 1. Set up folder, get picture
            putHere = self.folder('Encrypted_Pics')

            pic = filedialog.askopenfilename(initialdir=self.whereami, title='Select a Picture to Modify',
                                             filetypes=(("Pictures", ['*.png']), ('Invalid Files', '*.*')))

            if not os.path.isfile(str(pic)):  # User exited out; abort silently
                self.workLock = False
                print('\n~~~~~~~STOP ENCRY~~~~~~~\n')
                return

            # 2. Get message, end prematurely if empty, and save password
            toEncode = self.messEntry.get("1.0", "end-1c")  # Get message
            passwd = self.passEntry.get()  # Get password
            name = self.nameEntry.get()  # Get name, if there's any


            if passwd == '':  # Empty password invalid; abort
                self.setText(where=self.displayWin, text='Aborted: Enter or generate password first')
                print('[X] Failure: no password provided')
                self.workLock = False
                print('\n~~~~~~~STOP ENCRY~~~~~~~\n')
                return

            if toEncode == '':  # No message; abort
                self.setText(where=self.displayWin, text='Aborted: Nothing is in message')
                print('[X] Failure: bruh, you didn\'t even write a message. What exactly were you ' +
                      'expecting to happen?')
                self.workLock = False
                print('\n~~~~~~~STOP ENCRY~~~~~~~\n')
                return


            # 2.5 Determine name and extension
            fileInfo = self.fileInfo(pathway=pic)  # Gets name and extension (w/out '.') info as a tuple

            if name == '':  # If the user hasn't added a custom name
                name = fileInfo[0]  # Use default name
            extension = '.' + fileInfo[1]  # Save extension type
            del fileInfo  # Delete the tuple as it won't be used later

            if not extension == '.png':
                self.setText(where=self.displayWin, text='Aborted: Selected file not PNG')
                print('[X] Failure: image type not supported')
                self.workLock = False
                print('\n~~~~~~~STOP ENCRY~~~~~~~\n')
                return

            # 3. Pass text onto stegocrypt
            print('[+] Passing information into cipher')
            self.setText(where=self.displayWin, text='Now working on encrypting message with AES-256 cipher ...')

            with open(self.plainPath, 'w') as file:
                file.write(toEncode)  # Save plaintext to file

            run([self.program, '-e', passwd])  # Ask stegocryptgo to encrypt plaintext

            with open(self.ciphPath, 'r') as file:
                cipherText = file.read()  # Get the base64 aes-encrypted ciphertext

            # 4. Pass byte stream to embed
            print('[i] Ciphertext: ' + str(cipherText))
            print('[+] Passing ciphertext to embedding function')
            self.embed(content=cipherText, output=putHere, picture=pic, filename=name+extension)

            # 5. Clean up
            del passwd, cipherText

            with open(self.plainPath, 'w') as file:
                file.write(secrets.token_hex(10000))  # Overwrite to help conceal message

            print('[i] Flooded temp plaintext file with random bits')

            # 6. Release worklock, end
            self.workLock = False

        except Exception as e:
            print('[X] Error: ' + str(e))
            self.setText(where=self.displayWin, text='Error: ' + str(e))
            with open(self.plainPath, 'w') as file:
                file.write(secrets.token_hex(10000))  # Overwrite to help conceal message
                print('[i] Flooded temp plaintext file with random bits')
                print('\n~~~~~~~STOP ENCRY~~~~~~~\n')
            self.workLock = False
            return
        print('\n~~~~~~~STOP ENCRY~~~~~~~\n')


    def decryPic(self):
        try:

            """
            This will extract data from a message and attempt to decrypt it with the user
            provided password. If successful, displays message content to message textbox; else,
            it tells user that it failed in the display textbox.
    
            :return: None
            """
            # 0. Obtain worklock and get password
            self.workLock = True
            passwd = self.passEntry.get()  # Get password
            print('\n=======START DECRY=======\n')

            # 1. Set up folder, get picture. Determine if file is picture
            putHere = self.folder('Encrypted_Pics')

            pic = filedialog.askopenfilename(initialdir=self.whereami + '/' + putHere,
                                             title='Select a Picture to Investigate',
                                             filetypes=(("Pictures", ['*.png']), ('Invalid Files', '*.*')))

            if not os.path.isfile(str(pic)):  # User exited out; abort silently
                self.workLock = False
                print('\n~~~~~~~STOP DECRY~~~~~~~\n')
                return

            fileInfo = self.fileInfo(pathway=pic)  # Get name and extension
            if not fileInfo[1] == 'png':
                self.setText(where=self.displayWin, text='Aborted: Selected file not supported image (PNG)')
                self.workLock = False
                print('[X] Failure: image type not supported')
                print('\n~~~~~~~STOP DECRY~~~~~~~\n')
                return

            # 2. Look into image for any embedding
            try:
                results = steg.reveal(pic)  # Look into photo with steg module. Save string results

            except Exception as e:
                print(e)
                self.setText(where=self.displayWin, text='Error: ' + str(e))
                self.workLock = False
                print('[X] Failure: ' + str(e))
                print('\n~~~~~~~STOP DECRY~~~~~~~\n')
                return

            if results == None:
                self.setText(where=self.displayWin, text='Nothing was found in the image')
                self.workLock = False
                print('[X] No messages located within image. Cancelling ...')
                print('\n~~~~~~~STOP DECRY~~~~~~~\n')
                return

            else:
                self.setText(where=self.displayWin, text='Found something in image. Attempting to decrypt ...')

            # 3. Attempt decryption
            print('[+] Found: ' + results)

            with open(self.ciphPath, 'w') as file:
                file.write(results)  # Save ciphertext to file

            run([self.program, '-d', passwd])  # Tell stegocrypt to decrypt encoded message

            if os.path.isfile('Data/Messages/ERROR.log'):
                self.setText(where=self.displayWin, text='Failed to decrypt, incorrect password likely.')
                self.workLock = False
                os.remove('Data/Messages/ERROR.log')
                print('[X] Failure: incorrect password likely')
                print('\n~~~~~~~STOP DECRY~~~~~~~\n')
                return

            else:
                print('[+++] Decrypted message successfully [+++]')
        

            with open(self.plainPath, 'r') as file:
                plainText = file.read()  # Get plaintext


            self.setText(where=self.messEntry, text=plainText)
            self.setText(where=self.displayWin, text='Message successfully decrypted!')

            # 4. END
            with open(self.plainPath, 'w') as file:
                file.write(secrets.token_hex(10000))  # Overwrite to help conceal message

            self.workLock = False

        except Exception as e:
            print('[X] Error: ' + str(e))
            self.setText(where=self.displayWin, text='Error: ' + str(e))
            self.workLock = False
            print('\n~~~~~~~STOP DECRY~~~~~~~\n')
            return

        print('\n~~~~~~~STOP DECRY~~~~~~~\n')


    def embed(self, content, output, picture, filename):
        """
        This will embed text data into the image using stegano. Preferably input AES256-CBC encrypted
        data. Once completed, a file will be created in the encrypted_pics folder.

        :param content: String ot bytes
        :param output: Where we'll put the modified image
        :param picture: Specify what picture to modify
        :return: None
        """
        self.setText(where=self.displayWin, text='Now working on embedding cipher text to image ...')

        # 1. Try embedding data into unchanged image. Compare output to determine if corruption occurred due to size
        print('[+] Embedding ...')

        try:
            # We use base64 encoding here to allow bytes to be translated to and from strings
            modPic = steg.hide(picture, str(content))  # Create a modified pic in memory
            modPic.save(output + '/' + filename)  # Save pic to hard drive

            self.setText(where=self.displayWin,
                         text='Success! The message has been encrypted and hidden inside the image')
            print('[+++] Ciphertext successfully embedded [+++]')

        except Exception as e:
            self.setText(self.displayWin, text='FAILURE: ' + str(e))  # Show user what happened




    def fileInfo(self, pathway):
        """
        Determines the file's name and extension.

        :param pathway: String containing a pathway
        :return: Tuple with name and extension as (name, extension)
        """

        newName = []

        for char in range(len(pathway) - 1, -1, -1):  # Reverse iterate
            if pathway[char] == '/' or pathway[char] == '\\':  # If the character at pos char is a slash, end
                break

            else:  # Record everything
                newName.append(pathway[char])

        newName.reverse()  # Correct orientation (it's backwards since we were reverse iterating)
        results = ''  # Create a placeholder variable: this'll hold the string of the list compiled
        results = results.join(newName)  # Compile list

        print('[+] Determined filetype and filename')
        return tuple(results.split('.'))  # Split by the period. The name = 0, extension = 1


    def setText(self, where, text):
        """
        This sets text of textboxes. Partially yoinked from my other app EnKryptos.

        :param text: What you want to display
        :param where: tkEntry object ; 'password' = password textbox.
        :return: None
        """

        if not where == 'password':  # If you don't specify the password, use object
            where.config(state='normal')
            where.delete('1.0', 'end')
            where.insert('0.0', text)

            if where == self.displayWin:  # If this is meant for the display window
                self.displayWin.config(state='disabled')  # Re-lock display

        else:  # Else if where is 'password', print in password text entry
            self.passEntry.delete('0', 'end')  # Clean box of anything else
            self.passEntry.insert('0', text)
            self.passEntry.place()

    def randGen(self, size):  # This function will randomly generate text
        """
        This function will randomly generate text using a cryptographically secure pseudorandom number generator.
        Yoinked from EnKryptos with slight modification.

        :param size: This indicates how many chars we want to generate.
        :return: None
        """
        randName = []  # Empty list will hold the chars
        numOrChar = randbelow(4)  # Randomly determine what the first char will be
        specialCt = len(self.special)  # Size of the list containing special characters
        self.workLock = True  # Obtain worklock

        # 1. Randomly generate text until character length (size) is met
        for char in range(size):
            if numOrChar == 0:  # Use Number
                randName.append(chr(48 + randbelow(10)))  # ASCII Range = 48-57, 10 wont be met so it'll be between 0-9

            elif numOrChar == 1:  # Use Lowercase Character
                randName.append(chr(97 + randbelow(26)))  # 97-122

            elif numOrChar == 2:  # Use Special Character
                randName.append(self.special[randbelow(specialCt)])

            else:  # Use Capitalized Character
                randName.append(chr(65 + randbelow(26)))  # 65-90

            numOrChar = randbelow(4)  # Reset the chance

        # 2. Convert the list into a single string and return it
        gen = ''  # Set up empty string for compilation
        gen = gen.join(randName)  # Compile list to string


        self.setText(where='password', text=gen)  # Pass string to password text box
        self.setText(where=self.displayWin, text='Created new password (please record it as it\'s unsaved)')
        print('[i] Generated random cryptographically-secure password')
        self.workLock = False  # Release worklock
        return


    def folder(self, name):
        """
        Makes a directory if it hasn't already been made.

        :param name: This specifies the name of the directory.
        :return: The name of the directory
        """
        if not os.path.exists(self.whereami + '/' + name):
            os.mkdir(name)
        

        return name

    def isFile(self, path):
        """
        Makes a file if it hasn't already been made.

        :Param name: This specifies the name of the file.
        :Return: None
        """

        if not os.path.isfile(path):
            file = open(path, 'w')
            file.close()


    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(height=False, width=False)  # Prohibit resizing the height or width of window
    root.wm_title("Stegocrypt 0.2")  # Sets the title of the window to the string included as an argument

    app = Stegocrypt(root)
    app.run()
