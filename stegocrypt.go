// This will handle the encryption and decryption of text provided by the Python GUI

// Will encode text given to it with the switch -e (encrypt) by recieving text,
// encrypting with AES, then converting it to base64 and returning it to Python
// for embedding into an image.

// Will decode text given to it with the switch -d (decrypt) by recieving base64,
// decoding the base64, decrypting the text, and returing the text to Python

package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
	"io"
	"io/ioutil"
	"os"
)

func main() {
	// Syntax: stegocryptgo <-e/-d> <password>

	// 1. Get the total arguments and reject if invalid
	argLen := len(os.Args[1:])

	if argLen == 1 && os.Args[1] == "-h" { // If -h, tell about switches
		fmt.Println("Syntax: stegocryptgo <-e/-d> <password>\n")
		fmt.Println("-e  -> Encrypt\n-d  -> Decrypt")
		fmt.Println("\nPlease use from within Stegocrypt-GUI or another app")
		return
	}

	if argLen < 2 {
		fmt.Println("Syntax: stegocryptgo <-e/-d> <password>\nPlease use from within Stegocrypt-GUI or another app")
		return
	}

	if os.Args[1] == "-e" { // If -e switch, encrypt
		encrypt()

	} else if os.Args[1] == "-d" { // If -d switch, decrypt
		decrypt()

	}

}

/*
==============================================
== Main Functions ============================
==============================================
-> These will handle encryption and decryption
CONTENTS:
	I. decrypt() -> this will decrypt base64 encoded AES ciphertext
	II. encrypt() -> this will encrypt plaintext into base64 encoded AES ciphertext

*/

func decrypt() {
	/*
		This will decrypt text derived from base64 encoding
	*/

	// 1. Get info to work with
	b64Text := readFile("./Data/Messages/2.scg")

	// 2. Decode base64 info
	decoded, err := base64.StdEncoding.DecodeString(b64Text)

	if err != nil {
		os.WriteFile("./Data/Messages/ERROR.log", []byte(err.Error()), 0755)
		return
	}

	decoded = []byte(decoded)

	// 3. Decrypt info using password digest
	password := passwordHash(os.Args[2])

	// 3.1 Instantiate cipher
	ciph, err := aes.NewCipher(password)

	if err != nil {
		fmt.Println(err)
	}

	gcm, err := cipher.NewGCM(ciph)
	if err != nil {
		fmt.Println(err)
	}

	nonceSize := gcm.NonceSize()
	if len(decoded) < nonceSize {
		fmt.Println(err)
	}

	nonce, ciphertext := decoded[:nonceSize], decoded[nonceSize:]

	// 3.2 Decrypt
	plainText, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		fmt.Println(err)
        	os.WriteFile("./Data/Messages/ERROR.log", []byte(err.Error()), 0755)
	}

	// 4. Save info to 1.scg
	saveData(string(plainText), false)

}

func encrypt() {
	/*
		This will encrypt plaintext from messages folder
	*/

	// 1. Get info to work with (Python will write to the file first)
	plainText := []byte(readFile("./Data/Messages/1.scg")) // Windows path, swap for linux

	// 2. Encrypt info using password digest
	password := passwordHash(os.Args[2])

	// 2.1 Setup cipher
	ciph, err := aes.NewCipher(password) // Passes in a sha256 digest to use AES-256

	if err != nil {
		return
	}

	gcm, err := cipher.NewGCM(ciph)

	if err != nil {
		return
	}

	nonce := make([]byte, gcm.NonceSize())

	if _, err = io.ReadFull(rand.Reader, nonce); err != nil {
		return
	}

	// 2.3 Encrypt text
	encrypted := gcm.Seal(nonce, nonce, plainText, nil)

	// 3. Convert encrypted info to base64
	encoded := base64.StdEncoding.EncodeToString(encrypted)

	// 4. Save info to 1.scg
	saveData(encoded, true)

}

/*
==============================================
== Supporting Functions ======================
==============================================
-> These will assist the main functions.
CONTENTS:
	I. readFIle(path str) str -> get file contents as str
	II. saveData(content str, encrypt bool) -> save output of main functions
	III. passwordHash(password str) []byte -> converts a password into a sha256 digest

*/

func readFile(path string) string {
	/*
	 This will get the contents of a file and return it as a string

	 :Param path: This contains the pathway to the desired file
	 :Return: Returns the file's data as a string

	*/
	data, err := ioutil.ReadFile(path)

	if err != nil {
		return err.Error() // If something goes wrong, return the error info
	} else {
		return string(data)
	}
}

func saveData(content string, encrypt bool) {
	/*
		This will save info to a file

		:Param content: This contains the info that we're going to pass into the file
		:Param encrypt: If true, save to 2.scg; else, save to 1.scg
	*/

	// 1. Determine if encryption or decryption
	var path string

	if encrypt {
		path = "./Data/Messages/2.scg"

	} else if !encrypt {
		path = "./Data/Messages/1.scg"
	}

	// 2. Convert content to bytes and write to file
	data := []byte(content)

	err := os.WriteFile(path, data, 0755)

	if err != nil {
		os.WriteFile("./Data/Messages/ERROR.log", []byte(err.Error()), 0755)
	}
}

func passwordHash(password string) []byte {
	/*
		 This converts a given password into a SHA-256 digest

		:Param password: This is the string that will be used as a password
		:Return: Returns the sha256 digest of password to satisfy AES requirement
	*/
	hash := sha256.New()
	hash.Write([]byte(password))

	return hash.Sum(nil)

}
