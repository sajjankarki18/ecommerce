document.querySelectorAll('.js-add-to-cart').forEach((button) => {
    button.addEventListener('click', () => {
        let productId = button.dataset.product
        let action = button.dataset.action

        if(user == 'AnonymousUser'){
            console.log('The user is not logged in')
        }else{
            updateOrderQuantity(productId, action)
        }
    })
})

const updateOrderQuantity = (productId, action) => {
    
    let url = '/updateOrder/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((res) => {
        return res.json()
    })
    .then((data) => {
        console.log('data: ',data)
        location.reload()
    })
}