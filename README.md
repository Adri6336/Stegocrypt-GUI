# Stegocrypt-GUI
*Only PNG images are supported currently*

Tool for easily steganographically embedding AES-256 encrypted messages into images. 

All you'll need to do to start is:

1. Run Stegocrypt-GUI
2. Write a message
3. Enter or generate a password (save this or otherwise remember it)
4. Enter an optional name to replace your picture's filename
5. Press the "Encrypt" button, select one image (PNG image)
6. Done!

If you've recieved an image with encrypted text in it, you'll need to:

1. Run Stegocrypt-GUI
2. Enter password
3. Press the "Decrypt" button and read the message in the main text viewer.

# Getting Started With Stegocrypt-GUI

## Download and Run Stegocrypt-GUI v0.2.2:

1. Download Python [here](https://www.python.org/downloads/)
2. Windows: open PowerShell (Win + X, then 'A' after the options pop up) and use "pip install" to install this program's requirements as described in the file named requirements.txt. Look it up on Google if you get stuck.
3. Linux: I am taking the liberty to assume you've got the requirement installation handled.
4.  Windows: double-click main.py or type the command "python main.py" into the PowerShell window after you've navigated to Stegocrypt-GUI's folder (look up using cd command).
5.  Linux: "python3 main.py" 


- [Stegocrypt-GUI Linux Version 0.2.2](https://github.com/Adri6336/stegocrypt-gui_dl/raw/0.2.2/Stegocrypt-GUI-Lin.tar.gz)
- [Stegocrypt-GUI Windows Version 0.2.2](https://github.com/Adri6336/stegocrypt-gui_dl/raw/0.2.2/Stegocrypt-GUI_Win.zip)

## Compiling Yourself:

**1. Set up a Go pathway.**

    I. Make a new folder within Documents called "go".
  
    II. Within "go", make a folder called "src".
  
    III. Within "src", make a folder called "local-only".
  
    IV. Within "local-only", make a folder called "steg" (this folder can be called whatever you like).
  
    V. Within "steg", paste the "stegocrypt.go" file that I've included in this repository as well as the python script and requirements.txt.
  
**2. Use Go to build the binary for stegocrypt (Go must be installed first).**

    VI. Open the folder "~/Documents/go/src/local-only/steg" in your terminal (Powershell for Windows)
  
    VII. Enter the command, "go mod init example.com/user/steg"
  
    VIII. Enter the command, "go build stegocrypt.go". You should now have generated an executable file from the code that you've reviewed and certified to be malware-free.
    
**3. Install Python modules and run main.py**
  
    IX. With Python3 installed, enter the command, "pip install -r requirements.txt" (use pip3 if on Linux)
  
    X. Enter the command to start Stegocrypt-GUI:
      - Linux = python3 main.py
      - Windows = python main.py

## Setting Up Stegocrypt-GUI

1. Download the version appropriate for your operating system with the above links.
2. Extract contents.
3. On Windows, run the "Stegocrypt-GUI.exe" file found within. On Linux, execute the "start-stegocryptgui" script found within.

# Version 0.2.2 Changelog

- Made the terminal output more intelligible / useful
- Did some other stuff a while ago that made it better, but forgot to make a note of the changes :p. Just take my word for it that this version is better.
- Deleted useless code from script.
- Deleted unnecessary code that limited the randomness of password generation.


-------------------------

Note: Memes are inconspicuous, so they're the perfect vessel for secret messages (just saying, lol).

Note 2: You'll need to ensure that the image is not compressed when sending it to your recipient. Email attachments are usually good for this.

Note 3: Example picture's password is "Securepassword1!", without the quotation marks
