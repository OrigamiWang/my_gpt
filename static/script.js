let chatText = document.getElementById('chatText')
let submitBtn = document.getElementById('submitBtn')
let chatInfo = document.getElementById('chatInfo')
let session_id = null
// 页面加载成功时，获取session_id并保存在js中作为一次会话
window.onload = () => {
    console.log("the page is loaded...")
    fetch_session_id()
}
// 页面关闭时触发，将redis缓存中的数据持久化到mysql
window.onbeforeunload = () => {
    if (session_id != null) {
        navigator.sendBeacon('/cache/' + session_id, '');
        session_id = null
    }
}


chatText.addEventListener("keyup", (event) => {
    // 回车 触发点击事件
    if (event.code === 'Enter') {
        submitBtn.click();
    }
})

function modify_submit_style() {
    submitBtn.setAttribute('disabled', '')
    submitBtn.value = 'Wait'

}

function recover_submit_style() {
    submitBtn.removeAttribute('disabled')
    submitBtn.value = 'Submit'
}

function fetch_session_id() {
    fetch('/session_id')
        .then(function (response) {
            if (response) {
                session_id = response.headers.get('session_id')
                console.log("session_id is: " + session_id)
            }
        });
}

function submit() {
    console.log("submit...")
    modify_submit_style()
    let question = chatText.value

    console.log("input question is: " + question)
    let url = "/gpt/" + session_id + "?question=" + question
    let source = new EventSource(url);
    source.onmessage = function (event) {
        if (event.data === "[DONE]") {
            recover_submit_style()
            source.close();
        } else {
            chatInfo.innerText = chatInfo.innerText + event.data
        }
    }

}