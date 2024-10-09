const toggleButton = document.getElementById('toggleButton');
const menu = document.getElementById('menu');

toggleButton.addEventListener('click', function () {
    menu.classList.toggle('toolbar-expanded');
});
