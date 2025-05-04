<!-- Forgotten credentials page -->
<template>
    <div id="forgotCredentials">
        <h1>Forgot Username or Password</h1>

        <!-- The form necessary to get data from the user -->
        <form @submit.prevent="submitForm">
            
            <div class="inputs">
                <label for="name">Name:</label>
                <input type="text" v-model="form.name" id="name" required>
            </div>

            <div class="inputs">
                <label for="email">Email:</label>
                <input type="email" v-model="form.email" id="email" required>
            </div>

            <div class="inputs">
                <label for="birthday">Date of Birth:</label>
                <input type="date" v-model="form.birthday" id="birthday" required>
            </div>

            <div id="forgotButtons">
                <button type="button" @click="back" id="back">Back</button>
                <button type="submit" id="submit" v-if="noanswer">Submit</button>
                <button type="button" id="reset" v-if="answer" @click="reset">Reset Password</button>
            </div>

        </form>
    </div>
</template>


<script>
import axios from 'axios';
import router from '../router';

export default {

    name: 'ForgotCredentials',
    data() {
        return {
            form: {
                name: '',
                email: '',
                birthday: '',
            },

            // These variables are to or not to display the forgotten password page 
            // When noanswer is true, the username has been displayed and the submit button will disappear
            // When answer is true, Reset Password button will be displayed to allow the user reset their forgotten password
            answer: false,
            noanswer: true
        };
    },

    methods: {
        async submitForm() {
            try {
                // Sending the data to the backend
                const response = await axios.post('http://localhost:8000/forgotcredentials/', this.form);

                // Getting a response
                if (response.status === 200) {
                    alert(response.data.message);
                    this.answer = true
                    this.noanswer = false
                }

            } 
            
            // Displaying error 
            catch (error) {
                alert(error.response?.data?.error || "Error processing request");
            }
        },

        // Back button functionality
        back() {
            router.push('/login');
        },

        // Redirect the user to the reset password page
        reset(){
            router.push('/resetpassword');
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
    grid-gap: 40px;
    margin-top: 5%;
}

#forgotButtons{
    display: grid;
    grid-template-areas: 'back submit';
    justify-content: center;
    margin-top: 6%;
    grid-gap: 35%;
}

#back, #submit, #reset{
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

#submit, #reset{
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