<%@ Page Title="קלט ופלט" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="CsharpCourse3.aspx.cs" Inherits="CsharpCourse3" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך C# – קלט ופלט</h1>
    <hr />
    <p>בחלק זה נלמד כיצד לקלוט נתונים מהמשתמש וכן כיצד להציג למסך פלט למשתמש.</p>
    <p>ראשית, פתחו את Visual Studio 2019 וצרו פרויקט חדש בשם InputOutput, כפי שלמדנו בחלק הקודם במדריך.</p>
    <h2>המחלקה Console</h2>
    <p>
        כדי לקלוט נתונים מהמשתמש או להדפיס למסך יש להשתמש במחלקה Console.<br />
        מחלקה זו אחראית על עבודה מול מסך ה- Console. במחלקה זו יש פונקציות לקליטת נתונים והדפסתם, וכן פונקציות המאפשרות לשלוט בצבעים של הטקסט המודפס.
    </p>
    <h2>הצגת פלט למסך</h2>
    <p>
        כדי להציג קלט למסך נשתמש בפונקציות Write ו WriteLine של המחלקה Console.<br />
        הפקודה WriteLine מדפיסה מחרוזת למסך ולאחר מכן יורדת שורה.<br />
        לדוגמא, אם נכתוב את הקוד הבא בתוך פונקציית ה- Main, התוכנית תדפיס למסך בשורה ראשונה את המילה “Hello” ובשורה אחריה את המילה “World”:
    </p>
    <div class="code">
        <span class="cyan">Console</span>.WriteLine("Hello"); <br />
        <span class="cyan">Console</span>.WriteLine("World");
    </div>
    <p>הפלט של התוכנית יהיה:</p>
    <img src="pictures/InputOutput2.png" width="70%" />
    <p>
        הפקודה Write מדפיסה מחרוזת למסך אבל <b>לא יורדת שורה</b> בסוף ההדפסה.
        <br />
        לדוגמא, הקוד הבא מדפיס למסך באותה שורה “Hello ” ומייד לאחריו “World”:
    </p>
    <div class="code">
        <span class="cyan">Console</span>.Write("Hello "); <br />
        <span class="cyan">Console</span>.Write("World");
    </div>
    <p>
        שימו לב שהוספנו רווח לאחר המילה Hello כדי שהמילים לא יהיו דבוקות אחת לשניה.<br />
        הפלט של התוכנית יהיה:
    </p>
    <img src="pictures/InputOutput4.png" width="70%" />
    <h2>קליטת נתונים מהמשתמש</h2>
    <p>
        כדי לקלוט נתונים מהמשתמש נשתמש בפונקציה ReadLine של המחלקה Console.<br />
        שימוש בפונקציה ReadLine גורם לתוכנה שלנו להמתין לקבלת קלט מהמשתמש.<br />
        התוכנית תמשיך בריצה רק לאחר שהמשתמש יכניס נתונים וילחץ על מקש Enter.<br />
        הקלט שהמשתמש הכניס יוחזר מהפונקציה ReadLine לתוך משתנה מסוג string (מחרוזת).<br />
        לדוגמא, הקוד הבא מדפיס למסך “Enter user name: “, קולט מהמשתמש את שמו ושומר זאת בתוך משתנה מטיפוס string:
    </p>
    <div class="code">
        <span class="cyan">Console</span>.Write("Enter your name: "); <br />
        <span class="blue">string</span> user = Console.ReadLine();
    </div>
    <p>הפלט של התוכנית יהיה:</p>
    <img src="pictures/InputOutput6.png" width="70%" />
</asp:Content>

