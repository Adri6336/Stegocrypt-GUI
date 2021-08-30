# Stegocrypt-GUI
*Only PNG images are supported currently*

Tool for easily steganographically embedding AES-256 encrypted messages into images for ultra-secure communication. Designed for users with no programming experience to get the most out of steganographic communication. All you'll need to do to start is:

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

## Download:

*Note: Malwarebytes considers the exe to be malware because it uses PyInstaller (same tool others have used to compile malware). I assume this is a heuristics thing, so likely many other antivirus solutions that use heuristics will also read a false positive. If this concerns you, you can look through my code (to ensure that it's not malicious -- I promise it isn't), compile the Go, and run the script without having to run any of the executables I've provided. I'll detail the steps for this below "Downloads".*

- [Stegocrypt-GUI Linux Version 0.2](https://github.com/Adri6336/stegocrypt-gui_dl/raw/gh-pages/Stegocrypt-GUI_v0.2%20--%20Lin.tar.gz)
- [Stegocrypt-GUI Windows Version 0.2](https://github.com/Adri6336/stegocrypt-gui_dl/raw/gh-pages/Stegocrypt-GUI_v0.2%20--%20Win.zip)

## Compiling Yourself:

1. Set up a Go pathway.

    I. Make a new folder within Documents called "go".
  
    II. Within "go", make a folder called "src".
  
    III. Within "src", make a folder called "local-only".
  
    IV. Within "local-only", make a folder called "steg" (this folder can be called whatever you like).
  
    V. Within "steg", paste the "stegocrypt.go" file that I've included in this repository as well as the python script and requirements.txt.
  
2. Use Go to build the binary for stegocrypt (Go must be installed first).

    VI. Open the folder "~/Documents/go/src/local-only/steg" in your terminal (Powershell for Windows)
  
    VII. Enter the command, "go mod init example.com/user/steg"
  
    VIII. Enter the command, "go build stegocrypt.go". You should now have generated an executable file from the code that you've reviewed and certified to be malware-free.
  
    IX. With Python3 installed, enter the command, "pip install -r requirements.txt" (use pip3 if on Linux)
  
    X. Enter the command to start Stegocrypt-GUI:
      - Linux = python3 main.py
      - Windows = python main.py

## Setting Up Stegocrypt-GUI

1. Download the version appropriate for your operating system with the above links.
2. Extract contents.
3. On Windows, run the "Stegocrypt-GUI.exe" file found within. On Linux, execute the "start-stegocryptgui" script found within.

# Version 0.2 Changelog

- Stegocrypt-GUI now creates the directories and files it needs (except Go-derived exe) upon runtime.
- Fixed incorrect password decryption notification. Used to say 'decryption successful', now indicates that it actually failed.
- Made the Python script able to run on both Linux and Windows without forcing me to modify it every time.


-------------------------

Note: Memes are inconspicuous, so they're the perfect vessel for secret messages (just saying, lol).

Note 2: You'll need to ensure that the image is not compressed when sending it to your recipient. Email attachments are usually good for this.

Note 3: Example picture's password is Securepassword1!
