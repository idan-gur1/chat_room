<%@ Page Title="הרשמה" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="Register.aspx.cs" Inherits="Register" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <link rel="stylesheet" href="css/MainFormStyle.css" />
    <script src="js/FormValidation.js"></script>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <form method="post" runat="server" onsubmit="return fullCheckRegister()">

        <h1>הרשמה</h1>

        <label for="name">שם פרטי</label>
        <input type="text" id="fName" name="fName" value="<%=fName %>">
        <span id="err-fName"></span>

        <label for="name">שם משפחה:</label>
        <input type="text" id="lName" name="lName" value="<%=lName %>">
        <span id="err-lName"></span>

        <label for="mail">אימייל:</label>
        <input type="text" id="email" name="email" value="<%=email %>">
        <span id="err-email"><%=EmailErr %></span>

        <label for="mail">מספר טלפון:</label>
        <input type="text" id="phone" name="phone" value="<%=phone %>">
        <span id="err-phone"><%=PhoneErr %></span>

        <label for="password">סיסמא:</label>
        <input type="password" id="password" name="password">
        <span id="err-password"></span>

        <button type="submit" name="submit">הירשם</button>
    </form>
</asp:Content>

