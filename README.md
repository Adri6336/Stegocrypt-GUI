# Stegocrypt-GUI
*Only PNG images are supported currently*

Tool for easily steganographically embedding AES-256 encrypted messages into images. 


![_image](https://github.com/Adri6336/Stegocrypt-GUI/blob/v-0.2.2/stegocrypt.png)


# Getting Started

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

**Windows**

- [Stegocrypt-GUI Windows Version 0.2.2](https://github.com/Adri6336/stegocrypt-gui_dl/raw/0.2.2/Stegocrypt-GUI_Win.zip)

There's an exe file included, but it may not work in some cases. A more reliable way to run stegocrypt is by downloading python 3, opening powershell
and running the command "pip install -r requirements.txt" in the directory where you downloaded stegocrypt, and then entering "python main.py".

1. Download the zip in the below link titled, "Stegocrypt-GUI Windows".
2. Extract the zip and open the new folder.
3. Follow the steps ennumerated in the ReadMe.txt within.

**Linux/UNIX (Ubuntu / Debian Based)**

- [Stegocrypt-GUI Linux Version 0.2.2](https://github.com/Adri6336/stegocrypt-gui_dl/raw/0.2.2/Stegocrypt-GUI-Lin.tar.gz)

First you will need tkinter and pip installed. To do this, enter the command "sudo apt install python3-pip python3-tk". Once this is done, 
you can either manually install the requirements.txt modules or you can run the start-stegocryptgui script that will do it for you. To do it manually,
use the command, "pip3 install -r requirements.txt"


1. Download the tar.gz file in the below link titled, "Stegocrypt-GUI Linux".
2. Extract the tar.gz file, then open the terminal within the newly created folder.
3. enter the command "chmod +x start-stegocryptgui;./start-stegocryptgui" or "python3 main.py" (if you've downloaded the requirements txt)






# Version 0.2.2 Changelog

- Made the terminal output more intelligible / useful
- Did some other stuff a while ago that made it better, but forgot to make a note of the changes :p. Just take my word for it that this version is better.
- Deleted useless code from script.
- Deleted unnecessary code that limited the randomness of password generation.


-------------------------

Note: Memes are inconspicuous, so they're the perfect vessel for secret messages (just saying, lol).

Note 2: You'll need to ensure that the image is not compressed when sending it to your recipient. Email attachments are usually good for this.

Note 3: Example picture's password is "Securepassword1!", without the quotation marks
