const driver = class {
    constructor(curr_lat, curr_long, dst_lat, dst_long) {
        this.clat = curr_lat
        this.clng = curr_long
        this.dlat = dst_lat
        this.dlng = dst_long
    }
}

export default (details) => {
    var tx = {
        user_lat : details.clat,
        user_long : details.clng,
        dest_lat : details.dlat,
        dest_long : details.dlng
    }

    fetch('http://localhost:8000/', {
        method : "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tx)
    }).then((resp) => {
        if (!resp.ok) {
            throw new Error(`Can't connect :( ${resp.status}`)
        }
        return resp.json()["resp"];
    })
};