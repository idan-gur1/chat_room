var form = document.getElementById('form');
var firstname = document.getElementById('fName');
var lastname = document.getElementById('lName');
var email = document.getElementById('email');
var password = document.getElementById('password');
var passwordSame = document.getElementById('passwordSame');


// Check email
function checkEmail(id) {
    var thisEmail = document.getElementById(id);
    const re = /^[a-zA-z0-9@._-]+$/;
    if (thisEmail.value.trim() === '') {
        document.getElementById("err-"+id).innerText = "נא למלא את השדה";
        thisEmail.classList.remove("sucess-input");
        thisEmail.classList.add("err-input");
        return false;
    } else if (!thisEmail.value.match(re) || !thisEmail.value.includes("@") ||
        !thisEmail.value.includes(".") || thisEmail.value.split('@').length != 2 ||
        thisEmail.value.indexOf('@') == 0 || thisEmail.value.indexOf('@') == thisEmail.value.length - 1 ||
        thisEmail.value.indexOf('.') == 0 || thisEmail.value.lastIndexOf('.') == thisEmail.value.length - 1 ||
        thisEmail.value.indexOf('-') == 0 || thisEmail.value.lastIndexOf('-') == thisEmail.value.length - 1 ||
        thisEmail.value.includes("@.") || thisEmail.value.includes(".@") || thisEmail.value.length < 5 ||
        thisEmail.value.length > 50) {
        document.getElementById("err-" + id).innerText = "יש להכניס אימייל תקין";
        thisEmail.classList.remove("sucess-input");
        thisEmail.classList.add("err-input");
        return false;
    } else {
        document.getElementById("err-" + id).innerText = "";
        thisEmail.classList.add("sucess-input");
        thisEmail.classList.remove("err-input");
        return true;
    }
}

// Check phone
function checkPhone(id) {
    var thisPhone = document.getElementById(id);
    const re = /[0-9+-]+$/;
    if (thisPhone.value.trim() === '') {
        document.getElementById("err-" + id).innerText = "נא למלא את השדה";
        thisPhone.classList.remove("sucess-input");
        thisPhone.classList.add("err-input");
        return false;
    } else if ((thisPhone.value.includes('+') && thisPhone.value.indexOf('+') != 0) || !thisPhone.value.match(re) ||
        thisPhone.value.length < 10 || thisPhone.value.length > 20 || thisPhone.value.indexOf('0') != 0) {
        document.getElementById("err-" + id).innerText = "יש להכניס טלפון תקין";
        thisPhone.classList.remove("sucess-input");
        thisPhone.classList.add("err-input");
        return false;
    } else {
        document.getElementById("err-" + id).innerText = "";
        thisPhone.classList.add("sucess-input");
        thisPhone.classList.remove("err-input");
        return true;
    }
}

// Check password if it is greater than 6 and lesser than 25
function checkPassword(id, min, max) {
    var thisPassword = document.getElementById(id);
    if (thisPassword.value.trim() === '') {
        document.getElementById("err-" + id).innerText = "נא למלא את השדה";
        thisPassword.classList.remove("sucess-input");
        thisPassword.classList.add("err-input");
        return false;
    } else if (thisPassword.value.length < min) {
        document.getElementById("err-" + id).innerText = "יש להאריך את הסיסמא";
        thisPassword.classList.remove("sucess-input");
        thisPassword.classList.add("err-input");
        return false;
    } else if (thisPassword.value.length > max) {
        document.getElementById("err-" + id).innerText = "יש לקצר את הסיסמא";
        thisPassword.classList.remove("sucess-input");
        thisPassword.classList.add("err-input");
        return false;
    } else {
        document.getElementById("err-" + id).innerText = "";
        thisPassword.classList.add("sucess-input");
        thisPassword.classList.remove("err-input");
        return true;
    }
}

/**/

