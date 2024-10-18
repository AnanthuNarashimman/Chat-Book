const nameField = document.querySelector('.nameArea');
const signUp = document.querySelector('.signUp');
const signIn = document.querySelector('.signIn');
let head=document.querySelector('h2');
let btntext= document.querySelector('#register');
let form = document.querySelector('#authform');
let flashmsg = document.querySelector('.flash');

signIn.addEventListener('click', function() {
    nameField.style.maxHeight='0';
    head.innerText='Sign In';
    btntext.value='Log In';
    signIn.classList.add('active');
    signUp.classList.remove('active');
    document.getElementById('nameBox').removeAttribute('required')
    form.action = "/log_in";
    console.log("Form action set to:", form.action);
    if(flashmsg)
    {
        flashmsg.innerText='';
    }
});

signUp.addEventListener('click', function() {
    nameField.style.maxHeight='40px';
    head.innerText='Sign Up';
    btntext.value='Register';
    signUp.classList.add('active');
    signIn.classList.remove('active');
    form.action = "/add_user";
    console.log("Form action set to:", form.action);
});

