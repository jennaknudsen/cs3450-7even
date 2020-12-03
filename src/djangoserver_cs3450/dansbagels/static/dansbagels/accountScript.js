
var pickUpTime = document.getElementsByName("pickUpTime");
var pickUpDate = document.getElementsByName("pickUpDate");

var minTime = setMinTime();
pickUpTime.forEach(function (element) {
                        element.value = minTime;
                        element.min = minTime;
                        element.max = "22:00";
                   });
pickUpDate.forEach(function (element) {
                        element.min = new Date().toISOString().split('T')[0];
                        element.max = new Date(Date.now() + 6.048e8).toISOString().split('T')[0];//6.48e8 is a magic number which is 7 days in miliseconds
                  });

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

function setMinTime() {
        if (new Date().getMinutes() + 10 > 60){
            return String(new Date().getHours() + 1) + ":" + String(0) + String(new Date().getMinutes() - 50);
        }
        return String(new Date().getHours()) + ":" + String(new Date().getMinutes() + 10);
}