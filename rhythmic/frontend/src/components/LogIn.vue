<!-- This page is for the login functionality of the app -->
<template>
    <div id="login">
        <h1>Log In</h1>

        <!-- The form necessary to get data for login -->
        <form method="post" @submit.prevent="submitForm">

            <div class="inputs">
                <label for="username">Username:</label>
                <input type="text" v-model="form.username" id="username" name="username" required>
            </div>

            <div class="inputs">
                <label for="password">Password:</label>
                <input type="password" v-model="form.password" id="password" name="password" pattern="(?=.*\d)[A-Za-z\d]{6,}" required>
            </div>

            <p id="forgotten" @click="forgotten">Forgotten username or password</p>

            <div id="logInButtons">
                <button type="button" id="back" @click="backFunction">Back</button>
                <button type="submit" id="submit" @click="submitForm">Submit</button>
            </div>

        </form>
    </div>
</template>


<script>
import axios from 'axios';
import router from '../router';

export default{
    name: 'LogIn',

    data(){
        return{
            form: {
                username: '',
                password: '',
            }
        };
    },

    methods: {

        async submitForm(){

            event.preventDefault();

            try{
                // Sending the data to the backend
                const response = await axios.post('http://localhost:8000/login/', this.form, { withCredentials: true })

                // Getting response from the backend
                if(response.status === 200){
                    alert('You have successfully logged in');

                    localStorage.setItem('token', response.data.token);
                    localStorage.setItem('name', response.data.name);

                    router.push('/mainpage');
                }
            }

            // Displaying the error message
            catch(error){
                if (error.response && error.response.data.error){
                    alert(error.response.data.error);
                }

                else{
                    alert("error during login");
                }
            }
        },

        // The back button function
        backFunction(){
            router.push('/');
        },

        // When the forgotten credential option is chosen redirects the user
        forgotten(){
            router.push('/forgotcredentials');
        }
    }
};

</script>


<style scoped>

h1{
    font-size: 3em;
    color: white;
    margin-top: 0;
}

form{
    display: grid;
    grid-template-columns: 1fr;
    grid-gap: 55px;
    margin-top: 8%;
}

#logInButtons{
    display: grid;
    grid-template-areas: 'back submit';
    justify-content: center;
    margin-top: 3%;
    grid-gap: 35%;
}

#forgotten{
    color: rgb(214, 234, 58);
}

#forgotten:hover{
    color: white;
}

#back, #submit{
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

#back{
    grid-area: back;
}

#submit{
    grid-area: submit;
}

label{
    color: white;
    font-size: 20px;
    margin-right: 4%;
}

input{
    border-radius: 12px;
    padding: 10px;
    font-size: 20px;
    border: none;
}

.inputs{
    margin-top: 1.5%;
}

</style>