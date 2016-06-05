var storage = $.localStorage

var chirp = new Chirp();
var base_url = 'http://chirp.i2p.pub:8000/'
var user_login_url = 'user/login/'
var user_detail_url = 'user/detail/'
var discuss_url = 'discuss/'

function Chirp() {
    var self = this;
    self.jwt = storage.get('jwt');

    self.username = '';
    self.email = '';
    self.avatar = '';
    self.id = '';
    self.post_url = window.location.protocol +'//'+ window.location.hostname + window.location.pathname;

    self.ajax = function (url, method, data) {
        var request = {
            url: url,
            type: method,
            cache: false,
            dataType: 'json',
            data: data,
            beforeSend: function (xhr) {
                if (self.jwt != null) {
                    xhr.setRequestHeader("Authorization",
                        "JWT " + self.jwt);
                }
            },
            error: function (jqXHR) {
                console.log("ajax error " + jqXHR.responseText);
            }
        };
        return $.ajax(request);
    }
    self.setJWT = function (jwt) {
        storage.set('jwt', jwt);
        self.jwt = jwt;
    }
    self.initUser = function (user) {
        self.username = user.username;
        self.email = user.email;
        self.avatar = user.avatar;
        self.id = user.id;
    }
    return self;
}


function login() {
    vex.dialog.open({
        message: 'Enter your username and password:',
        input: "<input name=\"email\" type=\"text\" placeholder=\"Email\" required />\n<input name=\"password\" type=\"password\" placeholder=\"Password\" required />",
        buttons: [
            $.extend({}, vex.dialog.buttons.YES, {
                text: 'Login'
            }), $.extend({}, vex.dialog.buttons.NO, {
                text: 'Back'
            })
        ],
        callback: function (data) {
            if (data === false) {
                return console.log('Cancelled');
            }
            console.log(data)
            chirp.ajax(base_url + user_login_url, 'POST', data).done(function (resp) {
                chirp.setJWT(resp.jwt)
                console.log(resp);
                chirp.initUser(resp.user);
            });
            return console.log('Username', data.username, 'Password', data.password);
        }
    });
}

function init() {
    chirp.ajax(base_url + user_detail_url, 'get').done(function (resp) {
        console.log(resp);
        chirp.initUser(resp);
        $('.chirp-username').text(chirp.username);
        $('#chirp-social-oauth');
    });
    initDiscuss();
}

function initDiscuss() {
    data = {
        post_url: encodeURI(chirp.post_url)
    }
    console.log(data)
    chirp.ajax(base_url + discuss_url, 'get', data).done(function (resp) {
        console.log(resp.results);
        var discussHtml = template('chirp-discuss-template', {
            'discussList': resp.results
        });
        console.log(discussHtml);
        document.getElementById('content').innerHTML = discussHtml;
    });
}

function sendDiscuss(content) {
    data = {
        content: $('#chirp-discuss-content').val(),
        post_url: window.location.protocol +'//'+ window.location.hostname + window.location.pathname,
        reply_to: 4,
        parent_id: 1
    }
    console.log(data);
    chirp.ajax(base_url + discuss_url, 'post', data).done(function (resp) {
        console.log(resp)
    })
}

init();