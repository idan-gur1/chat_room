using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Register : System.Web.UI.Page
{
    public string EmailErr;
    public string PhoneErr;
    public string fName;
    public string lName;
    public string email;
    public string phone;
    protected void Page_Load(object sender, EventArgs e)
    {
        if (Request.Form["submit"] != null)
        {
            string fileName = "Database.mdf";
            string selectQueryEmail = "SELECT * FROM PeopleData WHERE Email = '" + Request.Form["email"] + "'";
            string selectQueryPhone = "SELECT * FROM PeopleData WHERE PhoneNumber = '" + Request.Form["phone"] + "'";
            if (MyAdoHelper.IsExist(fileName, selectQueryEmail))
            {
                EmailErr = "כתובת האימייל כבר קיימת במערכת";
                FillFields();
            }
            else if (MyAdoHelper.IsExist(fileName, selectQueryPhone))
            {
                PhoneErr = "מספר הטלפון כבר קיים במערכת";
                FillFields();
            }
            else
            {
                string sql = "INSERT INTO PeopleData";
                sql += " (FirstName, LastName, PhoneNumber, Email, Password, IsAdmin) ";
                sql += "VALUES (";
                sql += "N'" + Request.Form["fName"] + "'";
                sql += ",N'" + Request.Form["lName"] + "'";
                sql += ",'" + Request.Form["phone"] + "'";
                sql += ",'" + Request.Form["email"] + "'";
                sql += ",'" + Request.Form["password"] + "'";
                sql += ", 0";
                sql += ")";
                MyAdoHelper.DoQuery(fileName, sql);
                Response.Redirect("Default.aspx");
            }
        }
    }
    private void FillFields()
    {
        fName = Request.Form["fName"]; 
        lName = Request.Form["lName"];
        email = Request.Form["email"]; 
        phone = Request.Form["phone"];
    }
}