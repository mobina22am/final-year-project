<template>

    <head>
        <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    </head>

    <div id="home">

        <div id="icons">
            <button type="button" id="logout" @click="logout">
                <i class='bx bx-log-out'></i>
            </button>

            <button type="button" id="main" @click="main">
                <i class='bx bx-home'></i>
            </button>
        </div>

        <h1>Welcome {{ user }}</h1>

        <form>

            <div id="homeButtons">
                <button type="button" id="notes" @click="getNotes">Get Notes</button>
                <button type="button" id="folders" @click="accessFolders">Access Folder</button>
                <button type="button" id="profile" @click="editProfile">Edit Profile</button>
            </div>

        </form>

    </div>
</template>


<script>

export default {
    name: 'MainPage',

    data(){
        return{
            user: ''
        }
    },

    mounted(){
        this.user = localStorage.getItem('name');
    },

    methods: {
        getNotes(){
            this.$router.push('/getnotes');
        },

        accessFolders(){
            this.$router.push('/accessfolder');
        },

        logout(){
            localStorage.removeItem('token');
            this.$router.push('/');
        },

        editProfile(){
            this.$router.push('/profile');
        },

        main(){
            this.$router.push('/mainpage');
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

#homeButtons{
    display: grid;
    grid-template-areas: 'notes' 'folders';
    justify-content: center;
    margin-top: 3%;
    grid-gap: 40%;
}

#notes, #folders, #profile{
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

#folders{
    grid-area: folders;
}

#notes{
    grid-area: notes;
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

#main{
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