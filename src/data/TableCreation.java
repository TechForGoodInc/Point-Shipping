package data;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class TableCreation {

	public void makeTable() {
		Connection con = null;

		DataProcess sqlcon = new DataProcess();

		System.out.println(sqlcon.connecting());// <-return a string with connection info

		Statement state = null;// <-object needed to execute the query
		try {
			// Query to create a table
			String dataQuery = "create table testingTable(ID SERIAL primary key,productName varchar(200),price double precision)";
			state = sqlcon.connecting().createStatement();
			state.executeUpdate(dataQuery);
			System.out.println("Table created successfully!");
		} catch (SQLException e) {

			e.printStackTrace();
			System.out.println(e);
		}
	}

	

}
