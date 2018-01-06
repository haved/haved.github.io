const HOME_BUTTON_ID = "headerHomeButton";
const DAF_BUTTON_ID = "headerDafButton";
const HEADER_FILE = "header.html"

function loadHeader(div, buttonName=null) {
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            div.innerHTML = this.responseText;
            let button = document.getElementById(buttonName);
            if(button) {
                button.setAttribute("class", button.getAttribute("class")+" active");
                button.href="#";
            }
        } else {
            div.innerHTML = "Header was supposed to be here <br><hr>";
        }
    }
    xhttp.open("GET", HEADER_FILE, true);
    xhttp.send();
}