#  Note: print functions are everywhere here as this app is meant to be ran from an executable file, which allows
# me to turn off the console (I'm using pyinstaller).

# Handle encryption++
import secrets
from stegano import lsb as steg
from PIL import Image as img
from secrets import randbelow  # Needed for cryptographically secure password generation
from threading import Thread as th
from subprocess import run

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
            print('=======START ENCRY=======')

            # 1. Set up folder, get picture
            putHere = self.folder('Encrypted_Pics')

            pic = filedialog.askopenfilename(initialdir=self.whereami, title='Select a Picture to Modify',
                                             filetypes=(("Pictures", ['*.png']), ('Invalid Files', '*.*')))

            if not os.path.isfile(str(pic)):  # User exited out; abort silently
                self.workLock = False
                return

            # 2. Get message, end prematurely if empty, and save password
            toEncode = self.messEntry.get("1.0", "end-1c")  # Get message
            passwd = self.passEntry.get()  # Get password
            name = self.nameEntry.get()  # Get name, if there's any


            if passwd == '':  # Empty password invalid; abort
                self.setText(where=self.displayWin, text='Aborted: Enter or generate password first')
                self.workLock = False
                return

            if toEncode == '':  # No message; abort
                self.setText(where=self.displayWin, text='Aborted: Nothing is in message')
                self.workLock = False
                return


            # 2.5 Determine name and extension
            fileInfo = self.fileInfo(pathway=pic)  # Gets name and extension (w/out '.') info as a tuple

            if name == '':  # If the user hasn't added a custom name
                name = fileInfo[0]  # Use default name
            extension = '.' + fileInfo[1]  # Save extension type
            del fileInfo  # Delete the tuple as it won't be used later

            if not extension == '.png':
                self.setText(where=self.displayWin, text='Aborted: Selected file not PNG')
                self.workLock = False
                return

            # 3. Pass text onto stegocrypt
            print('Trying to encrypt')
            self.setText(where=self.displayWin, text='Now working on encrypting message with AES-256 cipher ...')

            with open('Data\\Messages\\1.scg', 'w') as file:
                file.write(toEncode)  # Save plaintext to file

            run(['stegocrypt.exe', '-e', passwd])  # Ask stegocryptgo to encrypt plaintext

            with open('Data\\Messages\\2.scg', 'r') as file:
                cipherText = file.read()  # Get the base64 aes-encrypted ciphertext

            # 4. Pass byte stream to embed
            print('Encrypted: ' + str(cipherText))
            print('Passing stuff to embed')
            self.embed(content=cipherText, output=putHere, picture=pic, filename=name+extension)

            # 5. Clean up
            del passwd, cipherText

            with open('Data\\Messages\\1.scg', 'w') as file:
                file.write(secrets.token_hex(10000))  # Overwrite to help conceal message

            # 6. Release worklock, end
            self.workLock = False
            return

        except Exception as e:
            print('Error: ' + str(e))
            self.setText(where=self.displayWin, text='Error: ' + str(e))
            self.workLock = False
            return

    def decryPic(self):
        try:

            """
            This will extract data from a message and attempt to decrypt it with the user
            provided password. If successful, displays message content to message textbox; else,
            tells user that it failed in the display textbox.
    
            :return: None
            """
            # 0. Obtain worklock and get password
            self.workLock = True
            passwd = self.passEntry.get()  # Get password
            print('=======START DECRY=======')

            # 1. Set up folder, get picture. Determine if file is picture
            putHere = self.folder('Encrypted_Pics')

            pic = filedialog.askopenfilename(initialdir=self.whereami + '/' + putHere,
                                             title='Select a Picture to Investigate',
                                             filetypes=(("Pictures", ['*.png']), ('Invalid Files', '*.*')))

            if not os.path.isfile(str(pic)):  # User exited out; abort silently
                self.workLock = False
                return

            fileInfo = self.fileInfo(pathway=pic)  # Get name and extension
            if not fileInfo[1] == 'png':
                self.setText(where=self.displayWin, text='Aborted: Selected file not supported image (PNG)')
                self.workLock = False
                return

            # 2. Look into image for any embedding
            try:
                results = steg.reveal(pic)  # Look into photo with steg module. Save string results

            except Exception as e:
                print(e)
                self.setText(where=self.displayWin, text='Nothing found in image or image is corrupted')
                self.workLock = False
                return

            if results == '':
                self.setText(where=self.displayWin, text='Nothing was found in the image')
                self.workLock = False
                return

            else:
                self.setText(where=self.displayWin, text='Found something in image. Attempting to decrypt ...')

            # 3. Attempt decryption
            print('Found: ' + results)

            with open('Data\\Messages\\2.scg', 'w') as file:
                file.write(results)  # Save ciphertext to file

            run(['stegocrypt.exe', '-d', passwd])  # Tell stegocryptgo to decrypt encoded message

            with open('Data\\Messages\\1.scg', 'r') as file:
                plainText = file.read()  # Get plaintext


            self.setText(where=self.messEntry, text=plainText)
            self.setText(where=self.displayWin, text='Message successfully decrypted!')

            # 4. END
            with open('Data\\Messages\\1.scg', 'w') as file:
                file.write(secrets.token_hex(10000))  # Overwrite to help conceal message

            self.workLock = False

        except Exception as e:
            print('Error: ' + str(e))
            self.setText(where=self.displayWin, text='Error: ' + str(e))
            self.workLock = False
            return


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
        print('Embedding without image alteration')

        # We use base64 encoding here to allow bytes to be translated to and from strings, allowing ease of translation
        modPic = steg.hide(picture, str(content))  # Create a modified pic in memory
        modPic.save(output + '/' + filename)  # Save pic to hard drive

        embedded = str(content) # This is what we embedded into the image
        x = steg.reveal(output + '/' + filename)  # This is what we were able to find in the image

        # 2. If corruption occurred, gradually increase size of image until no corruption is identified.
        try:

            if not embedded == str(x):  # If what we embedded does not match what we found, data was corrupted
                # 1. Purge old image, set up loop variables
                print('Data corrupt. Need larger image')
                os.remove(output + '/' + filename)  # Delete the corrupted image (no risk, data already encrypted)
                plusSize = 5  # We'll use this to gradually increase the image's size

                while not embedded == str(x):
                    # self.setText(where=self.displayWin, text='Now growing image by ' + str(plusSize))
                    print('Growing image by ' + str(plusSize))
                    # 2. Grow image
                    pic = img.open(picture)  # Put picture in memory
                    size = [pic.size[0]+plusSize, pic.size[1]+plusSize]  # W x H, with plusSize added
                    pic.resize((size[0], size[1]), img.ANTIALIAS)  # Resize

                    # 3. Re-attempt steganographic embedding
                    modPic = steg.hide(pic, str(embedded))  # Embed info into image
                    modPic.save(output + '/' + filename)  # Save to hard drive
                    del x  # Remove prior instance of x
                    x = steg.reveal(output + '/' + filename)  # Check info you embedded. Will be compared at while test

                    # 4. Increment plusSize by 5
                    plusSize += 5
                    print('Embedded: ' + embedded)
                    print('Recovered:' + str(x))

                    if plusSize >= 30:  # I'm not certain what to make the threshold.
                        print('Infinite loop detected')
                        self.setText(where=self.displayWin, text='Error: Unknown malfunction caused infinite loop')
                        try:
                            del plusSize, pic, size, x, embedded, modPic  # Clean up mess before leaving
                        except Exception as e:  # If something goes wrong, ignore & move on. No sensitive data here
                            print(e)  # Tell me what went wrong to help me patch it in the future
                        return

        except Exception as e:  # Since we're growing the image, eventually it may become too large to handle
            self.setText(where=self.displayWin, text='Error: Message too large to embed')
            print(e)
            try:
                del plusSize, pic, size, x, embedded, modPic  # Clean up mess before leaving
            except Exception as e:
                print('2: ' + str(e))  # The two signifies that this is a second-level exception-catch
            self.workLock = False
            return

        self.setText(where=self.displayWin, text='Success! The message has been encrypted and hidden inside the image')
        print('Image successfully embedded with encrypted text')


    def fileInfo(self, pathway):
        """
        Determines the file's name and extension.

        :param pathway: String containing a pathway
        :return: Tuple with name and extension as (name, extension)
        """

        print('Trying to determine name and extension')
        newName = []

        for char in range(len(pathway) - 1, -1, -1):  # Reverse iterate
            if pathway[char] == '/' or pathway[char] == '\\':  # If the character at pos char is a slash, end
                break

            else:  # Record everything
                newName.append(pathway[char])

        newName.reverse()  # Correct orientation (its backwards since we were reverse iterating)
        results = ''  # Create a placeholder variable: this'll hold the string of the list compiled
        results = results.join(newName)  # Compile list

        return tuple(results.split('.'))  # Split by the period. The name == 0, extension == 1


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
                if randName[-1] == "'" or randName[-1] == '"' or randName[-1] == '\\':  # This is unnecessary here, but idk
                    randName[-1] = '*'

            else:  # Use Capitalized Character
                randName.append(chr(65 + randbelow(26)))  # 65-90

            numOrChar = randbelow(4)  # Reset the chance

        # 2. Convert the list into a single string and return it
        gen = ''  # Set up empty string for compilation
        gen = gen.join(randName)  # Compile list to string


        self.setText(where='password', text=gen)  # Pass string to password text box
        self.setText(where=self.displayWin, text='Created new password (please record it as it\'s unsaved)')
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


    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(height=False, width=False)  # Prohibit resizing the height or width of window
    root.wm_title("Stegocrypt 0.1")  # Sets the title of the window to the string included as an argument

    app = Stegocrypt(root)
    app.run()
