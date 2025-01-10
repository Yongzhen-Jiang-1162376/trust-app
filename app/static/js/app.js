const notifySuccess = function(message) {
    new Notify({
        status: 'success',
        title: '',
        text: message,
        effect: 'fade',
        speed: 300,
        autotimeout: 1500,
        type: 'filled',
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
        type: 'filled',
        position: 'right bottom'
    })
}

const nzDateToISODate = function(dateString) {
    let DateTime = luxon.DateTime
    const nzDate = DateTime.fromFormat(dateString, "dd/MMM/yyyy")
    return nzDate.toISODate()
}
