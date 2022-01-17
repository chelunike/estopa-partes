function setNum() {
    var e = document.getElementById('mySelect');
    a = e.options[e.selectedIndex].value;
    $("#rowCards").removeClass().addClass("row row-cols-1 g-4").addClass(a);
}