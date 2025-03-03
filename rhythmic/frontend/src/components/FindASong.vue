<template>

    <head>
        <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    </head>

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

        <div id="popUpWindow" v-if="popup">
            <div id="insidePopUp">
                <h2>Instrument Detection Started</h2>
                <p>You have chosen the song: {{ this.songName }} by: {{ this.artistName }}.</p>
                <h3 class="inform">Please wait for the system to find the instruments</h3>
                <h3 class="inform">THIS MIGHT TAKE A FEW MINUTES</h3>

                <div id="loading">
                    <div id="loadingCircle">
                    </div>
                </div>

            </div>
        </div>

        <form @submit.prevent="search">
            <input type="text" v-model="userInput" placeholder="Type In The Song Detail" id="searchInput" required>
            <button type="button" id="back" @click="back" class="findASongButtons">Back</button>
            <button type="submit" id="search" class="findASongButtons">Search</button>
        </form>

        <div id="tableDiv">
            <table v-if="songs.length > 0" id="songsTable">
                <thead>
                    <tr>
                        <div id="headerDiv">
                            <th id="tableHeader1">Song</th>
                            <th id="tableHeader2">Artist</th>
                        </div>
                    </tr>
                </thead>

                <tbody> 
                    <tr v-for="(song, index) in songs" :key="index">
                        <td colspan="2">
                            <button type="button" class="songs" @click="songChosen(song)">
                                <p>{{ song.name }}</p>
                                <p>{{ song.artist }}</p>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script>

export default {
    name: 'FindASong',

    data(){
        return{
            userInput: '',
            songs: [],
            apiToken: '',
            popup: false,
            songName: '',
            artistName: ''
        }
    },

    async mounted(){
        this.apiToken = await this.getSpotifyToken();
    },

    
    methods: {


        async search(){
            if (this.userInput === ''){
                return;
            }

            if (this.apiToken === ''){
                this.apiToken = await this.getSpotifyToken();
            }

            const response = await fetch(`https://api.spotify.com/v1/search?q=${encodeURIComponent(this.userInput)}&type=track&limit=50`, { headers: { Authorization: `Bearer ${this.apiToken}` }});

            const data = await response.json();

            if (data.tracks && data.tracks.items) {
                this.songs = data.tracks.items.map(track => ({name: track.name, artist: track.artists.map(artist => artist.name).join(', ')}));
            } 
            
            else {
                this.songs = [];
            }

        },

        async getSpotifyToken() {
            const clientId = '14d9c89768f742eba1002eee652142c1';
            const clientSecret = '3899528fce97481cb861f4c058fc44fe';
            const response = await fetch('https://accounts.spotify.com/api/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({ grant_type: 'client_credentials', client_id: clientId, client_secret: clientSecret })
            });

            const data = await response.json();
            return data.access_token;
        },


        async songChosen(song){
            try {

                this.popup = true;
                this.songName = song.name;
                this.artistName = song.artist;

                
                // add a confirm here before downloading the song

                const response = await fetch("http://localhost:8000/findinstruments", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({name: song.name, artist: song.artist})
                });

                const data = await response.json();

                if (data.error) {
                    console.error("Error in finding instruments:", data.error);
                    return;
                }

                this.$router.push('/chooseinstrument');
            } 
            
            catch (error) {
                console.error("Error in finding instruments:", error);
            }
        },


        back(){
            this.$router.push('/getnotes');
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
    font-size: 30px;
    color: white;
    margin-top: 0;
}

form{
    display: grid;
    grid-template-columns: 1fr;
    grid-template-areas: 'searchInput' 'search';
    justify-content: center;
}

#searchInput, #search, #back{
    background-color: #ffffff;
    color: black;
    border: none;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    border-radius: 18px;
}

.findASongButtons{
    grid-area: search;
    width: 25%;
    margin-bottom: 20px;
    font-size: 30px;
    bottom: 0;
    position: absolute;
}

#back{
    left: 20%;
}

#search{
    right: 20%;
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

#tableDiv {
    width: 100%; 
    margin: auto; 
    max-height: 370px;
    overflow-y: auto;
    margin-top: 2%;
    display: block;
    border-radius: 27px;
}

#tableDiv::-webkit-scrollbar {
    display: none;
    scrollbar-width: none;
}

#songsTable{
    border: none;
    text-decoration: none;
    cursor: pointer;
    justify-content: center;
    width: 100%;
}

.songs {
    width: 100%;
    background-color: #ffffff;
    border: none;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    border-radius: 20px;
    padding-left: 30px;
    padding-right: 30px;
}

.songs:hover {
    background-color: #e0e0e0;
}

td {
    padding: 0;
}

thead{
    position: sticky;
    top: 0;
    color: white;
}

#headerDiv{
    border-collapse: collapse;
    background-color: black;
    border-radius: 20px;
    display: flex;
    justify-content: space-between;
    padding: 15px;
    padding-left: 30px;
    padding-right: 30px;
    font-size: 18px;
}

#tableHeader1{
    text-align: left;
}

#tableHeader2{
    text-align: right;
}

#popUpWindow{
    background-color: white;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 100;
    padding: 50px;
    border: black 2px solid;   
    height: 100%;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.5); 
}

#insidePopUp{
    background-color: white;
    padding: 50px;
    border-radius: 20px;
    text-align: center;
    font-size: 20px;
    color: black;
}

.inform{
    margin-top: 20px;
    font-size: 20px;
    color: red;
    text-align: center;
}

#loading{
    text-align: center;
    margin-top: 20px;
}

#loadingCircle {
    border: 10px solid #f3f3f3;
    border-top: 10px solid #3498db;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 2s linear infinite;
    display: inline-block;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

</style>
