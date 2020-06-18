package data;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DataProcess {

	private final String url = "jdbc:postgresql://localhost:5432/postgres";
	private final String user = "postgres";
	private final String password = "data";
/**
 * this method will confirm that you have or have not connected to database
 * @return
 * @throws SQLException
 */
	public Connection connecting()  {
		Connection con=null;
		
		 try {
			con = DriverManager.getConnection(url, user, password);
		} catch (SQLException e) {
			
			e.printStackTrace();
		}
			
			if (con != null) {
				 
				System.out.println("Connected to PostgreSQL");
				
			} else {
			
				System.out.println("Connection Failed!");
			
			}

		return con;
	}


}
