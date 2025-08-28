document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.likeunlike' ).forEach((button) => like_song(song_id))

})
function like_song(song_id){


    console.log(song_id)
    
fetch(`like/${song_id}`)
.then(response => response.json())
.then(response =>{
    if (response.liked){
        document.getElementById(`like-view-${song_id}`).style.display = 'none';
        document.getElementById(`unlike-view-${song_id}`).style.display = 'block';
    }
    else{
        document.getElementById(`like-view-${song_id}`).style.display = 'block';
        document.getElementById(`unlike-view-${song_id}`).style.display = 'none';
    }

    document.getElementById(`like-count -${song_id}`).innerHTML = "Likes: " + response.likes_count;


})

}
