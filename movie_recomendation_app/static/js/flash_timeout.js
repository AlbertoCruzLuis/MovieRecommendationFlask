setTimeout(function() {
    let element = document.getElementById("list_message");
    element.remove();
}, 2000);

document.getElementById("close").onclick = function() {
    document.getElementById("list_message").remove();
}