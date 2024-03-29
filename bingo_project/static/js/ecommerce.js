// start for contact form
// $(document).ready(function () {
//     var $contactForm = $(".contact-form")
//     var $contactFormMethod = $contactForm.attr("method")
//     var $contactFormEndPoint = $contactForm.attr("action")


// function for loading spinner
//     function displaySubmitting(submitbutton, defaultText, doSubmit) {
//         if (doSubmit) {
//             submitbutton.addClass("disabled")
//             submitbutton.html("<i class='fa fa-spinner'></i> Submitting....")
//         } else {
//             submitbutton.removeClass("disabled")
//             submitbutton.html(defaultText)
//         }
//     }

//     $contactForm.submit(function (event) {
//         event.preventDefault()

//         var $contactFormBtn = $contactForm.find("[type='submit']")
//         var $contactFormBtnTxt = $contactFormBtn.text()

//         var $contactFormData = $contactForm.serialize()
//         var $thisForm = $(this)
//         displaySubmitting($contactFormBtn, "", true)
//         $.ajax({
//             method: $contactFormMethod,
//             url: $contactFormEndPoint,
//             data: $contactFormData,
//             success: function (data) {
//                 $thisForm[0].reset()
//                 $.alert({
//                     title: "Success",
//                     content: "Thanks for your submission!!",
//                     theme: "modern",
//                 })

//                 setTimeout(function () { displaySubmitting($contactFormBtn, $contactFormBtnTxt, false) }, 2000)
//             },
//             error: function (error) {
//                 // console.log(error.responseJSON)
//                 var $jsnData = error.responseJSON
//                 var $msg = ""
//                 $.each($jsnData, function (key, value) {
//                     $msg += key + ": " + value[0].message + "<br/>"
//                 })
//                 $.alert({
//                     title: "ops",
//                     content: $msg,
//                     theme: "modern",
//                 })

//                 setTimeout(function () { displaySubmitting($contactFormBtn, $contactFormBtnTxt, false) }, 2000)
//             }
//         })
//     })

// })

// // start for auto search script
// $(document).ready(function () {
//     // auto search
//     var $searchForm = $(".search-form")
//     var $searchInput = $searchForm.find("[name='q']")
//     var $typingTimer;
//     var $typingInterval = 500
//     var $searchButoon = $searchForm.find("[type='submit']")
//     $searchInput.keyup(function (event) {
//         // key released
//         clearTimeout($typingTimer)
//         $typingTimer = setTimeout(performSearch, $typingInterval)
//     })

//     $searchInput.keydown(function (event) {
//         //key pressed
//         clearTimeout($typingTimer)
//     })

//     function displaySearh() {
//         $searchButoon.addClass("disabled")
//         $searchButoon.html("<i class='fa fa-spinner'></i> Searching....")
//     }

//     function performSearch() {
//         displaySearh()
//         var $query = $searchInput.val()
//         setTimeout(function () {
//             window.location.href = '/search/?q=' + $query
//         }, 1000)
//     }

// })


// start for cart ajax
$(document).ready(function () {
    // cart ajax
    var $productForm = $('.form-product-ajax')
    $productForm.submit(function (e) {
        e.preventDefault();
        //console.log("Form is not submitting")
        var $thisForm = $(this)
        var $httpMethod = $(this).attr("method");
        //var $endpointAction  = $(this).attr("action");
        var $endpointAction = $(this).attr("data-endpoint");
        var $formData = $(this).serialize();

        $.ajax({
            url: $endpointAction,
            method: $httpMethod,
            data: $formData,
            success: function (data) {
                var $submitData = $thisForm.find(".submit_span")
                if (data.added) {
                    $submitData.html("<button type=\"submit\" class=\"btn btn-link\" style=\"padding:0\">Remove?</button>")
                } else {
                    $submitData.html("<button type=\"submit\" class=\"btn btn-success\">Add</button>")
                }
                var $cartItemCount = $(".itemCount")
                $cartItemCount.text(data.itemCount)
                var $currentPath = window.location.href
                if ($currentPath.indexOf("cart")) {
                    refreshCart();
                }

            },
            error: function (errorData) {
                console.log("error")
                console.log(errorData)
            }

        })
    })
    function refreshCart() {
        // ajax cart functionality
        //console.log("In current curt!");
        var $cartTable = $(".cart-table")
        var $cartTableBody = $(".cart-table-body")

        //$cartTableBody.html("<h1>Changed</h1>")
        var $productsRows = $cartTableBody.find('.cart-product')
        var $currentUrl = window.location.href

        var $refreshCartUrl = "/api/cart/"
        var $refreshCartMethod = "GET"
        var $data = {};

        $.ajax({
            url: $refreshCartUrl,
            method: $refreshCartMethod,
            data: $data,
            success: function (data) {
                alert("operation successful");
                var $hiddenClassRemeveForm = $(".remove-product-item")
                if (data.products.length > 0) {
                    $productsRows.html("")
                    i = data.products.length
                    $.each(data.products, function (index, value) {
                        var $newCartRemoveItem = $hiddenClassRemeveForm.clone()
                        //$newCartRemoveItem.css("display":"block")
                        $newCartRemoveItem.find(".cart-item-product-id").val(value.id)
                        $cartTableBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.title + "</a>" + $newCartRemoveItem.html() + "</td><td>" + value.price + "</td></tr>")
                        i--
                    })
                    $cartTableBody.find('.cart-subtotal').text(data.subtotal)
                    $cartTableBody.find('.cart-total').text(data.total)

                } else {
                    window.location.href = $currentUrl
                }
            },
            error: function (errorData) {
                console.log("Error!")
            }
        })
    }
})