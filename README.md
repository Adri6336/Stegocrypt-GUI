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

# Setting up Stegocrypt-GUI

1. Download the "--Win.zip" file for Windows or the "--Lin.tar.gz" file for Linux.
2. Extract contents.
3. On Windows, run the "Stegocrypt-GUI.exe" file found within. On Linux, execute the "start-stegocryptgui" script found within.

# Version 0.2 Changelog

- Stegocrypt-GUI now creates the directories and files it needs (except Go-derived exe) upon runtime.
- Fixed incorrect password decryption notification. Used to say 'decryption successful', now indicates that it actually failed.
- Made the script able to run on both Linux and Windows without forcing me to modify the script.


-------------------------

Note: Memes are inconspicuous, so they're the perfect vessel for secret messages (just saying, lol).

Note 2: You'll need to ensure that the image is not compressed when sending it to your recipient. Email attachments are usually good for this.

Note 3: Example picture's password is Securepassword1!
