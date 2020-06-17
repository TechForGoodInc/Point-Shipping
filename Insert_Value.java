package com.emilylouden.com;

import java.sql.Connection;
import java.sql.Statement;

public class Insert_Value {
	private final String encryption_key = "kittens";
	
	public void insert_user(int ID, String lastName, String firstName, String address, String password) {
		Connection connection = null;
		Statement statement = null;

		ConnectDB obj_ConnectDB = new ConnectDB();

		connection = obj_ConnectDB.get_connection();
		
		String encrypted_password = PasswordEncryption.encrypt(password, encryption_key);

		try {
			String query = "insert into appUsers(ID,LastName,FirstName,Address,Password) values('" + ID + "\', \'"
					+ lastName + "\', \'" + firstName + "\', \'" + address + "\', \'" + encrypted_password + "\')";
			statement = connection.createStatement();
			statement.executeUpdate(query);
			System.out.println("finalized table update");

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public void insert_package(int userID, float cost, String destination, String origin) {
		Statement statement = null;

		ConnectDB obj_ConnectDB = new ConnectDB();

		Connection connection = obj_ConnectDB.get_connection();
		
		try {
			String query = "insert into appUsers(UserId,Cost,Destination,Origin) values('" + userID + "\', \'"
					+ cost + "\', \'" + destination + "\', \'" + origin + "\')";
			statement = connection.createStatement();
			statement.executeUpdate(query);
			System.out.println("finalized table update");

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
