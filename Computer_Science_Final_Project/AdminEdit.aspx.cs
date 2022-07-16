using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class AdminEdit : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (Session["isAdmin"] == null || !(bool)Session["isAdmin"])
        {
            Response.Redirect("AdminsOnly.aspx");
        }
        if (Request.Form["submit"] != null && (string)Session["id"]!= Request.Form["id"])
        {
            string id = Request.Form["id"];
            string fName = Request.Form["fName"];
            string lName = Request.Form["lName"];
            string phone = Request.Form["phone"];
            string email = Request.Form["email"];
            string password = Request.Form["password"];
            int admin = 0;
            if (Request.Form["isAdmin"] != null) { admin = 1; }
            string sql = "UPDATE PeopleData SET ";
            sql += "FirstName=N'"+fName+"'";
            sql += ",LastName=N'"+lName+"'";
            sql += ",PhoneNumber=N'"+phone+"'";
            sql += ",Email=N'"+email+"'";
            sql += ",Password=N'"+password+"'";
            sql += ",IsAdmin="+admin;
            sql += " WHERE Id="+id;
            MyAdoHelper.DoQuery("Database.mdf",sql);
            //Response.Write(sql);
        }
        Response.Redirect("AdminPage.aspx");
    }
}