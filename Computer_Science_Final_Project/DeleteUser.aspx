<%@ Page Title="מחיקת משתמש" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="DeleteUser.aspx.cs" Inherits="DeleteUser" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <link rel="stylesheet" href="css/MainFormStyle.css" />
    <script src="js/FormValidation.js"></script>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <form method="post" runat="server" onsubmit="return fullCheckDeleteUser()">

        <h1>מחיקת משתמש</h1>
        <h3 style="margin-bottom: 25px"><%=serverMsg %></h3>
        <label for="mail">אימייל:</label>
        <input type="email" id="email" name="email">
        <span id="err-email"></span>

        <label for="password">סיסמא:</label>
        <input type="password" id="password" name="password">
        <span id="err-password"></span>

        <button style="background-color:red" type="submit" name="submit">מחק</button>
    </form>
</asp:Content>

