<script lang="ts">
	import { onMount, onDestroy } from "svelte";
	import { ControllerConnection } from "./webSocket.svelte";
	import ControllerButton from "./ControllerButton.svelte";

	interface Props {
		controllerID: number;
	}

	let { controllerID }: Props = $props();

	let connection: ControllerConnection | null = $state(null);

	onMount(() => {
		connection = new ControllerConnection(controllerID);
	});

	onDestroy(() => {
		if (connection) connection.close();
	});
</script>

<ControllerButton
	id={100}
	{connection}>123456789</ControllerButton
>
