var sendDataToServer = function(){
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if (request.readyState === 4){
			if (request.status >= 200 && request.status < 400) {
				console.log("hey, something worked");
			} else {
				alert("The Oompa Loompas have already received your ticket. Please try again tomorrow.");
			}
		}
	};
	
	var userInput = document.getElementById("fName");
    var userInput1 = document.getElementById("age");
    var userInput2 = document.getElementById("gName");
	var inputValue = userInput.value;
    var inputValue1 = userInput1.value;
    var inputValue2 = userInput2.value;
    
    var the_data = '' + 'fName=' + encodeURIComponent(inputValue) + '&age=' + encodeURIComponent(inputValue1) + '&gName=' + inputValue2;
	
	request.open("POST", "http://localhost:8080/tickets");
	request.withCredentials = true;
	request.send(the_data);
	
	userInput.reset();
	userInput1.reset();
	userInput2.reset();
};

var myButton = document.getElementById("createButton");
	myButton.onclick = function(){
	console.log("the button was clicked!");
	sendDataToServer();
	getDataFromServer();
};




var getDataFromServer = function(){
	  var request = new XMLHttpRequest();
	
	request.open("GET", "http://localhost:8080/tickets");
	request.send(null);

	
	
	request.onreadystatechange = function() {
		if (request.readyState === 4){
			if (request.status >= 200 && request.status < 400) {
				console.log(request.responseText);
				var messages = JSON.parse(request.responseText);
				console.log(messages[0]);
				
				var list = document.getElementById("list");
					list.innerHTML = "";
                
                var dayOfWeek = new Date().getDay();
				
				for(index in messages) {
						var obj = messages[index];
                            if (messages[index]["random_token"] === dayOfWeek) {
                                var ticket = "<img src='golden.png' class='goldenTicket' />"
                            }
                            else {
                                var ticket = "<img src='normal.png' class='goldenTicket' />"
                            }
                            var newListItem = document.createElement("p");
							newListItem.innerHTML = obj["guest_name"] + ": " + obj["entrant_name"] + "-" + obj["entrant_age"] + ticket;
						
							var list = document.getElementById("list");
							list.appendChild(newListItem, ticket);
					}
		
		
			} else {
				console.error("that didnt work...");
			}
		}
	};
		
};

var getButton = document.getElementById("getButton");
	getButton.onclick = function () {
	console.log("the GET button was clicked!");
	getDataFromServer();
};