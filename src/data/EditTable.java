package data;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class EditTable {
	/**
	 * this method will make changes to the table, based on your preference.
	 */
	public void editTheTabl() {

		Connection con = null;
		DataProcess sqlcon = new DataProcess();
		Statement state = null;

		try {
			String dQuery = "update testingTable set productName='Iphone XR Max 10',price='749.99' where ID='1' ";
			state = sqlcon.connecting().createStatement();
			state.executeUpdate(dQuery);
			System.out.println("Changes Saved!");
		} catch (SQLException e) {

			e.printStackTrace();
			System.out.println(e);
		}
	}

}
