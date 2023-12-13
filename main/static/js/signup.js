console.log("Hi");

$("#send-sms").click(function () {
    $("#send-sms").attr("disabled", "disabled");
    $("#phone_number").attr("readonly", "readonly");
    $.ajax({
        method: "POST",
        url: "/sendcode/",
        data: { phone_number: $("#phone_number").val() },
        statusCode: {
            200: function() {
                console.log("SEND!");
                $("#send-sms").text("ارسال شد!");
                $("#code").removeAttr("disabled");
            },
            400: function() {
                $("#send-sms").removeAttr("disabled");
                $("#send-sms").text("دوباره تلاش کنید!");
                $("#phone_number").removeAttr("readonly");
            },
            500: function() {
                $("#send-sms").removeAttr("disabled");
                $("#send-sms").text("دوباره تلاش کنید!");
                $("#phone_number").removeAttr("readonly");
            }
          }
    });
})