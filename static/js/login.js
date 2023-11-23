$(document).ready(function() {
    $('#Form').submit(function(event) {
        event.preventDefault(); // Prevent form submission
        var formData = new FormData(); // Create a FormData object
        var userType = $('input[name="inlineRadioOptions"]:checked').val();
  
        // Append the form fields to the FormData object
        uname = $('#uname').val()
        formData.append('uname', uname);
        formData.append('passw', $('#password').val());
        formData.append('userType', userType);
  
        $.ajax({
            url: '/login/',
            method: 'POST',
            data: formData,
            contentType: false, // Prevent jQuery from setting content type
            processData: false, // Prevent jQuery from processing the data
            success: function(response) {
                //alert(response.msg);
                res = response.msg;
                if (res===true){
                  window.location.href = `/admin?uname=${uname}`; 
                }
                else if (res==="pilot"){
                  window.location.href = `/locate?uname=${uname}`; 
                }
                else{
                  $('#message').text("Invalid User or Password. Try again")
                }
                /*
                if (response.message == "LoginFailed"){
                  $('#message').text("Invalid User or Password. Try again");
                }
                else if(response.message == "LoginSuccessful"){
                  window.location.href = "/";
                }
                */
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
        // Reset the form items
        document.getElementById("Form").reset();
    });
  });