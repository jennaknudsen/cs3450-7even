//get the button html elements
var buttons = document.getElementsByName("button");
//loop through the buttons to assign an onClick function
buttons.forEach(function (button){
		document.getElementById("id_" + button.id).style.visibility = "hidden";
		button.onclick = function () {showField(button.id)};
	});
	
function showField(buttonID) {
		document.getElementById("id_" + buttonID).style.visibility = "visible";
		document.getElementById(buttonID).remove();
}