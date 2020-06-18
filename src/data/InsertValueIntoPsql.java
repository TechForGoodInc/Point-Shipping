package data;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class InsertValueIntoPsql {

	public void insertValue() {
		Connection con = null;
		DataProcess sqlcon = new DataProcess();
		Statement state = null;

		try {

			String dQuery = "insert into testingTable(productName,price) values('Iphone 11',999.99)";// <-These values
																										// will inserted
																										// in the table

			state = sqlcon.connecting().createStatement();
			state.executeUpdate(dQuery);
			System.out.println("Your database is updated!");
		} catch (SQLException e) {

			e.printStackTrace();
			System.out.println(e);
		}

	}

}
