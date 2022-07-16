<%@ Page Title="מערכים" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="CsharpCourse9.aspx.cs" Inherits="CsharpCourse9" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך C# – מערכים</h1>
    <hr />
    <p>בחלק זה נלמד על כיצד לעבוד עם מערכים בשפת #C.</p>
    <br />
    <h2>מה זה מערך?</h2>
    <p>מערך (array) הינו טיפוס נתונים המכיל מספר משתנים מאותו סוג שיושבים בזיכרון בצורה רציפה, כלומר אחד ליד השני.</p>
    <p>כאשר מגדירים משתנה מטיפוס מערך יש לציין את מספר המשתנים במערך, סוג המשתנים ושם המערך.</p>
    <br />
    <p>ניתן להתייחס למערך בצורה ויזואלית כאל שורה של משתנים רגילים:</p>
    <img src="pictures/array_visual.png" alt="array_visual" style="mix-blend-mode: multiply; width: 70%" />
    <p>בדוגמא בציור יש לנו מערך של משתנים מטיפוס int בשם arr, המערך הוא בגודל 10.</p>
    <p>הפניה למערך מתבצעת באמצעות שם המערך והאינדקס לאיבר, שימו לב שהאינדקס בשפת #C מתחיל מ 0, כלומר [arr[0 הוא האיבר הראשון במערך, [arr[1 הוא האיבר השני וכו’</p>
    <br />
    <h2>כיצד יוצרים מערך?</h2>
    <p>כדי לראות כיצד ליצור מערך, נתבונן בדוגמא הבא:</p>
    <div class="code">
        <span class="blue">int</span>[] arr = <span class="blue">new int</span>[10];
    </div>
    <p>בדוגמא זו יצרנו מערך של int בשם arr, בעל גודל 10.</p>
    <p>ראשית הגדרנו את סוג המשתנה []int, כלומר מערך של int, לאחר מכן נתנו לו שם arr ואז ביקשו להקצות זיכרון ל10 תאים ע"י שימוש בפקודה new.</p>
    <br />
    <p>נראה דוגמא נוספת:</p>
    <div class="code">
        <span class="blue">string</span>[] myStrings = <span class="blue">new string</span>[50];
    </div>
    <p>בדוגמא זו יצרנו מערך של string בשם myStrings בעל גודל 50, כלומר נוכל לאכסן במערך שלנו 50 משתנים מטיפוס string.</p>
    <br />
    <br />
    <h2>כיצד משתמשים במערך?</h2>
    <p>לאחר שיצרנו את המערך נוכל להשתמש בו בשביל לכתוב ולקרוא ערכים.</p>
    <br />
    <p>הגישה לאיברים במערך מעשית ע"י ציון שם המערך והאינדקס של האיבר הדרוש.</p>
    <br />
    <p>דוגמא, הקוד הבא ניגש לתא הראשון במערך בשם arr ומציב שם את המספר 5:</p>
    <div class="code">
        arr[0] = 5;
    </div>
    <br />
    <p>הקוד הבא ניגש לתא השלישי במערך myStrings ומציב שם את הערך "Hello":</p>
    <div class="code">
        myStrings[2] = "Hello";
    </div>
    <br />
    <h2>כיצד עוברים על איברי המערך?</h2>
    <p>כדי לעבור על איברי המערך נשתמש בדרך כלל בלולאה.</p>
    <br />
    <p>לדוגמא, לולאת for הבאה עוברת על איברי המערך arr ומציבה בהם את הספרים 1 עד 10:</p>
    <div class="code">
        <span class="blue">for </span>(<span class="blue">int </span>i = 0; i < arr.Length;i++)
        <br />
        {
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;arr[i] = i + 1;
        <br />
        }
    </div>
    <p>שימו לב לשימוש בתכונה Length של המערך arr, תכונה זו מחזירה את גודל המערך, במקרה שלנו arr.Length מחזירה את הערך 10.</p>
    <br />
    <p>נראה דוגמא נוספת שקולטת מספרים מהמשתמש ומציבה אותם במערך:</p>
    <div class="code">
        <span class="blue">int</span>[] arr = <span class="blue">new int</span>[10];
        <span class="blue">string</span> temp;
        <br />
        <span class="blue">for </span>(<span class="blue">int </span>i = 0; i < arr.Length;i++)
        <br />
        {
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;<span class="cyan">Console</span>.WriteLine("enter a number:");
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;temp = <span class="cyan">Console</span>.ReadLine();
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;arr[i] = <span class="blue">int</span>.Parse(temp);  
        <br />
        }
    </div>
</asp:Content>

