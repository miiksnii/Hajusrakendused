<script setup>
import { ref } from 'vue';

const emit = defineEmits(['auth']);

const username = ref('');
const newpassword = ref('');
const lastname = ref('');

const isPasswordValid = ref(true);
const isUsername = ref(true);

const error = ref({ exists: false, name: "" });
const isaccountCreated = ref(false);

const handleLogin = (e) => {
  e.preventDefault(); // stop page reload

  // Validate inputs
  isUsername.value = username.value.length > 0;
  isPasswordValid.value = newpassword.value.length >= 6;

    const data = {
      lastname: lastname.value,
      newPassword: newpassword.value,
      username: username.value, // include username
    };
    console.log(data);

  fetch("https://demo2.z-bit.ee/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);

        if (!data.access_token) {
          error.value = { exists: true, name: data[0].message || "Unknown error" };
        } else {
          emit("auth", data.access_token);
          error.value = { exists: false, name: "" };
          isaccountCreated.value = true;
        }
      })
      .catch((err) => {
        error.value = { exists: true, name: "Server error" };
        console.error("Request failed:", err);
      });


};
</script>

<template>
    <div class="Signin-container">
      <h1 class="title has-text-left">Create User</h1>
  
      <h3 v-if="error.exists === true" class="has-text-danger">{{ error.name }}</h3>
      <h3 v-if="isaccountCreated === true" class="has-text-success">SUCCESS</h3>
  
      <div id="SigninForm" class="is-flex is-flex-direction-column">
        
        <!-- Username Field -->
        <div class="field">
          <label class="label" for="Signin-username">Username</label>
          <div class="control">
            <input
              v-model="username"
              class="input"
              type="text"
              id="Signin-username"
              placeholder="your.name@gmail.com"
              :class="{ 'is-danger': isValidUsername }"
              autocomplete="off"
              required
            />
          </div>
        </div>
  
        <!-- New Password Field -->
        <div class="field">
          <label class="label" for="Signin-newpassword">New Password</label>
          <div class="control">
            <input
              v-model="newpassword"
              class="input"
              type="password"
              id="Signin-newpassword"
              :class="{ 'is-danger': isValidPassword }"
              placeholder="new password"
              autocomplete="off"
              required
            />
          </div>
        </div>
        
        <!-- Submit Button -->
        <div class="field is-grouped is-grouped-centered">
          <div class="control">
            <button class="button is-primary" @click="handleLogin">Create User</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  

<style scoped>
.Signin-container {
    width: 100%;
    max-width: 500px;
}
</style>