var intervalId = null; // Initialize the interval ID
var oldLat = 0.0
var oldLong = 0.0

$(document).ready(function() {
    $('#userid').css("color", "red");
    $('#Form').submit(function(event) {
        event.preventDefault();  
      
        // Check if an interval is already running
        if (intervalId === null) {
            intervalId = setInterval(sendData, 2000);
            alert('location staring started please wait')
        }
    });

    $('.stop').click(function(event) {

        //console.log("Stopped");
        $("#location").html(`Latitude: 0.00 <br> Longitude: 0.00`)
        // Clear the interval when the "Stop" button is clicked
        pilotId = $('#userid').text()
        busID = $('#id').val()
        makeOffline(pilotId,busID)
        clearInterval(intervalId);
        intervalId = null;
    });
});

async function sendData() {
    if ("geolocation" in navigator) {
        try {
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject);
            });

            const formData = new FormData();
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            formData.append('id', $('#id').val());
            formData.append('from', $('#from').val());
            formData.append('to', $('#to').val());
            formData.append('pilot', $('#userid').text());
            formData.append('message', $('#msg').val());
            formData.append('latitude', latitude);
            formData.append('longitude', longitude);

            if (oldLat !== latitude || oldLong !== longitude) {
                const response = await $.ajax({
                    url: '/locate',
                    method: 'POST',
                    data: formData,
                    contentType: false,
                    processData: false,
                });

                console.log(response.msg);
                $('#userid').css("color", "green");
                $("#location").html(`Latitude: ${latitude} <br> Longitude: ${longitude}`);
                oldLat = latitude;
                oldLong = longitude;
            }
        } catch (error) {
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    $("#location").html("User denied the request for geolocation.");
                    break;
                case error.POSITION_UNAVAILABLE:
                    $("#location").html("Location information is unavailable.");
                    break;
                case error.TIMEOUT:
                    $("#location").html("The request to get user location timed out.");
                    break;
                case error.UNKNOWN_ERROR:
                    $("#location").html("An unknown error occurred.");
                    break;
                default:
                    console.error(error);
            }
        }
    } else {
        $("#location").html("Geolocation is not available in this browser.");
    }
}



function makeOffline(pilotId,busID){
    var formData = new FormData();
    formData.append("username",pilotId)
    formData.append("busiD",busID)
    $.ajax({
        url: '/makeoffline',
        method: 'POST',
        data: formData,
        contentType: false, // Prevent jQuery from setting content type
        processData: false, // Prevent jQuery from processing the data
        success: function(response) {
            document.getElementById("Form").reset();
            if (response.msg==true){
                alert("Location Sharing Stopped")
                location.reload();}

        },
        error: function(error) {
            console.log(error)
        }
    });
}