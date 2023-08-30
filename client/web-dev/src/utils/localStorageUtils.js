function getCurrentUser() {
    return localStorage.getItem("user")
}
function setCurrentUser(user){
    localStorage.setItem('user', user)
}
function removeCurrentUser() {
    localStorage.removeItem('user')
}

export {getCurrentUser, setCurrentUser, removeCurrentUser}