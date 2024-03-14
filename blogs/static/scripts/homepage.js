document.addEventListener('DOMContentLoaded', function() {
    const allLinks = document.querySelectorAll(".all-links");
    allLinks.forEach((element) => {
        element.addEventListener("click", (event) => {
            const eachLinkElement = event.target;
            if (eachLinkElement.classList.contains("links-color1")) {
                eachLinkElement.classList.remove("links-color1");
                eachLinkElement.classList.add("links-color2");
            } else {
                eachLinkElement.classList.remove("links-color2");
                eachLinkElement.classList.add("links-color1");
            }
        });
    });
});
