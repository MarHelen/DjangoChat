
$(function() {

	 $('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});

    // AJAX for posting
    function create_post() {
        console.log("create post is working!") // sanity check
        $.ajax({
            url : "/chat/new_message/", // the endpoint
            type : "POST", // http method
            dataType: "json",
            data : { message_text : $('#message_text').val() }, // data sent with the post request
            // handle a successful response
            success : function(data) {
            	console.log($('#message_text').val());
            	alert('Your message has been sent successfuly')
                $('#message_text').val(''); // remove the value from the input
                //$('#form_message').append('  your message has been sent')
                console.log(data['result']); // log the returned json to the console
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

 	var last_message_id = 1

    setInterval(function(){my_function() }, 5000); 
     
    function my_function(){
    	console.log("Congrats!I'm in my_function!");
      $.getJSON('/content/', 
      	{ message_id: last_message_id }, //make data for get body requst, sending last outputed message id to backend for creating new message list
        function(data, status){
            console.log("Congrats!I'm in get function!"); //just sanity check
        	console.log(status);
        	last_message_id = data['id'] //update last message id for sending to backend
        	if (status == 'success'){    //if there is some data to update, make update
        		$.each( data['answer'], function(i,item){      
                    $('#refresh tr:last').after('<tr><td>'+ item +'</td></tr>')  //for every new message output it as new row of the table 'refresh'
                 });
        		$('#panel-body').animate({ scrollTop:  300 }, 'slow');
            };
        });
    };
});