
/*slick-carousel script*/
$(document).ready(function(){
    $('.scrolling-images').slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 1, // Change this to 1
        autoplay: true,
        autoplaySpeed: 100,
        speed: 10000, // Adjust the speed for a smoother continuous scroll
        pauseOnHover: false, // Allow continuous scroll even on hover
    });
});

//NAVBAR
document.addEventListener('DOMContentLoaded', function () {
    var navbarButton = document.querySelector('.navbar-toggler');
    var navbarCollapse = document.getElementById('navbarNav');

    navbarButton.addEventListener('click', function () {
        var expanded = navbarButton.getAttribute('aria-expanded') === 'true';
        navbarButton.setAttribute('aria-expanded', !expanded);
        navbarCollapse.classList.toggle('show'); // If you want to toggle the 'show' class as well
    });
});
   

//LOADING SPINNER  
document.getElementById('submitBtn').addEventListener('click', function() {
    document.getElementById('loading-spinner').style.display = 'block';
});