<script lang="ts">
  import Controller from './lib/controller/Controller.svelte';
  let num = $state(0);
</script>

<main>
  <h1>Hello</h1>
  <button onclick={() => (num++)}>
    num is {num}
  </button>
  <Controller controllerID={num} />
</main>