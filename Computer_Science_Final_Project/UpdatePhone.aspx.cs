using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class UpdatePhone : System.Web.UI.Page
{
    public string serverMsg;
    protected void Page_Load(object sender, EventArgs e)
    {
        if (Request.Form["submit"] != null)
        {
            string fileName = "Database.mdf";
            string select = "SELECT * FROM PeopleData WHERE Email='" + Request.Form["email"] + "' AND Password='" + Request.Form["password"] + "'";
            string update = "UPDATE PeopleData SET PhoneNumber='" + Request.Form["newPhone"] + "' WHERE Email='" + Request.Form["email"] + "' AND Password='" + Request.Form["password"] + "'";
            if (MyAdoHelper.IsExist(fileName, select))
            {
                MyAdoHelper.DoQuery(fileName, update);
                serverMsg = "הפרטים עודכנו בהצלחה";
            }
            else
            {
                serverMsg = "אימייל או סיסמא אינם נכונים";
            }
        }
    }
}