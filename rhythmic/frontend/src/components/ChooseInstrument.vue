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

        <h1>Choose Instrument</h1>


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

        <div id="tableDiv">
            <table v-if="instruments.length > 0" id="instrumentsTable">

                <thead>
                    <tr>
                        <th>Instruments Used In {{ song.name }}</th>
                    </tr>
                </thead>

                <tbody> 
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
            const response = await axios.get('http://localhost:8000/findinstruments', {withCredentials: true});

            if (response.status === 200) {
                this.song = response.data.song;
                this.artist = response.data.artist;
                this.instruments = response.data.instruments || [];
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

        async instrumentChosen(instrument){

            try{
                this.popup = true,

                console.log("Request Payload:", {instrument: instrument, song: this.song.name, artist: this.song.artist});
                
                const response = await fetch("http://localhost:8000/generatednotes", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({instrument: instrument, song: this.song.name, artist: this.song.artist})
                });

                const data = await response.json();

                if (data.error) {
                    console.error("Error in generating notes:", data.error);
                    return;
                }
                
                localStorage.setItem('songName', this.song.name);
                localStorage.setItem('artistName', this.song.artist);
                localStorage.setItem('instrument', instrument);

                this.$router.push('/generatednotes');
            }

            catch(error){
                console.error("Error in generating notes:", error);
            }
        },


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