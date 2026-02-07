<script lang="ts">
	interface Props {
		controllerID: number;
	}
	let { controllerID = 0 }: Props = $props();
</script>

<button onclick={() => controllerID++}>
    controllerID is {controllerID}
</button>
