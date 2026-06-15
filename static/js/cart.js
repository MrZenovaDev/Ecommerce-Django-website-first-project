const itemContainer = document.getElementById("ItemContainer")
const buyAllBtn = document.getElementById('BuyAll')
const msgBox = document.getElementById('msgBox')

function getCsrfToken() {
    return document.cookie.split(';')
        .find(c => c.trim().startsWith('csrftoken='))
        .split('=')[1]
}

buyAllBtn.addEventListener('click', async ()=>{
    const response = await fetch(`/products/placeorder/`,{
    method:'POST',
    headers: {
        'Content-Type':'application/json',
        'X-CSRFToken':getCsrfToken()
    }
        })
    const data = await response.json()
    if (data.success){
        itemContainer.innerHTML=`
        <div class="text-center mt-5">
            <p class="text-muted fs-4">🛒 Your cart is empty!</p>
            <a href="/products/" class="btn btn-primary">Continue shopping 👜</a>
        </div>
        `
        buyAllBtn.style.display='none'
        msgBox.innerHTML=`
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            All items order have been placed ✅
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        `
    }
    else {
        if (data.error==='Profile not created'){
            msgBox.innerHTML=`
            <div class="alert alert-warning" role="alert">
                Please complete your profile first! Redirecting...
            </div>
            `
            setTimeout(() => {
                window.location.href='/accounts/profile/?next=/products/cart/'
                
            }, 3000);
        }
        else {
            msgBox.innerHTML=`
            <div class="alert alert-warning" role="alert">
                Invalid request! Please try again.
            </div>
            `
        }
    }
})