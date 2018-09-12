/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('mp_seller_wise_checkout_theme_compatibility.mp_pharmacist_details_theme', function (require) {

    var ajax = require('web.ajax');

    $(document).ready(function() {

            $('a[href*="/shop/distributor_activate"]').on("click", function(ev) {
                ev.preventDefault();
                ev.stopPropagation();
                var href = $(this).attr('href')
                var seller = href.substring((href.indexOf('seller=')-1)) // this gives ?seller=51
                var seller_id = seller.slice(seller.indexOf('=') + 1).split('&')[0];
                if (seller != seller_id){
                    seller_id= parseInt(seller_id)
                }
                ajax.jsonRpc('/seller/wise/checkout', 'call', {
                    'seller_id': seller_id,
                }).done(function(res) {
                  window.location.href = '/shop/distributor_activate';
                });
            });

            $('#search_pharmacy_id').on('click', function(event){
                pharmacy_account_id = document.getElementById("search_distributor_id").value
                if (pharmacy_account_id == ''){
                    $(".search_pharmacy_error_msg").addClass("text text-danger")
                    $(".search_pharmacy_error_msg").html("Please enter Id")
                }
                else{
                    ajax.jsonRpc("/pharmacy/account/search", "call", {
                        "pharmacy_account_id": pharmacy_account_id,
                    })
                    .then(function (data) {
                        if (data){
                            $(".search_pharmacy_error_msg").addClass("text text-success")
                            $(".search_pharmacy_error_msg").html("Pharmacy Id found :-)")
                        }
                        else{
                            $(".search_pharmacy_error_msg").addClass("text text-danger")
                            $(".search_pharmacy_error_msg").html("Pharmacy Id not found :-)")
                        }
                    })
                }
            })


    })

})
