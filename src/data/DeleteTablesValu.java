package data;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class DeleteTablesValu {
	/**
	 * A row will be deleted by specifying the ID which is the primary key.
	 */
	public void DeleteValues() {
		Connection con = null;
		DataProcess sqlcon = new DataProcess();
		Statement state = null;

		try {
			String dQuery = "delete from testingTable where ID='1' ";
			state = sqlcon.connecting().createStatement();
			state.executeUpdate(dQuery);
			System.out.println("Value deleted!");
		} catch (SQLException e) {

			e.printStackTrace();
			System.out.println(e);
		}

	}

}
