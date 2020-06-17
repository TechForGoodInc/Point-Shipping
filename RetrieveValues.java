package com.emilylouden.com;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class RetrieveValues {

	public String[] retrieve_user(int userId) {
		Connection connection = null;
		Statement statement = null;

		ConnectDB obj_ConnectDB = new ConnectDB();

		connection = obj_ConnectDB.get_connection();

		int id = -1;
		String lastName = null, firstName = null, address = null;

		try {
			statement = connection.createStatement();

			String query = "SELECT * FROM appUsers WHERE ID=" + userId;
			ResultSet rs = statement.executeQuery(query);
			while (rs.next()) {
				id = rs.getInt("ID");
				lastName = rs.getString("LastName");
				firstName = rs.getString("FirstName");
				address = rs.getString("Address");
				// System.out.println(id + "\t" + lastName + ",\t" + firstName + "\t" + address
				// + "\t" + password);

			}

		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if (statement != null) {
				try {
					statement.close();
				} catch (SQLException e) {
					e.printStackTrace();
				}
			}
		}
		// will return id = -1 and String null values if try block is unsuccessful
		String[] return_list = { Integer.toString(id), lastName, firstName, address };
		return return_list;
	}
	
	public String[] retrieve_packages(int userId) {
		Connection connection = null;
		Statement statement = null;

		ConnectDB obj_ConnectDB = new ConnectDB();

		connection = obj_ConnectDB.get_connection();

		int id = -1;
		float cost = -1;
		String destination = null, origin = null;

		try {
			statement = connection.createStatement();

			String query = "SELECT * FROM packages WHERE userId=" + userId;
			ResultSet rs = statement.executeQuery(query);
			while (rs.next()) {
				id = rs.getInt("UserId");
				cost = rs.getFloat("Cost");
				destination = rs.getString("Destination");
				origin = rs.getString("Origin");
				// System.out.println(id + "\t" + lastName + ",\t" + firstName + "\t" + address
				// + "\t" + password);

			}

		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if (statement != null) {
				try {
					statement.close();
				} catch (SQLException e) {
					e.printStackTrace();
				}
			}
		}
		// will return id = -1 and String null values if try block is unsuccessful
		String[] return_list = { Integer.toString(id), Float.toString(cost), destination, origin };
		return return_list;
	}
}
