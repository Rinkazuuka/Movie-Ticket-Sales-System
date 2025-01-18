$(document).ready(function () {
    $("#coupon-form").on("submit", function (event) {
        event.preventDefault(); 

        var coupon_code = $("#discount-code").val();  // pobierz kupon z formsa

        $.ajax({
            url: "/check_coupon",  
            method: "POST",
            data: {
                coupon_code: coupon_code  
            },
            success: function (response) {

                if (response.valid) {
                    // Kod działa
                    $("#discount-value").text("-" + response.discount + " zł");
                } else {
                    // Kod nie działa
                    $("#discount-value").text("Brak rabatu");
                }
            },
            error: function () {
                alert("Wystąpił błąd podczas sprawdzania kodu rabatowego.");
            }
        });
    });
});