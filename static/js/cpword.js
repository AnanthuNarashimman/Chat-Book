
document.querySelector(".checkpword").addEventListener('click', function(e) {
    e.preventDefault();

    const oldpword = document.querySelector("#oldpwordBox").value; 
    const newpassword = document.querySelector('#newpwordBox');
    const renewpassword = document.querySelector('#renewpwordBox');
    const submitbtn = document.querySelector('#changepword');
    
    

    if(oldpword == '')
    {
        window.alert('Enter a password to check')
    }
    else
    {
        fetch('/validate_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ oldpword: oldpword }), 
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                console.log("Correct Password!");
                window.alert("Correct Password!");
                //msgarea.innerText = 'Correct Password!';
                newpassword.disabled = false;
                renewpassword.disabled = false;
                submitbtn.disabled = false;
                submitbtn.classList.add('enable');
                submitbtn.style.backgroundColor = '#478CCF';

            } else {
                console.log("Wrong Password!");
                window.alert("Wrong Pasword");
                //msgarea.innerText = 'Wrong Password';
                submitbtn.classList.remove('enable');
                submitbtn.style.backgroundColor = 'rgba(128, 128, 128, 0.473);';
            }
        })
        .catch(() => {
            console.log("Something went wrong while validating the password");
        });
    }

    
});


document.querySelector('#changepword').addEventListener('click',function() {
    const newpasswordvalue = document.querySelector('#newpwordBox').value;
    const renewpasswordvalue = document.querySelector('#renewpwordBox').value;
    if(newpasswordvalue==renewpasswordvalue){
        window.alert('Password changed successfully!');
    } else {
        window.alert('Enter new passwords correctly!');
    }
})

