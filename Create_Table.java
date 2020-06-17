package com.emilylouden.com;

import java.sql.Connection;
import java.sql.Statement;

public class Create_Table {
	public static void create_table(String table_type) {

		Connection connection = null;
		Statement statement = null;

		ConnectDB connect_obj = new ConnectDB();

		connection = connect_obj.get_connection();

		try {
			String query;
			if (table_type.contentEquals("users")) {
				query = "Create Table appUsers(ID int, LastName varchar, FirstName varchar, Address varchar, Password varchar)";
			} else if (table_type.contentEquals("packages")) {
				query = "Create Table packages(UserId int, Cost float, Destination varchar, Origin varchar)";
			} else {
				return;
			}
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
