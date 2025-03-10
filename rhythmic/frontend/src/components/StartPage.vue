<template>
    
    <h1>WELCOME TO RHYTHMIC</h1>

    <div id="startPageButtons">
        <button id="logInButton" @click="loginDirect">Log in</button>
        <button id="signUpButton" @click="signUpDirect">Sign Up</button>
    </div>

</template>

<script>

import router from '../router';

export default{
    name: 'StartPage',

    methods: {
        loginDirect(){
            router.push('/login');
        },

        signUpDirect(){
            router.push('/signup');
        }
    }
};

</script>



<style>

html{
    background: linear-gradient(90deg, #3471bc 0.39%, hsl(269, 73%, 40%) 99.86%);
}

h1{
    font-size: 3em;
    color: white;
    margin-top: 10%;
}


#startPageButtons{
    display: grid;
    grid-template-areas: 'logInButton' 'signUpButton';
    justify-content: center;
    margin-top: 10%;
}

#logInButton, #signUpButton{
    background-color: #ffffff;
    color: black;
    border: none;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 20px;
    cursor: pointer;
    border-radius: 12px;
}

#logInButton{
    grid-area: logInButton;
    margin-bottom: 60%;
}

#signUpButton{
    grid-area: signUpButton;
}

</style>