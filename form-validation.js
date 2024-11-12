document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", event => {
        const isValid = Array.from(form.elements).every(input => input.value.trim() !== "");
        if (!isValid) {
            event.preventDefault();
            alert("Please fill out all fields.");
        }
    });
});
