<%@ Page Title="שינוי טלפון" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="UpdatePhone.aspx.cs" Inherits="UpdatePhone" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <link rel="stylesheet" href="css/MainFormStyle.css" />
    <script src="js/FormValidation.js"></script>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <form method="post" runat="server" onsubmit="return fullCheckUpdatePhone()">

        <h1>עדכון טלפון</h1>
        <h3 style="margin-bottom:25px"><%=serverMsg %></h3>
        <label for="mail">אימייל:</label>
        <input type="email" id="email" name="email">
        <span id="err-email"></span>

        <label for="password">סיסמא:</label>
        <input type="password" id="password" name="password">
        <span id="err-password"></span>

        <label for="password">טלפון חדש:</label>
        <input type="text" id="newPhone" name="newPhone">
        <span id="err-newPhone"></span>

        <button type="submit" name="submit">עדכן</button>
    </form>
</asp:Content>

