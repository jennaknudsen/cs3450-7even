var pickUpTime = document.getElementById("id_pickUpTime");
var pickUpDate = document.getElementById("id_pickUpDate");

var minTime = String(new Date().getHours()) + ":" + String(new Date().getMinutes() + 10);
pickUpTime.value = minTime;
pickUpTime.min = minTime;
pickUpTime.max = "22:00"

pickUpDate.min = new Date().toISOString().split('T')[0];
pickUpDate.max = new Date(Date.now() + 6.048e8).toISOString().split('T')[0];//6.48e8 is a magic number which is 7 days in miliseconds

//get the button html elements
var buttons = document.getElementsByName("button");
//loop through the buttons to assign an onClick function
buttons.forEach(function (button){
		button.onclick = function () {showField(button.id)};
	});
	
function showField(buttonID) {
		document.getElementById("id_" + buttonID).type = "text";
		document.getElementById(buttonID).remove();
}