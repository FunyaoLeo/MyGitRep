<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%><%@ page import="java.util.ArrayList" %>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>List Post</title>
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
			
			p { 
				word-break:break-all;
			}
			
			.btn-group .button {
				width: 100px;
				display: block;
			}
			
			.button {
			  display: inline-block;
			  border-radius: 4px;
			  background-color: black;
			  border: none;
			  color: white;
			  text-align: center;
			  font-size: 15px;
			  padding: 15px;
			  transition: all 0.5s;
			  cursor: pointer;
			  margin: 2px;
			}

			.button span {
			  cursor: pointer;
			  display: inline-block;
			  position: relative;
			  transition: 0.5s;
			}

			.button span:after {
			  content: '\00bb';
			  position: absolute;
			  opacity: 0;
			  top: 0;
			  right: -20px;
			  transition: 0.5s;
			}

			.button:hover span {
			  padding-right: 25px;
			}

			.button:hover span:after {
			  opacity: 1;
			  right: 0;
			}

			.table td{
				width:20%;
			}

			.PostInfo{
				color:black;
				text-align: left;
			}
			</style>
	</head>
	<body>
		<h1>List Post</h1>
		
		<form action="post" method="POST">
			<input type="hidden" name="username" value='<%= request.getParameter("username") %>'>
			<input type="hidden" name="postid" value=-1>
				<button type="submit" class='button' name="action" value="open"><span>New Post</span></button>
			<br>
		</form>
		<br />
		<br />
		
		<table class='table'>
			<tr>
				<td class='PostInfo'> Title</td>
				<td class='PostInfo'>Created</td>
				<td class='PostInfo'>Modified</td>
			</tr>
				<% ArrayList<ArrayList<Object>> postList = (ArrayList)request.getAttribute("postList"); %>
					<% for (int i = 0; postList != null && i < postList.size(); i++) { %>
					<% 	ArrayList<Object> post = (ArrayList)postList.get(i); %>
					<tr>
						<td class='PostInfo'> <p><%= post.get(0) %><p></td>
						<td class='PostInfo'> <p><%= post.get(1) %><p></td>
						<td class='PostInfo'> <p><%= post.get(2) %><p></td>
						<td>
							<form id='<%= i+1 %>' action="post" method="POST">
								<input type="hidden" name="username" value='<%= request.getParameter("username") %>'>
								<input type="hidden" name="postid" value='<%= post.get(3) %>'>
								<div class = "btn-group">
									<button type="submit" class='button' name="action" value="open"><span>Open</span></button>
									<button type="submit" class='button' name="action" value="delete"><span>Delete</span></button>
								</div class = "btn-group">
							</form>
						</td>
					</tr>
				<% } %>
			
		</table><br>
	</body>
</html>
