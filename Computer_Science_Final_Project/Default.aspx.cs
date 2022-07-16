using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class _Default : System.Web.UI.Page
{
    public string errors;
    public double raiting;
    public int numOfVotes;
    protected void Page_Load(object sender, EventArgs e)
    {      
        if (Request.Form["submit"] != null)
        {
            if (Session["user"] == null)
            {
                errors = "יש להירשם כדי לדרג את האתר";
            }
            else if (Session["hasVoted"] != null)
            {
                errors = "אפשר לדרג רק פעם אחת";
            }
            else if (Request.Form["star"] == null)
            {
                errors = "יש לדרג כוכבים";
            }
            else
            {
                errors = "דורג בהצלחה";
                Application["raiting-count"] = (int)Application["raiting-count"] + 1;
                Application["raiting-sum"] = (int)Application["raiting-sum"] + int.Parse(Request.Form["star"]);
                Session["hasVoted"] = "yes";
            }
        }
        if ((int)Application["raiting-count"] != 0)
        {
            raiting = (double)(int)Application["raiting-sum"] / (int)Application["raiting-count"];
            raiting = Math.Round(raiting, 1);
            numOfVotes = (int)Application["raiting-count"];
        }
        else
        {
            raiting = 0;
            numOfVotes = 0;
        }
    }
}