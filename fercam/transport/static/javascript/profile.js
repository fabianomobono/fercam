

document.querySelector('#close').addEventListener('click', () => {
    const close = document.querySelector('#close')
    close.parentElement.style.display = 'none'
})


document.querySelector('#profile_picture').addEventListener('click', () => {
    document.querySelector('.upload_profile_pic_div').style.display= 'block'
})

document.querySelector('#profile_pic_input').addEventListener('change' , (event) => {
    const pic = document.querySelector('#upload_label')
    pic.innerHTML = ''
    var files = event.target.files['0']
    var image = document.createElement("IMG")
    var select = document.createElement("H6")
    select.innerHTML = 'Choose profile picture'
    image.setAttribute('id', 'profile_picture_in_upload_div')
    image.src = URL.createObjectURL(event.target.files['0']);
    document.querySelector("#upload_label").appendChild(image)
    document.querySelector("#upload_label").appendChild(select)
    document.querySelector("#save_picture_button").removeAttribute('disabled');
})



document.querySelector('#save_picture_button').addEventListener('click', () => {
    document.querySelector('#submit_pic').click()
})