import java.io.IOException;
import java.sql.* ;
import java.util.List;
import java.util.ArrayList;
import java.util.Date;
import java.text.SimpleDateFormat;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.servlet.Servlet;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.sql.DataSource;

import org.commonmark.node.*;
import org.commonmark.parser.Parser;
import org.commonmark.renderer.html.HtmlRenderer;

/**
 * Servlet implementation class for Servlet: ConfigurationTest
 *
 */
public class Editor extends HttpServlet {
    /**
     * The Servlet constructor
     * 
     * @see javax.servlet.http.HttpServlet#HttpServlet()
     */
	private String dbUsername;
	private String dbPassword;

    public Editor() {
		dbUsername = "cs144";
		dbPassword = "";
	}

    public void init() throws ServletException
    {
        /*  write any servlet initialization code here or remove this function */
		System.out.println("Entering init....\n\n");
		try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException ex) {
            System.out.println(ex);
            return;
        }
    }
    

    /**
     * Handles HTTP GET requests
     * 
     * @see javax.servlet.http.HttpServlet#doGet(HttpServletRequest request,
     *      HttpServletResponse response)
     */
    public void doGet(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException 
    {
	// implement your GET method handling code here
	// currently we simply show the page generated by "edit.jsp"
		String action = request.getParameter("action");
		checkInput(action, request, response);
		if(action.equals("list")){
			doList(request, response);
		}
		else if(action.equals("preview")){
			doPreview(request, response);
		}
		else if(action.equals("open")){
			doOpen(request, response);
		}
    }
    
    /**
     * Handles HTTP POST requests
     * 
     * @see javax.servlet.http.HttpServlet#doPost(HttpServletRequest request,
     *      HttpServletResponse response)
     */
    public void doPost(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException 
    {
	// implement your POST method handling code here
	// currently we simply show the page generated by "edit.jsp"
		String action = request.getParameter("action");
		checkInput(action, request, response);
		if(action.equals("save")){
			doSave(request, response);
		}
		else if(action.equals("preview")){
			doPreview(request, response);
		}
		else if(action.equals("delete")){
			doDelete(request, response);
		}
		else if(action.equals("open")){
			doOpen(request, response);
		}
		else if(action.equals("list")){
			doList(request, response);
		}
    }
	
	/**
     * Corresponding steps if the action is "save"
     */
	public void doSave(HttpServletRequest request, HttpServletResponse response)
		throws ServletException, IOException
	{
		// variable declaration
		int postid = 0;
		boolean insert = true;
		String title = null;
		String body = null;
		String username = null;
		String postidStr = null;
		Timestamp timestamp = null;
		Timestamp created = null;
		Timestamp modified = null;
		Connection con = null;
		ResultSet rs = null;
		PreparedStatement pStmtGetId = null;
		PreparedStatement pStmtIst = null;
		PreparedStatement pStmtUpdt = null;
		PreparedStatement pStmtSltById = null;
		
		// database connection
		try{
			con = DriverManager.getConnection("jdbc:mysql://localhost:3306/CS144", dbUsername, dbPassword);
			pStmtGetId = con.prepareStatement(
				"select max(postid) as postid from Posts where username = ?;"
			);
			pStmtIst = con.prepareStatement(
				"insert into Posts (username, postid, title, body, modified, created) values (?, ?, ?, ?, ?, ?);"
			);
			pStmtUpdt = con.prepareStatement(
				"update Posts set title = ?, body = ?, modified = ? WHERE username = ? AND postid = ?;"
			);
			pStmtSltById = con.prepareStatement(
				"select *  from Posts where username = ? and postid = ?;"
			);
		
			// retrieve data and input check for "save"
			postidStr = request.getParameter("postid");
			checkPostId(postidStr,request,response);
			username = request.getParameter("username");
			checkUsername(username,request,response);
			postid = Integer.parseInt(postidStr);
			title = request.getParameter("title");
			checkTitle(title,request,response);
			body = request.getParameter("body");
			created = new Timestamp(System.currentTimeMillis());
			modified = created;
			
			// check if this is a updating blog or new blog and take corresponding actions
			if(postid<=0){
				pStmtGetId.setString(1, username);
				rs = pStmtGetId.executeQuery();
				while(rs.next()){
					postid = rs.getInt("postid");
					System.out.println(postid);
				}
				postid += 1;
			}
			else{
				insert = false;
			}
			
			if(insert){
				pStmtIst.setString(1, username);
				pStmtIst.setInt(2, postid);
				pStmtIst.setString(3, title);
				pStmtIst.setString(4, body);
				pStmtIst.setTimestamp(5, created);
				pStmtIst.setTimestamp(6, modified);
				int n = pStmtIst.executeUpdate();
			}
			else{
				pStmtSltById.setString(1, username);
				pStmtSltById.setInt(2, postid);
				rs = pStmtSltById.executeQuery();
				// if postid+username combination exists in database, update. Otherwise, leave it there
				if(rs.next()){
					pStmtUpdt.setString(1, title);
					pStmtUpdt.setString(2, body);
					pStmtUpdt.setTimestamp(3, modified);
					pStmtUpdt.setString(4, username);
					pStmtUpdt.setInt(5, postid);
					int n = pStmtUpdt.executeUpdate();
				}
			}
		}catch (SQLException ex){
            System.out.println("SQLException caught");
            System.out.println("---");
            while ( ex != null ) {
                System.out.println("Message   : " + ex.getMessage());
                System.out.println("SQLState  : " + ex.getSQLState());
                System.out.println("ErrorCode : " + ex.getErrorCode());
                System.out.println("---");
                ex = ex.getNextException();
            }
		}finally{
			try { 
				if(rs!=null)
					rs.close(); 
			} catch (Exception e) { /* ignored */ }
			try {
				if(pStmtGetId!=null)
					pStmtGetId.close();
				if(pStmtIst!=null)
					pStmtIst.close(); 
				if(pStmtUpdt!=null)
					pStmtUpdt.close();
				if(pStmtSltById!=null)
					pStmtSltById.close();
			} catch (Exception e) { /* ignored */ }
			try {
				if(con!=null)
					con.close(); 
			} catch (Exception e) { /* ignored */ }
		}
		
		response.sendRedirect(request.getContextPath() + "/post?action=list&username=" + username);
	}
	
	/**
     * Corresponding steps if the action is "preview"
     */
	public void doPreview(HttpServletRequest request, HttpServletResponse response)
		throws ServletException, IOException
	{
		Parser parser = Parser.builder().build();
		HtmlRenderer renderer = HtmlRenderer.builder().build();
		String titleOfHtml = renderer.render(parser.parse(request.getParameter("title")));
		String bodyOfHtml = renderer.render(parser.parse(request.getParameter("body")));
		
		request.setAttribute("titleOfHtml", titleOfHtml);
		request.setAttribute("bodyOfHtml", bodyOfHtml);
		request.setAttribute("title", request.getParameter("title"));
		request.setAttribute("body", request.getParameter("body"));
		
		request.getRequestDispatcher("/preview.jsp").forward(request, response);
	}
	
	/**
     * Corresponding steps if the action is "list"
     */
	public void doList(HttpServletRequest request, HttpServletResponse response) 
		throws ServletException, IOException
	{
		// variable declaration
		int postid = 0;
		String title = null;
		String body = null;
		String username = null;
		ArrayList<Object> eachPost = null;
		ArrayList<ArrayList<Object>> postList = new ArrayList<>();
		Timestamp created = null;
		Timestamp modified = null;
		Connection con = null;
		ResultSet rs = null;
		PreparedStatement pStmtSlt = null;
		SimpleDateFormat dateFormat = new SimpleDateFormat("MM/dd/yyyy' 'HH:mm:ss");
		
		// database connection
		try{
			con = DriverManager.getConnection("jdbc:mysql://localhost:3306/CS144", dbUsername, dbPassword);
			pStmtSlt = con.prepareStatement(
				"select * from Posts where username = ? order by postid;"
			);
			
			// retrieve data and input check for action "list"
			username = request.getParameter("username");
            checkUsername(username,request,response);
			
			// query database and looking for posts
			pStmtSlt.setString(1, username);
			rs = pStmtSlt.executeQuery();
			while (rs.next()) {
				eachPost = new ArrayList<>();
				postid = rs.getInt("postid");
				title = rs.getString("title");
				created = rs.getTimestamp("created");
				modified = rs.getTimestamp("modified");
				
				eachPost.add(title);
				eachPost.add(dateFormat.format(created));
				eachPost.add(dateFormat.format(modified));
				eachPost.add(postid);
				postList.add(eachPost);
			}
			request.setAttribute("postList", postList);
		}catch (SQLException ex){
			System.out.println("SQLException caught");
			System.out.println("---");
			while ( ex != null ) {
				System.out.println("Message   : " + ex.getMessage());
				System.out.println("SQLState  : " + ex.getSQLState());
				System.out.println("ErrorCode : " + ex.getErrorCode());
				System.out.println("---");
				ex = ex.getNextException();
			}
		}finally{
			try { 
			if(rs!=null)
			rs.close(); 
			} catch (Exception e) { /* ignored */ }
			try {
				if(pStmtSlt!=null)
					pStmtSlt.close();
			} catch (Exception e) { /* ignored */ }
			try {
				if(con!=null)
					con.close(); 
			} catch (Exception e) { /* ignored */ }
		}
			
		request.getRequestDispatcher("/list.jsp").forward(request, response);
	}
	
	/**
     * Corresponding steps if the action is "delete"
     */
	public void doDelete(HttpServletRequest request, HttpServletResponse response) 
		throws ServletException, IOException
	{
		// variable declaration
		int postid = 0;
		String title = null;
		String body = null;
		String username = null;
		String postidStr = null;
		Timestamp timestamp = null;
		Timestamp created = null;
		Timestamp modified = null;
		Connection con = null;
		PreparedStatement pStmtDelt = null;
		
		// database connection
		try{
			con = DriverManager.getConnection("jdbc:mysql://localhost:3306/CS144", dbUsername, dbPassword);
			pStmtDelt = con.prepareStatement(
				"delete from Posts where username = ? and postid = ?;"
			);
			
			// retrieve data and input check for action "delete"
			postidStr=request.getParameter("postid");
			checkPostId(postidStr,request,response);
			postid = Integer.parseInt(postidStr);
			username = request.getParameter("username");
			
			// delete corresponding posts from the database
			if(postid>0){
				pStmtDelt.setString(1, username);
				pStmtDelt.setInt(2, postid);
				int n = pStmtDelt.executeUpdate();
			}
			
		}catch (SQLException ex){
			System.out.println("SQLException caught");
			System.out.println("---");
			while ( ex != null ) {
				System.out.println("Message   : " + ex.getMessage());
				System.out.println("SQLState  : " + ex.getSQLState());
				System.out.println("ErrorCode : " + ex.getErrorCode());
				System.out.println("---");
				ex = ex.getNextException();
			}
		}finally{
			try {
				if(pStmtDelt!=null)
					pStmtDelt.close(); 
			} catch (Exception e) { /* ignored */ }
			try {
				if(con!=null)
					con.close(); 
			} catch (Exception e) { /* ignored */ }
		}
		
		response.sendRedirect(request.getContextPath() + "/post?action=list&username=" + username);
	}
	
	/**
     * Corresponding steps if the action is "open"
     */
	public void doOpen(HttpServletRequest request, HttpServletResponse response)
		throws ServletException, IOException
	{
		// variable declaration
		int postid = 0;
		String title = null;
		String body = null;
		String username = null;
		String postidStr = null;
		Connection con = null;
		ResultSet rs = null;
		PreparedStatement pStmtSltById = null;
		
		// database connection
		try{
			con = DriverManager.getConnection("jdbc:mysql://localhost:3306/CS144", dbUsername, dbPassword);
			pStmtSltById = con.prepareStatement(
				"select *  from Posts where username = ? and postid = ?;"
			);
			
			// retrieve data and input check for action "open"
			username = request.getParameter("username");
            checkUsername(username,request,response);
            postidStr=request.getParameter("postid");
            checkPostId(postidStr,request,response);
			postid = Integer.parseInt(postidStr);
			
			// if both parameters don't exist, we can know that this page is redirected from List
			if(request.getParameter("title")==null&&request.getParameter("body")==null){
				// if postid is larger than 0, then an existing file has been opened
				if(postid>0){
					pStmtSltById.setString(1, username);
					pStmtSltById.setInt(2, postid);
					rs = pStmtSltById.executeQuery();
					if(rs.next()){
						title = rs.getString("title");
						body = rs.getString("body");
					}else{
                        String err_msg = "postid does't exist";
		                request.setAttribute("err_msg", err_msg);
						response.setStatus(404);
						request.getRequestDispatcher("/error.jsp").forward(request, response);
                    }
					request.setAttribute("title", title);
					request.setAttribute("body", body);
				}
			}
			// if one of the parameter exists, then this page is redirected from Preview
			// set the attribute to reopen the editor again
			else{
				if(request.getParameter("title")!=null){
                          checkTitle(request.getParameter("title"),request,response);
					request.setAttribute("title", request.getParameter("title"));
				}
				if(request.getParameter("body")!=null){
					request.setAttribute("body", request.getParameter("body"));
				}
			}
			
			
		}catch (SQLException ex){
			System.out.println("SQLException caught");
			System.out.println("---");
			while ( ex != null ) {
				System.out.println("Message   : " + ex.getMessage());
				System.out.println("SQLState  : " + ex.getSQLState());
				System.out.println("ErrorCode : " + ex.getErrorCode());
				System.out.println("---");
				ex = ex.getNextException();
			}
		}finally{
			try { 
				if(rs!=null)
					rs.close(); 
			} catch (Exception e) { /* ignored */ }
			try {
				
				if(pStmtSltById!=null)
					pStmtSltById.close(); 
			} catch (Exception e) { /* ignored */ }
			try {
				if(con!=null)
					con.close(); 
			} catch (Exception e) { /* ignored */ }
		}
		
		request.getRequestDispatcher("/edit.jsp").forward(request, response);
	}
	
	/**
     * Four input check functions
     */
	public void checkInput(String action, HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
        if(action.equals("open")||action.equals("")){
			if(request.getParameter("username")==null||request.getParameter("postid")==null){
				String err_msg = "missing input";
				request.setAttribute("err_msg", err_msg);
				response.setStatus(404);
				request.getRequestDispatcher("/error.jsp").forward(request, response);
			}
		}
		else if(action.equals("save")||action.equals("preview")){
			if(request.getParameter("username")==null||request.getParameter("postid")==null
				||request.getParameter("title")==null||request.getParameter("body")==null){
				String err_msg = "missing input";
				request.setAttribute("err_msg", err_msg);
				response.setStatus(404);
				request.getRequestDispatcher("/error.jsp").forward(request, response);
			}
		}
		else if(action.equals("list")){
			if(request.getParameter("username")==null){
				String err_msg = "missing input";
				request.setAttribute("err_msg", err_msg);
				response.setStatus(404);
				request.getRequestDispatcher("/error.jsp").forward(request, response);
			}
		}
		else{
			String err_msg = "invalid action";
			request.setAttribute("err_msg", err_msg);
			response.setStatus(404);
			request.getRequestDispatcher("/error.jsp").forward(request, response);
		}
    } 
	
    public void checkPostId(String postidStr, HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
        try{
            int postid=Integer.parseInt(postidStr);            
        }catch(NumberFormatException ex){
            String err_msg = ex.getMessage();
		    request.setAttribute("err_msg", err_msg);
			response.setStatus(400);
            request.getRequestDispatcher("/error.jsp").forward(request, response);
        }
    }
    public void checkUsername(String username, HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
        if(username!=null && username.length()>40){
            String err_msg = "username length more than 40";
			request.setAttribute("err_msg", err_msg);
			response.setStatus(400);
            request.getRequestDispatcher("/error.jsp").forward(request, response);
        }
        
    }
    public void checkTitle(String title, HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
	{
        if(title!=null && title.length()>100){
            String err_msg = "title length more than 100";
			request.setAttribute("err_msg", err_msg);
			response.setStatus(400);
            request.getRequestDispatcher("/error.jsp").forward(request, response);
        }
    }            
}

