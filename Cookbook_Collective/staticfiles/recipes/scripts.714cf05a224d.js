/**
 * DOM content loaded event handler.
 * @event
 */
console.log('DOM content loaded!');

/**
 * Initialize slick-carousel for scrolling images.
 * @function
 * @param {Object} settings - Slick-carousel settings.
 */
$('.scrolling-images').slick({
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 100,
    speed: 10000,
    pauseOnHover: false,
});

/**
 * Click event handler for the navbar-toggler button.
 * @event
 */
$('.navbar-toggler').click(function () {
    console.log("Navbar toggler clicked");
    var navbarCollapse = $('#navbarNav');
    navbarCollapse.toggleClass('show');
});
