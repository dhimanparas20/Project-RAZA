$(document).ready(function () {   
    $("#addUser").submit(function (e) {
        e.preventDefault(); // Prevent the default form submission

        // Get form data
        var formData = $(this).serialize();

        //Send the data to the server using AJAX
        $.ajax({
            type: "POST", // You can change the HTTP method to match your server-side handling
            url: "/admin/", // Replace with your server endpoint
            data: formData,
            success: function (response) {
                // Handle the server's response here (e.g., show a success message)
                alert(response.msg)
                //console.log(response.msg)
            },
            error: function (error) {
                // Handle errors (e.g., show an error message)
                alert("Error: " + error);
            }
        });
        document.getElementById("addUser").reset();
    });

    $("#busForm").submit(function (e) {
        e.preventDefault(); // Prevent the default form submission

        // Get form data
        var formData = $(this).serialize();

        //Send the data to the server using AJAX
        $.ajax({
            type: "POST", // You can change the HTTP method to match your server-side handling
            url: "/addBus/", // Replace with your server endpoint
            data: formData,
            success: function (response) {
                // Handle the server's response here (e.g., show a success message)
                alert(response.msg)
                //console.log(response.msg)
            },
            error: function (error) {
                // Handle errors (e.g., show an error message)
                alert("Error: " + error);
            }
        });
        document.getElementById("busForm").reset();
    });

    const backButton = document.getElementById("backButton");
    if (backButton !== null){
      backButton.addEventListener("click", function() {
      history.back();
      });
    }  
});

function del(type){
    var deldata = $('#delid').val()
    if (deldata != ""){
        $.ajax({
            type: "POST",
            url: "/delete/",
            data: {"id":deldata,"type":type},
            success: function (response) {
                if (response.msg==true){
                  $('#delid').val('');
                  //console.log(response.msg)
                }  
            },
            error: function (error) {
                // Handle errors (e.g., show an error message)
                alert("Error: " + error);
            }
        });
    }
    else{
        alert("Empty ID")
    }
}
