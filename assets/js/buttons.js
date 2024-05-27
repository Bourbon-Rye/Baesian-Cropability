var btn = document.querySelectorAll(".primary");
var modals = document.querySelectorAll('.modal');
var X = document.getElementsByClassName("button-round close");
var exit = document.getElementsByClassName("close-text");
var menu = document.getElementById("menu");
var nav = document.getElementsByClassName('navmen');


// When the user clicks the button, open the modal
for (var i = 0; i < btn.length; i++) {
    btn[i].onclick = function(e) {
        e.preventDefault();
        modal = document.querySelector(e.target.getAttribute("href"));
        modal.style.display = "block";
    }
}

for (var i = 0; i < nav.length; i++) {
    nav[i].onclick = function(e) {
        e.preventDefault();
        modal = document.querySelector(e.target.getAttribute("href"));
        modal.style.display = "block";
    }
}

// When the user clicks on(x), close the modal
for (var i = 0; i < X.length; i++) {
    X[i].onclick = function() {
        for (var index in modals) {
            if (typeof modals[index].style !== 'undefined') modals[index].style.display = "none";
        }
    }
}

for (var i = 0; i < exit.length; i++) {
    exit[i].onclick = function() {
        for (var index in modals) {
            if (typeof modals[index].style !== 'undefined') modals[index].style.display = "none";
        }
    }
}

function copy() {
    // Copy the text inside the text field
    navigator.clipboard.writeText("joshua.vonhofen@gmail.com").then(() => alert("E-mail copied!"));

    // Alert the copied text
    //alert("E-mail copied!");
}