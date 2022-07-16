using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class AdminPage : System.Web.UI.Page
{
    public string table;
    public string count;
    protected void Page_Load(object sender, EventArgs e)
    {
        if (Application["count"]!=null)
        {
            count = Application["count"].ToString();
        }
        if (Session["isAdmin"] == null || !(bool)Session["isAdmin"])
        {
            Response.Redirect("AdminsOnly.aspx");
        }
        string search = "";
        if (Request.QueryString["search"] != null) { search = Request.QueryString["search"]; }
        string sql = "SELECT * FROM PeopleData WHERE FirstName LIKE N'%" + search + "%' OR LastName LIKE N'%" + search + "%' ORDER BY LastName";
        DataTable dt = MyAdoHelper.ExecuteDataTable("Database.mdf", sql);
        table = "";
        foreach (DataRow row in dt.Rows)
        {
            table += "<tr>";
            table += "<form method='post' action='AdminEdit.aspx'>";
            table += "<input type='hidden' name='id' value='" + row["Id"] + "' />";
            table += "<td>" + row["Id"] + "</td>";
            table += "<td><input type='text' name='fName' value='" + row["FirstName"] + "' /></td>";
            table += "<td><input type='text' name='lName' value='" + row["LastName"] + "' /></td>";
            table += "<td><input type='text' name='phone' value='" + row["PhoneNumber"] + "' /></td>";
            table += "<td><input type='text' name='email' value='" + row["Email"] + "' /></td>";
            table += "<td><input type='text' name='password' value='" + row["Password"] + "' /></td>";
            if ((bool)row["IsAdmin"])
            {
                table += "<td><input type='checkbox' name='isAdmin' value='true' checked /></td>";
            }
            else
            {
                table += "<td><input type='checkbox' name='isAdmin' value='true' /></td>";
            }
            table += "<td><input type='submit' name='submit' value='עדכן' /></td>";
            table += "<td><input type='button' onclick='window.location.href=\"AdminRemove.aspx?id=" + row["Id"] + "\"' value='מחק' /></td>";
            table += "</form>";
            table += "</tr>";
        }
    }
}