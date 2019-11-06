<template>
  <div id="app">
    <img :src="qr_src" v-if="!isSuccess"/>
    <div id="success" v-else>
      <div id="info">{{nickName}}</div>
      <div>登录成功！</div>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "app",
  data() {
    return {
      isSuccess: false,
      qr_src: "",
      nickName: "",
      time: ""
    };
  },
  created() {
    const _this = this;
    this.checkStatus();
    this.time = setInterval(function() {
      _this.checkStatus();
    }, 3000);
  },
  methods: {
    checkStatus: function() {
      const _this = this;
      axios.get("/check_status").then(data => {
        data = data.data;
        switch (data.status) {
          case 0:
          case 2:
          case 4:
            this.isSuccess = false;
            this.qr_src = "";
            if(this.time == ""){
                 this.time = setInterval(function() {
                  _this.checkStatus();
                }, 3000);
            }
            break;
          case 1:
            this.qr_src = "";
            this.qr_src = "/qrcode.png";
            break;
          case 3:
            this.isSuccess = true;
            this.nickName = data.info.User.NickName;
            clearInterval(this.time);
            this.time = "";
            break;
        }
      });
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#btn {
  display: none;
}

.button {
  width: 120px;
  height: 40px;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
}

.qr img {
  display: none;
  width: 360px;
  height: 360px;
  border-radius: 10px;
  border: 8px solid #eae8e8;
}

#success div {
  margin: 10px 0;
  text-align: center;
}
</style>
