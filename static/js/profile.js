const userAddress = document.getElementById('id_address')
const submitBtn = document.getElementById('SubmitBtn')
const errorMsg = document.getElementById('error-msg')

submitBtn.addEventListener('click', async (event)=>{
    const address=userAddress.value
    console.log('hello')
    if (address===''){
        event.preventDefault()
        errorMsg.textContent='Address can`t be empty!'
    }
    else if (!isNaN(address)){
        event.preventDefault()
        errorMsg.textContent='Address can`t be all numbers!'
    }
})