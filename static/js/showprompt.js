'use strict';

function replacePrompt(results) {
    document.querySelector('#prompt-text').innerHTML = results;
}

function showPrompt(evt) {
    fetch('/show_prompt')
        .then((response) => response.text())
        .then(replacePrompt);
}

document.querySelector('#get-prompt-button').addEventListener('click', showPrompt);