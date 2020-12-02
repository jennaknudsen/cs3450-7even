//create the cart html elements
var basket = document.getElementById("cart")

var header = document.createElement("h2");
header.textContent = "Cart";
basket.append(header);

var table = document.createElement("table");
basket.append(table);

//define a onclick function for each menuItem div
var menuItems = document.getElementsByClassName("menuItem");

for (let i = 0; i < menuItems.length; i++) {
	let itemName = menuItems[i].getElementsByTagName("h3");
	let itemPrice = menuItems[i].getElementsByTagName("p");
    menuItems[i].onclick = function () { AddItemToCart(itemName[0].textContent, itemPrice[0].textContent) };
}

//initialize helper arrays to keep track of cart contents
var cartItemNames = [];
var cartItemBasePrices = [];
var cartItemPrices = [];
var cartItemQuantity = [];
var cartTotalPrice = 0.0;

//create checkout html elements
var checkout = document.getElementById("checkOut");

var totalPrice = document.createElement("p");
var itemsOrdered = document.getElementById("id_itemsOrdered");
var orderCost = document.getElementById("id_orderCost");
var pickUpTime = document.getElementById("id_pickUpTime");
var pickUpDate = document.getElementById("id_pickUpDate");
var orderForm = document.getElementById("orderForm");

var minTime = String(new Date().getHours()) + ":" + String(new Date().getMinutes() + 10);
pickUpTime.value = minTime;
pickUpTime.min = minTime;
pickUpTime.max = "22:00"

pickUpDate.min = new Date().toISOString().split('T')[0];
pickUpDate.max = new Date(Date.now() + 6.048e8).toISOString().split('T')[0];//6.48e8 is a magic number which is 7 days in miliseconds
totalPrice.style.visibility = "hidden";
orderForm.style.visibility = "hidden";

checkout.append(totalPrice);

function AddItemToCart(name, price) {
	//check to see if the item clicked is already in the cart
	var element = document.getElementById(name);	
	if (typeof(element) != "undefined" && element != null){
		//if so update the helper arrays to reflect the user adding the same item to the cart
		var index = cartItemNames.indexOf(name);
		
		cartItemQuantity[index]++;
		cartItemBasePrices[index] = parseFloat(price.replace("$",""));
		cartItemPrices[index] = (cartItemBasePrices[index] * cartItemQuantity[index]).toFixed(2);
		
		var tableHeaders = element.getElementsByTagName("th");
		tableHeaders[0].textContent = "x" + cartItemQuantity[index];
		tableHeaders[2].textContent = "$" + cartItemPrices[index];
	}
	else{
		//else add new data to the helper arrays and create another table row in the cart
		cartItemNames.push(name);
		cartItemBasePrices.push(parseFloat(price.replace("$","")));
		cartItemPrices.push(parseFloat(price.replace("$","")).toFixed(2));
		cartItemQuantity.push(1);
		
		var tableEntry = document.createElement("tr");
		tableEntry.className = "cartItem"
		tableEntry.id = name;
		tableEntry.onclick = function () { removeItemFromCart(tableEntry) };
		
		var quantity = document.createElement("th");
		quantity.textContent = "x1";
		tableEntry.append(quantity);
		
		var itemName = document.createElement("th");
		itemName.textContent = name;
		tableEntry.append(itemName);
		
		var itemPrice = document.createElement("th");
		itemPrice.textContent = price;
		tableEntry.append(itemPrice);
		
		table.append(tableEntry);
	}
	updateTotalPrice();
}

function removeItemFromCart(tableEntry){
	var entryComponents = tableEntry.getElementsByTagName("th");
	var index = cartItemNames.indexOf(entryComponents[1].textContent);
	//update helper arrays
	cartItemQuantity[index]--;
	cartItemPrices[index] = (cartItemBasePrices[index] * cartItemQuantity[index]).toFixed(2);
	//update tableEntry html components
	entryComponents[0].textContent = "x" + cartItemQuantity[index];
	entryComponents[2].textContent = "$" + cartItemPrices[index];
	
	if (cartItemQuantity[index] == 0){
		cartItemNames.splice(index, 1);
		cartItemBasePrices.splice(index, 1);
		cartItemPrices.splice(index, 1);
		cartItemQuantity.splice(index, 1);
		
		tableEntry.remove();
	}
	updateTotalPrice();
}

function updateTotalPrice(){
	if (cartItemNames.length != 0){
		totalPrice.style.visibility = "visible";
		orderForm.style.visibility = "visible";
		cartTotalPrice = 0.0;
		for (let i = 0; i<cartItemPrices.length; i++){
			cartTotalPrice += parseFloat(cartItemPrices[i]);
			if (i == 0){
				itemsOrdered.value = cartItemQuantity[i] + "," + cartItemNames[i];
			}
			else{
				itemsOrdered.value = itemsOrdered.value + "," + cartItemQuantity[i] + "," + cartItemNames[i];
			}
		}
		totalPrice.textContent = "Total Price is $" + parseFloat(cartTotalPrice).toFixed(2);
		orderCost.value = parseFloat(cartTotalPrice).toFixed(2);
	}
	else{
		cartTotalPrice = 0;
		totalPrice.style.visibility = "hidden";
		orderForm.style.visibility = "hidden";
	}
}