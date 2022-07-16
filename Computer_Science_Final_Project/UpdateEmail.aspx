<%@ Page Title="שינוי אימייל" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="UpdateEmail.aspx.cs" Inherits="UpdateEmail" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <link rel="stylesheet" href="css/MainFormStyle.css" />
    <script src="js/FormValidation.js"></script>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <form method="post" runat="server" onsubmit="return fullCheckUpdateEmail()">

        <h1>עדכון אימייל</h1>
        <h3 style="margin-bottom:25px"><%=serverMsg %></h3>
        <label for="mail">אימייל:</label>
        <input type="email" id="email" name="email">
        <span id="err-email"></span>

        <label for="password">סיסמא:</label>
        <input type="password" id="password" name="password">
        <span id="err-password"></span>

        <label for="password">אימייל חדש:</label>
        <input type="email" id="newEmail" name="newEmail">
        <span id="err-newEmail"></span>

        <button type="submit" name="submit">עדכן</button>
    </form>
</asp:Content>

