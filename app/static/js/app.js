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

const notifyWarning = function (message) {
    new Notify({
        status: 'warning',
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
    const DateTime = luxon.DateTime
    const nzDate = DateTime.fromFormat(dateString, "dd/MMM/yyyy")
    // return nzDate.toISODate()
    return nzDate.toFormat("yyyy-MM-dd")
}

const ISODateToNZDate = function(dateString) {
    const DateTime = luxon.DateTime
    const isoDate = DateTime.fromFormat(dateString, "yyyy-MM-dd")
    return isoDate.toFormat("dd/MMM/yyyy")
}
