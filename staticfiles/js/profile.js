const userAddress = document.getElementById('id_address')
const submitBtn = document.getElementById('SubmitBtn')
const errorMsg = document.getElementById('error-msg')

submitBtn.addEventListener('click', async (event)=>{
    const address=userAddress.ariaValueMax
    console.log('hello')
    if (userAddress===''){
        event.preventDefault()
        errorMsg.textContent='Address can`t be empty!'
    }
    else if (!isNaN(userAddress)){
        event.preventDefault()
        errorMsg.textContent='Address can`t be all numbers!'
    }
})