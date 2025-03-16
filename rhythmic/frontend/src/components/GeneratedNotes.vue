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


        <h1>Generated Notes For "{{ songName }}" By "{{ artistName }}" For "{{ instrument }}"</h1>
        
        <div v-if="musicSheet">
            <iframe v-if="musicSheet" :src="'http://localhost:8000' + musicSheet" width="100%" height="550px"></iframe>
        </div>

        <button type="button" id="back" @click="back">Back</button>
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
            const storedSongName = localStorage.getItem('songName');
            const storedArtistName = localStorage.getItem('artistName');
            const storedInstrument = localStorage.getItem('instrument');

            if (!storedSongName || !storedArtistName || !storedInstrument) {
                alert('Song, artist, or instrument not found. Please try again.');
            }

            this.songName = storedSongName;
            this.artistName = storedArtistName;
            this.instrument = storedInstrument;


            
            const response = await axios.get('http://localhost:8000/generatednotes', {params: {song: this.songName, artist: this.artistName, instrument: this.instrument}, withCredentials: true});

            if (response.status === 200 && response.data.musicSheet) {
                this.musicSheet = response.data.musicSheet;
            }

            else {
                alert('generating notes failed');
            }
        }

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

        async saveSheet() {
            try {
                const response = await fetch(this.musicSheet); // Fetch the actual PDF file
                const blob = await response.blob(); // Convert response to Blob
                const file = new File([blob], "music_sheet.pdf", { type: "application/pdf" }); // Create a File object

                let formData = new FormData();
                formData.append("song", this.songName);
                formData.append("artist", this.artistName);
                formData.append("instrument", this.instrument);
                formData.append("pdfFile", file); // Attach the actual file

                const saveResponse = await axios.post('http://localhost:8000/savemusicsheet', formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                    withCredentials: true
                });

                if (saveResponse.status === 201) {
                    alert('Music sheet saved successfully!');
                } else {
                    alert(saveResponse.data.error);
                }
            } 
            
            catch (error) {
                alert(error.response?.data?.error || 'Saving music sheet failed.');
            }
        },

        back(){
            this.$router.push('/chooseinstrument');
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