<%@ Page Title="פונקציות" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="CsharpCourse8.aspx.cs" Inherits="CsharpCourse8" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך C# – פונקציות</h1>
    <hr />
    <p>בחלק זה נלמד כיצד להגדיר ולהשתמש בפונקציות.</p>
    <br />
    <h2>מה זה פונקציה?</h2>
    <p>פונקציה הוא קטע קוד בעל שם, כדי להריץ את קטע הקוד ניתן פשוט לכתוב את שמו.</p>
    <br />
    <p>השתמשנו כבר במספר פונקציות במהלך המדריך, לדוגמא הפונקציה Console.WriteLine היא פונקציה ששייכת למחלקה Console ושמה הוא WriteLine.</p>
    <p>הפונקציה WriteLine מקבלת בתור פרמטר את מה שאנו רוצים להדפיס למסך והיא מדפיסה אותו.</p>
    <br />
    <p>בנוסף נשים לב שבכל תוכנית שאנו כותבים יש לפחות פונקציה אחת, והיא הפונקציה Main. פונקציה זו היא נקודת הפתיחה של התוכנית שלנו:</p>
    <div class="code">
        <span class="blue">static void </span>Main(<span class="blue">string</span>[] args)
        <br />
        {
        <br />
        <br />
        }
    </div>
    <br />
    <h2>כיצד מגדירים פונקציה?</h2>
    <p>כעת נראה כיצד אנו יכולים להגדיר פונקציה משלנו.</p>
    <br />
    <p>ראשית נציין שהגדרת פונקציה נמצאת מחוץ להגדרה של הפונקציה Main אבל בתוך המחלקה שבה אנו נמצאים.</p>
    <p>לדוגמא אם הקוד שנוצר כאשר אנו פותחים פרויקט חדש הוא:</p>
    <div class="code">
        <span class="blue">class </span><span class="cyan">Program</span>
        <br />
        {
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;<span class="blue">static void </span>Main(<span class="blue">string</span>[] args)
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;{
        <br />
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;}
        <br />
        }
    </div>
    <p>אז נכתוב את הקוד של הפונקציה שלנו ליד הפונקציה Main, כלומר אחריה או לפניה, אבל לא בתוכה.</p>
    <br />
    <p>לצורך דוגמא, נגדיר פונקציה בשם PrintNameTwoTimes שקולטת מהמשתמש את שמו ומדפיסה אותו פעמיים למסך.</p>
    <br />
    <p>לצורך הבנה של מיקום הפונקציה ביחס לפונקציה Main נביא את הקוד במלואו:</p>
    <div class="code">
        <span class="blue">class </span><span class="cyan">Program</span>
        <br />
        {
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;<span class="blue">static void </span>Main(<span class="blue">string</span>[] args)
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;{
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PrintNameTwoTimes();    
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;}
        <br />
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;<span class="blue">static void </span>PrintNameTwoTimes()
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;{
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="cyan">Console</span>.WriteLine("enter name:");
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="blue">string </span>name = <span class="cyan">Console</span>.ReadLine();     
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="cyan">Console</span>.WriteLine(name);
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="cyan">Console</span>.WriteLine(name);
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;}
        <br />
        }
    </div>
    <p>בקטע קוד זה הגדרנו פונקציה בשם PrintNameTwoTimes, שמבצעת קוד מסויים וקראנו לפונקציה זו מתוך הפונקציה הראשית Main.</p>
    <p><b>שימו לב</b> שאם לא היינו קוראים לפונקציה, התוכנית לא הייתה מבצעת דבר!</p>
    <br />
    <p>הריצה של התוכנית מתחילה תמיד מפונקציית הMain ומבצעת רק מה שכתוב שם.</p>
    <br />
    <br />
    <h1>העברת והחזרת פרמטרים לפונקציה</h1>
    <p>קודם למדנו כיצד להגדיר פונקציות בסיסית. בחלק זה נלמד כיצד להעביר לפונקציות פרמטרים ולקבל מהפונקציה את ערך החזרה.</p>
    <h2>מה הם פרמטרים של פונקציה?</h2>
    <p>פרמטרים הם ערכים שפונקציה יכולה לקבל מהקוד שקורא לה. השתמשנו כבר בפרמטרים של פונקציות כאשר קראנו לפונקציה Console.WriteLine והעברנו לה את התוכן להדפסה. תוכן זה הוא הערך שהעברנו כפרמטר לפונקציה.</p>
    <br />
    <h2>הגדרת פרמטרים לפונקציה</h2>
    <p>כדי להגדיר שיש לפונקציה פרמטרים נרשום לאחר שם הפונקציה, בתוך הסוגרים את רשימת הפרמטרים, מופרדת בפסיקים.</p>
    <p>כל פרמטר מוגדר על ידי טיפוס הפרמטר ושמו.</p>
    <br />
    <p>לדוגמא, הפונקציה הבאה מגדירה שתי פרמטרים מטיפוס string בעלי השמות firstName ו lastName, הפונקציה משתמשת בפרמטרים בשביל להדפיסם למסך:</p>
    <div class="code">
        <span class="blue">static void </span>PrintFullName(<span class="blue">string </span>firstName,<span class="blue">string </span>lastName)
        <br />
        {
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;<span class="cyan">Console</span>.WriteLine("full name: " + firstName + " " + lastName);
        <br />
        }
    </div>
    <br />
    <h2>העברת ערכים בקריאה לפונקציה</h2>
    <p>העברת ערכים בקריאה לפונקציה נעשית ע"י כתיבת שם הפונקציה ובסוגריים את הערכים שאנו רוצים, מופרדים בפסיקים.</p>
    <br />
    <p>דוגמא, כדי לקרוא לפונקציה שהגדרנו בסעיף הקודם נבצע:</p>
    <div class="code">
        <span class="blue">static void </span>Main(<span class="blue">string</span>[] args)
        <br />
        {
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;PrintFullName("Idan","Gur");
        <br />
        }
    </div>
    <br />
    <h2>החזרת ערך מפונקציה</h2>
    <p>פונקציות יכולות להחזיר ערכים למי שקרא להם. כדי להחזיר פרמטר מפונקציה ראשית יש להגדיר בפונקציה את סוג הערך המוחזר, זה נעשה ע"י כתיבת טיפוס הערך המוחזר <u>לפני</u> שם הפונקציה.</p>
    <br />
    כדי לבצע בפועל את החזרת הערך נשתמש בפקודה return בתוך גוף הפונקציה.
    <br />
    <p>לדוגמא, קטע הקוד הבא מגדיר פונקציה שמקבלת שני פרמטרים מטיפוס int ומחזירה ערך מסוג int:</p>
    <div class="code">
        <span class="blue">static <span class="blue">int </span></span>Add(<span class="blue">int</span> a, <span class="blue">int</span> b)
        <br />
        {
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;<span class="blue">return</span> x + y;
        <br />
        }
    </div>
    <p>ה- int שמופיע לפני שם הפונקציה Add מציין את טיפוס ערך ההחזרה של הפונקציה.</p>
    <br />
    <p>שימו לב שהפקודה return היא הפקודה האחרונה שמתבצעת בפונקציה. פקודה זו מבצעת החזרה של הערך המבוקש ו<u>סיום הפונקציה</u>.</p>
    <br />
    <p>כדי לקבל את הערך בפונקציית הMain נצטרך להציב את תוצאת הפונקציה לתוך משתנה באופן הבא:</p>
    <div class="code">
        <span class="blue">static void </span>Main(<span class="blue">string</span>[] args)
        <br />
        {
        <br />
        <span class="blue">int </span>z = Add(5,3);<span class="green">//z = 8</span>
        <br />
        }
    </div>
</asp:Content>

