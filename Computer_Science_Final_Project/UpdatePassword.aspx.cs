using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class UpdatePassword : System.Web.UI.Page
{
    public string serverMsg;
    protected void Page_Load(object sender, EventArgs e)
    {
        if (Request.Form["submit"] != null)
        {
            string fileName = "Database.mdf";
            string select = "SELECT * FROM PeopleData WHERE Email='" + Request.Form["email"] + "' AND Password='" + Request.Form["oldPassword"] + "'";
            string update = "UPDATE PeopleData SET Password='" + Request.Form["newPassword"] + "' WHERE Email='" + Request.Form["email"] + "' AND Password='" + Request.Form["oldPassword"] + "'";
            if (MyAdoHelper.IsExist(fileName,select))
            {
                MyAdoHelper.DoQuery(fileName,update);
                serverMsg = "הפרטים עודכנו בהצלחה";
            }
            else
            {
                serverMsg = "אימייל או סיסמא אינם נכונים";
            }
        }
    }
}