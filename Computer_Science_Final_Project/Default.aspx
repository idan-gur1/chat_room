<%@ Page Title="דף בית" Language="C#" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
        .stars {
            width: 360px;
            display: inline;
        }

        input.star {
            display: none;
        }

        label.star {
            float: right;
            padding: 10px;
            font-size: 36px;
            color: #444;
            transition: all .2s;
        }

        input.star:checked ~ label.star:before {
            content: '\f005';
            color: #FD4;
            transition: all .25s;
        }

        input.star-5:checked ~ label.star:before {
            color: #FE7;
        }

        input.star-1:checked ~ label.star:before {
            color: #F62;
        }

        label.star:hover {
            transform: rotate(-15deg) scale(1.3);
        }

        label.star:before {
            content: '\f006';
            font-family: FontAwesome;
        }

        .btn-3 {
            position: relative;
            background: rgb(0,172,238);
            background: linear-gradient(135deg, rgba(0,254,93,1) 0%, rgba(0,255,170,1) 85%);
            width: 130px;
            transform: translateY(40%);
            height: 40px;
            line-height: 42px;
            padding: 0;
            border: none;
        }

            .btn-3 span {
                position: relative;
                display: block;
                width: 100%;
                height: 100%;
                font-weight: 600;
            }

            .btn-3:before,
            .btn-3:after {
                position: absolute;
                content: "";
                right: 0;
                top: 0;
                background: rgba(0,225,0,1);
                transition: all 0.3s ease;
            }

            .btn-3:before {
                height: 0%;
                width: 2px;
            }

            .btn-3:after {
                width: 0%;
                height: 2px;
            }

            .btn-3:hover {
                background: transparent;
                box-shadow: none;
            }

                .btn-3:hover:before {
                    height: 100%;
                }

                .btn-3:hover:after {
                    width: 100%;
                }


            .btn-3 span:before,
            .btn-3 span:after {
                position: absolute;
                content: "";
                left: 0;
                bottom: 0;
                background: rgba(0,234,83,1);
                transition: all 0.3s ease;
            }

            .btn-3 span:before {
                width: 2px;
                height: 0%;
            }

            .btn-3 span:after {
                width: 0%;
                height: 2px;
            }

            .btn-3 span:hover:before {
                height: 100%;
            }

            .btn-3 span:hover:after {
                width: 100%;
            }

        .error-rait {
            display: block;
            font-size: 1em;
            margin-block-start: 0.53em;
            margin-block-end: 0.83em;
            margin-inline-start: 11px;
            margin-inline-end: 0px;
        }
    </style>
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder" runat="Server">
    <h1>מדריך #C</h1>
    <br />
    <p><small>(כדי לגשת לתכני האתר יש להרשם לאתר)</small></p>
    <br />
    <p>במדריך זה אנו נלמד את יסודות השפה #C</p>
    <p>שפת #C (מבוטא סי שארפ) היא שפת תכנות שפותחה ע”י מיקרוסופט ונחשבת לאחת משפות התכנות הפופולריות בעולם. היא מיועדת לפיתוח כללי של מגוון אפליקציות בכל התחומים – מאתרי Web, דרך משחקים, מאפליקציות למכשירי מובייל וטאבלטים ועד לשירותי ענן. התחביר והעקרונות שלה הם פשוטים מצד אחד אך עשירים ביכולות מצד שני.</p>
    <br />
    <p>
        ידיעת השפה #C היא תנאי הכרחי לצורך שימוש במגוון טכנולוגיות כגון:
    </p>
    <br />
    <ul style="margin-right: inherit">
        <li>פיתוח תוכנות Command Line) Console Applications)</li>
        <li>פיתוח תוכנות בעלות ממשק משתמש גרפי בעזרת WinForms או WPF</li>
        <li>פיתוח מערכות לאתרי אינטרנט מתקדמים בעזרת ASP.NET ו- HTML5</li>
        <li>פיתוח משחקים בתוכנת Unity</li>
    </ul>
    <br />
    <div></div>
    <span style="font-size:1.5rem;font-weight:bold;">הדירוג שלנו: <i style="color:#FD4" class="fa fa-star"></i><%=raiting %><small style="font-weight:normal">(<%=numOfVotes %> מצבעים)</small></span>
    <fieldset>
        <legend style="font-size: 1.5rem; margin-right: 1rem">דרגו אותנו:</legend>
        <form method="post" class="stars">
            <input class="star star-5" id="star-5" type="radio" value="5" name="star" />
            <label class="star star-5" for="star-5"></label>
            <input class="star star-4" id="star-4" type="radio" value="4" name="star" />
            <label class="star star-4" for="star-4"></label>
            <input class="star star-3" id="star-3" type="radio" value="3" name="star" />
            <label class="star star-3" for="star-3"></label>
            <input class="star star-2" id="star-2" type="radio" value="2" name="star" />
            <label class="star star-2" for="star-2"></label>
            <input class="star star-1" id="star-1" type="radio" value="1" name="star" />
            <label class="star star-1" for="star-1"></label>
            <button type="submit" name="submit" value="submit" class="custom-btn btn-3"><span>שלח דירוג</span></button>
        </form>
        <br />
        <br />
        <span class="error-rait"><%=errors %></span>

    </fieldset>

</asp:Content>

