new Vue({
    el: '#app',
    data: {
        innerVisible: true,
        form: {
            email: ''
        },
        //图片base64
        img_base64: '',
        //图片路径
        img_src: '',
        //标签
        label: '',
        host: '',
        warning_info: '',
        loading: false,
        //剩余文件数
        remain:'',
        mode:''
    },
    created: function() {},
    filters: {

    },
    mounted() {
        // this.drawLine();
    },
    methods: {
        submitForm(form) {
            this.$refs[form].validate((valid) => {
                if (valid) {
                    var email = this.form.email
                    this.start(email)
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        resetForm(form) {
            this.$refs[form].resetFields();
        },
        //开始任务
        start(username) {
            //debugger;
            var _this = this;
            _this.loading = true;
            var url = _this.host + '/start.label?username=' + username;
            axios.get(url, {
                    timeout: 10000 * 2000
                })
                .then(function(response) {
                    _this.loading = false;
                    var data = response.data;
                    _this.innerVisible = false;
                    if (data == '' || data.remain==-1) {
                        _this.warning_info = '恭喜你，你的任务已完成'
                        return;
                    }
                    _this.img_base64 = "data:image/png;base64," + data.img_stream;
                    _this.img_src = data.img_path;
                    _this.label = data.label;
                    _this.remain = data.remain;
                    _this.mode = data.mode;
                }).catch(() => {
                    _this.$message({
                        type: 'error',
                        message: '无法获取任务'
                    });
                });

        },
        //标注
        label_image(type) {
            var _this = this;
            var img_src = _this.img_src;
            var email = _this.form.email;
            var form = {
                "type": type,
                "img_path": img_src,
                "username": email
            };
            axios.post(_this.host + '/label', form, {
                    'Content-Type': 'application/json'
                })
                .then(function(response) {
                    var data = response.data;
                    if(data=='ok'){
                        _this.start(email)
                    }else{
                        _this.$message({
                            type: 'error',
                            message: '操作失败，原因：' + data
                        });
                    }
                }).catch(() => {
                    _this.$message({
                        type: 'error',
                        message: '操作失败，服务器发生错误'
                    });
                });
        },
        good(){
            var _this = this;
            var img_src = _this.img_src;
            var email = _this.form.email;
            var data = {
                "img_path": img_src,
                "username": email
            };
            axios.post(_this.host + '/good', data, {
                    'Content-Type': 'application/json'
                })
                .then(function(response) {
                    var data = response.data;
                    if(data=='ok'){
                        _this.start(email)
                    }else{
                        _this.$message({
                            type: 'error',
                            message: '操作失败，原因：' + data
                        });
                    }
                }).catch(() => {
                    _this.$message({
                        type: 'error',
                        message: '操作失败，服务器发生错误'
                });
            });
        },
        //标注不是单据
        bad(){
            var _this = this;
            var img_src = _this.img_src;
            var email = _this.form.email;
            var data = {
                "username": email
            };
            axios.post(_this.host + '/bad', data, {
                    'Content-Type': 'application/json'
                })
                .then(function(response) {
                    var data = response.data;
                    if(data=='ok'){
                        _this.start(email)
                    }else{
                        _this.$message({
                            type: 'error',
                            message: '操作失败，原因：' + data
                        });
                    }
                }).catch(() => {
                    _this.$message({
                        type: 'error',
                        message: '操作失败，服务器发生错误'
                });
            });
        },
        //返回前一张
        rollback(){
            var _this = this;
            var email = _this.form.email;
            var data = {
                "username": email
            };
            axios.post(_this.host + '/rollback', data, {
                    'Content-Type': 'application/json'
                })
                .then(function(response) {
                    var data = response.data;
                    if(data=='ok'){
                        _this.start(email)
                    }else{
                        _this.$message({
                            type: 'error',
                            message: '操作失败，原因：' + data
                        });
                    }
                }).catch(() => {
                    _this.$message({
                        type: 'error',
                        message: '操作失败，服务器发生错误'
                });
            });
        }

    }
})