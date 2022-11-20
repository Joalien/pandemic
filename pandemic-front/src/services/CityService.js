export class CityService {

    static getAllCities() {
        return [
            {
                name: "Los Angeles", color: "YELLOW", position: {x: 60, y: 294}, diseases: {
                    "Color.YELLOW": 3,
                    "Color.BLACK": 0,
                    "Color.BLUE": 2,
                    "Color.RED": 0,
                }
            },
            {
                name: "Mexico", color: "YELLOW", position: {x: 125, y: 318}, diseases: {
                    "Color.YELLOW": 1,
                    "Color.BLACK": 1,
                    "Color.BLUE": 0,
                    "Color.RED": 1,
                }
            }
        ]
    }
}