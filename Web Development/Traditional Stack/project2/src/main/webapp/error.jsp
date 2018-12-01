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
        
        ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #333;
        }
        
        li {
            float: left;
        }
        
        li a {
            display: block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }
        
        li a:hover {
            background-color: #111;
        }
        </style>

</head>
<body>
    <h1>Status : <%= response.getStatus() %></h1>
    <l1>Error Info: <%= request.getAttribute("err_msg") %></l1>
</body>
</html>