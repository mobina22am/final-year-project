<template>
    <div id="login">
        <h1>Log In</h1>
        <form method="post" @submit.prevent="submitForm">

            <div class="inputs">
                <label for="username">Username:</label>
                <input type="text" v-model="form.username" id="username" name="username" required>
            </div>

            <div class="inputs">
                <label for="password">Password:</label>
                <input type="password" v-model="form.password" id="password" name="password" pattern="(?=.*\d)[A-Za-z\d]{6,}" required>
            </div>

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
                const response = await axios.post('http://localhost:8000/login/', this.form, { withCredentials: true })

                if(response.status === 200){
                    alert('You have successfully logged in');

                    localStorage.setItem('token', response.data.token);


                    // you have to add the home page here   
                    router.push('/');
                }

            }

            catch(error){
                if (error.response && error.response.data.error){
                    alert(error.response.data.error);
                }

                else{
                    alert("error during login");
                }
            }
        
        
        },

        backFunction(){
            router.push('/');
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
    margin-top: 7%;
    grid-gap: 35%;
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