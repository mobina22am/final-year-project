<template>
    <div>
        <h1>Sign Up</h1>
        <form method="post" @submit.prevent="submitForm">
            <label for="username">Username:</label>
            <input type="text" v-model="form.name" id="username" name="username">

            <label for="birthday">Date Of Birth:</label>
            <input type="date" v-model="form.birthday" id="birthday" name="birthday">

            <label for="email">Email:</label>
            <input type="email" v-model="form.email" id="email" name="email">

            <label for="password">Password:</label>
            <input type="password" v-model="form.password" id="password" name="password">

            <button type="button" id="back" @click="backFunction">Back</button>
            <button type="submit" id="submit" @click="submitForm">Submit</button>
        </form>
    </div>
</template>


<script>
import router from '../router';

export default{
    name: 'SignUp',
    data(){
        return{
            form: {
                name: '',
                birthday: '',
                email: '',
                password: ''
            }
        };
    },
    methods: {
        submitForm(){
            console.log(this.form);
        },

        backFunction(){
            router.push('/');
        }
    }
};

</script>