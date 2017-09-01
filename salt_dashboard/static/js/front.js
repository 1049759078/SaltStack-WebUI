/*global $, document, Chart, LINECHART, data, options, window*/
$(document).ready(function () {

    'use strict';

    // Main Template Color
    var brandPrimary = '#33b35a';

    // ------------------------------------------------------- //
    // Custom Scrollbar
    // ------------------------------------------------------ //

    if ($(window).outerWidth() > 992) {
        $("nav.side-navbar").niceScroll({
            cursorcolor: brandPrimary,
            cursorwidth: '3px',
            cursorborder: 'none'
        });
    }


    // ------------------------------------------------------- //
    // Side Navbar Functionality
    // ------------------------------------------------------ //
    $('#toggle-btn').on('click', function (e) {

        e.preventDefault();

        if ($(window).outerWidth() > 1194) {
            $('nav.side-navbar').toggleClass('shrink');
            $('.basepage').toggleClass('active');
        } else {
            $('nav.side-navbar').toggleClass('show-sm');
            $('.basepage').toggleClass('active-sm');
        }
    });
});
