var storage = $.localStorage

var chirp = new Chirp();
var base_url = 'https://api.i2p.pub/'
var user_login_url = 'user/login/'
var user_register_url = 'user/registerpwd/'
var user_detail_url = 'user/detail/'
var discuss_url = 'discuss/'


function Chirp() {
    var self = this;
    self.jwt = storage.get('jwt');

    self.username = '';
    self.email = '';
    self.avatar = '';
    self.id = '';
    self.post_url = window.location.protocol + '//' + window.location.hostname + window.location.pathname;

    self.status = false

    self.ajax = function (url, method, data, isAuth) {
        if (isAuth == undefined) {
            isAuth = true;
        }
        var request = {
            url: url,
            type: method,
            cache: false,
            dataType: 'json',
            data: data,
            beforeSend: function (xhr) {
                if (isAuth && self.jwt != null) {
                    xhr.setRequestHeader("Authorization",
                        "JWT " + self.jwt);
                }
            },
            error: function (jqXHR) {
                if (jqXHR.status == 403 || jqXHR == 401) {

                }
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

    self.logout = function () {
        self.jwt = '';
        storage.remove('jwt');
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
                text: 'Register'
            })
        ],
        callback: function (data) {
            if (data === false) {
                return register();
            }
            console.log(data)
            chirp.ajax(base_url + user_login_url, 'POST', data).done(function (resp) {
                chirp.setJWT(resp.jwt)
                console.log(resp);
                chirp.initUser(resp.user);
                window.location.reload();
            });
        }
    });
}

function register() {
    vex.dialog.open({
        message: 'Enter your username and password:',
        input: "<input name=\"email\" type=\"text\" placeholder=\"Email\" required />\n" +
        "<input name=\"password\" type=\"password\" placeholder=\"Password\" required />" +
        "<input name=\"passwordAgain\" type=\"password\" placeholder=\"Password Again\" required />",
        buttons: [
            $.extend({}, vex.dialog.buttons.YES, {
                text: 'Register'
            }), $.extend({}, vex.dialog.buttons.NO, {
                text: 'Back'
            })
        ],
        callback: function (data) {
            if (data === false) {
                return console.log('Cancelled');
            }
            if (data.password != data.passwordAgain) {
                alert('两次密码不符合');
            }
            console.log(data)
            chirp.ajax(base_url + user_register_url, 'POST', data, false).done(function (resp) {
                console.log(resp);
                alert('注册成功, 请查收邮件以激活帐号');
                window.location.reload();
            });
        }
    });
}

function logout() {
    chirp.logout();
    window.location.reload();

}

function initDiscuss() {
    var data = {
        post_url: encodeURI(chirp.post_url)
    }
    console.log(data)
    chirp.ajax(base_url + discuss_url, 'get', data, false).done(function (resp) {
        console.log(resp.results);
        var discussHtml = template('chirp-discuss-template', {
            'discussList': resp.results
        });
        document.getElementById('content').innerHTML = discussHtml;
    });
}

function sendDiscuss(content) {
    if (chirp.status == false) {
        alert('请先登陆');
        return false;
    }
    if ($('#chirp-discuss-content').val() == ''){
        alert('请输入内容');
        return false;
    }
    var data = {
        content: $('#chirp-discuss-content').val(),
        post_url: window.location.protocol + '//' + window.location.hostname + window.location.pathname,
        reply_to: 1,
        parent_id: 1
    }
    console.log(data);
    chirp.ajax(base_url + discuss_url, 'post', data).done(function (resp) {
        console.log(resp);
        window.location.reload();
    });

}


function init() {
    if (storage.isEmpty('jwt')) {
        var userHtml = template('chirp-submit-area-template', {
            'username': '',
            'label': 'Login',
            'func': 'login()'
        });
        document.getElementById('submit-area').innerHTML = userHtml;
    }
    else {
        chirp.ajax(base_url + user_detail_url, 'get', []).done(function (resp) {
            chirp.initUser(resp);
            chirp.status = true;
            $('.chirp-username').text(chirp.username);
            $('#chirp-social-oauth');

            var userHtml = template('chirp-submit-area-template', {
                'username': chirp.username,
                'label': 'Logout',
                'func': 'logout()',
                'avatar': chirp.avatar
            });
            document.getElementById('submit-area').innerHTML = userHtml;

        }).fail(function (error) {
            if (error.status == 403 || error.status == 401) {
                // window.location.reload();
            }
        });
    }

    if (chirp.status == false) {
        $('#chirp-social-oauth').show();
    }
    initDiscuss();
}

init();

function githubOauth() {
    OAuth.initialize('cWoMH-Ym9_3szpTRj2-DcoCZDPo')
    OAuth.popup('github').done(function (result) {
        console.log(result)
    });
}

template.helper('dateFormat', function (date, format) {

    date = new Date(date);

    var map = {
        "M": date.getMonth() + 1, //月份
        "d": date.getDate(), //日
        "h": date.getHours(), //小时
        "m": date.getMinutes(), //分
        "s": date.getSeconds(), //秒
        "q": Math.floor((date.getMonth() + 3) / 3), //季度
        "S": date.getMilliseconds() //毫秒
    };
    format = format.replace(/([yMdhmsqS])+/g, function (all, t) {
        var v = map[t];
        if (v !== undefined) {
            if (all.length > 1) {
                v = '0' + v;
                v = v.substr(v.length - 2);
            }
            return v;
        }
        else if (t === 'y') {
            return (date.getFullYear() + '').substr(4 - all.length);
        }
        return all;
    });
    return format;
});
