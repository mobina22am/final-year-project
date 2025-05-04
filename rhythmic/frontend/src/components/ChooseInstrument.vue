<!-- This page is for the user to choose their instrumnets -->
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

        <h1>Choose Instrument</h1>

        <!-- This pop up window will display when the user chose the instrument they wanted -->
        <!-- The pop page lets the user know the app is working on their request -->
        <div id="popUpWindow" v-if="popup">
            <div id="insidePopUp">
                <h2>Note Generation Started</h2>
                <h3 class="inform">Please wait for the system to complete the note generation</h3>
                <h3 class="inform">This is going to take only a few moments</h3>

                <div id="loading">
                    <div id="loadingCircle">
                    </div>
                </div>

            </div>
        </div>

        <!-- The table to display the list of the instruments found -->
        <div id="tableDiv">

            <!-- The table will only show of the list variable, instruments, is not empty -->
            <table v-if="instruments.length > 0" id="instrumentsTable">

                <thead>
                    <tr>
                        <th>Instruments Used In {{ song.name }}</th>
                    </tr>
                </thead>

                <tbody> 
                    <!-- Looping through the instruments list and creating a tr element for each of them-->
                    <tr v-for="(instrument, index) in instruments" :key="index">
                        <td>
                            <button type="button" class="instruments" @click="instrumentChosen(instrument)">
                                <p id="instrumentsButton">{{ instrument }}</p>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <button type="button" id="back" @click="back">Back</button>

    </div>
</template>


<script>
import axios from 'axios';

export default{
    name: 'ChooseInstrument',
    

    data(){
        return{
            song: '',
            artist: '',
            instruments: [],
            popup: false,
        }
    },

    async mounted(){

        try{
            // Getting the list of the instrument detected by the backend
            const response = await axios.get('http://localhost:8000/findinstruments', {withCredentials: true});

            // Checking the response
            if (response.status === 200) {
                this.song = response.data.song;
                this.artist = response.data.artist;
                this.instruments = response.data.instruments || [];
            }

            // Displaying the error
            else {
                alert('Instruments retrieval failed. Please try again.');
            }
        }

        // Displaying the error
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

        // The funcion gets triggered when an instrument is chosen
        async instrumentChosen(instrument){

            try{

                // popup set to true to let the pop up page appear
                this.popup = true,

                console.log("Request Payload:", {instrument: instrument, song: this.song.name, artist: this.song.artist});
                
                // Sending the instrument and details chosen to the backend for the next stage
                const response = await fetch("http://localhost:8000/generatednotes", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({instrument: instrument, song: this.song.name, artist: this.song.artist})
                });

                // Getting a response
                const data = await response.json();

                // Displaying errors
                if (data.error) {
                    console.error("Error in generating notes:", data.error);
                    return;
                }
                
                // Store data in local storage to be used in the next page
                localStorage.setItem('songName', this.song.name);
                localStorage.setItem('artistName', this.song.artist);
                localStorage.setItem('instrument', instrument);

                // Redirect to the next page
                this.$router.push('/generatednotes');
            }

            // Displaying errors
            catch(error){
                console.error("Error in generating notes:", error);
            }
        },

        // Redirecting functionalities
        back(){
            this.$router.push('/findasong');
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

form{
    display: grid;
    grid-template-columns: 1fr;
    grid-template-areas: 'searchInput' 'search';
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

#tableDiv {
    width: 100%; 
    margin: auto; 
    max-height: 400px;
    overflow-y: auto;
    margin-top: 2%;
    border-radius: 27px;
}

#tableDiv::-webkit-scrollbar {
    display: none;
    scrollbar-width: none;
}

#instrumentsTable{
    border: none;
    text-decoration: none;
    cursor: pointer;
    width: 100%;
}

.instruments {
    width: 100%;
    background-color: #ffffff;
    border: none;
    font-size: 20px;
    cursor: pointer;
    border-radius: 20px;
    margin-top: 15px;
}

.instruments:hover {
    background-color: #e0e0e0;
}

thead{
    position: sticky;
    color: white;
}

th{
    background-color: black;
    border-radius: 20px;
    padding: 20px;
    font-size: 18px;
    text-align: center;
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