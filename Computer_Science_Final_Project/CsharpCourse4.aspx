<%@ Page Title="אופרטורים" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="CsharpCourse4.aspx.cs" Inherits="CsharpCourse4" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך C# – אופרטורים</h1>
    <hr />
    <h2>אופרטורים מתמטיים</h2>
    <p>לאחר שלמדנו על סוגי המשתנים הבסיסיים בחלק הקודם, בחלק זה נלמד על האופרטורים האריתמטיים שניתן להפעיל על משתנים מטיפוס מספר.</p>
    <h2>מה זה אופרטורים?</h2>
    <p>
        אופרטורים הם פעולות שניתן לעשות על משתנים, לרוב הן מיוצגות ע"י איזשהו סימן מיוחד, לדוגמא ‘+’ הוא אופרטור שמחבר בין שני משתנים ומחזיר את תוצאת החיבור.
    </p>
    <h2>אופרטורים שעובדים על מספרים</h2>
    <p>
        הסוג הכי מוכר של אופרטורים הוא כאלה שעובדים על שני מספרים ומחזירים מספר שלישי (המספרים יכולים להיות מטיפוסים שלמים או מטיפוסים לא שלמים).
        <br />
        באופרטורים מסוג זה נמצא את: + , – , * , / , %
    </p>
    <br />
    <p>אופרטור ‘+‘ מחבר שני מספרים, לדוגמא הקוד הבא מחבר בין שני מספרים x ו y ושם את תוצאת החיבור במשתנה z:</p>
    <div class="code">
        <span class="blue">int</span> x = 5;
        <br />
        <span class="blue">int</span> y = 3;
        <br />
        <span class="blue">int</span> z;
        <br />
        <br />
        z = x + y;
    </div>
    <p>
        באופן דומה פועלים האופרטורים האחרים.
        <br />

        אופרטור ‘–‘ מחסר שני מספרים.
        <br />

        אופרטור ‘*‘ מכפיל שני מספרים.
        <br />

        אופרטור ‘/‘ מחלק בין שני מספרים, נעיר שתוצאת החלוקה תלויה בסוג המשתנים.
        <br />

        אם נחלק שני מספרים מטיפוס double (שיכול להכיל מספרים לא שלמים) אז התוצאה יכולה להיות מספר לא שלם.
        <br />

        לעומת זאת, אם נחלק שני מספרים מטיפוס int התוצאה תהיה בהכרח מספר שלם (בעצם נקבל את התוצאה מעוגלת כלפי מטה).
        <br />

        לדוגמא, בקוד הבא אנו מחשבים חלוקה של 5 ב 2 ומקבלים 2.5 כאשר משתמשים במשתנה מסוג double ואילו כאשר נשתמש במשתנה מסוג int נקבל 2:
    </p>
    <div class="code">
        <span class="blue">double</span> x = 5;
        <br />
        <span class="blue">double</span> y = 2;
        <br />
        <span class="blue">double</span> z = x / y; <span class="green">// z = 2.5</span>
        <br />
        <br />
        <span class="blue">int</span> a = 5;
        <br />
        <span class="blue">int</span> b = 2;
        <br />
        <span class="blue">int</span> c = a / b; <span class="green">// c = 2</span>
        <br />
    </div>
    <p>
        <u>הערה:</u> החלקים בקוד הצבועים בירוק הם הערות.
        <br />

        בדרך כלל משתמשים בהערות בקוד כדי לספק הסברים לקוד מסובך.
        <br />

        הערה מתחילה בסימן // ונמשכת עד סוף השורה.
        <br />
        <br />
        האופרטור ‘%’ הוא אופרטור שעובד רק על מספרים שלמים ותפקידו להחזיר את שארית החלוקה.
        <br />

        לדוגמא, בקוד הבא נחשב את שארית החלוקה של 5 ב 2 ונקבל בתור תוצאה 1:
        <br />
    </p>
    <div class="code">
        <span class="blue">double</span> x = 5;
        <br />
        <span class="blue">double</span> y = 2;
        <br />
        <span class="blue">double</span> z = x % y; <span class="green">// z = 1</span>
    </div>
    <h2>הוספה והפחתה ב1</h2>
    <p>
        אופרטורים אלו עובדים על משתנה אחד מטיפוס שלם.
        <br />

        האופרטור ‘++‘ מקדם את המשתנה ב1, ואילו האופרטור ‘—‘ מפחית את ערך המשתנה ב1.
        <br />

        לדוגמא, ערך המשתנה a לאחר השורה השניה הוא 10 ולאחר השורה הרביעית הוא 8:
    </p>
    <div class="code">
        <span class="blue">int</span> x = 9;
        <br />
        a++; <span class="green">// x = 10</span><br />
        a--; <span class="green">// x = 9</span><br />
        a--; <span class="green">// x = 8</span>
    </div>
    <h2>הוספה והפחתה לפי מספר</h2>
    <p>
        אופרטורים אלו משמשים בעצם לכתיבה מקוצרת של האופרטורים האריתמטיים הרגילים.
        <br />

        האופרטור ‘+=’ מבצע חיבור והצבה באותה פעולה.
        <br />

        לדוגמא, בקוד הבא השורה השניה המשתמשת באופרטור ‘+=’ והשורה השלישית מבצעות בדיוק אותה פעולה:
    </p>
    <div class="code">
        <span class="blue">int</span> a = 5;
        <br />
        a += 3; <span class="green">// a = 8</span><br />
        a = a + 3; <span class="green">// a = 8</span>
    </div>
    <p>
        קיימים אופרטורים נוספים: ‘=%‘ , ‘=/‘ , ‘=*‘ , ‘=-‘.
        <br />

        האופרטור ‘=-‘ מבצע חיסור והצבה באותה פעולה, וכנ"ל לגבי שאר האופרטורים מסוג זה.
    </p>
    <h2>אופרטורים בוליאניים</h2>
    <p>בחלק הקודם למדנו על אופרטורים אריתמטיים. בחלק זה נלמד על אופרטורים שמחזירים תוצאות מטיפוס bool, כלומר מחזירים true או false.</p>
    <h2>אופרטורים שעובדים על משתני אמת/שקר</h2>
    <p>
        כזכור, משתנים מטיפוס bool יכולים להכיל רק אחד משני הערכים true או false.
        <br />
        האופרטורים הבאים יכולים לפעול רק על משתנים מטיפוס bool.
        <br />
        <br />
        האופרטור ‘!’ עובד על משתנה יחיד מטיפוס bool ומחזיר את ההפך מערך המשתנה, כלומר אם המשתנה מכיל את הערך true האופרטור יחזיר false, ולהיפך.
        <br />
        לדוגמא, הקוד הבא מציב false במשתנה מסוג bool ואז משתמש באופרטור ‘!’ בשביל להפוך את הערך:
    </p>
    <div class="code">
        <span class="blue">bool</span> myBool = <span class="blue">false</span>;
        <br />
        myBool = !myBool; <span class="green">// myBool = true</span>
    </div>
    <p>
        האופרטור && עובד על שני משתנים מטיפוס bool ומחזיר true רק אם שני המשתנים מכילים true.
        <br />
        <br />
        לדוגמא, בקוד הבא בשורה הראשונה נקבל את הערך true ואילו בשורה השנייה והשלישית נקבל false:
    </p>
    <div class="code">
        <span class="blue">bool</span> myBool1 = <span class="blue">true</span> && <span class="blue">true</span>;<br />
        <span class="blue">bool</span> myBool2 = <span class="blue">true</span> && <span class="blue">false</span>;<br />
        <span class="blue">bool</span> myBool3 = <span class="blue">false</span> && <span class="blue">true</span>;
    </div>
    <p>האופרטור ‘||‘ עובד על שני משתנים מטיפוס bool ומחזיר true אם לפחות אחד מהמשתנים מכיל true.</p>
    <h2>אופרטורים להשוואה</h2>
    <p>
        האופרטורים הבאים משמשים להשוואה בין זוגות של מספרים:
        <br />
        <br />
        האופרטור ‘>’ מחזיר true אם ורק אם המשתנה בצד שמאל קטן ממש מהמשתנה בצד ימין.
        <br />
        לדוגמא, הקוד הבא מציב במשתנה result1 ערך true ואילו במשתנה result2 ערך false:
    </p>
    <div class="code">
        <span class="blue">bool</span> myBool1 = 5 > 3; <span class="green">// myBool1 = true</span><br />
        <span class="blue">bool</span> myBool2 = 3 > 4; <span class="green">// myBool2 = false</span><br />
    </div>
</asp:Content>

