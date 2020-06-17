package com.emilylouden.com;

import java.sql.Connection;
import java.sql.Statement;

public class Insert_Value {
	private final String encryption_key = "kittens";
	
	public void insert_value(int ID, String lastName, String firstName, String address, String password) {
		Connection connection = null;
		Statement statement = null;
		PasswordEncryption encrypt = new PasswordEncryption();

		ConnectDB obj_ConnectDB = new ConnectDB();

		connection = obj_ConnectDB.get_connection();
		
		String encrypted_password = encrypt.encrypt(password, encryption_key);

		try {
			String query = "insert into appUsers(ID,LastName,FirstName,Address,Password) values('" + ID + "\', \'"
					+ lastName + "\', \'" + firstName + "\', \'" + address + "\', \'" + password + "\')";
			statement = connection.createStatement();
			statement.executeUpdate(query);
			System.out.println("finalized table update");

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
