$("#sbpc").click(function(){
    $("#pincode_div").show();
    $("#district_div").hide();
    $("#main_dropdown").html($("#sbpc").html());
    $("#btnpincode").attr("data-seven","false");
});

$("#sbd").click(function(){
    $("#pincode_div").hide();
    $("#district_div").show();
    $("#main_dropdown").html($("#sbd").html());
    $('#selectState').html("Select State");
    $("#sdid").html("Select District");
    $("#btndist").attr("data-seven","false");
});

$("#sbpc7").click(function(){
    $("#pincode_div").show();
    $("#district_div").hide();
    $("#main_dropdown").html($("#sbpc7").html());
    $("#btnpincode").attr("data-seven","true");
});

$("#sbd7").click(function(){
    $("#pincode_div").hide();
    $("#district_div").show();
    $("#main_dropdown").html($("#sbd7").html());
    $('#selectState').html("Select State");
    $("#sdid").html("Select District");
    $("#btndist").attr("data-seven","true");
});

$(".state-dropdown").click(function(){
    var state = $(this).html();
    $('#selectState').html(state);
    $("#sdid").html("Select District");
    $.ajax({
        url: "/getdistrict/",
        type: "POST",
        data: {"state":state},
        success: function(data, textStatus, jqXHR) {
            $("#districtdropdown").html(data.data);
            $("#district_div_id").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
        }
    });

});

$(document).on('click','.district-dropdown',function(){
       $("#sdid").html($(this).html());
    });

$(document).ready(function(){
    $("#sbpc").click();
    $("#district_div_id").hide();
});

function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}

$("#btnpincode").click(function(){
    var pin = $("#pincode").val();
    var att  = $("#btnpincode").attr('data-seven');
    var date = $("#example-date-input").val();
    if (pin == "" || date == ""){
        alert("Enter Pincode/Date");
        return false;
    }
    formData = {"pin":pin, "att":att, "date":date};
    $.ajax({
        url: "/findbypin/",
        type: "POST",
        data: formData,
        success: function(data, textStatus, jqXHR) {
            $("#card-deck-tabs").html(data.data);
            var elmnt = document.getElementById("card-deck-tabs");
            elmnt.scrollIntoView();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#card-deck-tabs").html("Something Went Wrong");
            var elmnt = document.getElementById("card-deck-tabs");
            elmnt.scrollIntoView();
        }
    });

});

$("#btndist").click(function(){
    var selstate = $("#selectState").html();
    var seldist = $("#sdid").html()
    var att  = $("#btndist").attr('data-seven');
    var date = $("#example-date-input-dis").val();
    if (selstate == "Select State" || seldist == "Select District" || date == ""){
        alert("Select State/District/Date");
        return false;
    }
    formData = {"selstate":selstate, "seldist":seldist, "att":att, "date":date};
    $.ajax({
        url: "/findbydistrict/",
        type: "POST",
        data: formData,
        success: function(data, textStatus, jqXHR) {
            $("#card-deck-tabs").html(data.data);
            var elmnt = document.getElementById("card-deck-tabs");
            elmnt.scrollIntoView();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#card-deck-tabs").html("Something Went Wrong");
            var elmnt = document.getElementById("card-deck-tabs");
            elmnt.scrollIntoView();
        }
    });
});

