window.onload = function () {
    let copyButtons = document.getElementsByClassName("copy-button")
    let removeInviteButton = document.getElementsByClassName("remove-invite-button")
    let actions = ['tap', 'click']
    for (let j = 0; j < actions.length; j++) {
        for (let i = 0; i < copyButtons.length; i++) {
            copyButtons[i].addEventListener(actions[j], function () {
                copyToClipboard(copyButtons[i])
            })
        }
        for (let i = 0; i < removeInviteButton.length; i++) {
            removeInviteButton[i].addEventListener(actions[j], function () {
                removeInvite(removeInviteButton[i])
            })
        }
    }
}

function copyToClipboard(obj) {
    /* Get the text field */
    let text = obj.dataset.welcome + "\n";
    text += document.getElementById("wedding-invite-text")?.value || ""
    text += "\n";
    text += decodeURIComponent(obj.dataset.link);
    copyTextToClipboard(text);
    obj.classList.add("active");
    let dummy = document.createElement("a")
    dummy.innerHTML = "Copied"
    obj.appendChild(dummy)
    setTimeout(() => {obj.classList.remove("active"); obj.removeChild(dummy)}, 2000)
}


function copyTextToClipboard(text) {
    var dummy = document.createElement("textarea");
    // to avoid breaking orgain page when copying more words
    // cant copy when adding below this code
    // dummy.style.display = 'none'
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
    // alert("Copied!")
}

function removeInvite(button) {
    let target = button.parentNode;
    target.parentNode.removeChild(target);
}