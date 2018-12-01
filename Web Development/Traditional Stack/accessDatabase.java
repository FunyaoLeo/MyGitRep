/***
 * File        : accessDatabase.java
 * Description : Simple program to illustrate concepts in tutorial
 */

import java.sql.*;

public class accessDatabase {
    public static void main(String[] args) 
    {
        /* load the driver */
        try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException ex) {
            System.out.println(ex);
            return;
        }
    
        Connection c = null;
        Statement  s = null; 
        ResultSet rs = null; 

        try {
            String bar, beer ;
            float price ;
    
            /* create an instance of a Connection object */
            c = DriverManager.getConnection("jdbc:mysql://localhost:3306/CS144", "cs144", ""); 
			
			/* You can think of a JDBC Statement object as a channel
			sitting on a connection, and passing one or more of your
			SQL statements (which you ask it to execute) to the DBMS*/

            s = c.createStatement() ;

            s.executeUpdate("DROP TABLE IF EXISTS Sells" ) ;
            s.executeUpdate("CREATE TABLE Sells(bar VARCHAR(40), beer VARCHAR(40), price REAL)" ) ;
            s.executeUpdate("INSERT INTO Sells VALUES('Bar Of Foo', 'BudLite', 2.00)") ;

            rs = s.executeQuery("SELECT * FROM Sells") ;
            while( rs.next() ){
                 bar = rs.getString("bar");
                 beer = rs.getString("beer");
                 price = rs.getFloat("price");
                 System.out.println(bar + " sells " + beer + " for " + price + " dollars.");
            }
        } catch (SQLException ex){
            System.out.println("SQLException caught");
            System.out.println("---");
            while ( ex != null ) {
                System.out.println("Message   : " + ex.getMessage());
                System.out.println("SQLState  : " + ex.getSQLState());
                System.out.println("ErrorCode : " + ex.getErrorCode());
                System.out.println("---");
                ex = ex.getNextException();
            }
        } finally {
            try { rs.close(); } catch (Exception e) { /* ignored */ }
            try { s.close(); } catch (Exception e) { /* ignored */ }
            try { c.close(); } catch (Exception e) { /* ignored */ }
        }
    }
}
