<%@ Page Title=" - ניהולעמוד מנהל" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="AdminPage.aspx.cs" Inherits="AdminPage" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
        h1 {
            margin-bottom: 30px;
        }

        table {
            font-family: Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
            margin: auto;
        }

            table td, table th {
                border: 1px solid #ddd;
                padding: 8px;
            }

            table tr {
                background-color: #f2f2f2;
            }

            table th {
                padding-top: 12px;
                padding-bottom: 12px;
                background-color: #4CAF50;
                color: white;
            }

            table td {
                text-align: center;
            }

        form.search {
            width: 300px;
        }

            form.search input[type=text] {
                padding: 10px;
                font-size: 17px;
                border: 1px solid grey;
                float: left;
                width: 80%;
                margin-bottom: 30px;
            }

            form.search button {
                float: left;
                width: 20%;
                padding: 10px;
                background-color: mediumseagreen;
                color: white;
                font-size: 17px;
                border: 1px solid grey;
                border-left: none;
                cursor: pointer;
            }

                form.search button:hover {
                    background-color: seagreen;
                }
                .main-info{

                }
        .count {
            position: absolute;
            top: 20px;
            left: 50%;
            transform:translateX(-50%);
        }
    </style>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h2 class="count">כמות כניסות לאתר:<%=count %></h2>
    <h1>ניהול רשומים</h1>
    <form method="get" class="search">
        <button type="submit"><i class="fa fa-search"></i></button>
        <input type="text" placeholder="חיפוש.." name="search">
    </form>
    <table>
        <tr>
            <th>מספר סידורי</th>
            <th>שם פרטי</th>
            <th>שם משפחה</th>
            <th>טלפון</th>
            <th>אימייל</th>
            <th>סיסמא</th>
            <th>מנהל</th>
            <th>עדכון</th>
            <th>מחיקה</th>
        </tr>
        <%=table %>
    </table>
</asp:Content>

