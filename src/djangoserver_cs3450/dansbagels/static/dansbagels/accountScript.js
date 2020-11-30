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