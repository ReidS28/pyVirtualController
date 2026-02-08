<script lang="ts">
  import Controller from './lib/controller/Controller.svelte';
</script>

<main>
  <div class="container">
    <Controller controllerID={0} />
  </div>
</main>

<style>
  .container {
    width: 80%;
  }
</style>