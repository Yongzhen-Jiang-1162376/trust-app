const notifySuccess = function(message) {
    new Notify({
        status: 'success',
        title: '',
        text: message,
        effect: 'fade',
        speed: 300,
        autotimeout: 1500,
        position: 'right bottom'
    })
}

const notifyError = function(message) {
    new Notify({
        status: 'error',
        title: '',
        text: message,
        effect: 'fade',
        speed: 300,
        autotimeout: 1500,
        position: 'right bottom'
    })
}

const nzDateToISO = function(dateString) {
    const nzDate = DateTime.fromFormat(dateString, "dd/MMM/yyyy")
    return nzDate.toISO()
}
