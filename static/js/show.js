$(document).ready(function() {
    $(".onlineStatus").each(function() {
        var status = $(this).text();
        if (status === "True") {
          $(this).css("color", "green");
        } else if (status === "False") {
          $(this).css("color", "red");
        }
        // Add more conditions for other status values as needed
      });
    const backButton = document.getElementById("backButton");
    if (backButton !== null){
        backButton.addEventListener("click", function() {
        history.back();
        });
    }  
});        