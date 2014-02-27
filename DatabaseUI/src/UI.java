import java.io.*;
import java.sql.*;
import java.util.*;
import java.util.regex.*;

public class UI {

	public static void main(String[] args) throws Exception {
		
		Scanner u = new Scanner(System.in);
		System.out.print("Username: ");
		String user = u.nextLine();
		
		// Mask password typed into the command line
		Console cons = System.console();
		System.out.print("Password: ");
		char[] password = cons.readPassword();
		
		// Convert password from char array to string
		String pass = new String(password);
		
		// Creates a new model object to connect to/retrieve information from the database
		Model m = new Model(user, pass);
		Connection c = m.getConnection();
		
		// Checks for proper database connection via correct a username/password combination
		while (c == null) {
			System.out.println("Error: Could not establish connection to database.");
			u = new Scanner(System.in);
			System.out.print("Username: ");
			user = u.nextLine();
			
			cons = System.console();
			System.out.print("Password: ");
			password = cons.readPassword();
			
			pass = new String(password);
			
			m = new Model(user, pass);
			c = m.getConnection();
		}
		
		// Initial command prompt
		System.out.print("ps> ");
		Scanner q = new Scanner(System.in);
		String query = q.nextLine();
		
		// Repeated user input
		while (!query.equalsIgnoreCase("quit")) {
			
			// Gets user-entered database query
			ResultSet answer = m.query(c, query);
			
			// Regex pattern to error check user-entered query
			Pattern pattern = Pattern.compile("^select.*;$");
			Matcher matcher = pattern.matcher(query);
			
			// While query does not match the patter or query is invalid, ask for new query
			while (!matcher.matches() || answer == null) {
				System.out.println("Error: Invalid database query.");
				System.out.print("ps> ");
				q = new Scanner(System.in);
				query = q.nextLine();
				matcher = pattern.matcher(query);
				answer = m.query(c, query);
			}
			
			// Creates a new view object to populate and display a JTable
			View v = new View(answer);
				
			// Command line prompt
			System.out.print("ps> ");
			q = new Scanner(System.in);
			query = q.nextLine();
		}
		
		// To quit
		if (query.equalsIgnoreCase("quit")) {
			System.exit(0);
		}
	}
}
