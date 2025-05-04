<!-- This page displays the generated music sheet -->
<template>

    <head>
        <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    </head>

    <div id="home">

        <!-- The icons at the top to allow the user to logout or come back to the main page -->
        <div id="icons">
            <button type="button" id="logout" @click="logout">
                <i class='bx bx-log-out'></i>
            </button>

            <button type="button" id="main" @click="main">
                <i class='bx bx-home'></i>
            </button>
        </div>

        <h1>Generated Notes For "{{ songName }}" By "{{ artistName }}" For "{{ instrument }}"</h1>
        
        <!-- If there is any music sheet available, the PDF will be displayed -->
        <div v-if="musicSheet">
            <iframe v-if="musicSheet" :src="'http://localhost:8000' + musicSheet" width="100%" height="550px"></iframe>
        </div>

        <button type="button" id="back" @click="back">Back</button>

        <!-- The save button -->
        <button type="button" id="saveSheet" @click="saveSheet">Save</button>

    </div>
</template>


<script>
import axios from 'axios';

export default{
    name: 'GeneratedNotes',

    data(){
        return{
            songName: '',
            artistName: '', 
            instrument: '', 
            musicSheet: ''
        }
    },

    async mounted(){
        try{
            // Getting the song data from the local storage
            const storedSongName = localStorage.getItem('songName');
            const storedArtistName = localStorage.getItem('artistName');
            const storedInstrument = localStorage.getItem('instrument');

            // Check to see if there is any data missing
            if (!storedSongName || !storedArtistName || !storedInstrument) {
                alert('Song, artist, or instrument not found. Please try again.');
            }

            // Setting the song data from the local storage to variables
            this.songName = storedSongName;
            this.artistName = storedArtistName;
            this.instrument = storedInstrument;
            
            // Sending a request to the backend to get the PDF file
            const response = await axios.get('http://localhost:8000/generatednotes', {params: {song: this.songName, artist: this.artistName, instrument: this.instrument}, withCredentials: true});

            // Check the response
            if (response.status === 200 && response.data.musicSheet) {
                this.musicSheet = response.data.musicSheet;
            }

            // Display the error
            else {
                alert('generating notes failed');
            }
        }

        // Display the error
        catch(error){
            if (error.response || error.response.data.error) {
                alert(error.response.data.error);
            } 
            
            else {
                alert('generating notes failed.');
            }
        }
    },

    methods: {

        // The function will be called to save the music sheet
        async saveSheet() {

            try {

                // Check to see if the music sheet is available
                if (!this.musicSheet) {
                    alert("No music sheet available to save.");
                    return;
                }

                // Get the music sheet PDF file
                const response = await fetch(`http://localhost:8000${this.musicSheet}`); 
                const blob = await response.blob(); 
                const file = new File([blob], `${this.songName}.pdf`, { type: "application/pdf" }); 

                // Create FormData and append data to be stored in the database
                let formData = new FormData();
                formData.append("song", this.songName);
                formData.append("artist", this.artistName);
                formData.append("instrument", this.instrument);

                // Attach the actual PDF file
                formData.append("pdfFile", file); 

                console.log(file)

                // Send the POST request to save the music sheet
                const saveResponse = await axios.post('http://localhost:8000/savemusicsheet', formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                    withCredentials: true
                });

                // Check the response
                if (saveResponse.status === 201) {
                    alert("Music sheet saved successfully!");
                } 
                
                // Displaying error
                else {
                    alert(saveResponse.data.error);
                }
            } 
            
            // Displaying error
            catch (error) {
                alert(error.response?.data?.error || "Saving music sheet failed.");
            }
        },

        // Redirecting functionalities
        back(){
            this.$router.push('/chooseinstrument');
        },

        logout(){
            localStorage.removeItem('token');
            this.$router.push('/');
        },

        main(){
            this.$router.push('/mainpage');
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
    right: 65%;
    margin-bottom: 2%;
}

#saveSheet{
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
    left: 65%;
    margin-bottom: 2%;
}

</style>