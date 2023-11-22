  // Initialize the map when the Google Maps API script is loaded
  //var busId = $("#busid").val()
  var latitude = "32.1034"
  var longitude = "76.1659"
  function initMap() {
      var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 15,
          center: { lat: 0, lng: 0 }, // Default center
          mapTypeId: google.maps.MapTypeId.SATELLITE, // Set the default map type to satellite
          label: { text: 'Default Label', fontSize: '26px', color: 'white' } // Enable default map label
        });
        

    var marker; // Initialize the marker variable
    var mapData; // Store map data received from AJAX

    // Function to update the map location based on data
    function updateMapLocation() {
      if (marker) {
        marker.setMap(null); // Remove the previous marker
      }
      var lat = parseFloat(latitude); // Ensure it's a valid number
      var long = parseFloat(longitude); // Ensure it's a valid number
      console.log(lat,long)

      if (!isNaN(lat) && !isNaN(long)) {
        marker = new google.maps.Marker({
          position: { lat: lat, lng: long },
          map: map,
          title: 'Location'
        });

        // Center the map on the new location
        map.setCenter(marker.getPosition());
      } else {
        console.log('Invalid latitude or longitude data');
        // var latitude = 32.1034
        // var longitude = 76.1659
      }
    }

    // AJAX request to get data and update the map
    function getDataAndRefreshMap() {
      var busId = $('#busid').val();
      var start = $("#start").val()
      var dest = $("#destination").val()
      if (busId === ""){
        busId=1
      }
      // console.log("==========================")
      // console.log(busId)
      // console.log("==========================")
      $.ajax({
        url: `/getData`,
        method: 'GET',
        data:{"id":busId,"start":start,"dest":dest},
        success: function(response) {
          mapData = response;
          updateMapLocation();
          settable(response.data)
        },
        error: function(error) {
          console.log('Error:', error);
        }
      });
    }

    //Call the initial data load
    //getDataAndRefreshMap();

    // Update the map every 5 seconds (adjust the interval as needed)
    setInterval(getDataAndRefreshMap, 1000);
  }

  function settable(data) {
    var tableContainer = $("#tabledata");

    // Clear the table content
    tableContainer.empty();

    // Add a header row to the table
    var table = $("<table>").addClass("table");
    var headerRow = $("<tr>").appendTo(table);
    $("<th>").text("Sr No.").appendTo(headerRow);
    $("<th>").text("Bus ID").appendTo(headerRow);
    $("<th>").text("From").appendTo(headerRow);
    $("<th>").text("To").appendTo(headerRow);
    $("<th>").text("Message").appendTo(headerRow);
    $("<th>").text("Location").appendTo(headerRow);

    // Iterate through the data and create table rows for each entry
    for (let i = 0; i < data.length; i++) {
        var results = data[i];
        var srno = i+1
        var id = results.busID;
        var from = results.from;
        var to = results.to;
        var message = results.msg;

        var newRow = $("<tr>").appendTo(table);
        $("<td>").text(srno).appendTo(newRow);
        $("<td>").text(id).appendTo(newRow);
        $("<td>").text(from).appendTo(newRow);
        $("<td>").text(to).appendTo(newRow);
        $("<td>").text(message).appendTo(newRow);
        var trackLink = $("<a>").text("Track").attr("href", "javascript:void(0)").click(function() {
            latitude = results.latitude
            longitude = results.longitude
         });
        $("<td>").append(trackLink).appendTo(newRow);

        // Add the location column as needed.
    }

    // Append the table to the tableContainer div
    table.appendTo(tableContainer);
}