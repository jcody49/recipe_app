console.log('Script loaded!');

//$(document).ready(function () {
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

    // Loading Spinner
    $('#submitBtn').click(function () {
        $('#loading-spinner').css('display', 'block');
    });
//});

$('#submitBtn').click(function () {
    // Show the loading spinner
    $('#loading-spinner').css('display', 'block');

    // Perform your loading operation (e.g., AJAX request)
    // ...

    // Assuming the loading is complete, hide the loading spinner
    $('#loading-spinner').css('display', 'none');
});
