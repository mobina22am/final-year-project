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
                                <p>{{ instrument }}</p>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

export default{
    name: 'ChooseInstrument',

    data(){
        return{
            song: '',
            instruments: []
        }
    },

    mounted(){
        this.song = JSON.parse(localStorage.getItem('song')) || {};
        this.instruments = this.song.instruments || [];
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
    display: grid;
    grid-template-areas: 'searchInput' 'search';
    justify-content: center;
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

#instrumentsTable{
    border: none;
    text-decoration: none;
    cursor: pointer;
    justify-content: center;
    width: 100%;
}

.instruments {
    width: 100%;
    background-color: #ffffff;
    border: none;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    border-radius: 20px;
    text-align: center;
    padding: 8px;
}


.instruments:hover {
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

th{
    background-color: black;
    border-radius: 20px;
    padding: 15px;
    font-size: 18px;
    text-align: center;
}


</style>