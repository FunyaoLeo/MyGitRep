<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%><%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>Post Preview</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">

		<style>
			body{
				font-family:"Arial";
			}
			
			h1{
				font-size: 30pt;
				color:white;
				background-color: skyblue;
			}
			
			button{
				background-color: black;
				border: none;
				display: block;
				color: white;
				text-align: center;
				padding: 8px 28px;
				cursor: pointer;
			}
		</style>

	</head>
	<body>
		<h1>Preview Post</h1>
		<h3><%= request.getAttribute("titleOfHtml") %></h3><br>
		<%= request.getAttribute("bodyOfHtml") %><br>
		<form action="post" method="post">
			<input type="hidden" name="username" value='<%= request.getParameter("username") %>'/>
			<input type="hidden" name="postid" value='<%= request.getParameter("postid") %>'/>
			<input type="hidden" name="title" value='<%= request.getAttribute("title") %>'>
			<input type="hidden" name="body" value='<%= request.getAttribute("body") %>'><br>
			<button type="submit" name="action" value="open">Close Preview</button>
			<br>
		</form>
	</body>
</html>