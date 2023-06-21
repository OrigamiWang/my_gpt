function fetch_tts(conversation_idx) {
    fetch('/tts/' + conversation_idx + '/' + session_id)
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
}

function text_to_speach(div) {
    div.addEventListener("click", () => {
        const conversation_idx = div.getAttribute('conversation_idx')
        fetch_tts(conversation_idx)
    })
}