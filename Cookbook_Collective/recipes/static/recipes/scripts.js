document.addEventListener('DOMContentLoaded', function() {
    // slick-carousel script
    $('.scrolling-images').slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 100,
        speed: 10000,
        pauseOnHover: false,
    });

    // NAVBAR
    var navbarButton = document.querySelector('.navbar-toggler');
    var navbarCollapse = document.getElementById('navbarNav');

    navbarButton.addEventListener('click', function () {
        var expanded = navbarButton.getAttribute('aria-expanded') === 'true';
        navbarButton.setAttribute('aria-expanded', !expanded);
        navbarCollapse.classList.toggle('show');
    });

    // LOADING SPINNER
    var submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.addEventListener('click', function() {
            document.getElementById('loading-spinner').style.display = 'block';
        });
    }
});
