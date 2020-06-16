package com.emilylouden.com;

import java.sql.Connection;
import java.sql.Statement;

public class Create_Table {
	public static void create_table() {

		Connection connection = null;
		Statement statement = null;

		ConnectDB connect_obj = new ConnectDB();

		connection = connect_obj.get_connection();

		try {
			
			String query = "Create Table appUsers(ID int, LastName varchar, FirstName varchar, Address varchar, Password varchar)";
			statement = connection.createStatement();
			statement.executeUpdate(query);
			System.out.println("done and done!");
			statement.close();
			connection.close();
			

		} catch (Exception e) {
			System.err.println(e.getClass().getName() + ": " + e.getMessage());

		}
	}
}
