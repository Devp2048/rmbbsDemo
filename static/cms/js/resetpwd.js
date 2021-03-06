
$(function () {
    $("#submit").click(function (event) {
        event.preventDefault(); //阻止按钮默认的提交表单的事件

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        zlajax.post({
            'url':'/cms/resetpwd/',
            'data':{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'newpwd2':newpwd2
            },
            'success': function (data) {
                if(data['code'] === 200){
                    zlalert.alertSuccessToast("恭喜！密码修改成功！");
                    oldpwdE.val("")  //修改成功后清除输入的内容
                    newpwdE.val("")
                    newpwd2E.val("")
                }else{
                    var message = data['message'];
                    zlalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError(error)
            }
        });
    });
});