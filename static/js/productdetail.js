const productStock=document.getElementById('stock-count')
const buyBtn=document.getElementById('buy-btn')
const productId=buyBtn.dataset.productId
const errorMsg=document.getElementById('error-msg')
const cartBtn=document.getElementById('cartbtn')

function getCsrfToken() {
    return document.cookie.split(';')
        .find(c => c.trim().startsWith('csrftoken='))
        .split('=')[1]
}

if (Number(productStock.textContent) <=0 ){
    productStock.textContent='Out of stock!'
    buyBtn.disabled=true
    cartBtn.disabled=true
}
buyBtn.addEventListener('click',async ()=>{

    const response = await fetch(`/products/buyitem/${productId}/`,{
    method:'POST',
    headers: {
        'Content-Type':'application/json',
        'X-CSRFToken':getCsrfToken()
    },
    body:JSON.stringify({productId})
        })
    const data = await response.json()
    if (data.success){
        productStock.textContent=data.new_stock
        buyBtn.disabled=true
        buyBtn.classList.toggle('btn-active')
        buyBtn.textContent='✅✅'
        setTimeout(() => {
            buyBtn.textContent='Buy now'
            buyBtn.disabled=false
            buyBtn.classList.toggle('btn-active')
        }, 2500);
        
    }
    else {
        if (data.error==='Please complete your profile first!'){
            window.location.href='/accounts/profile/'
        }
        else {
            errorMsg.textContent='Invalid request'
        }
    }
})
cartBtn.addEventListener('click',async ()=>{
    console.log('hello')
    const response = await fetch(`/products/Add2cart/${productId}/`,{
    method:'POST',
    headers: {
        'Content-Type':'application/json',
        'X-CSRFToken':getCsrfToken()
    },
    body:JSON.stringify({productId})
        })
    const data = await response.json()
    if (data.success){
        cartBtn.textContent='Added! ✅'
        cartBtn.classList.toggle('success')
        setTimeout(() => {
            cartBtn.textContent='Add to cart'
            cartBtn.classList.toggle('success')
        }, 2000);
    }
    else {
        if (data.error==='noStock'){
            errorMsg.textContent='Sorry the product is out of stock!'
        }
        else {
            errorMsg.textContent='Invalid request! Please try again'
        }
    }
})

