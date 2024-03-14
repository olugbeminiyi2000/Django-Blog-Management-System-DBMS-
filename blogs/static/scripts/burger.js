document.addEventListener('DOMContentLoaded', function() {
    const hamButtonDiv = document.querySelector("button");
    const hamDisplay = document.querySelector("#ham-display");

    hamButtonDiv.addEventListener("click", function() {
        if (hamDisplay.classList.contains("ham-display-1")) {
            hamDisplay.classList.remove("ham-display-1");
            hamDisplay.classList.add("ham-display-2");
            console.log("changed from none to block display!!!")
        } else {
            hamDisplay.classList.remove("ham-display-2");
            hamDisplay.classList.add("ham-display-1");
            console.log("changed from block to none display!!!")
        }
    });
});
