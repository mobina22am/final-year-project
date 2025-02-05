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

        <h1>Welcome User</h1>

        <form>

            <div id="homeButtons">
                <button type="button" id="notes" @click="getNotes">Get Notes</button>
                <button type="button" id="folders" @click="accessFolders">Access Folsers</button>
            </div>

        </form>

    </div>
</template>


<script>

export default {
    name: 'MainPage',
    methods: {
        getNotes(){
            this.$router.push('/notes');
        },
        accessFolders(){
            this.$router.push('/folders');
        },

        logout(){
            localStorage.removeItem('token');
            this.$router.push('/');
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
    margin-top: 7%;
    grid-gap: 90%;
}

#notes, #folders{
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