// Variable global
var actual_page = 0;
var total_pages = 0;
var post_number = 0;
var url = [];
var actual_user;

document.addEventListener('DOMContentLoaded', () => {
    actual_user = localStorage.getItem('user');
    localStorage.clear();
    get_url();
    show_posts();    
    get_total_posts();
});


function get_url() {
    url = [];
    // Vemos si estamos en profile.html o en index.html
    var aux = window.location.pathname.split('/');
    // Si estamos en profile.html
    if (aux[1] == "following") {
        url.push(`/posts?page=${actual_page}&profile=${aux[2]}&following=true`)
        url.push(`/total_posts?profile=${aux[2]}&following=true`)
    }
    else if (aux[2] != undefined) {
        url.push(`/posts?page=${actual_page}&profile=${aux[2]}`)
        url.push(`/total_posts?profile=${aux[2]}`)
    }
    else {
        url.push(`/posts?page=${actual_page}`)
        url.push(`/total_posts`)
    }
}

function show_posts() {
    // Elemento div padre
    const posts = document.getElementById('posts');
    fetch(url[0])
    .then(response => response.json())
    .then( (data) => {
        data.forEach(element => {
            post_number = element.id;
            // Elemento div hijo
            let post = document.createElement('div');
            post.classList.add('row');
            posts.appendChild(post);
            
            //Element div
            let div = document.createElement('div');
            div.classList.add('div_100')
            post.appendChild(div);

            // Usuario
            let user = document.createElement('h4');
            let a = document.createElement('a');
            a.setAttribute('href',`/profile/${element.user}`)
            a.innerHTML = element.user;
            user.classList.add('new_post');
            user.appendChild(a);
            div.appendChild(user);
            
            // Contenedor para edicion
            let edit_div = document.createElement('div');
            edit_div.setAttribute('id', `post${post_number}`);
            div.appendChild(edit_div);

            // Edit
            if (actual_user == element.user)    {
                let edit = document.createElement('h6');
                edit.classList.add('edit');
                edit.setAttribute('onclick', `edit_post(${post_number})`);
                edit.innerHTML = "Edit";
                edit_div.appendChild(edit);
            }

            // Texto
            let text = document.createElement('h6');
            text.classList.add('text');
            text.innerHTML = element.post;
            text.setAttribute('id', `text_post${post_number}`);
            edit_div.appendChild(text);

            // Fecha
            let date = document.createElement('h6');
            date.classList.add('date');
            date.innerHTML = element.date;
            div.appendChild(date);
            
            // Likes
            let like_div = document.createElement('div');
            like_div.classList.add('flex_div');
            div.appendChild(like_div);
            let heart = document.createElement('h6');       // Corazon
            heart.setAttribute('id',`heart${post_number}`)
            heart.classList.add('heart_unlike')
            like_unlike(post_number);
            heart.innerHTML = "&hearts;";
            like_div.appendChild(heart);
            let number_like = document.createElement('h6'); // Numero de likes
            number_like.classList.add('number_like');
            number_like.setAttribute('id',`like${post_number}`)
            number_like.innerHTML = element.like;
            like_div.appendChild(number_like);
        });
    })
};


function like_unlike(post_number) {
    fetch(`is_liked/${post_number}`)
    .then(response => response.json())
    .then((is_like) => {
        let heart = document.getElementById(`heart${post_number}`)
        if (is_like.like == "True") {
            heart.classList.remove('heart_unlike')
            heart.classList.add("heart_like");
            heart.setAttribute('onclick', `dislike(${post_number})`)
        }
        else {
            heart.classList.add("heart_unlike");
            heart.setAttribute('onclick', `like(${post_number})`)
        }
    });
};


function get_total_posts() {
    fetch(url[1])
    .then(response => response.json())
    .then((posts) => {
        show_pages(posts.total);
    });
};


function show_pages(total_posts) {
    let total_pages = Math.ceil(total_posts/10);
    if (total_pages > 1) {
        const pagination = document.getElementById('pagination')
        var pages = [];
        if (actual_page != 0) {
            pages.push('Previous');
        }
        for (let i = 1; i < total_pages + 1; i++) {
            pages.push(i);
        }
        if (actual_page + 1 != total_pages) {
            pages.push('Next');
        }
        for (let i = 0; i < pages.length; i++) {
            let page = document.createElement('li');
            page.classList.add("page-item", "page-link");
            page.setAttribute("onclick",`show_page("${pages[i]}")`)
            page.innerHTML = pages[i];
            pagination.appendChild(page);
        }
    }
}


function show_page(page) {
    if (page == "Previous") {
        actual_page = (actual_page - 1) * 10;
    }
    else if (page == "Next") {
        actual_page = actual_page*10 + 10;
    }
    else {
        actual_page = (page-1)*10;
    }
    delete_child();
    get_url();
    show_posts();
    actual_page = actual_page/10;
    get_total_posts();
    show_pages();
}


function delete_child () {
    const posts = document.getElementById("posts");
    while (posts.firstChild) {
        posts.removeChild(posts.firstChild);
    }
    const pagination = document.getElementById("pagination");
    while (pagination.firstChild) {
        pagination.removeChild(pagination.firstChild);
    }
}


function edit_post(post) {
    div = document.getElementById(`post${post}`);
    text = document.getElementById(`text_post${post}`).innerHTML;
    // Textarea
    textarea = document.createElement('textarea');
    textarea.classList.add('form-control');
    textarea.value = text;
    textarea.setAttribute('id', `textarea${post}`)
    // Boton de edicion
    edit_button = document.createElement('button');
    edit_button.innerHTML = "Edit Post";
    edit_button.classList.add('btn','btn-primary', 'edit_button')
    edit_button.setAttribute('onclick',`change_post(${post})`)
    while (div.firstChild) {
        div.removeChild(div.firstChild);
    }
    div.appendChild(textarea);
    div.appendChild(edit_button);
}


function change_post(post) {
    div = document.getElementById(`post${post}`);
    textarea_value = document.getElementById(`textarea${post}`).value;
    while (div.firstChild) {
        div.removeChild(div.firstChild);
    }
    // Edit
    let edit = document.createElement('h6');
    edit.classList.add('edit');
    edit.setAttribute('onclick', `edit_post(${post})`);
    edit.innerHTML = "Edit";
    div.appendChild(edit);

    // Texto
    let text = document.createElement('h6');
    text.classList.add('text');
    text.innerHTML = textarea_value;
    text.setAttribute('id', `text_post${post}`);
    div.appendChild(text);

    fetch(`/post/${post}`, {
        method: 'PUT',
        body: JSON.stringify({
            post: textarea_value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    });
}


function like(id) {
    heart = document.getElementById(`heart${id}`);
    heart.classList.remove('heart_unlike');
    heart.classList.add('heart_like');
    heart.setAttribute('onclick',`dislike(${id})`);
    
    likes = document.getElementById(`like${id}`);
    number_like = likes.innerHTML;
    number_like++;
    likes.innerHTML = number_like;

    fetch(`/like_post/${id}`)
    .then(response => response.json())
    .then((response) => {
        console.log(response)
    });
}

function dislike(id) {
    heart = document.getElementById(`heart${id}`);
    heart.classList.remove('heart_like');
    heart.classList.add('heart_unlike');
    heart.setAttribute('onclick',`like(${id})`);

    likes = document.getElementById(`like${id}`);
    number_like = likes.innerHTML;
    number_like--;
    likes.innerHTML = number_like;

    fetch(`/dislike_post/${id}`)
    .then(response => response.json())
    .then((response) => {
        console.log(response)
    });
}