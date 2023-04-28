function like(slug, id){
    var element = document.getElementById(elemendid="like")
    var count = document.getElementById(elemendid="count")
    $.get(`/like/${slug}/${id}`).then(response =>{
        if(response['response'] === "liked"){
            element.className = "fa fa-heart text-primary"
            count.innerText = Number(count.innerText)+1
        }else{
            element.className = "fa fa-heart"
            element.style = "color: #ebdada;"
            count.innerText = Number(count.innerText)-1
        }
    })
}