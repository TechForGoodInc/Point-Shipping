package com.emilylouden.com;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

public class Password_Validation {

	Connection con;
	Statement statement;
	private String database_password;
	private final String decryption_key = "kittens";

	private void database_password(int ID) {

		String password;

		try {

			ConnectDB obj_ConnectDB = new ConnectDB();
			con = obj_ConnectDB.get_connection();
			statement = con.createStatement();
			String query = "SELECT * FROM appUsers WHERE ID =" + ID;
			ResultSet rs = statement.executeQuery(query);

			if (rs.next()) {
				password = rs.getString("Password");
				database_password = PasswordEncryption.decrypt(password, decryption_key);
			}

			else {
				System.err.println("User could not be found");
			}

		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	public boolean check_password(int ID, String password_input) {
		// get user ID and password
		database_password(ID);
		return password_input.equals(database_password);
	}

}
