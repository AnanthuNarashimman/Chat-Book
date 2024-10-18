const hamlist = document.querySelector('.navlinks');
const hambtn = document.querySelector('.hambur');

hambtn.addEventListener('click', function() {
    hambtn.classList.toggle('hamactive');
    hamlist.classList.toggle('active');
})