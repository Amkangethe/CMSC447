// Function to scroll movie list left
function scrollLeft(containerId) {
    const container = document.getElementById(containerId);
    container.scrollBy({ left: -300, behavior: 'smooth' });
}

// Function to scroll movie list right
function scrollRight(containerId) {
    const container = document.getElementById(containerId);
    container.scrollBy({ left: 300, behavior: 'smooth' });
}
