$(document).ready(function(){

            $(".signup-form").hide();

            // var socket = io.connect('https://' + document.domain + ':' + location.port);
            var socket = io();
            socket.on('connect', function() {
                socket.emit('myEvent');
                console.log("Emitted");
            });
            socket.on('disconnect', function() {
                $('#log').append('<br>Disconnected');
            });
            socket.on('my response', function(msg) {
                $('#log').append('<br>Received: ' + msg.data);
            });

            // event handler for server sent data
            // the data is displayed in the "Received" section of the page
            // handlers for the different forms in the page
            // these send data to the server in a variety of ways
            $('.login-button').click(function(event) {
                var uname = $("#username").val();
                var pass = $("#password").val();

                if(uname == "" || password == ""){
                    Materialize.toast("Invalid username or password", 4000, 'rounded');
                    return;
                }

               $.ajax({
                    type: "POST",
                    url: '/login',
                    data: JSON.stringify({uname:uname, pass:password}) ,
                    success: function(response){
                        console.log(response);
                        window.location = response;
                    },
                    error: function(httpObj, textStatus){
                        if(httpObj = 401){
                            Materialize.toast("Your username or password was wrong", 4000, 'rounded');
                        }
                    },
                    contentType: 'application/json'
                });

            });

            $('.signup-button').click(function(event){
                var fname = $("#firstname").val();
                var lname = $("#lastname").val();
                var uname = $("#username-signup").val();
                var pass = $("#password-signup").val();

                if (fname == "" || lname == "" || uname == "" || pass == ""){
                    Materialize.toast("You left one or more details blank", 4000, 'rounded');
                    return;
                }

                var data = {
                    fname: fname,
                    lname: lname,
                    uname: uname,
                    pass: pass
                }
                //console.log(data)

                $.ajax({
                    type: "POST",
                    url: '/addUser',
                    data: JSON.stringify(data) ,
                    success: function(response){
                        console.log(response);
                        window.location = response;
                    },
                    error: function(httpObj, status){
                        if(httpObj == 500){
                            Materialize.toast("Username already exists", 4000, 'rounded');
                        }
                    },
                    contentType: 'application/json'
                });

                //socket.emit('addUser', {fname, lname, uname, pass});

                return;
            });

            $('#login-tab').click(function(event){
                console.log("Clicked Login");
                $(".login-form").show();
                $(".signup-form").hide();
            });

            $('#signup-tab').click(function(event){
                console.log("Clicked sign up");
                $(".login-form").hide();
                $(".signup-form").show();

            });

        });
