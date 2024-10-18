let send = document.querySelector('.sendbtn');
let chatarea = document.querySelector('.msgarea');


async function sendMessage() {
    let msgbox = document.querySelector('.msgbox');
    let msg = msgbox.value;
    if (msg) {
        
        let mess = document.createElement('p');
        mess.classList.add('msg');
        let sourcelang = document.querySelector('.srclang').value;
        let targetlang = document.querySelector('.trglang').value;

        const baseUrl = window.location.hostname === 'localhost'
            ? 'http://localhost:5000'
            : 'https://translatorchat.vercel.app';
        
        mess.innerText = `You: ${msg}`;
        chatarea.append(mess);

        
        msgbox.value = '';  

        
        scrollToBottom();

        try {
            
            let response = await fetch(`${baseUrl}/translate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: msg, 
                    source: sourcelang, 
                    target: targetlang 
                })
            });
            
            if (response.ok) {
                let data = await response.json();
                let translatedMessage = data.translated_text;
                
                
                let translatedMess = document.createElement('p');
                translatedMess.classList.add('translated-msg');
                
                translatedMess.innerText = `Translated: ${translatedMessage}`;
                
                chatarea.append(translatedMess);
                
                
                scrollToBottom();
            } else {
                console.error('Translation request failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}


send.addEventListener('click', sendMessage);


let msgbox = document.querySelector('.msgbox');
msgbox.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); 
        sendMessage(); 
    }
});


function scrollToBottom() {
    chatarea.scrollTop = chatarea.scrollHeight;
}
