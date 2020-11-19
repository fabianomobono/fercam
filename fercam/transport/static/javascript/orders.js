
// autofill function
function activatePlacesSearch(){
  // declare variables origin and destination
  var origin = document.getElementById("origin_input");
  var destination = document.getElementById("destination_input");

  // assign the autocomplete google feature to these fields
  var autocomplete = new google.maps.places.Autocomplete(origin);
  var autocomplete2 = new google.maps.places.Autocomplete(destination)

  // display the map on the page
  initMap()
}


// calculate path if user clicks on calculate path button
function calculate_path(){
  // display loader wheel
  document.querySelector(".loader").style.display = 'block';

  //define variables
  var origin = document.querySelector("#origin_input").value
  var destination = document.querySelector("#destination_input").value
  var data = {'origin': origin, 'destination': destination}
  // the ol XML request
  request = new XMLHttpRequest();
  const csrftoken = Cookies.get('csrftoken')
  request.open("POST",'/calculate_path', true)
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
  // what happens when the request comes back
  request.onload = () => {

    // hide loader wheel
    document.querySelector(".loader").style.display = 'none';

    // parse response textm
    response = JSON.parse(request.responseText)
    console.log(response)
    // if there weren't any results
    if (response.status == 'ZERO_RESULTS'){

      // display error message
      document.querySelector("#path_error_message").style.display = "block";
      document.querySelector("#path_error_message").innerHTML = "couldn't calculate Path"
    }

    // if the user didn't provide origin or destination
    else if (response.status == "INVALID_REQUEST"){
      document.querySelector("#path_error_message").style.display = "block";
      document.querySelector("#path_error_message").innerHTML = "Invalid Request"
    }



    // if the request comes back ok
    else if (response.status == "OK"){

      // hide an eventual error message
      document.querySelector("#path_error_message").style.display = "none";

      // store distance and duration, origin and destination
      var origin = response.routes['0'].legs['0'].start_address
      var destination = response.routes['0'].legs['0'].end_address
      var distance = response.routes['0'].legs['0'].distance.text
      var duration = response.routes['0'].legs['0'].duration.text

      // show distance and duration on page
      document.querySelector("#span_distance").innerHTML = distance
      document.querySelector("#span_duration").innerHTML = duration
      document.querySelector("#span_origin").innerHTML = origin
      document.querySelector("#span_destination").innerHTML = destination
      document.querySelector("#distance_value").value = response.routes['0'].legs['0'].distance.value
      document.querySelector("#duration_value").value = response.routes['0'].legs['0'].duration.value
      document.querySelector("#origin_input_submit").value = origin
      document.querySelector("#destination_input_submit").value = destination

      var distance = document.querySelector("#distance_value").value
      var duration = document.querySelector("#duration_value").value
      var weight = document.querySelector("#weight_input").value
      var size = document.querySelector("#size_input").value
      console.log(weight, size)
      if (weight == 0 || size == 0){
        alert("weight or size can not be 0")
        return false
      }

      // get gas price

     
     // send price request to server
      const csrftoken = Cookies.get('csrftoken')
      price_request = new XMLHttpRequest()
      price_request.open("POST", "/calculate_price", true)
      price_request.setRequestHeader("X-CSRFToken", csrftoken);
      price_request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");

      // variables that are needed to send to the server
      var info = {'distance': distance, 'duration': duration, 'weight': weight, 'size': size}

      // when the response comes back from the server
      price_request.onload = () => {
        message = JSON.parse(price_request.responseText)
        console.log(message)
        document.querySelector("#span_price").innerHTML = message['price'] + "$"
        document.querySelector("#price_value").value = message['price']
      }
      price_request.send(JSON.stringify(info))


      document.querySelector("#submit_order_button").removeAttribute('disabled')
      document.querySelector("#submit_order_button").innerHTML = 'Submit Order'


    }
  };
  // actually send the request
  request.send(JSON.stringify(data))

}


// create a map and show map after page is loaded
function initMap() {
  //get directions and map renderer
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer();
  // The location of Uluru
  var new_york = {lat: 40.748327, lng: -73.986330};
  // The map, centered at Uluru
  // Map function(method) takes these arguments( where to put the map, {zoom and center position})
  var map = new google.maps.Map(document.querySelector('.map'), {zoom: 4, center: new_york});
      directionsRenderer.setMap(map);
  // The marker, positioned at Uluru

  const onChangeHandler = function () {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
  };

  // listen for click
  document.getElementById("calculate_path_button").addEventListener("click", onChangeHandler);

}


// calculate abd display directions on map
function calculateAndDisplayRoute(directionsService, directionsRenderer){
  directionsService.route({
    origin: document.querySelector("#origin_input").value,
    destination: document.querySelector("#destination_input").value,
    travelMode: "DRIVING"
  }, function(response, status){
    if (status === 'OK'){
      directionsRenderer.setDirections(response);
    }
    else{
      window.alert("Couldn't calculate directions because of " + status)
    }
  })
}


// calculate coordinates
function getLocation(button){

  //depending on what button was clicked put location in origin or destination
  if (navigator.geolocation){
    if (button.id == 'location_origin'){

        navigator.geolocation.getCurrentPosition(showPositionOrigin)
    }
    else if (button.id == 'location_destination'){

      navigator.geolocation.getCurrentPosition(showPositionDestination)
    }
  }

  // if something goes wrong
  else{
    document.querySelector("#path_error_message").style.display = 'block';
    document.querySelector("#path_error_message").innerHTML = "Location not available!"
  }
}


// put position in Origin input
function showPositionOrigin(position){
  document.querySelector("#origin_input").value = position.coords.latitude + ',' + position.coords.longitude;
}


// put position in destination input
function showPositionDestination(position){
  document.querySelector("#destination_input").value = position.coords.latitude + ',' + position.coords.longitude;
}


var loadFile = function(event){
  document.querySelector(".order_images").innerHTML = ''

  files = event.target.files
  for (var i = 0; i < files.length; i++){
    var image = document.createElement("IMG")
    image.width = 200
    image.src = URL.createObjectURL(event.target.files[i]);
    document.querySelector(".order_images").appendChild(image)
  }
}
