var e = document.getElementById("ML_QA");


function selected() {
    var selected_QA = e.selectedIndex;
    var elem1 = document.getElementById("elem1");
    var elem2 = document.getElementById("elem2");

    elem1.style.visibility = "visible";
    elem2.style.visibility = "visible";

    if (selected_QA == 0){
        elem2.style.visibility = "hidden";

    }
    else{
        elem1.style.visibility = "hidden";
    }
}