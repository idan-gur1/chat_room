<%@ Page Title="תנאי if" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="CsharpCourse5.aspx.cs" Inherits="CsharpCourse5" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך C# – תנאי if</h1>
    <hr />
    <p>בחלק זה נלמד כיצד להשתמש בתנאי if.</p>
    <h2>משפט if בסיסי</h2>
    <p>
        לפעמים עולה צורך לבצע קטע קוד מסויים רק כאשר מתקיים איזשהו תנאי.
        <br />
        לדוגמא נרצה להדפיס למשתמש את המחרוזת “Hello” רק אם משתנה age מכיל ערך גדול או שווה ל18.
        <br />
        לצורך זה נוכל להשתמש במשפט if באופן הבא:
    </p>
    <div class="code">
        <span class="blue">if</span> (age >= 18)
        <br />
        {
        <br />
        <span class="cyan">Console</span>.WriteLine("Hello");
        <br />
        }
    </div>
    <br />
    <p>באופן כללי משפט if יראה בצורה הבאה:</p>
    <div class="code">
        <span class="blue">if</span> (condition)
        <br />
        {
        <br />
        <small>statements</small>
        <br />
        }
    </div>
    <p>כאשר condition מציין איזשהו ביטוי מטיפוס bool ואילו statements מציין אוסף פקודות שנרצה להריץ במקרה שהביטוי condition הוא true.</p>
    <br />
    <p>בתור condition ניתן לשים כל ביטוי שהתוצאה שלו היא bool, בדרך כלל נשתמש באופרטורים הבוליאניים שלמדנו עליהם בחלק קודם של המדריך.</p>
    <br />
    <p>להלן מספר דוגמאות בעלי תנאים מסוגים שונים:</p>
    <br />
    <ul style="margin-right: inherit">
        <li>
            <p>קטע הקוד שבתנאי תמיד מתבצע:</p>
            <div class="code">
                <span class="blue">if</span> (<span class="blue">true</span>)
        <br />
                {
        <br />
                <span class="cyan">Console</span>.WriteLine("runs always");
        <br />
                }
            </div>
        </li>

        <li>
            <p>קטע הקוד שבתנאי אף פעם לא מתבצע:</p>
            <div class="code">
                <span class="blue">if</span> (<span class="blue">false</span>)
        <br />
                {
        <br />
                <span class="cyan">Console</span>.WriteLine("never runs");
        <br />
                }
            </div>
        </li>
        <li>
            <p>קטע הקוד שבתנאי מתבצע אם המשתמש הכניס את הערך “idan”:</p>
            <div class="code">
                <span class="blue">string </span>name = <span class="cyan">Console</span>.ReadLine();
                <br />
                <span class="blue">if</span> (name == "idan")
        <br />
                {
        <br />
                <span class="cyan">Console</span>.WriteLine("runs if name is idan");
        <br />
                }
            </div>
        </li>
        <li>
            <p>קטע הקוד שבתנאי מתבצע אם המשתמש הכניס את הערך “arik” וגם משתנה age מכיל ערך שגדול מ 18:</p>
            <div class="code">
                <span class="blue">string </span>name = <span class="cyan">Console</span>.ReadLine();
                <br />
                <span class="blue">if</span> ((name == "arik") && (age > 18))
        <br />
                {
        <br />
                <span class="cyan">Console</span>.WriteLine("name is arik AND age is bigger than 18");
        <br />
                }
            </div>
        </li>
    </ul>
    <br />
    <h2>משפט if-else</h2>
    <p>
        באמצעות משפט if-else ניתן לבצע קוד מסוים כאשר התנאי ב if הוא true ולבצע קוד אחר כאשר התנאי הוא false.
        <br />
        המבנה הכללי של משפט if-else יראה בצורה הבאה:
    </p>
    <div class="code">
        <span class="blue">if</span> (condition)
        <br />
        {
        <br />
        <small>statements</small>
        <br />
        }
        <br />
        <span class="blue">else</span>
        <br />
        {
        <br />
        <small>else statements</small>
        <br />
        }
    </div>
    <p>כאשר condition מציין איזשהו ביטוי מטיפוס bool ואילו statements מציין אוסף פקודות שנרצה להריץ במקרה שהביטוי condition הוא true. ו-else statements מציין אוסף של פקודות שיורצו אם הביטוי condition הוא false.</p>
    <br />
    <p>(ניתן לשים תנאי if בתוך תנאי if אחרים)</p>
</asp:Content>

