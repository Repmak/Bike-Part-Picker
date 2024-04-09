
function publicorpriv() {
    if (document.getElementById("publicorpriv").checked === false) {
        document.getElementById("publicorpriv").checked = true;
        document.getElementById("publicorprivtitle").innerHTML = 'Privacy setting: Public';
        document.getElementById("publicorpriv").value = "public1";
    }
    else {
        document.getElementById("publicorpriv").checked = false;
        document.getElementById("publicorprivtitle").innerHTML = 'Privacy setting: Private';
        document.getElementById("publicorpriv").value = "private0";
    }
}