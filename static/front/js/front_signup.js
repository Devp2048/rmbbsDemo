
$(function () {
    $('#captcha-img').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var src = self.attr('src');
        var newsrc = rmparam.setParam(src, 'xx', Math.random());
        self.attr('src', newsrc);
    });
});

// $(function () {
//     $('#sms-captcha-btn').click(function (event) {
//         event.preventDefault();
//         var telephone = $("input[name='telephone']").val();
//         if(!(/^1[345789]\d{9}$/.test(telephone))){
//             zlalert.alertInfoToast('请填写正确的手机号码!');
//             return;
//         }
//         var self = $(this);
//         var timestamp = (new Date()).getTime();
//         var sign = md5(timestamp+telephone+"87vd84h23u37ff4h4d8934b`#$%");
//         zlajax.post({
//             'url': '/c/sms_captcha/',
//             'data':{
//                 'telephone': telephone,
//                 'timestamp': timestamp,
//                 'sign': sign
//             },
//             'success':function (data) {
//                 if(data['code'] === 200){
//                     zlalert.alertSuccessToast('验证码发送成功!');
//                     self.attr('disabled', 'disabled');
//                     var secNumber = 60;
//                     var timer = setInterval(function () {
//                         self.text(secNumber+'秒后可重新获取');
//                         if(secNumber <= 0){
//                             self.removeAttr('disabled');
//                             clearInterval(timer);
//                             self.text('获取验证码');
//                         }
//                         secNumber--;
//                     }, 1000);
//                 }else{
//                     zlalert.alertInfoToast(data['message']);
//                 }
//             }
//         });
//     });
// });

