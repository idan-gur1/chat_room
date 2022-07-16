using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class MasterPage : System.Web.UI.MasterPage
{
    public bool loggedIn;
    public bool isAdmin;
    public string name;
    protected void Page_Load(object sender, EventArgs e)
    {
        loggedIn = false;
        if (Session["user"] != null)
        {
            loggedIn = true;
            name = (string)Session["user"];
        }

        isAdmin = false;
        if (Session["isAdmin"] != null && (bool)Session["isAdmin"] == true)
        {
            isAdmin = true;
        }
        
        Application.Lock();
        if (Session["firstLog"]==null)
        {
            Application["count"] = (int)Application["count"]+1;
            Session["firstLog"] = "no";
        }
        Application.UnLock();
    }
}
