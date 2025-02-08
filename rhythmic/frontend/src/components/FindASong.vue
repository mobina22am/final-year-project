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

        <h1>Find A Song</h1>

        <form>

            <input type="text" placeholder="Type In The Song Detail" id="searchInput" required>

                <table id="songsTable">
                    <tr id="tableHeader">
                        <th><p id="tableHeader1">name of the song</p></th>
                        <th><p id="tableHeader2">name of the artist</p></th>
                    </tr>

                    <tr>
                        <button type="button" class="songs" @click="songChosen">
                            <td><p>song name</p></td>
                            <td><p>artist name</p></td>
                        </button>
                    </tr>
                    <tr>
                        <button type="button" class="songs" @click="songChosen">
                            <td><p>song name</p></td>
                            <td><p>artist name</p></td>
                        </button>
                    </tr>
                </table>
                
            <button type="button" id="search" @click="search">Search</button>

        </form>

    </div>
</template>


<script>

export default {
    name: 'FindASong',

    methods: {

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
    font-size: 50px;
    color: white;
    margin-top: 0;
}

form{
    display: grid;
    grid-template-columns: 1fr;
    margin-top: 5%;
    display: grid;
    grid-template-areas: 'searchInput' 'search';
    justify-content: center;
}

#searchInput, #search{
    background-color: #ffffff;
    color: black;
    border: none;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    border-radius: 18px;
}

#search{
    grid-area: search;
    font-size: 30px;
    position: absolute;
    bottom: 0;
    margin-bottom: 20px;
    width: 25%;
    left: 37.5%;
}

#searchInput{
    grid-area: searchInput;
    font-size: 20px;
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

#songsTable{
    color: black;
    border: none;
    text-decoration: none;
    cursor: pointer;
    width: 100%;
}

#tableHeader{
    color: black;
    border: none;
    padding: 15px 32px;
    font-size: 20px;
}

</style>