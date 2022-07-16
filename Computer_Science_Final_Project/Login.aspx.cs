using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Login : System.Web.UI.Page
{
    public string cookieEmail;
    public string cookiePassword;
    public string emailErr;
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!(Request.Cookies["email"]==null || Request.Cookies["password"] == null))
        {
            cookieEmail = Request.Cookies["email"].Value;
            cookiePassword = Request.Cookies["password"].Value;
        }
        
        if (Request.Form["submit"] != null)
        {
            string select = "SELECT * FROM PeopleData WHERE Email='"+Request.Form["email"]+"' AND Password='" + Request.Form["password"] + "'";
            string fileName = "Database.mdf";
            if (MyAdoHelper.IsExist(fileName,select))
            {
                HttpCookie cookieEmail = new HttpCookie("email");
                HttpCookie cookiePassword = new HttpCookie("password");
                cookieEmail.Value = Request.Form["email"];
                cookiePassword.Value = Request.Form["password"];
                cookieEmail.Expires = DateTime.Now.AddDays(30);
                cookiePassword.Expires = DateTime.Now.AddDays(30);
                Response.Cookies.Add(cookieEmail);
                Response.Cookies.Add(cookiePassword);

                DataTable table = MyAdoHelper.ExecuteDataTable(fileName, select);
                Session["user"] = (string)table.Rows[0]["FirstName"];
                Session["isAdmin"] = (bool)table.Rows[0]["IsAdmin"]; 
                Session["id"] = ""+table.Rows[0]["Id"];           
                Response.Redirect("Default.aspx");
            }
            else
            {
                emailErr = "אימייל או סיסמא שגויים";
            }
        }
    }
}