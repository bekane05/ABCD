import java.sql.*;

public class Model {
	
	private String username, password;
	
	/**
	 * Constructor
	 * @param username
	 * @param password
	 * 
	 * Preconditions: username is a string (not null) and has permission to access the desired database
	 * 				  password is a string and is the correct password for user "username"
	 */
	public Model(String username, String password) {
		this.username = username;
		this.password = password;
	}
	
	/**
	 * Function to try to establish connection to the database
	 */
	public Connection getConnection() {
		
		// Attempts to get this jdbc driver
		try {
			Class.forName("com.mysql.jdbc.Driver").newInstance();
		} catch (InstantiationException e) {
			System.out.println("Error: Could not get new instance of jdbc Driver.");
			return null;
		} catch (IllegalAccessException e) {
			System.out.println("Error: Could not get new instance of jdbc Driver.");
			return null;
		} catch (ClassNotFoundException e) {
			System.out.println("Error: Could not get new instance of jdbc Driver.");
			return null;
		}
		
		String host = "jdbc:MySQL://csdb.stlawu.local";
		String userpass = "user=" + this.username + "&password=" + this.password;
		String db = "cs348";
		
		// Attempts to connect to the database "db"
		try {
			Connection c = DriverManager.getConnection(host + "/" + db + "?" + userpass);
			return c;
		} catch (SQLException e) { // Passes null back to controller for invalid username/password combinations or other connectivity errors
			return null;
		}
	}
	
	/**
	 * Function to execute user-given query on the database
	 * @param c
	 * @param query
	 * @returns a ResultSet answer
	 * @throws SQLException
	 * 
	 * Preconditions: a Connection c was successfully established prior to function call
	 * 				  query is a string and a valid MySQL database query
	 */
	public ResultSet query(Connection c, String query) throws SQLException {
		
		// Attempts to process the user-entered query
		try {
			Statement s = c.createStatement();
			ResultSet answer = s.executeQuery(query);
			return answer;
		} catch (SQLException e) { // Passes null back to the controller for invalid query
			return null;
		}
	}
}