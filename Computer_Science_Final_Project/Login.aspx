<%@ Page Title="כניסת רשומים" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="Login.aspx.cs" Inherits="Login" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <link rel="stylesheet" href="css/MainFormStyle.css" />
    <script src="js/FormValidation.js"></script>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <form method="post" runat="server" onsubmit="return fullCheckLogin()">

        <h1>כניסה</h1>

        <label for="mail">אימייל:</label>
        <input type="email" id="email" name="email" value="<%=cookieEmail %>">
        <span id="err-email"><%=emailErr %></span>

        <label for="password">סיסמא:</label>
        <input type="password" id="password" name="password" value="<%=cookiePassword %>">
        <span id="err-password"></span>

        <button type="submit" name="submit">כניסה</button>
    </form>
</asp:Content>

