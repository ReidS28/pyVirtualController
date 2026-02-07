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
	id={0}
	{connection}>Button 0</ControllerButton
>
<ControllerButton
	id={1}
	{connection}>Button 1</ControllerButton
>
<ControllerButton
	id={2}
	{connection}>Button 2</ControllerButton
>
<ControllerButton
	id={3}
	{connection}>Button 3</ControllerButton
>
<ControllerButton
	id={4}
	{connection}>Button 4</ControllerButton
>
<ControllerButton
	id={5}
	{connection}>Button 5</ControllerButton
>
<ControllerButton
	id={6}
	{connection}>Button 6</ControllerButton
>
<ControllerButton
	id={7}
	{connection}>Button 7</ControllerButton
>
<ControllerButton
	id={8}
	{connection}>Button 8</ControllerButton
>
<ControllerButton
	id={9}
	{connection}>Button 9</ControllerButton
>
<ControllerButton
	id={10}
	{connection}>Button 10</ControllerButton
>
<ControllerButton
	id={11}
	{connection}>Button 11</ControllerButton
>

