# Stegocrypt-GUI
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

Note: The code here is out of date. I've fixed its main issue and will be uploading a working version shortly. My solution: use Go for the encrypting and decrypting. You'll have a plaintext file created on your computer, but this shouldn't be an issue unless you've been hacked. The point of Stegocrypt-GUI is to enable you to covertly send encrypted messages using images.

Note 2: Memes are inconspicuous, so they're the perfect vessel for secret messages (just saying, lol).

Note 3: You'll need to ensure that the image is not compressed when sending it to your recipient. Email attachments are usually good for this.

Note 4: Example picture's password is Securepassword1!
