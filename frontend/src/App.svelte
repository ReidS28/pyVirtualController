<script lang="ts">
  import Controller from './lib/controller/Controller.svelte';
  let num = 0
</script>

<main>
  <h1>Hello</h1>
  <Controller controllerID={num} />
</main>