using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class AdminRemove : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (Session["isAdmin"] == null || !(bool)Session["isAdmin"])
        {
            Response.Redirect("AdminsOnly.aspx");
        }
        if (Request.QueryString["id"] != null && (string)Session["id"] != Request.QueryString["id"])
        {
            string id = Request.QueryString["id"];
            string sql = "DELETE FROM PeopleData WHERE Id="+id;
            MyAdoHelper.DoQuery("Database.mdf",sql);
            //Response.Write(sql);
        }
        Response.Redirect("AdminPage.aspx");
    }
}