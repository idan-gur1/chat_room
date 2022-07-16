<%@ Page Title="משתנים" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="CsharpCourse2.aspx.cs" Inherits="CsharpCourse2" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <style>
        table {
            font-family: Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
            margin: auto;
        }

            table td, table th {
                border: 1px solid #ddd;
                padding: 8px;
                width: 25%;
            }



            table tr {
                background-color: #f2f2f2;
            }

            table th {
                padding-top: 12px;
                padding-bottom: 12px;
                background-color: #4CAF50;
                color: white;
            }

            table:last-of-type tr td:nth-child(3) {
                direction: ltr;
            }

        
    </style>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך C# – משתנים</h1>
    <hr />
    <p>בחלק זה נלמד כיצד לעבוד עם משתנים (Variables) מטיפוסים בסיסיים.</p>
    <p>פתחו את סביבת העבודה וצרו פרויקט חדש.</p>
    <h2>מה זה משתנה?</h2>
    <p>
        משתנה הוא איזור בזיכרון של המחשב שנתתם לו שם. בעזרת שם המשתנה ניתן לפנות לאזור הזיכרון ולכתוב שם ערכים או לקרוא משם ערכים.
        <br />
        משתנים הם מרכיב חשוב ביותר בכל שפת תכנות.
        <br />
        לכל משתנה יש שם וסוג (טיפוס), טיפוס המשתנה קובע את סוג הערכים שניתן להכניס לתוך המשתנה.
        <br />
        הטיפוסים החשובים ביותר של משתנים הם: משתני אמת/שקר, מחרוזות, מספרים שלמים ומספרים שאינם שלמים.
        <br />
    </p>   
    <h2>משתנה מטיפוס אמת/שקר (בוליאני)</h2>
    <p>
        משתנה מטיפוס אמת/שקר הוא משתנה שיכול להכיל רק את הערכים הבאים: true , false.
        <br />
        בדרך כלל נשתמש במשתנה מסוג זה כאשר נרצה לזכור משהו שיש לו רק שתי אפשרויות.
        <br />
    </p>
    <p>לדוגמא, בקוד הבא אנו מגדירים משתנה מטיפוס אמת/שקר בעל השם hasJob, ומציבים בו את הערך true:</p>
    <div class="code">
        <span class="blue">bool</span> hasJob = true;
    </div>
    <p>לחילופין יכולנו להציב את הערך false:</p>
    <div class="code">
        <span class="blue">bool</span> hasJob = false;
    </div>
    <br />
    <h2>משתנה מסוג תו</h2>
    <p>משתנה מסוג תו מסוגל לשמור תו בודד כגון האות 'a' או הסימן '@'.</p>
    <p>לדוגמא, בקוד הבא אנו מציבים במשתנה מסוג תו את הסימן '@' ובשורה שאחריו אנו מציבים בו את האות 'a'.</p>
    <div class="code">
        <span class="blue">char</span> myChar = '@';<br />
        myChar='a';
    </div>
    <br />
    <h2>משתנה מסוג מחרוזת</h2>
    <p>משתנה מסוג מחרוזת רצף כלשהו של תווים, כמו שם של אדם</p>
    <p>לדוגמא, בקוד הבא אנו מגדירים משתנה מטיפוס string ומציבים בו מחרוזת:</p>
    <div class="code">
        <span class="blue">string</span> nyName = "Idan";
    </div>
    <br />
    <h2>משתנים מטיפוס מספרים שלמים</h2>
    <p>ישנם מספר סוגים שונים של משתנים שיכולים להכיל מספרים שלמים.</p>
    <br />
    <p>ההבדל בין הסוגים השונים הוא טווח המספרים שהם יכולים לקבל.</p>
    <br />
    <p>הסיבה שיש טיפוסים שונים בעלי טווחים שונים היא שמשתנה בעל טווח רחב יותר תופס יותר מקום בזיכרון (יותר ביטים בכונן).</p>
    <p>להלן טבלה שמפרטת את סוגי המשתנים השונים והטווחים שלהם:</p>
    <br />
    <table>
        <tr>
            <th>טיפוס המשתנה</th>
            <th>ערך מינימלי</th>
            <th>ערך מקסימלי</th>
            <th>הזיכרון הדרוש בביטים</th>
        </tr>
        <tr>
            <td>sbyte</td>
            <td>128-</td>
            <td>127</td>
            <td>8</td>
        </tr>
        <tr>
            <td>byte</td>
            <td>0</td>
            <td>255</td>
            <td>8</td>
        </tr>
        <tr>
            <td>short</td>
            <td>32768-</td>
            <td>32767</td>
            <td>16</td>
        </tr>
        <tr>
            <td>ushort</td>
            <td>0</td>
            <td>65535</td>
            <td>16</td>
        </tr>
        <tr>
            <td>int</td>
            <td>2,147,483,648-</td>
            <td>2,147,483,647</td>
            <td>32</td>
        </tr>
        <tr>
            <td>uint</td>
            <td>0</td>
            <td>4,294,967,295</td>
            <td>32</td>
        </tr>
        <tr>
            <td>long</td>
            <td>9,223,372,036,854,775,808-</td>
            <td>9,223,372,036,854,775,807</td>
            <td>64</td>
        </tr>
        <tr>
            <td>ulong</td>
            <td>0</td>
            <td>18,446,744,073,709,551,615</td>
            <td>64</td>
        </tr>
    </table>
    <br />
    <p>לרוב משתנים מטיפוס int מספיקים לנו ונשתמש בהם בדרך כלל ליצוג מספרים שלמים.</p>
    <br />
    <h2>משתנים מטיפוס מספרים לא שלמים</h2>
    <p>ישנם מספר סוגים שונים של משתנים שיכולים להכיל מספרים לא שאינם בהכרח שלמים.</p>
    <br />
    <p>ההבדל בין הסוגים השונים הוא טווח המספרים שהם יכולים לקבל.</p>
    <br />
    <p>להלן טבלה שמפרטת את סוגי המשתנים השונים והטווחים שלהם:</p>
    <br />
    <table>
        <tr>
            <th>טיפוס המשתנה</th>
            <th>דיוק בספרות</th>
            <th>טווח משוער</th>
            <th>הזיכרון הדרוש בביטים</th>
        </tr>
        <tr>
            <td>float</td>
            <td>7</td>
            <td>±1.5 x 10E−45 to ±3.4 x 10E38</td>
            <td>32</td>
        </tr>
        <tr>
            <td>double</td>
            <td>16</td>
            <td>±5.0 × 10E−324 to ±1.7 × 10E308</td>
            <td>64</td>
        </tr>
        <tr>
            <td>decimal</td>
            <td>28</td>
            <td>±1.0 x 10E-28 to ±7.9228 x 10E28</td>
            <td>16</td>
        </tr>
    </table>
    <br />
    <p>לרוב משתנים מטיפוסלרוב כאשר נרצה לעבור עם מספרים לא שלמים נעבוד עם משתנים מטיפוס double.</p>
</asp:Content>

