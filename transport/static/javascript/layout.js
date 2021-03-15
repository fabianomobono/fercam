
// when the page is done loading
document.addEventListener("DOMContentLoaded", () => {

  //add listen for clicks  on the login dropdown button
  document.querySelector("#login_dropdown_button").addEventListener("click", () =>{
    var login_form = document.querySelector(".login_form");

    // make the login form visible, if it is not already for some reason
    if (login_form.style.display != 'block'){
      login_form.style.display = 'block';

      // make the other info divs invisible
      divs = {'login_company_link':'company_div','login_sectors_link':'sectors_div', 'login_service_link':'service_div', 'login_why_fercam_link':'why_fercam_div', 'message': 'message'}

      for (const property in divs){
          document.getElementById(divs[property]).style.display = 'none';
      }

      // hide the sign up form invisible if it is visible
      document.querySelector(".sign_up_form").style.display = 'none'
    }

    // if the login form was visible make it invisible
    else {
      login_form.style.display = 'none'
    }
  });


  // listen for clicks on the register link
  document.querySelector("#register_link").addEventListener("click", () =>{
    var sign_up_form = document.querySelector(".sign_up_form")

    // if the sign up form is invisible
    if (sign_up_form.style.display != 'block'){

      // make it visible
      sign_up_form.style.display = 'block';

      // make the other overlapping divs invisible
      divs = {'login_company_link':'company_div','login_sectors_link':'sectors_div', 'login_service_link':'service_div', 'login_why_fercam_link':'why_fercam_div', 'message': 'message'}
      for (const property in divs){
          document.getElementById(divs[property]).style.display = 'none';
      }

      // make the login form invisible
      document.querySelector(".login_form").style.display = 'none';
    }

    // if the sign up form is visible make it invisible
    else {
      sign_up_form.style.display = 'none'
    }
  });
})


// this function shows the additional information divs on the login page.
window.addEventListener('mouseover', e => {
  // this get's the id of the element the mouse is currently hovering on
  var element = e.target.getAttribute("id")

  // this is a js object that contains all the divs that need to be considered
  divs = {'login_company_link':'company_div','login_sectors_link':'sectors_div', 'login_service_link':'service_div', 'login_why_fercam_link':'why_fercam_div', 'message': 'message'}
  // this is a js object that keeps track of the current showing div
  showing = {}
    if (element in divs){
    for (const property in divs){
      document.getElementById(divs[property]).style.display = 'none';
    }
    document.querySelector(".login_form").style.display = 'none';
    document.querySelector(".sign_up_form").style.display = 'none'
    document.getElementById(divs[element]).style.display = 'block';
    showing.element = divs[element]
  }
  else if (element in showing){
    for (const property in divs){
      document.getElementById(divs[property]).style.display = 'none';
      showing = {};
    }
  }

});


// this function hides elements if the user clicks around on the page
window.addEventListener('click', e => {

  // get the clicked on element
  var element = e.target.getAttribute("id");
  divs = {'login_company_link':'company_div','login_sectors_link':'sectors_div', 'login_service_link':'service_div', 'login_why_fercam_link':'why_fercam_div'}

  // if the element does not have an ID hide the following elements
  if (element == null){
    document.querySelector(".login_form").style.display = 'none';
    document.querySelector(".sign_up_form").style.display = 'none'
    for (const poperty in divs){
      document.getElementById(divs[poperty]).style.display = 'none'
    }
  }
});
