console.log('DOM content loaded!');

// Slick-carousel script
$('.scrolling-images').slick({
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 100,
    speed: 10000,
    pauseOnHover: false,
});

// Navbar
$('.navbar-toggler').click(function () {
    console.log("clicked");
    var navbarCollapse = $('#navbarNav');
    navbarCollapse.toggleClass('show');
});




