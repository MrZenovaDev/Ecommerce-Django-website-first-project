const form=document.getElementById('login_form')
const error_msg=document.getElementById('error-msg')
const usernameInput=document.getElementById('id_username')
const passwordInput=document.getElementById('id_password')

function getCsrfToken() {
    return document.cookie.split(';')
        .find(c => c.trim().startsWith('csrftoken='))
        .split('=')[1]
}

form.addEventListener('submit',async (event)=>{
    console.log('hello')
    event.preventDefault()
    let username=usernameInput.value
    let password=passwordInput.value
    if (username===''){
        error_msg.textContent='Username cannot be empty!'
    }
    else if (password===''){
        error_msg.textContent='Password cannot be empty!'
    }
    else {
        const response = await fetch('/accounts/login/',{
        method:'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':getCsrfToken()
        },
        body:JSON.stringify({username,password})
        })
        const data=await response.json()
        if (data.success){
            window.location.href='/products/'
        }
        else {
            error_msg.textContent=data.error
        }
    }
})