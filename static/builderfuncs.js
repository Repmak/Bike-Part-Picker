
function startup(parts) {
    for (let i = 0; i < parts.length; i++) {
        document.getElementById(String(parts[i][1]) + "name").innerHTML = String(parts[i][2]);
        document.getElementById(String(parts[i][1]) + "price").innerHTML = String(parts[i][4]);
        if (parts[i][6] !== '-') {
            document.getElementById(String(parts[i][1]) + "retailernone").classList.toggle("hiddengrid");
            document.getElementById(String(parts[i][1]) + "retailer").classList.toggle("hiddengrid");
            document.getElementById(String(parts[i][1]) + "retailer").href = String(parts[i][6]);
            document.getElementById(String(parts[i][1]) + "retailer").innerHTML = String(parts[i][7]);
        }
        else {
            document.getElementById(String(parts[i][1]) + "retailernone").innerHTML = '-';
        }
        document.getElementById(String(parts[i][1]) + "button").value = "Delete";
        document.getElementById(String(parts[i][1]) + "button").classList.remove("selectbutton");
        document.getElementById(String(parts[i][1]) + "button").classList.add("selectbuttondelete");
    }
}


function framesetclick() {
    document.getElementById("category1").classList.toggle("hiddengrid");
    document.getElementById("category2").classList.toggle("hiddengrid");
    document.getElementById("category3").classList.toggle("hiddengrid");
}


function brakesclick() {
    document.getElementById("category12").classList.toggle("hiddengrid");
    document.getElementById("category13").classList.toggle("hiddengrid");
    document.getElementById("category14").classList.toggle("hiddengrid");
    document.getElementById("category15").classList.toggle("hiddengrid");
    document.getElementById("category16").classList.toggle("hiddengrid");
    document.getElementById("category17").classList.toggle("hiddengrid");
    document.getElementById("category18").classList.toggle("hiddengrid");
    document.getElementById("category19").classList.toggle("hiddengrid");
}

function wheelsclick() {
    document.getElementById("category4").classList.toggle("hiddengrid");
    document.getElementById("category5").classList.toggle("hiddengrid");
    document.getElementById("category6").classList.toggle("hiddengrid");
    document.getElementById("category7").classList.toggle("hiddengrid");
    document.getElementById("category8").classList.toggle("hiddengrid");
    document.getElementById("category9").classList.toggle("hiddengrid");
    document.getElementById("category10").classList.toggle("hiddengrid");
    document.getElementById("category11").classList.toggle("hiddengrid");
}