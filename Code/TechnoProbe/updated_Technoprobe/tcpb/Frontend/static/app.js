function toggleContent(post) {
    const excerpt = post.querySelector('.excerpt');
    const fullContent = post.querySelector('.full-content');

    if (excerpt.style.display === 'none') {
        excerpt.style.display = 'block';
        fullContent.style.display = 'none';
    } else {
        excerpt.style.display = 'none';
        fullContent.style.display = 'block';
    }
}
