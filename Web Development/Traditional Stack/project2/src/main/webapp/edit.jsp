<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%><%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>Edit Post</title>
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

			ul {
				list-style-type: none;
				margin: 0;
				padding: 0;
				overflow: hidden;
				background-color: #333;
			}

			textarea{
				width: calc(100% - 100px);
				height: calc(100% - 80px);
			}

			li {
			   float: left; 
			}

			li button {
				background-color: black;
				border: none;
				display: block;
				color: white;
				text-align: center;
				padding: 8px 28px;
				cursor: pointer;
			}

			li button:hover {
				background-color: #444;
			}

			label{
				font-size: 20pt;
				color:black;
			}
		</style>
	</head>

	<body>
	<div><h1>Edit Post</h1></div>
		<form action="post" method="POST">
			<input type="hidden" name = "username" value='<%=request.getParameter("username")%>'/>
			<input type="hidden" name = "postid" value='<%=request.getParameter("postid")%>'/>
			<div>
				<ul>
				  <li><button type="submit" name="action" value="save">Save</button></li>
				  <li><button type="submit" name="action" value="list">Close</button></li>
				  <li><button type="submit" name="action" value="preview">Preview</button></li>
				  <li><button type="submit" name="action" value="delete">Delete</button></li>
				</ul>
			</div>
			
			<div>
				<label for="title">Title<label><br>
				<input type="text" name="title" value='<%=((request.getAttribute("title")==null)?"":request.getAttribute("title"))%>'>
			</div>

			<div>
				<label for="body">Body<label><br>
				<textarea rows="30" cols="70" name="body" ><%=((request.getAttribute("body")==null)?"":request.getAttribute("body"))%></textarea>
			</div>
		</form>
	</body>
</html>