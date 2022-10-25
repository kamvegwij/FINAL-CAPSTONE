//client side of the server

var confidant = document.getElementById('conf').value;
// console.log(confidant);

$(document).ready(function() {
    var socket = io.connect("http://127.0.0.1:5000")
    
    
    socket.on('connect', function(){
        socket.send("joined the chat" + "~" + confidant); //listen to 'connect' event
    });
    socket.on('message', function(msg){
        sent_message = msg.split("~")
        if (sent_message[0] == confidant) {
            $('#messages').append($('<p class="ctextmessage">').text(sent_message[1])); //listen to 'message' event
        } else {
            $('#messages').append($('<p class="ptextmessage">').text(sent_message[1])); //listen to 'message' event
        }
        
        console.log(msg)
    });

    $('#sendbtn').on('click', function(){
        socket.send($('#message').val() + "~" + confidant);
        $('#message').val('');
    });
});


//$(document).on('submit', '#msgfrm', function(e) {
//    console.log('hello');
//    $.ajax({
//        type: 'POST',
//        url: '/chat/{{ confidant }}',
//        data: {message: $('#message').val()},
//        success: function(){
//            alert('done')
//        }
//    });
//    e.preventDefault();
//    console.log($('#message').val());
//});
