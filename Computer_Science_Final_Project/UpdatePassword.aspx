<%@ Page Title="שינוי סיסמא" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="UpdatePassword.aspx.cs" Inherits="UpdatePassword" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <link rel="stylesheet" href="css/MainFormStyle.css" />
    <script src="js/FormValidation.js"></script>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <form method="post" runat="server" onsubmit="return fullCheckUpdatePassword()">

        <h1>עדכון סיסמא</h1>
        <h3 style="margin-bottom:25px"><%=serverMsg %></h3>
        <label for="mail">אימייל:</label>
        <input type="email" id="email" name="email">
        <span id="err-email"></span>

        <label for="password">סיסמא:</label>
        <input type="password" id="oldPassword" name="oldPassword">
        <span id="err-oldPassword"></span>

        <label for="password">סיסמא חדשה:</label>
        <input type="password" id="newPassword" name="newPassword">
        <span id="err-newPassword"></span>

        <button type="submit" name="submit">עדכן</button>
    </form>
</asp:Content>

