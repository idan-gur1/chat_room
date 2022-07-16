<%@ Page Title="לולאת while" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="CsharpCourse7.aspx.cs" Inherits="CsharpCourse7" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך C# – לולאת while</h1>
    <hr />
    <p>בחלק הקודם למדנו על שימוש בלולאת for. בחלק זה נלמד כיצד להשתמש בלולאת while.</p>
    <h2>לולאת while</h2>
    <p>לולאת while הינה עוד סוג של לולאה בשפת #C, כלומר היא נשתמש בה כאשר נרצה לבצע קטע קוד מספר לא ידוע מראש כלשהוא של פעמים.</p>
    <br />
    <p>ללולאת while יש את המבנה הבא:</p>
    <div class="code">
        <span class="blue">while</span> (condition)
        <br />
        {
        <br />
        statements
        <br />
        }
    </div>
    <p>במבנה הזה הביטוי condition הוא תנאי שהלולאה בודקת לפני ביצוע גוף הלולאה. גוף הלולאה מתבצע רק אם הביטוי condition מחזיר ערך true.</p>
    <p>הביטוי statements הוא גוף הלולאה.</p>
    <br />
    <p>לדוגמא, התוכנית הבאה מבצעת הדפסה של המחרוזת "Using while loop" 3 פעמים:</p>
    <div class="code">
        <span class="blue">int</span> i = 0;
        <span class="blue">while</span> (i < 3)
        <br />
        {
        <br />
        i++;
        <span class="cyan">Console</span>.WriteLine("While loop active");
        <br />
        }
    </div>
    <p>תוכנית זו יכלה גם להשתמש בלולאת for כפי שראינו בחלק הקודם.</p>
    <br />
    <p>דוגמא נוספת, בה אנו קולטים שמות מהמשתמש ומדפיסים הודעת "Welcome" לכל אחד מהשמות, עד אשר המשתמש מכניס שם ריק "":</p>
    <div class="code">
        <span class="cyan">Console</span>.WriteLine("Enter name:");
        <br />
        <span class="blue">string</span> name = <span class="cyan">Console</span>.ReadLine();
        <br />
        <span class="blue">while</span> (name != "")
        <br />
        {
        <br />
        <span class="cyan">Console</span>.WriteLine("Welcome " + name + "!");
        <br />
        name = <span class="cyan">Console</span>.ReadLine();
        <br />
        }
    </div>
    <p>שימו לב שבדוגמא זו לא ידוע מראש כמה פעמים גוף הלולאה יתבצע, מאחר וזה תלוי בקלט של המשתמש.</p>
</asp:Content>

