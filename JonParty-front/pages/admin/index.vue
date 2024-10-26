<script lang="ts" setup>
import { ref, onMounted } from 'vue';

// Define the structure of a theme for type safety
interface Theme {
  id: number;
  title: string;
}

// Reactive reference to store themes
const themes = ref<Theme[]>([]);
const newThemeTitle = ref('');

// Fetch themes when the component is mounted
onMounted(async () => {
  try {
    const response = await fetch('http://apostophe.fr:5000/themes');
    themes.value = await response.json();
  } catch (error) {
    console.error('Error fetching themes:', error);
  }
});

// Add a new theme to the list
const addTheme = async () => {
  const trimmedTitle = newThemeTitle.value.trim();
  if (!trimmedTitle) return; // Avoid empty themes

  try {
    const response = await fetch('http://apostophe.fr:5000/themes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title: trimmedTitle }),
    });

    const addedTheme = await response.json();
    themes.value.push(addedTheme);
    newThemeTitle.value = ''; // Clear the input field
  } catch (error) {
    console.error('Error adding theme:', error);
  }
};

// Delete a theme from the list
const deleteTheme = async (themeId: number) => {
  try {
    await fetch(`http://apostophe.fr:5000/themes/${themeId}`, {
      method: 'DELETE',
    });

    // Update local state to remove the deleted theme
    themes.value = themes.value.filter((theme) => theme.id !== themeId);
  } catch (error) {
    console.error('Error deleting theme:', error);
  }
};
</script>

<template>
    <div>
      <h1>Themes</h1>
      <v-form @submit.prevent="addTheme">
        <input v-model="newThemeTitle" placeholder="New Theme title" />
        <v-btn type="submit">Add Theme</v-btn>
      </v-form>
      <ul>
        <li v-for="Theme in themes" :key="Theme.id">
          {{ Theme.title }}
          <button @click="deleteTheme(Theme.id)">Delete</button>
        </li>
      </ul>
    </div>
</template>
  
