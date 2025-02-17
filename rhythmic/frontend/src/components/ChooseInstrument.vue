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

        <h1>Choose Instrument</h1>

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
                            <button type="button" class="instruments">
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
            instruments: []
        }
    },

    async mounted(){

        try{
            const response = await axios.get('http://localhost:8000/findinstruments', {withCredentials: true});

            if (response.status === 200) {
                this.song = response.data.song;
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

</style>