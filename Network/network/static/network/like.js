// // Check if there is already a vlaue in local storage
// if (!localStorage.getItem('counter')) {

//     // If not, set the counter to 0 in local storage
//     localStorage.setItem('counter', 0);
// }


document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.likeunlike' ).forEach((button) => like_post(post_id))

})
function like_post(post_id){


    console.log(post_id)
    
fetch(`like/${post_id}`)
.then(response => response.json())
.then(response =>{
    if (response.liked){
        document.getElementById(`like-view-${post_id}`).style.display = 'none';
        document.getElementById(`unlike-view-${post_id}`).style.display = 'block';
    }
    else{
        document.getElementById(`like-view-${post_id}`).style.display = 'block';
        document.getElementById(`unlike-view-${post_id}`).style.display = 'none';
    }

    document.getElementById(`like-count -${post_id}`).innerHTML = "Likes: " + response.likes_count;
})

}