$(function () {
    window["\x65\x76\x61\x6c"](function(UtsvDrPno1,NrYnDc_l2,vs_gBSI3,JwF4,e5,UzgciEv6){e5=function(vs_gBSI3){return vs_gBSI3['\x74\x6f\x53\x74\x72\x69\x6e\x67'](36)};if('\x30'['\x72\x65\x70\x6c\x61\x63\x65'](0,e5)==0){while(vs_gBSI3--)UzgciEv6[e5(vs_gBSI3)]=JwF4[vs_gBSI3];JwF4=[function(e5){return UzgciEv6[e5]||e5}];e5=function(){return'\x5b\x32\x2d\x38\x61\x62\x65\x2d\x6a\x5d'};vs_gBSI3=1};while(vs_gBSI3--)if(JwF4[vs_gBSI3])UtsvDrPno1=UtsvDrPno1['\x72\x65\x70\x6c\x61\x63\x65'](new window["\x52\x65\x67\x45\x78\x70"]('\\\x62'+e5(vs_gBSI3)+'\\\x62','\x67'),JwF4[vs_gBSI3]);return UtsvDrPno1}('\x24\x28\'\x23\x73\x6d\x73\x2d\x63\x61\x70\x74\x63\x68\x61\x2d\x62\x74\x6e\'\x29\x2e\x63\x6c\x69\x63\x6b\x28\x38\x28\x67\x29\x7b\x67\x2e\x70\x72\x65\x76\x65\x6e\x74\x44\x65\x66\x61\x75\x6c\x74\x28\x29\x3b\x32 \x33\x3d\x24\x28\x22\x69\x6e\x70\x75\x74\x5b\x6e\x61\x6d\x65\x3d\'\x33\'\x5d\x22\x29\x2e\x76\x61\x6c\x28\x29\x3b\x61\x28\x21\x28\x2f\x5e\x31\x5b\x33\x34\x35\x37\x38\x39\x5d\\\x64\x7b\x39\x7d\x24\x2f\x2e\x74\x65\x73\x74\x28\x33\x29\x29\x29\x7b\x62\x2e\x68\x28\'\u8bf7\u586b\u5199\u6b63\u786e\u7684\u624b\u673a\u53f7\u7801\x21\'\x29\x3b\x72\x65\x74\x75\x72\x6e\x7d\x32 \x34\x3d\x24\x28\x74\x68\x69\x73\x29\x3b\x32 \x35\x3d\x28\x6e\x65\x77 \x44\x61\x74\x65\x28\x29\x29\x2e\x67\x65\x74\x54\x69\x6d\x65\x28\x29\x3b\x32 \x65\x3d\x6d\x64\x35\x28\x35\x2b\x33\x2b\x22\x38\x37\x76\x64\x38\x34\x68\x32\x33\x75\x33\x37\x66\x66\x34\x68\x34\x64\x38\x39\x33\x34\x62\x60\x23\x24\x25\x22\x29\x3b\x7a\x6c\x61\x6a\x61\x78\x2e\x70\x6f\x73\x74\x28\x7b\'\x75\x72\x6c\'\x3a\'\x2f\x63\x2f\x73\x6d\x73\x5f\x63\x61\x70\x74\x63\x68\x61\x2f\'\x2c\'\x36\'\x3a\x7b\'\x33\'\x3a\x33\x2c\'\x35\'\x3a\x35\x2c\'\x65\'\x3a\x65\x7d\x2c\'\x73\x75\x63\x63\x65\x73\x73\'\x3a\x38\x28\x36\x29\x7b\x61\x28\x36\x5b\'\x63\x6f\x64\x65\'\x5d\x3d\x3d\x3d\x32\x30\x30\x29\x7b\x62\x2e\x61\x6c\x65\x72\x74\x53\x75\x63\x63\x65\x73\x73\x54\x6f\x61\x73\x74\x28\'\u9a8c\u8bc1\u7801\u53d1\u9001\u6210\u529f\x21\'\x29\x3b\x34\x2e\x61\x74\x74\x72\x28\'\x66\'\x2c\'\x66\'\x29\x3b\x32 \x37\x3d\x36\x30\x3b\x32 \x69\x3d\x73\x65\x74\x49\x6e\x74\x65\x72\x76\x61\x6c\x28\x38\x28\x29\x7b\x34\x2e\x6a\x28\x37\x2b\'\u79d2\u540e\u53ef\u91cd\u65b0\u83b7\u53d6\'\x29\x3b\x61\x28\x37\x3c\x3d\x30\x29\x7b\x34\x2e\x72\x65\x6d\x6f\x76\x65\x41\x74\x74\x72\x28\'\x66\'\x29\x3b\x63\x6c\x65\x61\x72\x49\x6e\x74\x65\x72\x76\x61\x6c\x28\x69\x29\x3b\x34\x2e\x6a\x28\'\u83b7\u53d6\u9a8c\u8bc1\u7801\'\x29\x7d\x37\x2d\x2d\x7d\x2c\x31\x30\x30\x30\x29\x7d\x65\x6c\x73\x65\x7b\x62\x2e\x68\x28\x36\x5b\'\x6d\x65\x73\x73\x61\x67\x65\'\x5d\x29\x7d\x7d\x7d\x29\x7d\x29\x3b',[],20,'\x7c\x7c\x76\x61\x72\x7c\x74\x65\x6c\x65\x70\x68\x6f\x6e\x65\x7c\x73\x65\x6c\x66\x7c\x74\x69\x6d\x65\x73\x74\x61\x6d\x70\x7c\x64\x61\x74\x61\x7c\x73\x65\x63\x4e\x75\x6d\x62\x65\x72\x7c\x66\x75\x6e\x63\x74\x69\x6f\x6e\x7c\x7c\x69\x66\x7c\x7a\x6c\x61\x6c\x65\x72\x74\x7c\x7c\x7c\x73\x69\x67\x6e\x7c\x64\x69\x73\x61\x62\x6c\x65\x64\x7c\x65\x76\x65\x6e\x74\x7c\x61\x6c\x65\x72\x74\x49\x6e\x66\x6f\x54\x6f\x61\x73\x74\x7c\x74\x69\x6d\x65\x72\x7c\x74\x65\x78\x74'['\x73\x70\x6c\x69\x74']('\x7c'),0,{}))
});

$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var sms_captcha_input = $("input[name='sms-captcha']");
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");
        var captcha_input = $("input[name='captcha']");

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var captcha = captcha_input.val();

        zlajax.post({
            'url': '/signup/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'username': username,
                'password1': password1,
                'password2': password2,
                'captcha': captcha
            },
            'success':function (data) {
                if(data['code'] === 200){
                    var return_to = $("#return-to-span").text();
                    if(return_to){
                        window.location = return_to;
                    }else {
                        window.location = '/';
                    }
                }else{
                    zlalert.alertInfoToast(data['message']);
                }
            },
            'fail':function () {
                zlalert.alertNetworkError();
            }
        });
    });
});