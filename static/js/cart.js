let updateBtn = document.getElementsByClassName('add-to-cart')

for(let i=0; i<updateBtn.length; i++){
    updateBtn[i].addEventListener('click', () => {
        product_id = updateBtn[i].dataset.product_id
        action = updateBtn[i].dataset.action
        
        updateOrderFunction(product_id, action)
    })


}

function updateOrderFunction(product_id, action){
    console.log('user:', user);
    console.log('product_id:', product_id, 'action:', action);

    let url = '/update_cart/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            product_id: product_id,
            action: action
        })
    
    })
    window.location.reload()
    .then(response => response.json())
    .then(data => console.log(data))
    
}
