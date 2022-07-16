<%@ Page Title="לולאת for" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="CsharpCourse6.aspx.cs" Inherits="CsharpCourse6" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך C# – לולאת for</h1>
    <hr />
    <p>בחלקים הקודמים במדריך למדנו כיצד לעבוד עם משתנים וכיצד להשתמש במשפטי if. בחלק זה נלמד על לולאת for.</p>
    <h2>מה זה לולאה?</h2>
    <p>לולאה היא קטע קוד שנרצה שיתבצע מספר פעמים.</p>
    <p>לדוגמא תארו לכם שנרצה להדפיס למסך 3 פעמים את המשפט "Welcome", אופציה אחת היא לכתוב תוכנית שמשתמשת בפונקציה Console.WriteLine 3 פעמים:</p>
    <div class="code">
        <span class="cyan">Console</span>.WriteLine("Welcome"); <br />
        <span class="cyan">Console</span>.WriteLine("Welcome"); <br />
        <span class="cyan">Console</span>.WriteLine("Welcome");
    </div>
    <p>אופציה זו היא יחסית סבירה, אבל מה יקרה אם נרצה להדפיס זאת 30 פעמים? או 300?</p>
    <p>בשביל זה נשתמש בלולאה שבה יהיה כתוב מה רוצים לבצע ומספר הפעמים הדרוש.</p>
    <h2>לולאת for</h2>
    <p>לולאת for היא הסוג הפשוט ביותר של לולאות הקיים בשפת #C.</p>
    <br />
    <p>ראשית נראה דוגמא לשימוש בלולאת for, בתוכנית הבאה אנו מבצעים הדפסה של המחרוזת "Welcome to C#" 3 פעמים:</p>
    <div class="code">
        <span class="blue">for </span>(<span class="blue">int </span>i = 0;i < 3;i++)
        <br />
        {
        <br />
        <span class="cyan">Console</span>.WriteLine("Welcome");
        <br />
        }
    </div>
    <p>נסביר כעת את דוגמא זו:</p>
    <br />
    <p>קטע הקוד: int i = 0 מתבצע פעם אחת בלבד בתחילת הלולאה, פה אנו מאתחלים משתנה חדש מטיפוס int בשם i שיספור כמה פעמים גוף הלולאה כבר התבצע, בהתחלה משתנה זה מכיל את הערך 0.</p>
    <br />
    <p>קטע הקוד i < 3 מתבצע לפני כל ריצה של גוף הלולאה, אם הערך הוא true גוף הלולאה מתבצע, אחרת התוכנית מפסיקה את הלולאה ועוברת לקטע קוד שמופיע אחריה.</p>
    <br />
    <p>קטע הקוד ++i מתבצע אחרי כל ריצה של גוף הלולאה, תפקידו לקדם את הערך במשתנה i כדי לספור כמה פעמים התבצע גוף הלולאה.</p>
    <br />
    <p>לבסוף, קטע הקוד Console.WriteLine משמש בתור גוף הלולאה, זהו הקוד שנרצה שירוץ בכל פעם.</p>
    <br />
    <p>באופן כללי, לולאת for נראית בצורה הבאה:</p>
    <div class="code">
        <span class="blue">for </span>( index decleration; condition; index increment)
        <br />
        {
        <br />
        <span class="green">//loop body</span>
        <br />
        }
    </div>
</asp:Content>

