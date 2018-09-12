/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('theme_pharmacistplace.theme', function (require) {
    "use strict";

    function numberWithCommas(number) {
        // https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    //Simple Animated Counter on Scroll  https://codepen.io/dmcreis/pen/VLLYPo
    function animateNumber($this) {
        var countTo = $this.attr('data-count');
        $({
            countNum: $this.text()
        }).animate({
            countNum: countTo
        },
        {
            duration: 2000,
            easing: 'swing',
            step: function () {
                $this.text(Math.floor(this.countNum));
            },
            complete: function () {
                $this.text(numberWithCommas(this.countNum)); //number with comma
                // $this.text(this.countNum);
            }
        });
    }

    var scroll_down = 0;
    $(document).ready(function () {
        $('.wk_js_count span').each(function () {
            if ($(".wk_js_count_label")[0].getBoundingClientRect().bottom <= window.innerHeight){
                // console.log("-----NOT SCROLL BAR---------=", $(this).offset().top - window.innerHeight );
                animateNumber($(this));
                scroll_down = 1;
            }
        });
    });

    $(window).scroll(function () {
        // var oTop = $('.wk_js_count_div').offset().top - window.innerHeight;
        if (scroll_down == 0 && $(".wk_js_count_label")[0].getBoundingClientRect().bottom <= window.innerHeight) {
            // console.log("-----HAS SCROLL BAR---------=" );
            $('.wk_js_count span').each(function () {
                animateNumber($(this));
            });
            scroll_down = 1;
        }
    });
});
