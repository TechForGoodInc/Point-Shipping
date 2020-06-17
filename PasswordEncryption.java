package com.emilylouden.com;

import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Base64;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class PasswordEncryption {

	private static SecretKeySpec secretKey;
	private static byte[] key;

	public static void setKey(String inputKey) {
		MessageDigest sha = null;
		try {
			// key is a byte array version of inputKey
			key = inputKey.getBytes("UTF-8");

			// clarifies we are using SHA-1 algorithm
			sha = MessageDigest.getInstance("SHA-1");

			// returns a hash code
			key = sha.digest(key);

			// pads key to make sure it is length 16
			key = Arrays.copyOf(key, 16);

			// creates secret key using AES algorithm
			secretKey = new SecretKeySpec(key, "AES");

		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
	}

	// input is the original string and the secret key needed to decrypt the file
	public static String encrypt(String strToEncrypt, String secret) {
		try {
			setKey(secret);

			// AES: algorithm, ECB: electronic code book divides string into blocks to
			// decipher, PKC: padding method
			Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");

			// encrypts key, encrypt_mode is a constant that initializes the cipher
			cipher.init(Cipher.ENCRYPT_MODE, secretKey);

			// turns the string into a byte array
			byte[] plainText = strToEncrypt.getBytes("UTF-8");

			// encrypts the byte array
			byte[] encryptedText = cipher.doFinal(plainText);

			// turns the byte array into a string
			String output = new String(encryptedText);

			return output;

		} catch (Exception e) {
			System.out.println("Error while encrypting: " + e.toString());
		}
		return null;
	}

	public static String decrypt(String strToDecrypt, String secret) {
		try {
			setKey(secret);
			Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5PADDING");
			System.out.println("1");
			cipher.init(Cipher.DECRYPT_MODE, secretKey);

			System.out.println("2");
			// turns the String object into a byte string object
			byte[] byteString = Base64.getMimeDecoder().decode(strToDecrypt.getBytes("UTF-8"));

			System.out.println("3");
			byte[] decrypted = cipher.doFinal(byteString);

			System.out.println("4");
			return new String(decrypted);
		} catch (Exception e) {
			System.out.println("Error while decrypting: " + e.toString());
		}
		return null;
	}

	public static void main(String[] args) {
		String encrypted = PasswordEncryption.encrypt("test string", "secret key");
		String decrypted = PasswordEncryption.decrypt(encrypted, "secret key");
		System.out.println(decrypted);

	}
}

// credit to https://howtodoinjava.com/security/java-aes-encryption-example/
