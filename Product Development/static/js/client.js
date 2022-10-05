//client side of the server
$(document).ready(function() {
                var socket = io.connect("http://127.0.0.1:5000")
                
                socket.on('connect', function(){
                    socket.send("User connected"); //listen to 'connect' event
                });
                socket.on('message', function(msg){
                    $('#messages').append($('<li>').text(msg)); //listen to 'message' event
                });

                $('#sendbtn').on('click', function(){
                    //socket.send($('#username').val + ': ' + $('#message').val());
                    socket.send($('#message').val());
                    $('#message').val('');
                });
            });