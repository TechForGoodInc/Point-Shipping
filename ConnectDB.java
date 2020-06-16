package com.emilylouden.com;

import java.sql.Connection;
import java.sql.DriverManager;

public class ConnectDB {

	public Connection get_connection() {

		Connection connection = null;

		try {
			Class.forName("org.postgresql.Driver");
			connection = DriverManager.getConnection("jdbc:postgresql://localhost:5432/emilylouden", "postgres",
					"root");

			if (connection != null) {
				System.out.println("Connection successful");
			} else {
				System.out.println("Connection...not good");
			}

		} catch (Exception e) {
			e.printStackTrace();
		}

		return connection;
	}
}
