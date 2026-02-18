const STORAGE_KEY = 'news_posts';
function getFormData() {
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    
    return { title, content };

function createPost(title, content) {
    return {
        id: Date.now(), 
        title: title,
        content: content,
        date: new Date().toLocaleString('uk-UA'),
        timestamp: Date.now()
    };
}

function savePost(post) {

    let posts = getPostsFromStorage();
    
    posts.unshift(post);
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(posts));
    
    return posts;
}

function getPostsFromStorage() {
    const storedPosts = localStorage.getItem(STORAGE_KEY);
    
    if (storedPosts) {
        try {
            return JSON.parse(storedPosts);
        } catch (e) {
            console.error('Помилка парсингу даних:', e);
            return [];
        }
    }
    
    return [];
}

function createPostElement(post) {
    const postDiv = document.createElement('div');
    postDiv.className = 'post-card';
    postDiv.innerHTML = `
        <h3>${escapeHtml(post.title)}</h3>
        <p>${escapeHtml(post.content)}</p>
        <div class="post-date"> ${post.date}</div>
    `;
    return postDiv;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function displayPosts(posts) {
    const container = document.getElementById('postsContainer');
    container.innerHTML = '';
    
    if (posts.length === 0) {
        container.innerHTML = '<div class="empty-state">Поки що немає дописів. Будьте першим, хто додасть новину!</div>';
        return;
    }
    
    posts.forEach(post => {
        const postElement = createPostElement(post);
        container.appendChild(postElement);
    });
}

function handleFormSubmit(event) {
    event.preventDefault(); 
    
    const formData = getFormData();

    if (!formData.title.trim() || !formData.content.trim()) {
        alert('Будь ласка, заповніть всі поля!');
        return;
    }

    const newPost = createPost(formData.title, formData.content);

    const updatedPosts = savePost(newPost);

    displayPosts(updatedPosts);

    document.getElementById('postForm').reset();

    showNotification('Допис успішно додано!');
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #4CAF50;
        color: white;
        padding: 15px 25px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);


document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('postForm');
    form.addEventListener('submit', handleFormSubmit);
    
    const posts = getPostsFromStorage();
    displayPosts(posts);
});

console.log('💡 Для очищення всіх дописів використовуйте localStorage.removeItem("news_posts")');