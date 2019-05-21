
$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var newemail = $("input[name=newemail]").val();
        if (!newemail) {
            zlalert.alertInfoToast('请输入邮箱');
            return;
        }
        zlajax.get({
            'url': '/cms/email_captcha/',
            'data': {
                'newemail': newemail
            },
            'success': function (data) {
                if(data['code'] === 200){
                    zlalert.alertSuccessToast('邮件发送成功，请注意查收！');
                }else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var newemailE = $("input[name=newemail]");
        var captchaE = $("input[name=captcha]");

        var newemail = newemailE.val();
        var captcha = captchaE.val();

        zlajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'newemail': newemail,
                'captcha': captcha
            },
            'success': function (data) {
                if(data['code'] === 200){
                    zlalert.alertSuccessToast('恭喜，邮箱修改成功！');
                    newemailE.val("");
                    captchaE.val("");
                }else {
                    zlalert.alertInfo(data['message']);
                    captchaE.val("");
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        })
    })
})