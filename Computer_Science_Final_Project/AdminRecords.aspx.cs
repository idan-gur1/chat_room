using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class AdminRecords : System.Web.UI.Page
{
    public string table;
    protected void Page_Load(object sender, EventArgs e)
    {
        if (Session["isAdmin"] == null || !(bool)Session["isAdmin"])
        {
            Response.Redirect("AdminsOnly.aspx");
        }
        string search = "";
        string sql = "";
        if (Request.QueryString["search"] != null) { search = Request.QueryString["search"]; }
        if(search.Split(' ').Length == 2)
        {
            sql = "SELECT FirstName,LastName,PhoneNumber,Email FROM PeopleData WHERE FirstName LIKE N'%" + search + "%' OR FirstName LIKE N'%" + search.Split(' ')[0] + "%' OR LastName LIKE N'%" + search + "%' OR LastName LIKE N'%" + search.Split(' ')[1] + "%' OR Email LIKE N'%" + search + "%' OR Phonenumber LIKE N'%" + search + "%' ORDER BY LastName";

        }
        else
        {
            sql = "SELECT FirstName,LastName,PhoneNumber,Email FROM PeopleData WHERE FirstName LIKE N'%" + search + "%' OR LastName LIKE N'%" + search + "%' OR Email LIKE N'%" + search + "%' OR Phonenumber LIKE N'%" + search + "%' ORDER BY LastName";
        }
        table = MyAdoHelper.GetTableContent("Database.mdf",sql);
        
    }
}