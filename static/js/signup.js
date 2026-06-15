const usernameInput=document.getElementById('id_username')
const password1Input=document.getElementById('id_password1')
const password2Input=document.getElementById('id_password2')
const error_msg=document.getElementById('error-msg')
const form=document.getElementById('signup-form')

function getCsrfToken() {
    return document.cookie.split(';')
        .find(c => c.trim().startsWith('csrftoken='))
        .split('=')[1]
}

form.addEventListener('submit',async (event)=>{
    event.preventDefault()
    let username=usernameInput.value
    let password1=password1Input.value
    let password2=password2Input.value

    if (username===''){
        error_msg.textContent='Username field cannot be empty!'
    }
    else if (password1===''){
        error_msg.textContent='Password field cannot be empty!'
    }
    else if (password2!==password1){
        error_msg.textContent='Passwords donot match!'
    }
    else {
        const response = await fetch('/accounts/signup/',{
            method:'POST',
            headers: {
                'Content-Type':'application/json',
                'X-CSRFToken':getCsrfToken()
            },
            body:JSON.stringify({username,password1,password2})
        })
        console.log('response status:', response.status)
        const data = await response.json()
        console.log('data:', data)
        console.log('hi')
        if (data.success){
            window.location.href='/accounts/profile/'
        }
        else {
            error_msg.textContent='Oops something went wrong!'
        }
    }
})
