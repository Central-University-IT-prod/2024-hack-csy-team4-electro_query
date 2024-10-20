<template>
  <div>
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <div>
        <label for="registerName">Имя:</label>
        <input type="text" id="registerName" v-model="registerName">
      </div>
      <div>
        <label for="registerSureName">фамилия:</label>
        <input type="text" id="registerSureName" v-model="registerSureName">
      </div>
      <div>
        <label for="registerAge">возраст:</label>
        <input type="text" id="registerAge" v-model="registerAge">
      </div>
      <button type="submit">зарегистрироватся</button>
    </form>

    <h2>Авторизация</h2>
    <form @submit.prevent="login">
      <div>
        <label for="loginName">Имя:</label>
        <input type="text" id="loginName" v-model="loginName">
      </div>
      <div>
        <label for="loginSureName">фамилия:</label>
        <input type="text" id="loginSureName" v-model="loginSureName">
      </div>
      <button type="submit">войти</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'AuthComponent',
  data() {
    return {
      registerName: '',
      registerSureName: '',
      registerAge: '',
      loginName: '',
      loginSureName: '',
    }
  },
  methods: {
    async register() {
      const response = await axios.post('http://127.0.0.1:8000/users/', {
        name: this.registerName,
        surname: this.registerSureName,
        age: Number(this.registerAge)
      });

      console.log("Register " + response.data);
      this.$emit('handleAunt');
    },

    async login() {

    }
  }
}
</script>

<style>
</style>
