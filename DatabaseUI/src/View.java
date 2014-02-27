import java.awt.*;

import javax.swing.*;
import javax.swing.table.*;

import java.sql.*;
import java.util.*;

public class View {
	
	/**
	 * Constructor (constructs a JTable from the table model given by the resultSetToTableModel method)
	 * @param answer
	 * 
	 * Precondition: answer is a valid ResultSet
	 */
	public View(ResultSet answer) {
		
		// For top-level window and border
		JFrame frame = new JFrame("Parts and Suppliers");
		
		
		JPanel panel = new JPanel();
		panel.setLayout(new BorderLayout());
		
		JTable table = new JTable();
		try {
			table.setModel(View.resultSetToTableModel(answer));
		} catch (SQLException e) {
			System.out.println("Error: Could not populate JTable.");
		}
		
		JScrollPane tableContainer = new JScrollPane(table);
		table.setFillsViewportHeight(true);
		
		panel.add(tableContainer, BorderLayout.CENTER);
		frame.getContentPane().add(panel);
		frame.pack();
		frame.setVisible(true);
	}
	
	/**
	 *  Method to take the ResultSet instance from the database query and build a table model
	 * @param answer
	 * @returns a new TableModel
	 * @throws SQLException
	 * 
	 * Precondition: a ResultSet answer was successfully obtained and answer is not null
	 */
	public static TableModel resultSetToTableModel(ResultSet answer) throws SQLException {
		
		try {
			// Get database metadata for displaying output
			ResultSetMetaData rsMetaData = answer.getMetaData();
			int numberOfColumns = rsMetaData.getColumnCount();
			
			// Set the column names
			Vector<String> columnNames = new Vector<String>();
			for (int i=1; i<=numberOfColumns; i++) {
				columnNames.add(rsMetaData.getColumnLabel(i));
			}
			
			// Populate the table with data
			Vector<Vector<Object>> rows = new Vector<Vector<Object>>();
			while (answer.next()) {
				Vector<Object> newRow = new Vector<Object>();
				for (int i=1; i<=numberOfColumns; i++) {
					newRow.add(answer.getObject(i));
				}
				rows.add(newRow);
			}
			return new DefaultTableModel(rows, columnNames);
			
		} catch (SQLException e) {
			System.out.println("Error: Could not retrieve ResultSet data.");
			return null;
		}
	}
}
