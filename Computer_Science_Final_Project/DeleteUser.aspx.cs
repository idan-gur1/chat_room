using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class DeleteUser : System.Web.UI.Page
{
    public string serverMsg;
    protected void Page_Load(object sender, EventArgs e)
    {
        if (Request.Form["submit"] != null)
        {
            string fileName = "Database.mdf";
            string select = "SELECT * FROM PeopleData WHERE Email='" + Request.Form["email"] + "' AND Password='" + Request.Form["password"] + "'";
            string delete = "DELETE FROM PeopleData WHERE Email='" + Request.Form["email"] + "' AND Password='" + Request.Form["password"] + "'";
            if (MyAdoHelper.IsExist(fileName, select))
            {
                MyAdoHelper.DoQuery(fileName, delete);
                serverMsg = "המשתמש נמחק";
            }
            else
            {
                serverMsg = "אימייל או סיסמא אינם נכונים";
            }
        }
    }
}