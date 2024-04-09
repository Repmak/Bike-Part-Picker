const emailpattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
const usernamepattern = /^[a-zA-Z0-9_.-]{3,30}$/;
const passwordpattern = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,256}$/;


function checkemail() {
  if (document.getElementById("email").value.match(emailpattern)) {
    document.getElementById("email").classList.remove("inputinvalid");
    return true;
  }
  else {  /* EMAIL DOES NOT MATCH THE REGEX FILTER */
    document.getElementById("email").classList.add("inputinvalid");
    return false;
  }
}


function checkusername() {
  if (document.getElementById("username").value.match(usernamepattern)) {
    document.getElementById("username").classList.remove("inputinvalid");
    return true;
  }
  else {  /* EMAIL DOES NOT MATCH THE REGEX FILTER */
    document.getElementById("username").classList.add("inputinvalid");
    return false;
  }
}


function checkpassword() {
  if (document.getElementById("password").value.match(passwordpattern)) {
    document.getElementById("password").classList.remove("inputinvalid");
    return true;
  }
  else {  /* EMAIL DOES NOT MATCH THE REGEX FILTER */
    document.getElementById("password").classList.add("inputinvalid");
    return false;
  }
}


function checkinputs() {
  var email = checkemail.call(this)
  var username = checkusername.call(this)
  var password = checkpassword.call(this)
  if (email && username && password) {
    document.getElementById("submitbutton").classList.remove("submitbuttoninvalid");
  }
  else {
    document.getElementById("submitbutton").classList.add("submitbuttoninvalid");
  }
}


function regexcheck() {
  var email = checkemail.call(this)
  var username = checkusername.call(this)
  var password = checkpassword.call(this)
  if (email && username && password) {
    return true;
  }
  else {
    return false;
  }
}