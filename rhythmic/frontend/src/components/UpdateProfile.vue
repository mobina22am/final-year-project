<!-- This page is for the users to update their profile -->
<template>
    <div id="profile">
        <h1>Profile</h1>

        <!-- The form to display and get data along with validations -->
        <form method="post" @submit.prevent="submitForm">

            <div class="inputs">
                <label for="name">Name:</label>
                <input type="text" v-model="form.name" id="name" name="name" pattern="[A-Za-z0-9]{3,}" required>
            </div>

            <div class="inputs">
                <label for="birthday">Date Of Birth:</label>
                <input type="date" v-model="form.birthday" id="birthday" name="birthday" required>
            </div>

            <div class="inputs">
                <label for="username">Username:</label>
                <input type="text" v-model="form.username" id="username" name="username" required>
            </div>


            <div class="inputs">
                <label for="email">Email:</label>
                <input type="email" v-model="form.email" id="email" name="email" pattern="[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"  required>
            </div>


            <div class="inputs">
                <label for="password">New Password: (optional)</label>
                <input type="password" v-model="form.password" id="password" name="password" pattern="(?=.*\d)[A-Za-z\d]{6,}">
            </div>


            <div class="inputs">
                <label for="confirmPassword">Confirm New Password:</label>
                <input type="password" v-model="form.confirmPassword" id="confirmPassword" name="confirmPassword" pattern="(?=.*\d)[A-Za-z\d]{6,}">
            </div>


            <div class="inputs">
                <label for="password">Old Password:</label>
                <input type="password" v-model="form.oldPassword" id="oldPassword" name="password" pattern="(?=.*\d)[A-Za-z\d]{6,}" required>
            </div>


            <div id="signUpButtons">
                <button type="button" id="back" @click="backFunction">Back</button>
                <button type="submit" id="submit" @click="submitForm">Update</button>
            </div>

        </form>
    </div>
</template>


<script>
import axios from 'axios';
import router from '../router';

export default{
    name: 'UpdateProfile',
    data(){
        return{
            form: {
                name: '',
                username: '',
                birthday: '',
                email: '',
                password: '',
                confirmPassword: '',
                oldPassword: '',
            }
        };
    },

    async mounted() {
        try {
            // Get data from the backend, restored from the database
            const response = await axios.get('http://localhost:8000/profile/', {withCredentials: true});

            // Setting the variables values to the data gotten from the backend
            this.form = response.data;

            if (response.status === 200) {
                this.form = response.data;
            }
        } 

        // Didplaying error data
        catch (error) {
            if (error.response && error.response.data.error) {
                alert(error.response.data.error); 
            } 
            
            else {
                alert('Profile retrieval failed. Please try again.');
            }
        }
    },

    methods: {

        async submitForm(){

            event.preventDefault();

            // The passwords should match to allow the form to be submitted
            if(this.form.password !== this.form.confirmPassword){
                alert('Passwords do not match');
                return;
            }

            try {

                // Getting data of the form and storethem in variables
                const newData = {
                    name: this.form.name,
                    username: this.form.username,
                    birthday: this.form.birthday,
                    email: this.form.email,
                    oldPassword: this.form.oldPassword,
                };

                // Check to see if the user has put a new password
                if (this.form.password) {
                    newData.password = this.form.password;
                }

                // Send request to the backend
                const response = await axios.put('http://localhost:8000/profile/', newData, {withCredentials: true});

                // Get a response
                if (response.status === 200){
                    alert('Profile Update successfully');

                    localStorage.setItem('token', response.data.token);
                    localStorage.setItem('name', response.data.name);

                    // Going back to the main page after updating
                    router.push('/mainpage');
                } 

                // Let the user know the password is wrong
                if (response.status === 400){
                    alert('Old password is incorrect');
                }
            }

            // Dispalying the error message
            catch(error){

                if (error.response && error.response.data.error) {
                    alert(error.response.data.error); 
                } 
                
                else {
                    alert('Update failed. Please try again.');
                }
            }
        },

        // Back button functionality
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
    grid-gap: 5px;
    margin-top: 1%;
}

#signUpButtons{
    display: grid;
    grid-template-areas: 'back submit';
    justify-content: center;
    margin-top: 3%;
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