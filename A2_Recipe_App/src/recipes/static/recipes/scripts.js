$(document).ready(function(){
    $('.scrolling-images').slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 1000,
        autoplay: true,
        autoplaySpeed: 100,
        speed: 130000, // Adjust the speed for a smoother continuous scroll
        pauseOnHover: false, // Allow continuous scroll even on hover
    });
});