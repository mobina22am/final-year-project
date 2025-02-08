<template>
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>

    <div id="home">

        <div id="icons">
            <button type="button" id="logout" @click="logout">
                <i class='bx bx-log-out'></i>
            </button>

            <button type="button" id="profile" @click="profile">
                <i class='bx bx-user'></i>
            </button>
        </div>

        <h1>Get Notes</h1>

        <form>

            <div id="getNotesButtons">
                <button type="button" id="find" @click="findASong">Find A Song</button>
                <button type="button" id="suggest" @click="suggestASong">Suggest A Song</button>
            </div>

        </form>

    </div>
</template>


<script>

export default {
    name: 'GetNotes',

    methods: {
        findASong(){
            this.$router.push('/findasong');
        },  

        suggestASong(){
            this.$router.push('/suggestasong');
        },

        logout(){
            localStorage.removeItem('token');
            this.$router.push('/');
        },

        profile(){
            this.$router.push('/profile');
        }
    }
}

</script>


<style scoped>


h1{
    font-size: 4em;
    color: white;
    margin-top: 0;
}

form{
    display: grid;
    grid-template-columns: 1fr;
    grid-gap: 55px;
    margin-top: 5%;
}

#getNotesButtons{
    display: grid;
    grid-template-areas: 'find' 'suggest';
    justify-content: center;
    margin-top: 7%;
    grid-gap: 90%;
}

#find, #suggest{
    background-color: #ffffff;
    color: black;
    border: none;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 30px;
    cursor: pointer;
    border-radius: 18px;
}

#suggest{
    grid-area: suggest;
}

#find{
    grid-area: find;
}

#logout{
    background-color: #ffffff00;
    color: rgb(255, 255, 255);
    border: none;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    font-size: 40px;
    cursor: pointer;
    position: absolute;
    top: 0;
    left: 0;
}

#profile{
    background-color: #ffffff00;
    color: rgb(255, 255, 255);
    border: none;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    font-size: 40px;
    cursor: pointer;
    position: absolute;
    top: 0;
    right: 0;
}

</style>