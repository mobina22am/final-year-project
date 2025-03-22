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


        <h1>Saved Music Sheets</h1>

        <div id="tableDiv">

            <table v-if="storedSongs.length > 0">
                <thead>
                    <tr>
                        <div id="headerDiv">
                            <th>Song Name</th>
                            <th>Artist</th>
                            <th>Instrument</th>
                        </div>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="song in storedSongs" :key="song.id" class="songRows">
                        <td class="filesTd">
                            <button type="button" class="files" @click="viewPdf(song.id)">
                                <p>{{ song.name }}</p>
                                <p>{{ song.artist }}</p>
                                <p>{{ song.instrument}}</p>
                            </button>
                        </td>

                        <td class="deleteTd">
                            <button type="button" id="delete" @click="deleteFile(song.id)">
                                <i class='bx bx-trash'></i>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>

        </div>

        <button @click="back" id="back">Main Page</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {

    name:"AccessFolder",

    data() {
        return {
            storedSongs: []
        };
    },

    async mounted() {
        try {
            const response = await axios.get('http://localhost:8000/getsavedsongs', { withCredentials: true });

            if (response.status === 200) {
                this.storedSongs = response.data.songs;
            } else {
                alert('Failed to load saved sheets.');
            }
        } catch (error) {
            alert(error.response?.data?.error || 'Failed to fetch saved songs.');
        }
    },
    
    methods: {
        viewPdf(songId) {
            const pdfUrl = `http://localhost:8000/getmusicsheet/${songId}`;
            window.open(pdfUrl, "_blank");  // Open in a new tab
        },


        async deleteFile(songId) {
            try {
                const response = await axios.delete(`http://localhost:8000/deletesong/${songId}`, { withCredentials: true });

                if (response.status === 200) {
                    // Remove the deleted song from the array
                    this.storedSongs = this.storedSongs.filter(song => song.id !== songId);
                    alert('Music sheet deleted successfully.');
                } else {
                    alert('Failed to delete the music sheet.');
                }
            } catch (error) {
                alert(error.response?.data?.error || 'Failed to delete the song.');
            }
        },


        back(){
            this.$router.push('/mainpage');
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

h1{
    font-size: 40px;
    color: white;
    margin-top: 0;
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

table {
    border: none;
    text-decoration: none;
    cursor: pointer;
    justify-content: center;
    width: 100%;
}

.songRows{
    display: flex;
    width: 100%;
    background-color: white;
    border-radius: 20px;
    margin-bottom: 10px;
}

.filesTd{
    width: 95%;
    margin-right: 20px;
}

.deleteTd{
    margin-right: 20px;
}

.files{
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

.files:hover {
    background-color: #e0e0e0;
}

#delete{
    border: none;
    background-color: white;
    font-size: 30px;
    border-radius: 20px;
}

#delete:hover{
    background-color: red;
}

td {
    padding: 0;
    display: flex;
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
    padding-right: 100px;
    font-size: 18px;
    margin-bottom: 5px;
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
    bottom: 5%;
    right: 45%;
}


#viewPdfButton{
    background-color: white;
    color: black;
    border: none;
    padding: 10px 30px;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    border-radius: 18px;
    font-size: 20px;
    width: 100%;
}
</style>