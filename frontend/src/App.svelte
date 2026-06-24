<script lang="ts">
  import Controller from './lib/controller/Controller.svelte';

  function getControllerIdFromUrl(): number {
    const pathParts = window.location.pathname.split('/');
    const parsedId = parseInt(pathParts[pathParts.length - 1], 10);
    
    return isNaN(parsedId) ? 0 : parsedId;
  }

  const dynamicControllerID = getControllerIdFromUrl();
  console.log(dynamicControllerID);
</script>

<main>
  <div class="container">
    <Controller controllerID={dynamicControllerID} />
  </div>
</main>

<style>
  .container {
    width: 80%;
  }
</style>