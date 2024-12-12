// --------------- Функції для відкриття та закриття бічного меню ------------------------

function openNav(menuId) {
    const menu = document.getElementById(menuId);
    menu.style.width = "400px";
    menu.style.opacity = "1";
}

function closeNav(menuId) {
    const menu = document.getElementById(menuId);
    menu.style.width = "0";
}

// --------------- Функції для відкриття та закриття меню курсу валют --------------------

function openTable(menuId) {
    const menu = document.getElementById(menuId);
    menu.style.width = "300px";
    menu.style.height = "200px";
    menu.style.display = "block";
}

function closeTable(menuId) {
    document.getElementById(menuId).style.width = "0";
    document.getElementById(menuId).style.height = "0";
    document.getElementById(menuId).style.display = "none";
}