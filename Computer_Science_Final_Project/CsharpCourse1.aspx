<%@ Page Title="תוכנית ראשונה" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="CsharpCourse1.aspx.cs" Inherits="CsharpCourse1" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך C# – תוכנית #C ראשונה</h1>
    <hr />
    <p>בחלק זה נראה כיצד להשתמש בסביבת העבודה Visual Studio 2019 בשביל ליצור תוכנית ראשונה בשפת #C.</p>
    <h2>יצירת התוכנית</h2>
    <p>ראשית, פתחו את Visual Studio 2019 ובחרו באפשרות Create a new Project</p>
    <img src="pictures/CreateProj.png" width="70%" />
    <p>
        כעת יש לבחור בסוג הפרויקט המבוקש.<br />
        ברשימת התבניות נבחר בתבניות בשפת C#, נבחר בתבנית מסוג Console Application, שמשמעותה יצירת תוכנית בעלת ממשק טקסט ונלחץ על Next.
    </p>
    <img src="pictures/CreateProj2.png" width="70%" />
    <p>
        לאחר מכן, נבחר שם לתוכנית ומיקום על המחשב.<br />
        ואז נלחץ על Create
    </p>
    <img src="pictures/CreateProj3.png" width="70%" />
    <p>
        Visual Studio יצור עבורנו תוכנית מסוג Console Application ובסיום התהליך נקבל את מסך העבודה הראשי של Visual Studio 2019.<br />
        מצד ימין נוכל לראות את החלון Solution Explorer שבו מופיעים רשימת הקבצים בפרויקט שיצרנו. כרגע יש רק קובץ אחד, Program.cs.
    </p>
    <p>בחלון הראשי ניתן לראות ולערוך את תוכן הקובץ Program.cs שמכיל את התוכנית שלנו.</p>
    <img src="pictures/CreateProj4.png" width="70%" />
    <h2>הרצת התכנית</h2>
    <p>כעת נרצה להריץ את התוכנית שכתבנו. בשורת התפריט נלחץ על כפתור ההפעלה או לחילופין נוכל ללחוץ על מקש F5.</p>
    <img src="pictures/CreateProj5.png" width="70%" />
    <p>
        כעת התוכנית שלנו רצהכעת התוכנית שלנו רצה!<br />
        למסך מודפסת המחרוזת Hello World! והתוכנית ממתינה ללחיצה על מקש. ברגע שנלחץ על מקש כלשהו התוכנית תסתיים.(יש להתעלם מכל הטקסט הנוסף)
    </p>
    <img src="pictures/CreateProj6.png" width="70%" />
    <p>ברכות! יצרנו תוכנית ראשונה בשפת C#!</p>
    <p>בפרק הבא במדריך נדבר על קלט ופלט.</p>
</asp:Content>