// Check first name if its length greater than 1 and lesser than 20 characters
function checkFirstName(id, min, max) {
    var thisFirstName = document.getElementById(id);
    const re = /[א-תA-Za-z]+$/;
    if (thisFirstName.value.trim() === '') {
        document.getElementById("err-" + id).innerText = "יש למלא את השדה";
        thisFirstName.classList.remove("sucess-input");
        thisFirstName.classList.add("err-input");
        return false;
    } else if (thisFirstName.value.length < min) {
        document.getElementById("err-" + id).innerText = "יש להאריך את השדה";
        thisFirstName.classList.remove("sucess-input");
        thisFirstName.classList.add("err-input");
        return false;
    } else if (thisFirstName.value.length > max) {
        document.getElementById("err-" + id).innerText = "יש לקצר את השדה";
        thisFirstName.classList.remove("sucess-input");
        thisFirstName.classList.add("err-input");
        return false;
    } else if (!thisFirstName.value.match(re)) {
        document.getElementById("err-" + id).innerText = "יש להכניס רק אותיות לשם";
        thisFirstName.classList.remove("sucess-input");
        thisFirstName.classList.add("err-input");
        return false;
    } else {
        document.getElementById("err-" + id).innerText = "";
        thisFirstName.classList.add("sucess-input");
        thisFirstName.classList.remove("err-input");
        return true;
    }
}

// Check last name if its length greater than 1 and lesser than 20 characters
function checkLastName(id, min, max) {
    var thisLastName = document.getElementById(id);
    const re = /[א-תA-Za-z]+$/;
    if (thisLastName.value.trim() === '') {
        document.getElementById("err-" + id).innerText = "יש למלא את השדה";
        thisLastName.classList.remove("sucess-input");
        thisLastName.classList.add("err-input");
        return false;
    } else if (thisLastName.value.length < min) {
        document.getElementById("err-" + id).innerText = "יש להאריך את השדה";
        thisLastName.classList.remove("sucess-input");
        thisLastName.classList.add("err-input");
        return false;
    } else if (thisLastName.value.length > max) {
        document.getElementById("err-" + id).innerText = "יש לקצר את השדה";
        thisLastName.classList.remove("sucess-input");
        thisLastName.classList.add("err-input");
        return false;
    } else if (!thisLastName.value.match(re)) {
        document.getElementById("err-" + id).innerText = "יש להכניס רק אותיות לשם";
        thisLastName.classList.remove("sucess-input");
        thisLastName.classList.add("err-input");
        return false;
    } else {
        document.getElementById("err-" + id).innerText = "";
        thisLastName.classList.add("sucess-input");
        thisLastName.classList.remove("err-input");
        return true;
    }
}


/**//**//**//**//**//**//**//**/

function fullCheckDeleteUser() {
    var bool = true;
    if (!checkEmail("email")) {
        bool = false;
    }
    if (!checkPassword("password", 6, 25)) {
        bool = false;
    }

    return bool;
}

function fullCheckUpdatePhone() {
    var bool = true;
    if (!checkEmail("email")) {
        bool = false;
    }
    if (!checkPassword("password", 6, 25)) {
        bool = false;
    }
    if (!checkPhone("newPhone")) {
        bool = false;
    }

    return bool;
}

function fullCheckUpdatePassword() {
    var bool = true;
    if (!checkEmail("email")) {
        bool = false;
    }
    if (!checkPassword("oldPassword", 6, 25)) {
        bool = false;
    }
    if (!checkPassword("newPassword", 6, 25)) {
        bool = false;
    }
    return bool;
}

function fullCheckUpdateEmail() {
    var bool = true;
    if (!checkEmail("email")) {
        bool = false;
    }
    if (!checkPassword("password", 6, 25)) {
        bool = false;
    }
    if (!checkEmail("newEmail")) {
        bool = false;
    }

    return bool;
}

function fullCheckLogin() {
    var bool = true;
    if (!checkEmail("email")) {
        bool = false;
    }
    if (!checkPassword("password", 6, 25)) {
        bool = false;
    }

    return bool;
}

function fullCheckRegister() {
    var bool = true;
    if (!checkEmail("email")) {
        bool = false;
    }
    if (!checkPhone("phone")) {
        bool = false;
    }
    if (!checkFirstName("fName", 1, 20)) {
        bool = false;
    }
    if (!checkLastName("lName", 2, 20)) {
        bool = false;
    }
    if (!checkPassword("password", 6, 25)) {
        bool = false;
    }

    return bool;
}