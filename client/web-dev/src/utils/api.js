const API_URL = 'http://maze2.skipper.keenetic.link/user_account/'

export async function checkLogin(username, password) {
    let body = JSON.stringify({
        username: username,
        pwd: password,
        remember: false
    })
    try {
        let response = await fetch(API_URL+'login', {
            method: "POST",
            body: body,
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        response = await response.json()
        return response
    }
    catch {
        return {status: "NOT OK"}
    }
}

export async function checkLogOut (token) {
    let response = await fetch(API_URL+'logout', {
        method: "get",
        headers: {
            "token": token,
            "Content-type": "application/json; charset=UTF-8"
        }
    });

    response = await response.json()
    console.log(response)
    return response
}

export async function registration (userName, full_name, email, password) {
    let body = JSON.stringify({
        username: userName,
        full_name: full_name,
        email: email,
        phone: null,
        contacts: null,
        pwd: password,
    })
    try {
        let response = await fetch(API_URL+'registration', {
            method: "POST",
            body: body,
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        response = await response.json()
        return response
    }
    catch (error){
        console.log(error)
        return {status: "NOT OK"}
    }
}