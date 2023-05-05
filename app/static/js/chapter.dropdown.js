var btnDrop = $("#chapter-drop");
var listMenu = $("#chapter-list");
var btnDrop2 = $("#chapter-drop2");
var listMenu2 = $("#chapter-list2");

btnDrop.click(function () {
    if (!listMenu.hasClass("visible"))
        listMenu.addClass("visible")
    else
        listMenu.removeClass("visible")
});

btnDrop2.click(function () {
    if (!listMenu2.hasClass("visible"))
        listMenu2.addClass("visible")
    else
        listMenu2.removeClass("visible")
});