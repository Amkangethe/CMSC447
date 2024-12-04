// Scroll left & right functions
const ScrollFunctions = {
    scrollLeft: function(sectionId) {
        const container = document.getElementById(sectionId);
        if (container) {
            container.scrollBy({ left: -200, behavior: 'smooth' }); // Scroll left
        }
    },
    scrollRight: function(sectionId) {
        const container = document.getElementById(sectionId);
        if (container) {
            container.scrollBy({ left: 200, behavior: 'smooth' }); // Scroll right
        }
    }
};


function openChatMenu() {
    document.getElementById("chatMenu").style.width = "300px"; // Adjust width as needed
}

function closeChatMenu() {
    document.getElementById("chatMenu").style.width = "0";
}

// Filter friends based on search input
function filterFriends() {
    const input = document.getElementById('searchBar').value.toLowerCase();
    const friends = document.getElementById('friendsContainer').getElementsByClassName('friend-profile');

    for (let i = 0; i < friends.length; i++) {
        const name = friends[i].getElementsByTagName('h3')[0].innerText.toLowerCase();
        if (name.includes(input)) {
            friends[i].style.display = '';
        } else {
            friends[i].style.display = 'none';
        }
    }
}

// Placeholder functions for button actions
function messageFriend(name) {
    alert('Opening chat with ' + name);
}

function addFriend(name) {
    alert('Sending friend request to ' + name);
}

// Function to toggle between profile sections
function showSection(sectionId) {
    const sections = document.querySelectorAll('.profile-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}
