export class BoardService {

    static getBoard(worldId) {
        return fetch('http://localhost:8000/api/worlds/' + worldId)
            .then(r => r.json())
    }

    static async getAllCities(worldId) {
        await this.simulate_delay(1000)
        return fetch('http://localhost:8000/api/worlds/' + worldId + '/cities')
            .then(r => r.json())
    }

    static async getAllPlayers(worldId) {
        await this.simulate_delay(500)
        return fetch('http://localhost:8000/api/worlds/' + worldId + '/players')
            .then(r => r.json())
    }

    static getIndexOfPlayerInCity(worldId, player) {
        return fetch('http://localhost:8000/api/worlds/' + worldId + '/cities/' + player.city.id)
            .then(r => r.json())
            .then(city => city.players_in_city.indexOf(player.id)) // That logic might not be here
    }

    static simulate_delay(delay) {
        return new Promise( res => setTimeout(res, delay) );
    }
}