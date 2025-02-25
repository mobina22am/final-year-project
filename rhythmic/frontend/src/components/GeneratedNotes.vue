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

        <h1>Generated Notes For {{ songName }} By {{ artistName }} For {{ instrument }}</h1>
        
        <div v-if="notes.length > 0">
            <div id="generatedNotes">
                <table>
                    <thead>
                        <tr>
                            <th>Pitch</th>
                            <th>Note</th>
                            <th>Start Time (s)</th>
                            <th>End Time (s)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(note, index) in notes" :key="index">
                            <td>{{ note.pitch }}</td>
                            <td>{{ note.note }}</td>
                            <td>{{ note.start_time.toFixed(2) }}</td>
                            <td>{{ note.end_time.toFixed(2) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <button type="button" id="back" @click="back">Back</button>

    </div>
</template>



<script>
import axios from 'axios';

export default{
    name: 'GeneratedNotes',

    data(){
        return{
            notes: [],
            songName: '',
            artistName: '', 
            instrument: ''
        }
    },

    async mounted(){
        try{
            const storedSongName = localStorage.getItem('songName');
            const storedArtistName = localStorage.getItem('artistName');
            const storedInstrument = localStorage.getItem('instrument');

            if (!storedSongName || !storedArtistName || !storedInstrument) {
                alert('Song, artist, or instrument not found. Please try again.');
            }

            this.songName = storedSongName;
            this.artistName = storedArtistName;
            this.instrument = storedInstrument;


            const response = await axios.get('http://localhost:8000/generatednotes', {params: {song: this.songName, instrument: this.instrument, artist: this.artistName}, withCredentials: true});

            if (response.status === 200) {
                this.notes = response.data.notes;
            }

            else {
                alert('Instruments retrieval failed. Please try again.');
            }
        }

        catch(error){
            if (error.response || error.response.data.error) {
                alert(error.response.data.error);
            } 
            
            else {
                alert('Instruments retrieval failed. Please try again.');
            }
        }

    },

    methods: {

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
};

</script>


<style scoped>



h1{
    font-size: 40px;
    color: white;
    margin-top: 0;
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

#back{
    background-color: #ffffff;
    color: black;
    border: none;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    border-radius: 18px;
    font-size: 20px;
    position: absolute;
    bottom: 0;
    right: 45%;
    margin-bottom: 2%;
}

</style>